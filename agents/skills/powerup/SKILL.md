---
name: powerup
description: Drafts a daily PowerUp update for the Ramen Club Slack — short post about what the user shipped, is working on, or is thinking about today, to keep the streak alive. Use when the user says "powerup", "daily update", "ramen club update", asks to post their PowerUp, or asks what to post for today.
---

# PowerUp (Ramen Club daily streak)

PowerUp is a Slack app that tracks a daily posting streak via a shared leaderboard. The user is in [Ramen Club](https://ramenclub.so), which runs one PowerUp channel for the community. FAQs: https://ramenclubhq.notion.site/PowerUp-FAQs-15abe6bdd83a450e967b578dc7a27287

## Rules that actually matter

- **One post per day = 1 point.** Multiple posts in a day still only count as 1 point. The point is the streak, not the volume.
- **Deadline: 00:00 UTC.** Anything after that rolls into the next day's bucket. The user is on UK time, so the deadline is **01:00 BST / 00:00 GMT**.
- **Weekend mode is on.** Saturday & Sunday (UTC) don't break the streak if missed — but posting still adds to it. Don't pressure the user to post on weekends.
- **Format is flexible.** PowerUp doesn't parse the message; any post counts. Bare text, a checklist, an emoji, "thinking about X" — all valid.

## House style (Ramen Club channel)

Members tend to use one of these shapes — pick whichever fits the day:

**Project-led with checkmarks** (common when shipping):
```
:todo-done: <Project>
  • <bullet>
  • <bullet>
```

**Narrative one-liner**:
```
Just looked for more leads today and reached out to a couple. Was a busy day at the competition.
```

**Status shorthand** (no emoji needed):
```
- working on <thing>
```

**Rest day**:
```
:todo-done: Rest day
```

Use the literal Slack shortcode `:todo-done:` (Slack renders it as the channel's custom checkmark emoji) — not a unicode ✅. Multiple `:todo-done:` blocks stacked is fine for multi-project days. Inline links to artefacts (live URL, PR, doc, screenshot) are welcome. Bullets are fragments, not sentences.

**Tone: understated.** No grandiosity, no hype words ("shipped a stack of", "closed the loop on", "real CNMC numbers"). Plain verbs, low-key framing, let the numbers speak. "Merged 3 playbooks into one" beats "consolidated feasibility playbooks into a single viability-deep-dive". If a bullet sounds like a LinkedIn post, rewrite it.

## Drafting flow

When the user asks for help drafting today's PowerUp:

1. Ask, or infer, the day's shape: shipping mode, thinking mode, rest day. Don't manufacture activity.
2. If shipping mode, pull what they actually did:
   - Recent git activity across `~/tse/*`: `git -C <repo> log --since="6am" --author="$(git config user.email)" --pretty=format:"%h %s"` — covers all ventures.
   - Linear issues moved today: use the `linear-cli` skill (`--workspace the-software-engineer --assignee @me`).
   - Recent meetings via the `my-meetings` skill if the day was meeting-heavy.
3. Group by project, compress each project into 1–3 short bullets, drop noise (lockfile bumps, formatting, WIP commits). Surface obvious external links inline.
4. Output the draft as a single fenced code block ready to paste into Slack, AND pipe the same draft to `pbcopy` so it's already on the clipboard. Use a heredoc to preserve formatting exactly:
   ```bash
   pbcopy <<'EOF'
   <draft body, no fences>
   EOF
   ```
   Mention briefly that it's been copied to the clipboard.

If it's a rest day or nothing shipped, output `✅ Rest day` — don't pad. Still pipe it to `pbcopy`.

## Where to post

The Ramen Club Slack PowerUp channel. The user posts manually; this skill drafts, it doesn't send.
