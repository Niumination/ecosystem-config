#!/usr/bin/env bash
# =============================================================================
# build-credentials.sh — bekukan kredensial ke repo niumination-restore (terenkripsi)
# =============================================================================
# SISI BUILD. Dijalankan di device yang masih hidup, membaca berkas nyata,
# menghasilkan credentials/*.enc (ciphertext) untuk di-commit.
#
# Passphrase: dibuat acak 32 byte, disimpan di Keychain (service: niumination-restore-dr).
# TIDAK PERNAH dicetak ke stdout/log. Untuk melihatnya:
#   security find-generic-password -s niumination-restore-dr -w
#
# Pemakaian: bash build-credentials.sh [--verify-only]
# =============================================================================
set -Eeuo pipefail

REPO="$HOME/Desktop/Niumination/apps/niumination-restore"
KC_SERVICE="niumination-restore-dr"
OUT="$REPO/credentials"
VERIFY_ONLY=false
[[ "${1:-}" == "--verify-only" ]] && VERIFY_ONLY=true

command -v openssl >/dev/null || { echo "GAGAL: openssl tidak ada" >&2; exit 1; }

# --- passphrase: dari Keychain, buat bila belum ada ---------------------------
if security find-generic-password -s "$KC_SERVICE" >/dev/null 2>&1; then
  DR_PASS=$(security find-generic-password -s "$KC_SERVICE" -w)
  echo "== passphrase: diambil dari Keychain ($KC_SERVICE)"
else
  DR_PASS=$(openssl rand -base64 32 | tr -d '\n')
  security add-generic-password -a "$USER" -s "$KC_SERVICE" -w "$DR_PASS" -U
  echo "== passphrase: BARU dibuat acak & disimpan di Keychain ($KC_SERVICE)"
  echo "   !! WAJIB simpan salinannya DI LUAR device ini (kertas/cloud pribadi)."
  echo "   !! Lihat dengan: security find-generic-password -s $KC_SERVICE -w"
fi
export DR_PASS

# --- daftar sumber → nama keluaran -------------------------------------------
E="$HOME/Desktop/Niumination"
declare -a SRC DST
SRC+=("$HOME/.ssh/id_ed25519_niumination");   DST+=("ssh-id_ed25519_niumination.enc")
SRC+=("$HOME/.ssh/config");                    DST+=("ssh-config.enc")
SRC+=("$HOME/.9router/auth/cli-secret");       DST+=("9router-auth.enc")
SRC+=("$HOME/.9router/jwt-secret");            DST+=("9router-jwt-secret.enc")
SRC+=("$HOME/.9router/machine-id");            DST+=("9router-machine-id.enc")
SRC+=("$HOME/.9router/db/data.sqlite");        DST+=("9router-db.enc")
SRC+=("$E/vault/secrets.zsh");                 DST+=("vault-secrets-zsh.enc")

enc() {  # enc <in> <out>
  openssl enc -aes-256-cbc -pbkdf2 -iter 200000 -salt \
    -in "$1" -out "$2" -pass env:DR_PASS
}

mkdir -p "$OUT"
echo
if $VERIFY_ONLY; then
  echo "== MODE VERIFIKASI saja (tidak menulis apa pun)"
else
  echo "== enkripsi → $OUT"
fi

FAIL=0
for i in "${!SRC[@]}"; do
  s="${SRC[$i]}"; d="${DST[$i]}"; o="$OUT/$d"
  [[ -f "$s" ]] || { echo "  ✗ SUMBER TIDAK ADA: $s" >&2; FAIL=$((FAIL+1)); continue; }

  if ! $VERIFY_ONLY; then
    enc "$s" "$o"
  fi
  [[ -f "$o" ]] || { echo "  ✗ keluaran tidak ada: $d" >&2; FAIL=$((FAIL+1)); continue; }

  # verifikasi: dekripsi balik → bandingkan hash dengan sumber (hash, bukan keberadaan)
  tmp=$(mktemp)
  if openssl enc -d -aes-256-cbc -pbkdf2 -iter 200000 -in "$o" -out "$tmp" -pass env:DR_PASS 2>/dev/null; then
    h_src=$(shasum -a 256 "$s" | cut -d' ' -f1)
    h_bak=$(shasum -a 256 "$tmp" | cut -d' ' -f1)
    rm -f "$tmp"
    if [[ "$h_src" == "$h_bak" ]]; then
      printf "  ✓ %-32s %7s B  sha256:%s\n" "$d" "$(wc -c < "$o" | tr -d ' ')" "${h_src:0:16}"
    else
      echo "  ✗ $d — HASH TIDAK COCOK setelah dekripsi" >&2; FAIL=$((FAIL+1))
    fi
  else
    rm -f "$tmp"
    echo "  ✗ $d — gagal didekripsi (passphrase/format)" >&2; FAIL=$((FAIL+1))
  fi
done
echo
if [[ $FAIL -gt 0 ]]; then
  echo "GAGAL: $FAIL masalah — repo TIDAK boleh di-commit" >&2; exit 1
fi
echo "Selesai: ${#SRC[@]} kredensial terbukti utuh (hash sumber == hash hasil dekripsi)"
echo "Catatan: hash ditampilkan saja, TIDAK disimpan — hash plaintext di repo = celah konfirmasi."
