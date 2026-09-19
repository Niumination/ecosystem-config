# Pipeline Build Cost Control & Auth Patterns

Techniques learned from video pipeline production and AgentRouter integration. Apply before any data pipeline or build.

## Pipeline: Regenerate Production Data Before Build

**Problem**: Pipelines that bundle a static artifact (e.g., `data/dossier.pdf`) alongside dynamic JSON (`data/live.json`) risk building from stale bundled data. The bundled artifact may be from a demo era and fail QC (`qc_angka_terlarang: N temuan`).

**Rule**: If a regeneration script exists (e.g., `make_dossier_live.py`), run it BEFORE `build --force`. The regeneration reads production JSON and overwrites the bundled artifact. Skipping this = building from stale data = wasted model quota + failed QC.

**Sequence**:
1. Check if `make_dossier_live.py` or equivalent exists
2. Run it: `python3 make_dossier_live.py` (regenerates `data/dossier.pdf` from `data/live.json`)
3. Verify output changed: `ls -la data/dossier.pdf` (mtime recent)
4. THEN run `bash hermes-run.sh build --force`

**Cost**: Skipping regeneration burns $5+ in model calls (tts + render + assemble) before failing at QC. Regeneration costs nothing.

## AgentRouter: Required Auth Header

**Problem**: AgentRouter (`sk-Od2...Jbmu` + system token `bJlvZAq0Wsgsu7JyQ44bgc607s7rLrY=`) returns `401 Unauthorized` on ALL endpoints without a specific header, even with correct credentials.

**Rule**: Every AgentRouter request MUST include `User-Agent: hermes-agent/0.19.0` header. Credentials alone are insufficient. Without this header, all 6 registered models return 401.

**Example**:
```bash
curl -s -H "Authorization: Bearer sk-Od2...Jbmu" \
     -H "Content-Type: application/json" \
     -H "User-Agent: hermes-agent/0.19.0" \
     http://127.0.0.1:20128/v1/models
```

**After fix**: `glm-5.3`, `deepseek-v4-flash` return 200. Other models (`gpt-6-astra`, `gpt-5.6-sol`, `claude-opus-5`, `claude-opus-4-8`) return 402 Payment Required — those need top-up at `ps.air-outer.com/console/token`.

## Video Pipeline: Venv & Dependencies

**Required venv**: `~/.venv-mata` with packages: `pillow`, `edge-tts`, `imageio-ffmpeg`, `fpdf2`.

**PEP 668**: macOS system Python rejects `pip install`. Use `uv venv ~/.venv-mata` then `uv pip install` or activate venv and use `pip install` inside it.

**Missing transitive dependency trap**: `imageio-ffmpeg` is required by `imageio` for FFmpeg binding. Without it, `ffmpeg` calls fail silently until `assemble`/`render` stages — ALL prior stages (tts, subsync, short) pass, burning quota before failure.

**Check before build**: `ls ~/.venv-mata/bin/ffmpeg` and `python3 -c "import imageio_ffmpeg; print(imageio_ffmpeg.get_ffmpeg_exe())"`.
