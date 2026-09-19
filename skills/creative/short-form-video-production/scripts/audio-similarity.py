#!/usr/bin/env python3
"""audio-similarity.py — apakah dua berkas audio berasal dari voice/engine yang sama?

Dua mode, dua pertanyaan yang BERBEDA. Pilih sesuai pertanyaan, jangan campur:

  (default)  DTW log-mel   -> "A vs B: voice/engine sama?"
                              SYARAT: kedua berkas mengucapkan TEKS YANG SAMA.
  --timbre                 -> "lintas teks: apakah set ini satu voice?" dan
                              "kandidat mana yang paling dekat ke referensi?"
                              Butuh kontrol teks (--text-control) untuk bisa dibaca.

Alasan dua mode: DTW mengukur bentuk waktu + spektrum, jadi ia menghukum perbedaan tempo dan
susunan jeda — besar jaraknya di antara dua berkas berteks beda TIDAK berarti voice-nya berbeda.
Timbre (rata-rata spektrum log-mel pada frame bersuara) membuang informasi waktu, sehingga tahan
teks, tempo, dan jeda; itu satu-satunya metrik yang sah untuk pertanyaan lintas-berkas.

KALIBRASI (diukur, bukan tebakan) — jarak timbre:
  berkas identik                        0.0000
  voice sama, rate beda 22%             0.0002
  voice sama, TEKS BEDA                 ~0.001   <-- ambang pembanding WAJIB
  voice sama, adegan berbeda           0.007 - 0.015
  voice lain (kandidat edge-tts)        0.027 +
Tanpa kontrol teks, angka 0.02 terlihat "dekat" padahal sudah jelas voice lain.

KALIBRASI jarak DTW (hanya sah untuk teks sama):
  referensi vs dirinya sendiri    ~0      (validasi metode)
  voice sama dirender ulang       ~0.1    (skala "voice identik")
  berkas sama di-encode ulang     ~1      (batas atas "voice sama", dihitung otomatis)
  >= ~5x batas atas                = voice/engine berbeda

JANGAN pakai f0 median untuk memutuskan "satu voice atau banyak". Di dalam SATU berkas, f0 median
berayun 40-55 Hz hanya karena titik potongnya berbeda — angkanya akan melahirkan "banyak voice"
dari satu voice. f0 hanya petunjuk kasar untuk memilih kandidat.

Pakai:
  python3 audio-similarity.py ref.mp3 kandidat1.mp3 kandidat2.mp3 ...        # teks harus sama
  python3 audio-similarity.py --timbre --text-control a.mp3 b.mp3 ref.mp3 kandidat.mp3 ...
  python3 audio-similarity.py --f0 ref.mp3 kandidat.mp3                      # tambah f0 (petunjuk)

Butuh numpy + ffmpeg. Kalau numpy belum ada: python3 -m pip install numpy (atau pakai venv proyek).
"""

import os
import statistics
import subprocess
import sys
import tempfile

try:
    import numpy as np
except ImportError:  # noqa: TRY002 - pesan yang memberi jalan keluar, bukan traceback
    raise SystemExit("butuh numpy: python3 -m pip install numpy (atau pakai venv yang sudah punya)")

SR, N_FFT, WIN, HOP = 16000, 512, 400, 160
N_MEL_DTW, N_MEL_TIMBRE = 40, 80
F0_FRAME, F0_HOP = 1024, 512


def pcm(path):
    """Baca apa pun yang bisa didekode ffmpeg menjadi float mono 16 kHz.

    Berkas PCM mentah (mis. keluaran TTS bertanda audio/L16) TIDAK bisa dibaca sebagai media:
    ffprobe akan melaporkan durasi kosong. Pakai pcm_raw() untuk itu.
    """
    raw = subprocess.Popen(
        ["ffmpeg", "-v", "error", "-i", path, "-ac", "1", "-ar", str(SR), "-f", "s16le", "-"],
        stdout=subprocess.PIPE,
    ).communicate()[0]
    return np.frombuffer(raw, dtype=np.int16).astype(np.float32) / 32768.0


