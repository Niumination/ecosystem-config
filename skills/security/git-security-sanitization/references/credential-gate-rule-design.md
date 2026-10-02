# Credential Gate: Prove the Rule Can Actually Fire

A gate that never matches is indistinguishable from a clean tree. Two failure modes hide a
credential past a scanner for as long as the credential lives, and both are silent.

## 1. Word-boundary anchors miss every SCREAMING_SNAKE name

`\b` cannot match immediately before `API_KEY` inside `CAMOFOX_API_KEY`, because `_` is a word
character — so there is no boundary there. A rule anchored that way silently excludes every
environment-variable name, which is the single most common place a leaked key sits:

```
BAD   \b(api[_-]?key|secret|token)\b\s*[=:]\s*["'][A-Za-z0-9_-]{24,}["']
GOOD  (?:\b|[A-Z0-9]+_)(?:api[_-]?key|admin[_-]?key|secret|token|access[_-]?key)\s*[=:]\s*["']?[A-Za-z0-9_-]{16,}["']?
```

Three fixes usually travel together — change one and re-test, because the others hide behind it:

| Symptom | Cause | Fix |
|---|---|---|
| `CAMOFOX_API_KEY=...` not caught | `\b` before `API_KEY` | explicit `(?:[A-Z0-9]+_)*` prefix run |
| a real 19-char key not caught | length floor set to 24 | lower the floor to 16, size it to the shortest real key |
| `..._ADMIN_KEY=...` not caught | `admin_key` absent from the alternation | enumerate every suffix actually in use |

The length floor is the subtle one: a floor tuned to "looks long enough" rejects short-but-real keys.
Derive the floor from the shortest credential the system actually issues, not from a round number.

## 2. A character class needs its headroom

`\d{16}` matches a 16-digit NIK, so a pattern written for exactly 16 digits also flags every longer
digit run — an order id, a timestamp, a 20-digit id — and those appear constantly in legitimate
files. Give the class room and anchor it:

```
\b\d{17,25}\b
```

Test both directions explicitly: a bare 16 digits must **not** match, and a 20-digit id must **not**
match. A rule that flags everything gets disabled, and a disabled rule catches nothing.

## 3. Lock the rules with a self-test the gate itself cannot trip

The gate's own source and its test file are staged content, so they must not contain a literal that
matches. Build fixtures at run time from concatenated fragments:

```python
V_API  = "API" + "_KEY"          # no literal `API_KEY=<value>` line anywhere
PREFIX = "CAMOFOX_" + V_API
S1     = "cfapi" + "-" + "synthetic0"
fixture = f'{PREFIX}="{S1}"'
```

Keep the assertions in two lists so a failure names the direction: `MUST_CATCH` (synthetic leaks) and
`MUST_PASS` (env-var references, shell/JS interpolation, `<REDACTED>`, `__PLACEHOLDER__` strings,
prose that merely names the variable). Both must be non-empty; a `MUST_PASS` list is what proves the
rule was not loosened into uselessness.

Comments explaining the rule are scanned too. Describe the pattern in prose — "the anchor missed
names where the underscore joins the prefix" — rather than pasting `CAMOFOX_API_KEY=value` into a
comment, which is exactly the shape the gate rejects.

Run the self-test after **every** rule change, and again immediately before committing a rule change:
the commit itself is the first test of whether the new rule blocks its own author.

## 4. Sanity-check the extractor when a test disagrees with itself

If a gate test fails while a direct regex probe of the same string passes, the extractor is lying, not
the pattern. Two known liars:

- the chat/shell output layer substituting a token-shaped string before you read it, so a match looks
  like a miss (`***`, `REDACTED`) and hand-written replacements come back as `replaced 0`
- a shell heredoc interpolating `$VAR`, turning the intended literal into an empty string

When output and reality disagree, re-probe with a script that prints only counts and labels, and
prefer editing over shell-embedded string surgery.