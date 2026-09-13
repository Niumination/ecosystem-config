# Redaction Patterns

Exact-string replacement recipes that preserve syntax.

## JSON fixture
```python
import re, json
path = 'data/golden-queries.json'
txt = open(path, encoding='utf-8').read()
txt = txt.replace('3216022603070011', '[NIK REDACTED]')
txt = txt.replace('cPtnkHE7NYD3Gg_s', '[PASSWORD REDACTED]')
open(path, 'w', encoding='utf-8').write(txt)
```

## TypeScript test fixture
```python
from pathlib import Path
p = Path('src/services/__tests__/faseL.dtsen-multisource.test.ts')
txt = p.read_text()
txt = txt.replace("'1104080304610001'", "'[NIK TEST REDACTED]'")
txt = txt.replace("'1104080304610002'", "'[NIK TEST REDACTED]'")
p.write_text(txt)
```

## Markdown docs
- Replace whole lines containing literal password/NIK with redacted references
- Never leave dangling quotes or half-replaced tokens

## After redaction
```bash
npx tsc --noEmit 2>&1 | tail -3
npx vitest run src/services/__tests__/<file>.test.ts
```
