#!/usr/bin/env python3
"""gemini_vo.py — mesin produksi voice-over standar Niumination (dikunci 19 Sep 2026).

Menggantikan seluruh pendekatan lama (edge-tts + normalisasi teks berlapis).

PRINSIP YANG DIKUNCI:
  1. Naskah dikirim APA ADANYA. Jangan "memasak" teks. Gemini TTS berbasis LLM dan
     sudah memahami angka, tanggal, singkatan, serta campuran Indonesia-Inggris.
     Menambah ejaan buatan (mis. "es ka pe de", "titik web titik id") justru membuat
     ucapan terpenggal — persis kegagalan yang pernah terjadi.
  2. Gaya diatur lewat PROMPT, bukan lewat teks. Persona + adegan + arahan performa.
  3. Jeda & penekanan diatur lewat AUDIO TAG berbahasa Inggris (wajib Inggris walau
     naskahnya Indonesia), mis. [short pause] [interest] [thoughtfully] [warmly].
  4. Jangan menaruh dua tag berdampingan — harus dipisah teks atau tanda baca.
  5. Aksen diatur lewat prompt gaya, BUKAN lewat setelan bahasa.
  6. Satu permintaan = satu naskah utuh (hemat kuota; kuota gratis 10/hari PER MODEL).

Pemakaian:
    python3 gemini_vo.py NASKAH.txt --suara charon --keluaran out/
    python3 gemini_vo.py NASKAH.txt --suara algenib --preset pengumuman
    python3 gemini_vo.py NASKAH.txt --tanpa-gaya          # pembanding/kontrol
    python3 gemini_vo.py NASKAH.txt --suara sadaltager --daftar-suara

Kunci API dibaca dari ~/.hermes/.env (GOOGLE_API_KEY) — tidak pernah dicetak.
"""
from __future__ import annotations

import argparse
import base64
import json
import os
import subprocess
import sys
from pathlib import Path

MODEL_UTAMA = "gemini-3.1-flash-tts-preview"
MODEL_CADANGAN = ["gemini-2.5-flash-preview-tts", "gemini-2.5-pro-preview-tts"]
ENV_HERMES = Path.home() / ".hermes" / ".env"

# Kedua konstanta ini sudah TIDAK DIPEAKAI lagi sejak fallback edge-tts dicabut
# dari alur utama (23 Sep 2026) — lihat edge_cadangan() untuk alasannya.
# Disimpan hanya supaya jelas suara apa yang dulunya dipakai mesin cadangan.
EDGE_TTS = Path.home() / ".venv-mata" / "bin" / "edge-tts"
EDGE_VOICE = "id-ID-ArdiNeural"

# Tiga suara yang dikunci pemilik 19 Sep 2026 — untuk variasi antar konten.
SUARA_DIKUNCI = {
    "algenib": "Gravelly — serak, berkarakter; cocok untuk storytelling & narasi personal",
    "charon": "Informative — paling cocok untuk narator data publik / laporan resmi",
    "sadaltager": "Knowledgeable — berwawasan; cocok untuk edukasi & penjelasan teknis",
}
# Suara lain yang tersedia di Gemini (30 total) — dipakai bila karakter lain dibutuhkan.
SUARA_LAIN = ["Puck", "Kore", "Fenrir", "Orus", "Iapetus", "Umbriel", "Rasalgethi",
              "Schedar", "Gacrux", "Achird", "Alnilam", "Enceladus", "Sulafat", "Zephyr"]

