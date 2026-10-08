# Verifikasi Premis: "Shim 3.14 Karena `_launchers.py` Hilang dari `main`"

**Tanggal:** 8 Okt 2026
**Verifikator:** thread #General (orchestrator)
**Sumber klaim:** `docs/reports/TEMUAN-SHIM-HERMES-3.14-CACAT-2026-10-08.md`
**Status:** premis **TIDAK AKURAT** — tindakan yang diminta akan memperburuk, bukan memperbaiki

---

## Ringkasan

Klaim: `_launchers.py` hilang dari `main` → itu akar masalah shim Python 3.14 →
selesaikan reconcile supaya file masuk `main` → `hermes update` akan menulis shim benar.

Verifikasi menemukan **tiga koreksi material**:

1. **`main` tidak punya `stage_launcher` sama sekali** — jadi `hermes update` di `main`
   memang tidak menulis shim store-python. Bahaya justru ada di branch reconcile.
2. **`_launchers.py` di branch reconcile lebih TUA dari upstream** — bukan sekadar "ada
   di reconcile", tapi versi yang sudah tertinggal 1.157 commit.
3. **Tidak ada guard versi Python di mana pun** — bahkan versi upstream terbaru tetap
   memilih Python 3.14 dari `facts.json`. **Merge tidak akan memperbaiki apa pun.**

---

## Koreksi 1 — `main` tidak punya `stage_launcher`

```
$ git grep -n "stage_launcher" main
(kosong — 0 hasil)

$ git grep -c "stage_launcher" reconcile-upstream-20261007
hermes_cli/_install_repair.py:2
hermes_cli/_launchers.py:5
hermes_cli/doctor_platform.py:2
hermes_cli/gateway.py:1
tests/compat/old_updater_surface.json:1
```

`stage_launcher` adalah satu-satunya fungsi yang memanggil `resolve_store_python(..., publication=True)`
dan menulis launcher ke disk. Ia **tidak ada di `main`**.

Konsekuensi: `hermes update` di `main` **tidak** menulis shim store-python. Yang menulis shim
3.14 pada 7 Okt 12:56 adalah `hermes update` yang dijalankan **saat branch reconcile aktif** —
terkonfirmasi dari reflog:

```
01637af3db HEAD@{2026-10-07 12:55:52}: commit: fix(gateway): port P5 to has_durably_delivered_text
2160f78d84 HEAD@{2026-10-07 13:36:31}: checkout: moving from reconcile-upstream-20261007 to main
```

Shim ditulis 12:56 — **40 detik setelah commit terakhir reconcile, dan 40 menit SEBELUM**
checkout kembali ke `main`. Branch yang aktif saat itu adalah `reconcile-upstream-20261007`.

---

## Koreksi 2 — `_launchers.py` di reconcile lebih tua dari upstream

```
$ git cat-file -s 1e15625cb190af83e9978e8cdca9145d388a516b   # upstream/main
43411

$ git cat-file -s 35d53d3bc24156744838e369161cc82c89caaa5f   # reconcile
34719
```

Diff upstream → reconcile (arah: reconcile kehilangan):

```
-PIN_DEFAULT_HOME_FLAG = "_hermes_pin_default_home"
-    if home is not None:
-        pin, settle = (f"os.environ['HERMES_HOME'] = ...")
-    else:
-        pin = f"sys.{PIN_DEFAULT_HOME_FLAG} = True; "
-        settle = (...get_default_hermes_root())
+    default_home = (...)
```

Penyebab: branch reconcile di-rebase ke `a02278293e` (6 Okt 12:37). Sejak itu
`upstream/main` sudah maju **1.157 commit**, termasuk **7 commit yang menyentuh
`_launchers.py`**:

```
37074db421 fix(update): the minted launcher keeps the first line gateway identity recognises
ebf002cd3e fix(update): a stdlib-named file in the checkout never runs ahead of the launch repair
c42e9f6211 fix(update): the launch repair never runs git object bytes that do not hash to pre's blob
0e430b2d82 fix(update): the launch repair runs a published closure only when it hashes to pre's blobs
1c7a26726a fix(update): --print-runtime-command keeps tolerating a tree without the repair
b4f65a5967 fix(update): with no published closure the launcher reads it from git's objects
c18755d69e fix(update): a launch repairs a move that tore the repair's own code
```

**Merge reconcile → `main` akan memasukkan versi 6 Okt yang sudah tertinggal**, bukan versi
terkini. Klaim "selesaikan reconcile hingga `_launchers.py` masuk `main`" menghasilkan kode
yang sudah usang sebelum sempat dipakai.

---

## Koreksi 3 — Cherry-pick file itu sendiri tidak bisa (ImportError)

```
$ git show reconcile-upstream-20261007:hermes_cli/_launchers.py | grep -n "from pm"
23:from pm.environments import owning_home_root, store_root
590:    from pm.paths import install_root

$ git ls-tree main -- pm/ | wc -l
0
```

`_launchers.py` bergantung pada paket `pm/` yang **tidak ada di `main`** (0 entri).
Cherry-pick file tunggal = `ModuleNotFoundError: No module named 'pm'` saat import.

Saran "cherry-pick file itu sendiri bila ingin cepat" **tidak dapat dijalankan**.

---

## Koreksi 4 — TIDAK ADA guard versi Python (temuan paling penting)

Klaim tersirat: setelah merge, launcher "akan menulis shim yang benar".

Verifikasi `_store_python()` di `upstream/main` (versi terbaru):

