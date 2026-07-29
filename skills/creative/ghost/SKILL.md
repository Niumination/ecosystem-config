---
name: ghost
description: "Rewrite AI-generated or stilted text so it reads naturally and human — stripping common AI writing tells while preserving all factual content."
version: 1.1.0
author: Agentpedia (sisi-tarak) + Niumination
source: sisi-tarak/claude-skills
tags: [creative, writing, humanizer, content]
platforms: [macos, linux]
---

# Ghost — AI Text Humanizer

## Purpose
Close the gap between "technically correct" writing and writing that sounds like a specific human wrote it — because AI-generated text has recognizable patterns that readers increasingly notice and discount.

## When to Use
- A draft reads as generic, over-hedged, or oddly uniform in rhythm.
- A user explicitly asks to make text sound more human/natural.
- Content will be published somewhere authorship and tone matters (emails, posts, essays under someone's name).

## Required Context
- The draft text to revise.
- Ideally, a sample of the target voice (the person's past writing) — without one, aim for generically natural rather than a specific voice.

## Inputs
- The text to rewrite.
- Optional: a voice/tone sample or explicit style constraints.

## Outputs
- The same content, restructured to read naturally: varied sentence length, direct claims instead of hedged ones, transitions cut rather than padded.

## Step-by-Step Workflow
1. **Cut hedging that isn't load-bearing.** "It's worth noting that," "In many cases," "It's important to remember" — remove unless the qualification is actually doing work.
2. **Vary sentence rhythm.** Uniform medium-length sentences are a tell; mix short punchy ones with longer ones.
3. **Replace empty transitions** ("Furthermore," "Additionally," "Moreover") with either nothing or a transition that carries real meaning.
4. **Remove reflexive even-handedness** ("On one hand... on the other hand...") where the content doesn't actually require balancing two views.
5. **Cut restated conclusions** — don't summarize a paragraph immediately after making its point.
6. **Read it aloud (mentally).** If it doesn't sound like something a person would say out loud, it likely still reads as generated.
7. **Preserve all factual content and claims exactly** — this is a style pass, not a content pass; never change what's being asserted while fixing how it's said.

## Best Practices
- Match register to context — "natural" for a technical doc looks different from "natural" for a social post.
- Keep specific, concrete details (numbers, names, examples) — genericness is itself a tell, independent of sentence structure.
- When a voice sample exists, mirror its actual quirks rather than a generic "human" default.

## Common Mistakes
- Over-correcting into forced casualness (slang, exclamation points) that's its own kind of tell.
- Changing factual claims or softening/hardening statements while trying to fix tone — style and substance should stay separate.
- Applying the same treatment regardless of context (a legal memo and a tweet shouldn't converge on the same "natural" voice).

## Token Optimization Notes
- Apply as a single pass over the full draft rather than sentence-by-sentence — rhythm variation only works evaluated across the whole piece.

## Related Skills
- `creative/ghost/SKILL.md` (this skill)
