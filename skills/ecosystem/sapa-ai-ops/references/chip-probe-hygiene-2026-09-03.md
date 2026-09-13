# Chip + Probe Hygiene — sapa-ai (2026-09-03)

Session learnings from the chip-keyword fix (`1334697`) + localhost crash fix (`fbfee4f`).

## Chip keywords (sapa-only, probe-verified)

Queries must be short single-topic strings with proven `matched>0` against live
SPLP (2048 records / 38 OPD):

`stunting`, `prevalensi stunting`, `IPM`, `PDRB`, `kopi arabika`, `ASN`,
`kesehatan`, `pendidikan`, `Belanja APBD`, `sebaran data sapa per tahun`

Anti-pattern: long natural-language chips (`berapa jumlah ASN di aceh tengah`,
`Tenaga Kerja`, `Pertanian`) — they miss or drag wrong aggregates.
Group label: `SAPA · SPLP` + hint with real record/OPD counts.

## Bucket pitfall

Route `prevalensi` to bucket C BEFORE the `stunting` check — `Prevalensi
Stunting` contains `stunting` and otherwise lands in bucket A, polluting the
Hero (730) with % values.

## OAuth pitfall

Never read `SAPA_CLIENT_SECRET` at module top level in `sapa-client.ts` — a
missing env crashes every import on localhost. Wrap in lazy
`getSapaAccessToken()`.

## Probe hygiene (approval timeouts)

`curl ... | python3 -c ...` pipes and shell `&` backgrounding trigger approval
blocks. Instead: `curl ... --output /tmp/probe.json` then `read_file`, and
`terminal(background=true)` for `next start`. Verify with `ls -lh` +
`read_file`; never claim from transcript.