PRESET = {
    "narator": """# AUDIO PROFILE: Pak Rizal
## "Narator data publik yang tenang dan jelas"

## SCENE: Ruang kerja sunyi di pagi hari, menyampaikan pengumuman resmi
Ia membaca laporan pagi dengan nada tenang, percaya diri, dan tidak dramatis. Tidak terburu-buru, seperti orang yang sudah hafal isinya.

### PERFORMANCE
Style: tenang dan jelas, seperti narator dokumenter investigatif yang menahan diri. Hangat tapi tidak berlebihan.
Pace: sedang dan mengalir. Berhenti sejenak sebelum angka penting supaya sempat dicerna.
Accent: Bahasa Indonesia baku, dengan istilah teknis Inggris diucapkan wajar seperti orang Indonesia berpendidikan mengucapkannya.

### CONTEXT
Ia menyampaikan informasi penting ke rekan kerja. Ingin dipahami, bukan dikagumi.""",

    "pengumuman": """# AUDIO PROFILE: Bu Sari
## "Penyampai pengumuman resmi instansi"

## SCENE: Ruang rapat pagi, menyampaikan instruksi kepada seluruh pegawai
Ia berdiri di depan rekan-rekan, membaca pengumuman dengan sikap tenang dan wibawa yang bersahabat.

### PERFORMANCE
Style: resmi, jelas, dan bersahabat. Wibawa tanpa kesan kaku atau menggurui. Pastikan setiap angka dan nama kegiatan terdengar utuh.
Pace: sedang dan mantap. Beri jeda pada setiap poin agar mudah dicatat.
Accent: Bahasa Indonesia baku, pengucapan dinas yang rapi.

### CONTEXT
Pengumuman ini akan ditindaklanjuti. Ia ingin tidak ada yang salah dengar.""",

    "edukasi": """# AUDIO PROFILE: Kak Danu
## "Pengajar yang menjelaskan dengan sabar"

## SCENE: Sesi penjelasan singkat kepada peserta baru
Ia menjelaskan sesuatu yang cukup rumit, dengan nada antusias namun tetap mudah diikuti.

### PERFORMANCE
Style: hangat, antusias, dan bersahabat. Terdengar seperti orang yang senang berbagi, bukan seperti membacakan buku.
Pace: mengalir. Perlambat tepat sebelum istilah atau angka penting, lalu lanjutkan normal.
Accent: Bahasa Indonesia percakapan yang rapi, istilah teknis Inggris diucapkan fasih.

### CONTEXT
Peserta baru pertama kali mendengar ini. Ia ingin mereka paham, bukan merasa bodoh.""",

    "story": """# AUDIO PROFILE: Bang Iyan
## "Penutur cerita yang tenang dan berkarakter"

## SCENE: Malam sunyi, menceritakan pengalaman kepada satu pendengar
Suaranya sedikit serak dan personal, seperti orang yang bercerita dari ingatan, bukan dari naskah.

### PERFORMANCE
Style: reflektif dan jujur. Ada keraguan sesaat di beberapa bagian, seperti mengingat kembali. Hindari nada iklan.
Pace: lambat sampai sedang. Biarkan kalimat penting menggantung sebentar sebelum lanjut.
Accent: Bahasa Indonesia dengan warna daerah yang tipis dan wajar.

### CONTEXT
Ini cerita nyata yang ia alami sendiri. Ia ingin pendengar merasakannya, bukan sekadar tahu.""",
}

PREAMBLE = (
    "Synthesize speech for the performance defined below. The profile, scene, and "
    "performance notes are direction only. Do NOT speak them. Speak ONLY the lines "
    "under #### TRANSCRIPT.\n\n"
)


def ambil_kunci() -> str:
    if os.environ.get("GOOGLE_API_KEY"):
        return os.environ["GOOGLE_API_KEY"]
    if ENV_HERMES.exists():
        for baris in ENV_HERMES.read_text(encoding="utf-8").splitlines():
            if baris.startswith("GOOGLE_API_KEY="):
                return baris.split("=", 1)[1].strip().strip('"').strip("'")
    sys.exit("GOOGLE_API_KEY tidak ditemukan (env atau ~/.hermes/.env)")


def bangun_prompt(naskah: str, preset: str | None) -> str:
    if not preset:
        return naskah
    if preset not in PRESET:
        sys.exit(f"preset tidak dikenal: {preset}. Pilihan: {', '.join(PRESET)}")
    return PREAMBLE + PRESET[preset] + "\n\n#### TRANSCRIPT\n" + naskah


def periksa_tag(naskah: str) -> list[str]:
    """Peringatan non-fatal: tag berdampingan = sumber galat sistemik."""
    import re
    masalah = []
    for m in re.finditer(r"\]\s*\[", naskah):
        masalah.append(f"dua tag berdampingan di posisi {m.start()}: '{naskah[max(0,m.start()-25):m.start()+25]}'")
    return masalah


