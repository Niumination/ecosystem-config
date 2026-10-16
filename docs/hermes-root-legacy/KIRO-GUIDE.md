# Quick Guide: Check Kiro Models on 9router

## Status
**Kiro models PENDING** — belum muncul di katalog (user baru daftar di dashboard).

## Quick Check Commands

### 1. Check if kiro models exist
```bash
bash ~/.hermes/check-kiro-quick.sh
```

### 2. Monitor for new models (run periodically)
```bash
python3 ~/.hermes/monitor-9router.py
```

### 3. Test kiro models (once available)
```bash
python3 ~/.hermes/test-kiro-models.py
```

## Expected Behavior
- Model baru biasanya muncul **5-15 menit** setelah pendaftaran di dashboard
- Run monitor script setiap 5 menit untuk deteksi otomatis
- Script akan alert ketika kiro models muncul

## Current Catalog (89 models)
Prefixes available:
- `ag` (16): Gemini flash, Claude, GPT-oss
- `gemini` (7): Google Gemini
- `gh` (32): GPT variants, Claude Haiku
- `kr` (34): DeepSeek, GLM, MiniMax, Qwen

**Kiro not yet in catalog.**

## Next Actions
1. Tunggu 5-15 menit untuk propagasi
2. Run `bash ~/.hermes/check-kiro-quick.sh` untuk cek
3. Jika sudah ada, run `python3 ~/.hermes/test-kiro-models.py` untuk test
4. Update mapping sesuai hasil test
