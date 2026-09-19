#!/usr/bin/env python3
"""periksa_vo.py — periksa apa yang BENAR-BENAR terdengar pada berkas VO, tanpa unduhan.

Memakai Gemini API sebagai pentranskrip (audio masuk ke model, bukan teks). Dipilih
karena: tidak menambah berkas di disk, kuotanya terpisah dari kuota TTS, dan lebih
akurat untuk Bahasa Indonesia + campuran Inggris daripada model STT lokal kecil.

Mengapa tidak memakai STT lokal:
  · whisper `base` berhalusinasi pada Bahasa Indonesia (pernah mengubah "es ka pe de"
    menjadi "Eskapi diri")
  · whisper menerapkan inverse text normalization → pemeriksaan kata kunci melahirkan
    gagal palsu; pernah membuat 9 dari 13 kasus salah dinyatakan gagal
  · model yang akurat berukuran 1,5 GB dan butuh ~2,5 menit per potongan di CPU tanpa GPU

Pemakaian:
    python3 periksa_vo.py berkas_vo.mp3
    python3 periksa_vo.py berkas_vo.mp3 --unsur "3.117.360.000" "4.1.0" "Diskominfo"

Keluaran: transkrip apa adanya + status tiap unsur yang diminta diperiksa.
"""
from __future__ import annotations

import argparse
import base64
import json
import os
import subprocess
import sys
from pathlib import Path

MODEL = "gemini-2.5-flash"
ENV_HERMES = Path.home() / ".hermes" / ".env"

INSTRUKSI = (
    "Transkripsikan audio ini apa adanya, kata per kata, dalam Bahasa Indonesia. "
    "PENTING: tuliskan angka, singkatan, nama, dan alamat web PERSIS seperti yang "
    "diucapkan oleh suara itu — jangan diubah menjadi bentuk lain. Contoh: kalau "
    "suaranya mengeja huruf, tuliskan ejaan hurufnya; kalau suaranya membaca angka "
    "sebagai bilangan, tuliskan bilangannya. Jangan menambahkan komentar, jangan "
    "meringkas, jangan menerjemahkan. Keluarkan hanya transkripnya."
)


def ambil_kunci() -> str:
    if os.environ.get("GOOGLE_API_KEY"):
        return os.environ["GOOGLE_API_KEY"]
    if ENV_HERMES.exists():
        for b in ENV_HERMES.read_text(encoding="utf-8").splitlines():
            if b.startswith("GOOGLE_API_KEY="):
                return b.split("=", 1)[1].strip().strip('"').strip("'")
    sys.exit("GOOGLE_API_KEY tidak ditemukan")


def transkrip(berkas: Path, kunci: str) -> str:
    mime = {"mp3": "audio/mp3", "wav": "audio/wav", "m4a": "audio/mp4",
            "flac": "audio/flac", "ogg": "audio/ogg"}.get(berkas.suffix.lstrip(".").lower())
    if not mime:
        sys.exit(f"format tidak didukung: {berkas.suffix} (pakai mp3/wav/m4a/flac/ogg)")
    if berkas.stat().st_size > 18 * 1024 * 1024:
        sys.exit("berkas >18 MB — pecah dulu, batas aman permintaan sebaris")
    badan = {"contents": [{"parts": [
        {"text": INSTRUKSI},
        {"inline_data": {"mime_type": mime,
                         "data": base64.b64encode(berkas.read_bytes()).decode()}},
    ]}]}
    f = Path("/tmp/_periksa_vo_req.json")
    f.write_text(json.dumps(badan), encoding="utf-8")
    r = subprocess.run(["curl", "-sS", "-m", "300", "-X", "POST",
                        f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={kunci}",
                        "-H", "Content-Type: application/json", "-d", f"@{f}"],
                       capture_output=True, text=True)
    f.unlink(missing_ok=True)
    try:
        j = json.loads(r.stdout)
    except json.JSONDecodeError:
        sys.exit(f"respons bukan JSON: {r.stdout[:200]}")
    if "error" in j:
        sys.exit(f"GALAT: {j['error'].get('message','')[:250]}")
    return j["candidates"][0]["content"]["parts"][0]["text"].strip()


def utama() -> int:
    ap = argparse.ArgumentParser(description="Periksa VO lewat transkripsi Gemini (tanpa unduhan)")
    ap.add_argument("berkas", help="berkas VO (mp3/wav/m4a/flac/ogg)")
    ap.add_argument("--unsur", nargs="*", default=[],
                    help="teks yang harus muncul di transkrip, mis. '4.1.0' 'Diskominfo'")
    ap.add_argument("--simpan", default=None, help="simpan transkrip ke berkas")
    a = ap.parse_args()

    b = Path(a.berkas)
    if not b.exists():
        sys.exit(f"tidak ditemukan: {b}")

    t = transkrip(b, ambil_kunci())
    print(f"berkas : {b.name} ({b.stat().st_size/1024:.0f} KB)")
    print(f"model  : {MODEL}  (kuota terpisah dari kuota TTS)\n")
    print("=== TRANSKRIP ===")
    print(t)

    if a.simpan:
        Path(a.simpan).write_text(t, encoding="utf-8")
        print(f"\n(disimpan ke {a.simpan})")

    if a.unsur:
        tl = t.lower()
        print("\n=== PEMERIKSAAN UNSUR ===")
        gagal = 0
        for u in a.unsur:
            ada = u.lower() in tl
            gagal += 0 if ada else 1
            print(f"  {'ADA    ' if ada else 'TIDAK  '} {u}")
        print(f"\n{gagal} unsur tidak ditemukan dari {len(a.unsur)}")
        if gagal:
            print("CATATAN: transkrip juga bisa menormalkan bentuk (mis. '3,117,360,000' vs")
            print("'tiga miliar seratus tujuh belas juta'). Baca transkripnya sebelum menyimpulkan.")
        return 1 if gagal else 0
    return 0


if __name__ == "__main__":
    sys.exit(utama())