def gemini(teks: str, suara: str, kunci: str, keluar_wav: Path) -> tuple[bool, str]:
    """Panggil Gemini TTS. Kembalikan (berhasil, pesan)."""
    badan = {
        "contents": [{"parts": [{"text": teks}]}],
        "generationConfig": {
            "responseModalities": ["AUDIO"],
            "speechConfig": {"voiceConfig": {"prebuiltVoiceConfig": {"voiceName": suara}}},
        },
    }
    berkas = keluar_wav.with_suffix(".req.json")
    berkas.write_text(json.dumps(badan), encoding="utf-8")

    for model in [MODEL_UTAMA] + MODEL_CADANGAN:
        r = subprocess.run(
            ["curl", "-sS", "-m", "240", "-X", "POST",
             f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={kunci}",
             "-H", "Content-Type: application/json", "-d", f"@{berkas}"],
            capture_output=True, text=True)
        try:
            j = json.loads(r.stdout)
        except json.JSONDecodeError:
            return False, f"{model}: respons bukan JSON ({r.stdout[:120]})"
        if "error" in j:
            pesan = j["error"].get("message", "")[:160]
            if "quota" in pesan.lower() or j["error"].get("code") == 429:
                # kuota habis untuk model ini → coba model berikutnya
                continue
            return False, f"{model}: {pesan}"
        try:
            mentah = base64.b64decode(j["candidates"][0]["content"]["parts"][0]["inlineData"]["data"])
        except (KeyError, IndexError):
            return False, f"{model}: struktur respons tak terduga"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "s16le", "-ar", "24000", "-ac", "1",
                        "-i", "pipe:0", str(keluar_wav)], input=mentah, capture_output=True)
        return True, f"{model} ({len(mentah)/2/24000:.2f}s)"
    return False, "kuota habis untuk semua model Gemini hari ini"


def edge_cadangan(naskah: str, keluar_mp3: Path) -> bool:
    """DILARANG DIPAKAI — sengaja dihapus dari alur utama 23 Sep 2026.

    Fungsi ini pernah menjadi jalur gagal di `utama()`: bila Gemini kehabisan
    kuota, mesin menulis suara edge-tts ke berkas bernama `vo_charon.mp3`.
    Nama berkas itu jadi bohong, dan proyek pun lolos QA dengan audio yang
    melanggar standarnya sendiri (reels-001 stuck di 5.PPRODUK "BLOKIR: VO
    USANG"). Kelemahannya yang tak bisa diperbaiki: tidak ada penanda di
    dalam berkas bahwa mesinnya bukan Charon.

    Dipertahankan di sini sebagai jejak bahwa jalur ini pernah ada dan kenapa
    ia dicabut — bukan untuk dipanggil lagi. Hapus total bila tak ada yang
    lagi perlu mengingatnya.
    """
    raise RuntimeError(
        "edge_cadangan() dicabut dari alur utama 23 Sep 2026. "
        "Tulis VO Gemini gagal itu sebagai GAGAL, bukan sebagai hasil."
    )


def ke_standar(sumber: Path, tujuan: Path) -> None:
    """Normalkan ke standar MATA: 44,1 kHz · stereo · 192 kbps."""
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(sumber), "-ar", "44100", "-ac", "2",
                    "-b:a", "192k", str(tujuan)], capture_output=True)


def durasi(p: Path) -> str:
    return subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                           "-of", "csv=p=0", str(p)], capture_output=True, text=True).stdout.strip()


