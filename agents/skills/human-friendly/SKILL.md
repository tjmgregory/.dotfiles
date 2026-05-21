---
name: human-friendly
description: Renders the next structured response (plan, design proposal, architecture notes, anything that would normally be more than ~5 lines of headers/bullets/tables) as an editable HTML artifact on the user's Desktop instead of as chat output, then opens it in the default browser. Use when the user invokes /human-friendly, or when the user explicitly asks for plans/designs to be delivered as an editable HTML doc rather than markdown in chat.
---

# Human-Friendly Plans

When this skill is active, the next response that would normally be a structured plan (multi-step plan, architecture notes, design proposal, anything > ~5 lines with headers, bullets, or tables) is written to disk as an editable HTML file and opened in the browser. The chat reply is reduced to a one-or-two-sentence summary plus the file path.

The HTML file is the artifact. The user can mutate it freely in the browser (designMode is on — type anywhere, Cmd+S writes back to disk). Do not duplicate the plan in chat.

## When to apply

Apply to the NEXT plan-shaped response after activation. After that response is written, the skill's job is done — subsequent turns are normal chat unless `/human-friendly` is invoked again.

A "plan-shaped" response is anything that would normally render in chat as more than about 5 lines of structured content — multiple headings, multiple bullet groups, a table, a numbered sequence of steps, etc. For short conversational answers, ignore the skill and reply normally in chat.

## Procedure

1. **Decide on a slug.** Derive a short kebab-case slug from the plan topic (e.g. "Plan: migrate auth to OAuth" → `migrate-auth-to-oauth`). Keep it under ~50 chars, lowercase, alphanumeric + hyphens only.

2. **Build the body HTML.** Compose the plan as HTML using these elements (all already styled by the template):
   - `<h1>` — the plan title (also goes in `<title>`)
   - `<p class="subtitle">` — optional one-line subtitle
   - `<div class="meta">` with `<span><b>Label</b>Value</span>` items, and `<span class="pill">…</span>` for status-style chips — optional
   - `<hr>` — separator
   - `<h2>`, `<h3>`, `<h4>`, `<h5>` — section headings
   - `<p>` — paragraphs (the template uses `<p>` as the default block; do NOT use `<div>` for prose)
   - `<ul>` / `<ol>` with `<li>` — lists
   - `<blockquote><p>…</p></blockquote>` — quotes / callouts
   - `<table><thead><tr><th>…</th></tr></thead><tbody><tr><td>…</td></tr></tbody></table>` — tables
   - `<code>…</code>` inline; `<pre><code>…</code></pre>` for code blocks
   - `<a href="…">` for links

3. **Read the template.** Read `assets/template.html` from this skill directory. (Resolve via the skill's own path; do not hardcode a user path.)

4. **Swap the body.** Produce the output HTML by making exactly these substitutions on the template:
   - Replace the contents of `<title>…</title>` with the plan title (plain text only).
   - Replace everything between `<main>` and `</main>` (inclusive of the inner content, exclusive of the `<main>` tags themselves) with the body HTML from step 2. The body MUST start with `<h1>` matching the plan title.
   - Leave EVERYTHING ELSE untouched: `<!doctype html>`, `<head>` (except the `<title>` swap), all `<style>`, the `<div class="banner">` at the top of `<body>`, and the entire `<script>` block. These power the editing, save, undo, shortcuts, and table affordances — do not modify them.

5. **Write the file.** Save to `~/Desktop/<slug>.html`. If a file with that slug already exists, append `-2`, `-3`, etc., until you find a free name. Do not overwrite without confirmation.

6. **Open it.** Run `open <absolute-path>` via Bash. This launches the user's default browser.

7. **Reply in chat.** One or two sentences max: what the plan covers, plus the absolute file path. Do NOT recap the plan content — the HTML is the artifact, the user is about to read it there.

## Reading the user's edits back

If a later turn references "the plan I edited" or similar, read the HTML file back from disk — it is the new source of truth, not the original draft. The user may have rewritten headings, added rows, deleted bullets, etc. Parse the `<main>…</main>` section for the current content.

## Worked example

User invokes `/human-friendly` then says: "Plan the OAuth migration — phases, owners, rollout."

Output flow:
- Slug: `oauth-migration`
- Path: `~/Desktop/oauth-migration.html`
- Body HTML inside `<main>`: `<h1>OAuth Migration Plan</h1>`, a `<p class="subtitle">`, a `.meta` div with Owner/Status/Target, `<hr>`, then `<h2>` sections for Phases / Owners / Rollout, with `<ol>` and a `<table>`.
- Write file, run `open ~/Desktop/oauth-migration.html`.
- Chat reply: "Wrote the OAuth migration plan to ~/Desktop/oauth-migration.html and opened it — edit anything in the browser, ⌘S to save."

## Notes

- The template depends on the File System Access API for in-place save (Chromium browsers). On Safari/Firefox it falls back to a download. This is fine; the template handles it.
- The banner, table-wrap buttons, and any `data-ui` elements are injected by the script at load time and stripped on save — never include them in the body HTML you produce.
- Do not edit the template at `assets/template.html` from inside this skill at runtime. Treat it as read-only.
