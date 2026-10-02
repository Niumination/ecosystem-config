---
name: long-form-markdown-deliverables
description: Use when writing reports, plans, or backlog docs.
version: 1.0.0
---

# Long-form Markdown Deliverables

Reports, plans, backlog documents, registry rows, and any Markdown over roughly a screen of prose. The risk that makes this a separate skill: **generated long-form text silently acquires characters from another script**, and the corruption lands in committed files where a reader sees gibberish and cannot tell the document was ever machine-broken.

## The defect

Token generation splices in tokens from other scripts. Observed shapes:

```
plain Indonesian sentence      →   Temuan最重要的 yang harus ditetapkan
correct Indonesian             →   berkas yang的感情 sudah memenuhi EFI
correct Indonesian             →   perlu langkah 操作 dari Windows
correct Indonesian             →   sudah penuh (a full-width/Chinese variant)
correct Indonesian             →   服务 dan OpenCore  ("services" → CN + "and")
Latin-script splice, no CJK    →   setZona,  danPertanyaan,  Andastitucionalkan
whole commit message replaced  →   Mandarin prose + a leftover tool-call fragment
```

It correlates with length and with dense technical prose, and it can hit a `write_file` payload or a commit message exactly as easily as a document body.

**Never trust that a long write survived.** Verified length is not verification of content.

## Procedure

1. **Write the file with `write_file`, never a heredoc.** A multi-line `git commit -F - <<'EOF'` came back as one enormous message containing CJK prose and a stray tool-call fragment; the commit landed with that message. `write_file` lets you re-read before it counts.
2. **Re-read the file** after any write longer than a few hundred characters. Check the paragraphs you did not intend to change, not just the first lines.
3. **Run the scanner on every file you wrote:**
   ```bash
   python3 ~/.hermes/skills/ecosystem/long-form-markdown-deliverables/scripts/scan-foreign-chars.py <file> [...]
   ```
   Exit 0 = clean. Exit 1 = findings with line numbers and context. Fix each one, then re-run.
4. **Read the flagged context, do not assume.** A CJK hit is usually a whole spliced phrase that must be rewritten, not one character to delete.
5. **Commit messages go through a file.** Write the message with `write_file`, re-read it, confirm zero foreign characters, then `git commit -F <file>`. Verify afterwards with `git log -1 --format='%B'`.
6. **When a commit message or file is already corrupted,** amend rather than adding a second commit. Confirm the *files* are clean separately (`git show --stat`, then scan each path) before assuming the damage was only in the message.

## Latin-script splices are not regex-detectable

`setZona`, `danPertanyaan`, and `Andastitucionalkan` contain no CJK — the scanner will pass them. Catch them by reading the diff of prose you wrote, especially at the seam where a sentence was assembled from fragments. When you notice one, fix it and re-read that whole section.

## Standing output requirements

- Close any complex report with a `## Bukti` section: the commands run and their exit codes.
- Mark anything you could not verify as `UNCHECKED` plus the reason. Never let a plausible claim stand in for a measurement.
- Redact credentials, tokens, and personal numbers by shape (prefix + last characters + length), never by value.
- Keep documents in their designated home; do not invent new folders under `docs/`.

## Boundaries

Emoji, box-drawing, arrows, and checkmarks are legitimate in these documents — the scanner deliberately ignores them. Widen the scanner's ranges only if the documents genuinely contain CJK text, not because a scan came back noisy.