def utama() -> int:
    ap = argparse.ArgumentParser(description="Mesin VO standar Niumination (Gemini TTS)")
    ap.add_argument("naskah", nargs="?", help="berkas naskah (.txt) — teks dikirim apa adanya")
    ap.add_argument("--suara", default="charon", help="algenib | charon | sadaltager | <nama lain>")
    ap.add_argument("--preset", default="narator", help="narator | pengumuman | edukasi | story | tanpa")
    ap.add_argument("--keluaran", default=".", help="direktori keluaran")
    ap.add_argument("--tanpa-gaya", action="store_true", help="kirim naskah tanpa prompt gaya")
    ap.add_argument("--nama", default=None, help="nama berkas keluaran (tanpa ekstensi)")
    ap.add_argument("--daftar-suara", action="store_true", help="tampilkan daftar suara lalu keluar")
    a = ap.parse_args()

    if a.daftar_suara:
        print("Suara yang DIKUNCI untuk konten Niumination:")
        for n, d in SUARA_DIKUNCI.items():
            print(f"  {n:<12} {d}")
        print("\nSuara lain yang tersedia di Gemini:")
        for s in SUARA_LAIN:
            print(f"  {s}")
        print("\nPreset gaya:", ", ".join(PRESET))
        return 0

    if not a.naskah:
        ap.error("berkas naskah wajib (atau --daftar-suara)")

    naskah = Path(a.naskah).read_text(encoding="utf-8").strip()
    if not naskah:
        sys.exit("naskah kosong")
    if len(naskah) > 1500:
        print(f"PERINGATAN: naskah {len(naskah)} karakter melampaui batas aman aplikasi (±1500). "
              f"Pertimbangkan memecah menjadi beberapa bagian.")

    for p in periksa_tag(naskah):
        print(f"PERINGATAN TAG: {p}")

    preset = None if (a.tanpa_gaya or a.preset == "tanpa") else a.preset
    prompt = bangun_prompt(naskah, preset)
    suara = a.suara.strip()
    suara_api = SUARA_DIKUNCI.get(suara.lower(), "").split(" —")[0] if suara.lower() in SUARA_DIKUNCI else suara
    suara_api = {"algenib": "Algenib", "charon": "Charon", "sadaltager": "Sadaltager"}.get(
        suara.lower(), suara_api)
    suara_api = suara_api[:1].upper() + suara_api[1:]

    keluaran = Path(a.keluaran)
    keluaran.mkdir(parents=True, exist_ok=True)
    nama = a.nama or f"vo_{suara.lower()}" + ("" if preset else "_polos")
    akhir = keluaran / f"{nama}.mp3"
    wav = keluaran / f"{nama}.wav"

    print(f"naskah   : {Path(a.naskah).name} · {len(naskah)} karakter")
    print(f"suara    : {suara_api}  ({SUARA_DIKUNCI.get(suara.lower(), 'suara tambahan')})")
    print(f"preset   : {preset or 'TANPA arahan gaya'}")
    print(f"keluaran : {akhir}")

    kunci = ambil_kunci()
    ok, pesan = gemini(prompt, suara_api, kunci, wav)
    if not ok:
        # GAGAL TEgas. Sengaja TIDAK ada fallback ke engine lain.
        # Alasan (insiden nyata, lihat BRAND.md abstract-studio): berkas bernama
        # vo_charon.mp3 yang isinya suara engine lain membuat proyek lolos QA
        # dengan audio yang melanggar standar sendiri — reels-001 stuck di
        # 5.PPRODUK "BLOKIR: VO USANG" dan tak ada cara teknikal membedakannya.
        # Nama berkas adalah kontrak. Kalau engine yang dipakai bukan Charon,
        # nama vo_charon.mp3 adalah kebohongan. Gagal keras itu biaya 1 menit;
        # audio bohong yang lolos tayang adalah insiden publik.
        print(f"GAGAL — Gemini TTS: {pesan}")
        print("Tidak dibuat fallback. Jangan ganti nama berkas ini dengan nama suara lain,")
        print("dan jangan catat proyek ini sebagai lolos QA sebelum VO dari Charon ada.")
        print("Opsi: cek sisa kuota lalu ulangi, atau rekam suara sendiri (satu-satunya")
        print("jalur non-Gemini yang diizinkan — harus bernama sesuai mesinnya, mis. vo_suara-sendiri.mp3).")
        return 1

    print(f"mesin    : Gemini TTS — {pesan}")
    ke_standar(wav, akhir)
    wav.unlink(missing_ok=True)
    (keluaran / f"{nama}.req.json").unlink(missing_ok=True)

    # Jejak provenance. Sengaja berkas teks, bukan tag di dalam MP3:
    # metadata audio hanya membuktikan mesinnya Gemini (ID3 TSOO), bukan
    # model/voice/preset yang dipakai. Ketiganya penting karena MODEL_UTAMA dan
    # kedua cadangannya berlabel "preview" — Google boleh mengubah karakter
    # suara Charon kapan saja tanpa pemberitahuan. Berselisihnya baris model
    # antar proyek itu tandanya suara sudah bergeser, dan harusnya didengar
    # ulang sebelum episode berikutnya direkam.
    import datetime as _dt
    prov = akhir.with_suffix(".provenance.txt")
    prov.write_text(
        "PROVENANCE VO — Niumination\n"
        f"berkas        : {akhir.name}\n"
        f"produksi      : {_dt.datetime.now().astimezone().strftime('%Y-%m-%d %H:%M:%S %Z')}\n"
        f"mesin         : Gemini TTS\n"
        f"model         : {pesan.split(' ')[0]}\n"
        f"suara         : {suara_api}\n"
        f"preset        : {preset or 'TANPA arahan gaya'}\n"
        f"naskah        : {Path(a.naskah).name} ({len(naskah)} karakter)\n"
        f"naskah_gaya   : {'utuh (PREAMBLE + preset + TRANSCRIPT)' if preset else 'kosong'}\n"
        f"stdout        : {pesan}\n"
        f"mesin_script  : skills/creative/gemini-vo-narration/scripts/gemini_vo.py\n",
        encoding="utf-8")
    print(f"jejak    : {prov.name}")

    print(f"durasi   : {durasi(akhir)} s")
    print(f"format   : " + subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "stream=sample_rate,channels,bit_rate",
         "-of", "csv=p=0", str(akhir)], capture_output=True, text=True).stdout.strip())
    print(f"ukuran   : {akhir.stat().st_size} bita")
    print(f"md5      : " + subprocess.run(["md5", "-q", str(akhir)],
                                          capture_output=True, text=True).stdout.strip())
    return 0


if __name__ == "__main__":
    sys.exit(utama())