```
def _store_python(runtime: Path) -> Path | None:
    rel = "python.exe" if _is_windows() else "bin/python3"
    facts = runtime / "facts.json"
    if facts.is_file():
        try:
            packages = json.loads(facts.read_text(encoding="utf-8-sig")).get("packages", {})
            entry = (packages.get("python") or {}).get("entry")
        except (OSError, ValueError):
            entry = None
        if entry:
            candidate = runtime / entry / rel
            if candidate.is_file():
                return candidate
    return None
```

Grep guard versi di seluruh file:

```
$ git show upstream/main:hermes_cli/_launchers.py | grep -n "requires.python\|3\.14\|version_info\|_MIN_PY\|supported"
(kosong — 0 hasil)
```

**Fungsi ini membaca `packages.python` dari `facts.json` tanpa memeriksa versi.** Dan
`facts.json` di mesin ini **memuat entry python**:

```
$ python3 -c "import json; d=json.load(open('~/.hermes/tools/facts.json')); print(list(d['packages']))"
['agent-browser', 'chromium', 'cua-driver', 'ffmpeg', 'node', 'npm', 'python', 'ripgrep', 'uv']

entry python: 3.14.7+202****0901
```

Juga dikonfirmasi: 7 commit upstream yang menyentuh `_launchers.py` **tidak menyentuh**
`resolve_store_python` / `_store_python` / `facts` sama sekali (grep pada diff: 0 hasil).

**Kesimpulan: bahkan dengan versi upstream paling baru sekalipun, `stage_launcher` akan tetap
memilih Python 3.14** karena `facts.json` mencantumkannya sebagai paket store. Merge tidak
memperbaiki bug ini — merge justru **memasukkan** mekanisme yang menabraknya.

---

## Rantai sebab yang sebenarnya

| Waktu | Peristiwa | Bukti |
|---|---|---|
| 31 Agu | `feat(pm)` masuk upstream — `_launchers.py` lahir | `3d12e86ef1` |
| 7 Okt 12:37 | reconcile di-rebase ke `a02278293e` | reflog |
| 7 Okt 12:55 | commit terakhir reconcile | reflog |
| 7 Okt **12:56** | **shim 3.14 ditulis** — `hermes update` di branch reconcile | mtime |
| 7 Okt 13:36 | checkout kembali ke `main` | reflog |

Akar masalah: `hermes update` dijalankan **saat branch reconcile aktif**. Reconcile punya
`stage_launcher` → `resolve_store_python(publication=True)` → `_store_python()` → `facts.json`
→ entry `python` 3.14.7 → shim menunjuk 3.14.

`main` sendiri **tidak punya jalur itu**, sehingga tidak akan menulis shim tersebut.

---

## Rekomendasi

**JANGAN jalankan langkah yang diminta** (merge reconcile ke `main` + `hermes update`).
Itu akan memasukkan `stage_launcher` ke `main` **tanpa guard versi** — artinya setiap
`hermes update` berikutnya di `main` akan kembali menulis shim 3.14, persis masalah yang
mau dihilangkan.

Perbaikan sebenarnya ada di **sisi resolusi Python**, bukan di keberadaan file:

1. **Tambah guard `requires-python` di `_store_python()`** — tolak kandidat yang berada di
   luar rentang `requires-python` (`>=3.11,<3.14`). Ini memperbaiki kelas bug-nya, bukan
   gejalanya.
2. **ATAU keluarkan `python` dari `facts.json` store tool** — python 3.14 di sana adalah
   runtime pendamping untuk node/uv/ffmpeg/chromium, bukan runtime Hermes. Kalau store tool
   memang perlu python sendiri, ia harus berada di namespace berbeda yang tidak dibaca
   `_store_python()`.
3. **Baru kemudian** pertimbangkan merge reconcile — dengan kesadaran bahwa reconcile
   tertinggal 1.157 commit dan perlu re-rebase ke `upstream/main` terkini lebih dulu.

---

## Kondisi saat ini (terverifikasi)

```
$ command -v hermes
/Users/zaryu/src/hermes-agent/.venv/bin/hermes

$ hermes --version
Hermes Agent v0.21.1 (2026.9.7) · upstream 02244472 · local 2160f78d (+7946 carried commits)
Python: 3.11.16
OpenAI SDK: 2.24.0

$ ls ~/.local/bin/hermes ~/src/hermes-agent/.hermes/bin/hermes
No such file or directory   (kedua shim sudah dihapus)
```

Sistem **stabil sekarang**. Risiko tunggal yang tersisa: menjalankan `hermes update`
**saat branch reconcile aktif** akan menulis ulang shim 3.14. Selama di `main`, tidak.

---

## Bukti

```
$ git grep -n "stage_launcher" main                                    → 0 hasil
$ git grep -c "stage_launcher" reconcile-upstream-20261007             → 5 berkas
$ git cat-file -s 1e15625c...  (upstream _launchers.py)                → 43411
$ git cat-file -s 35d53d3b...  (reconcile _launchers.py)               → 34719
$ git rev-list --count a02278293e..upstream/main                       → 1157
$ git log --oneline a02278293e..upstream/main -- hermes_cli/_launchers.py → 7 commit
$ git show upstream/main:hermes_cli/_launchers.py | grep -c "version_info" → 0
$ git ls-tree main -- pm/ | wc -l                                      → 0
$ git show reconcile...:_launchers.py | grep -c "from pm"              → 2
$ command -v hermes → /Users/zaryu/src/hermes-agent/.venv/bin/hermes   (sehat)
```
