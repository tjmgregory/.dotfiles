# Claude Code marketplace

This directory exposes the repo as a [Claude Code plugin marketplace](https://docs.claude.com/en/docs/claude-code/plugins) so others can install the skills it ships.

## Install

In Claude Code:

```
/plugin marketplace add tjmgregory/.dotfiles
/plugin install human-friendly@tjmgregory
```

The marketplace name is `tjmgregory` (see `marketplace.json`). Plugin sources are paths inside this repo, so installation pulls directly from the relevant subdirectory.

## Published plugins

| Name | What it does |
|---|---|
| `human-friendly` | Renders the next plan/design as an editable HTML doc on your Desktop instead of chat markdown — `designMode` editing, ⌘S file-save, markdown shortcuts, live reload. |

## Adding a new plugin

1. Author the skill under `agents/skills/<name>/` following the [agentskills.io](https://agentskills.io/specification) layout.
2. Add an entry to `plugins[]` in `marketplace.json` with `source: "./agents/skills/<name>"`.
3. Commit and push — installs are pulled from the default branch.