def mel_filters(n_mel, n_fft=N_FFT, sr=SR):
    def hz2mel(f):
        return 2595.0 * np.log10(1.0 + f / 700.0)

    def mel2hz(m):
        return 700.0 * (10.0 ** (m / 2595.0) - 1.0)

    mels = np.linspace(hz2mel(50), hz2mel(sr / 2), n_mel + 2)
    bins = np.floor((n_fft + 1) * mel2hz(mels) / sr).astype(int)
    fb = np.zeros((n_mel, n_fft // 2 + 1))
    for i in range(n_mel):
        left, centre, right = bins[i], bins[i + 1], bins[i + 2]
        right = max(right, left + 1)
        for k in range(left, min(centre, n_fft // 2 + 1)):
            fb[i, k] = (k - left) / max(1, centre - left)
        for k in range(centre, min(right, n_fft // 2 + 1)):
            fb[i, k] = (right - k) / max(1, right - centre)
    return fb


MEL_DTW = mel_filters(N_MEL_DTW)
MEL_TIMBRE = mel_filters(N_MEL_TIMBRE)


def frames_of(path):
    x = pcm(path)
    idx = np.arange(0, max(0, len(x) - WIN), HOP)
    if len(idx) == 0:
        raise SystemExit(f"berkas terlalu pendek untuk dianalisis (atau PCM mentah yang tidak terdekode): {path}")
    return np.stack([x[i:i + WIN] * np.hanning(WIN) for i in idx])


def logmel(path):
    frames = frames_of(path)
    spec = (np.abs(np.fft.rfft(frames, N_FFT)) ** 2) @ MEL_DTW.T
    lm = np.log(spec + 1e-10)
    return (lm - lm.mean(0, keepdims=True)) / (lm.std(0, keepdims=True) + 1e-6)


def timbre(path):
    """Vektor timbre: rata-rata log-mel pada frame bersuara, dinormalkan L2.

    Tahan terhadap tempo, jeda, dan perbedaan teks — inilah yang membuatnya sah untuk menjawab
    "apakah himpunan berkas ini satu voice".
    """
    frames = frames_of(path)
    rms = np.sqrt((frames ** 2).mean(1))
    voiced = frames[rms > np.percentile(rms, 40)]
    spec = (np.abs(np.fft.rfft(voiced, N_FFT)) ** 2) @ MEL_TIMBRE.T
    v = np.log(spec + 1e-10).mean(0)
    return v / (np.linalg.norm(v) + 1e-9)


def cos_dist(a, b):
    return float(1.0 - float(np.dot(a, b)))


def dtw(a, b, band=0.35):
    """DTW ber-band; matriks biaya lewat perkalian matriks supaya cukup cepat di numpy."""
    n, m = len(a), len(b)
    cost = (a * a).sum(1)[:, None] + (b * b).sum(1)[None, :] - 2.0 * a @ b.T
    np.maximum(cost, 0.0, out=cost)
    inf = 1e12
    prev = np.full(m, inf)
    prev[0] = cost[0, 0]
    width = max(10, int(band * max(n, m)))
    for i in range(1, n):
        centre = int(i * m / n)
        lo, hi = max(0, centre - width), min(m, centre + width + 1)
        cur = np.full(m, inf)
        for j in range(lo, hi):
            cur[j] = cost[i, j] + (prev[j] if j == 0 else min(prev[j], cur[j - 1], prev[j - 1]))
        prev = cur
    return prev[m - 1] / max(n, m)


def median_f0(path):
    """Petunjuk kasar saja — autokorelasi sederhana rawan kesalahan oktav, dan di dalam satu
    berkas angkanya bergeser 40-55 Hz hanya karena titik potong berbeda. Jangan pernah dipakai
    untuk menyimpulkan berapa banyak voice di satu set."""
    x = pcm(path)
    vals = []
    for i in range(0, max(0, len(x) - F0_FRAME), F0_HOP):
        seg = x[i:i + F0_FRAME]
        if float(np.sqrt((seg ** 2).mean())) < 0.02:
            continue
        seg = seg - seg.mean()
        energy = float((seg ** 2).sum()) or 1.0
        for lag in range(int(SR / 350), int(SR / 70)):
            if float((seg[:-lag] * seg[lag:]).sum()) / energy > 0.35:
                vals.append(SR / lag)
                break
    return statistics.median(vals) if vals else 0.0


def duration(path):
    """Durasi hasil dekode — 0 berarti berkas tidak terbaca (probe tidak valid, bukan kandidat gugur)."""
    x = pcm(path)
    return len(x) / float(SR)


def reencode_control(path):
    """Berkas yang sama setelah di-encode ulang mp3 24 kHz 32 kbps: batas atas 'voice sama'."""
    out = os.path.join(tempfile.mkdtemp(prefix="audsim-"), "reenc.mp3")
    subprocess.run(
        ["ffmpeg", "-v", "error", "-y", "-i", path, "-ar", "24000", "-ac", "1", "-b:a", "32k", out],
        capture_output=True,
    )
    return out if os.path.exists(out) and os.path.getsize(out) else None


def assert_readable(label, path):
    """Tolak kandidat yang probenya tidak menghasilkan audio — bukan 'gugur', tapi 'tidak diuji'."""
    d = duration(path)
    if d < 0.3:
        print(f"  !! {label}: hanya {d:.2f} s terdekode — probe TIDAK VALID, kandidat belum teruji")
        print("     (PCM mentah? dekode eksplisit: ffmpeg -f s16le -ar <rate> -ac 1 -i pipe:0 out.mp3)")
        return False
    return True


def main(argv):
    show_f0 = "--f0" in argv
    use_timbre = "--timbre" in argv
    args = [a for a in argv if a not in ("--f0", "--timbre")]

    text_control = None
    if "--text-control" in args:
        i = args.index("--text-control")
        text_control = (args[i + 1], args[i + 2])
        del args[i:i + 3]

    if len(args) < 2:
        print(__doc__)
        return 2

    ref, cands = args[0], args[1:]
    for p in [ref] + cands:
        if not os.path.exists(p):
            raise SystemExit(f"berkas tidak ada: {p}")

    if use_timbre:
        return timbre_mode(ref, cands, text_control, show_f0)
    return dtw_mode(ref, cands, show_f0)


def dtw_mode(ref, cands, show_f0):
    print("Mode DTW log-mel — HANYA sah bila setiap pasangan mengucapkan teks yang sama.")
    print("Untuk pertanyaan lintas teks (satu voice atau banyak?) pakai --timbre.\n")

    ref_m = logmel(ref)
    self_d = dtw(ref_m, ref_m)
    reenc = reencode_control(ref)
    ceil_d = dtw(ref_m, logmel(reenc)) if reenc else float("nan")

    print(f"kontrol: referensi vs dirinya sendiri = {self_d:6.3f}  (harus ~0)")
    if reenc:
        print(f"kontrol: referensi di-encode ulang    = {ceil_d:6.3f}  (batas atas 'voice sama')")
    print()

    print(f"{'kandidat':<44}{'jarak':>8}  putusan")
    for c in cands:
        if not assert_readable(os.path.basename(c), c):
            continue
        d = dtw(ref_m, logmel(c))
        if reenc and ceil_d > 0:
            if d <= 3 * ceil_d:
                verdict = "kemungkinan voice sama"
            elif d <= 8 * ceil_d:
                verdict = "tidak konklusif"
            else:
                verdict = "beda voice/engine"
        else:
            verdict = "bandingkan dengan kontrol"
        line = f"{os.path.basename(c):<44}{d:8.2f}  {verdict}"
        if show_f0:
            line += f"   f0 ref={median_f0(ref):6.1f} Hz  kandidat={median_f0(c):6.1f} Hz"
        print(line)

    print("\nCatatan: jarak hanya bermakna bila kedua berkas mengucapkan teks yang sama.")
    print("'Beda voice/engine' berarti engine belum diketahui — bukan bukti rekaman manusia.")
    return 0


def timbre_mode(ref, cands, text_control, show_f0):
    print("Mode timbre (tempo-invariant) — untuk pertanyaan lintas teks.\n")

    ctrl = None
    if text_control:
        a, b = text_control
        ctrl = cos_dist(timbre(a), timbre(b))
        print(f"kontrol TEKS: voice sama, teks beda  = {ctrl:.4f}   <-- ambang pembanding")
    else:
        print("kontrol TEKS: TIDAK ADA. Angka di bawah belum bisa dibaca.")
        print("  Render DUA kalimat berbeda dengan SATU voice (rate sama), lalu:")
        print("  --text-control kalimatA.mp3 kalimatB.mp3")
        print("  Acuan: ~0.001 = voice sama teks beda · 0.027+ = voice lain.\n")

    ref_t = timbre(ref)
    print(f"kontrol: referensi vs dirinya sendiri = {cos_dist(ref_t, ref_t):.4f}  (harus 0)\n")
    print(f"{'kandidat':<44}{'timbre':>8}  putusan")
    for c in cands:
        if not assert_readable(os.path.basename(c), c):
            continue
        d = cos_dist(timbre(c), ref_t)
        if ctrl:
            if d <= 2 * ctrl:
                verdict = "voice sama"
            elif d <= 4 * ctrl:
                verdict = "tidak konklusif"
            else:
                verdict = "beda voice"
        else:
            verdict = "belum bisa dibaca"
        line = f"{os.path.basename(c):<44}{d:8.4f}  {verdict}"
        if show_f0:
            line += f"   f0 ref={median_f0(ref):6.1f} Hz  kandidat={median_f0(c):6.1f} Hz"
        print(line)

    print("\nCatatan: timbre membuang waktu — perbedaan tempo/jeda tidak memengaruhi angka ini.")
    print("f0 median TIDAK bisa menjawab 'satu voice atau banyak': di dalam satu berkas angkanya")
    print("bergeser 40-55 Hz hanya karena titik potongnya berbeda.")
    print("'Beda voice' berarti engine belum diketahui — bukan bukti rekaman manusia.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
