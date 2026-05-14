---
name: skill-seekers
description: Use when creating, enhancing, packaging, or managing AI skills from documentation, codebases, GitHub repos, PDFs, videos, and 17+ source types using the Skill Seekers CLI. Covers the full workflow from source ingestion to deployment on Claude, Gemini, OpenAI, and RAG platforms.
---

# Skill Seekers

Skill Seekers is the data layer for AI systems. It converts documentation sites, GitHub repos, local codebases, PDFs, videos, notebooks, and 17+ source types into structured knowledge assets — ready for Claude skills, RAG pipelines, vector databases, and AI coding assistants.

## When to Use This Skill

- Creating a new AI skill from any source (docs, GitHub, PDF, local code, video, etc.)
- Enhancing an existing skill with AI
- Packaging/uploading skills to Claude, Gemini, OpenAI, or other platforms
- Setting up unified multi-source skills (docs + code + PDF combined)
- Configuring enhancement workflows
- Troubleshooting scraping, enhancement, or packaging issues
- Working with the MCP server integration

## Getting Started

### 1. Install

```bash
pip install skill-seekers
```

### 2. Create your first skill

```bash
# Pick any documentation URL, GitHub repo, or local project
skill-seekers create https://docs.example.com/ -p quick --name my-first-skill
```

### 3. Enhance with AI (optional, takes quality from 3/10 to 9/10)

```bash
skill-seekers enhance output/my-first-skill/
```

### 4. Package and install

```bash
skill-seekers package output/my-first-skill/
skill-seekers install-agent output/my-first-skill/ --agent claude
```

Your skill is now available in `~/.claude/skills/my-first-skill/`.

## Installation

```bash
# Base install (Claude support included)
pip install skill-seekers

# With additional platform support
pip install skill-seekers[gemini]    # Google Gemini
pip install skill-seekers[openai]    # OpenAI / ChatGPT
pip install skill-seekers[all-llms]  # All platforms
pip install skill-seekers[video]     # Video extraction (YouTube, local)
pip install skill-seekers[all]       # Everything
```

## Core Workflow

The fundamental flow is: **Ingest → Enhance → Package → Deploy**

```bash
# 1. Create skill from any source (auto-detects type)
skill-seekers create <source>

# 2. Enhance with AI (optional but recommended — takes quality from 3/10 to 9/10)
skill-seekers enhance output/<name>/

# 3. Package for target platform
skill-seekers package output/<name>/ --target claude

# 4. Install to agent or upload
skill-seekers install-agent output/<name>/ --agent claude
# or
skill-seekers upload output/<name>.zip
```

## Commands Reference

### `create` — Universal Entry Point (auto-detects source type)

```bash
# URL → web docs scraping
skill-seekers create https://docs.react.dev/

# owner/repo → GitHub repository analysis
skill-seekers create facebook/react

# ./path → local codebase analysis
skill-seekers create ./my-project

# file.pdf → PDF extraction
skill-seekers create manual.pdf

# file.json → config file (multi-source)
skill-seekers create config.json
```

**Key flags:**

| Flag | Purpose |
|------|---------|
| `--name NAME` | Override auto-detected name |
| `-p quick\|standard\|comprehensive` | Analysis depth preset (1-2m / 5-10m / 20-60m) |
| `--enhance-level 0-3` | 0=off, 1=SKILL.md only, 2=+arch/config (default), 3=full |
| `--enhance-workflow PRESET` | Apply named workflow (e.g., `security-focus`, `api-documentation`) |
| `-o DIR` | Output directory |
| `--dry-run` | Preview without executing |

### `scrape` — Documentation Website Scraping

```bash
# With preset config
skill-seekers scrape --config configs/react.json

# Direct URL (needs config file for non-interactive mode)
skill-seekers create https://docs.example.com/ --name myskill
```

**Key flags:**

| Flag | Purpose |
|------|---------|
| `--config FILE` | JSON config with selectors, URL patterns, categories |
| `--max-pages N` | Limit pages scraped |
| `--resume` | Continue interrupted scrape |
| `--fresh` | Clear checkpoint and restart |
| `--workers N` | Parallel workers (1-10, default 1) |
| `--async` | Async mode for 2-3x faster scraping |

### `github` — GitHub Repository Analysis

```bash
skill-seekers github --repo owner/repo --name myskill
```

**Key flags:**

| Flag | Purpose |
|------|---------|
| `--repo OWNER/REPO` | Target repository |
| `--token TOKEN` | GitHub PAT (or set `GITHUB_TOKEN` env var) |
| `--local-repo-path PATH` | Use local clone for unlimited C3.x analysis |
| `--no-issues` | Skip fetching issues |
| `--max-issues N` | Limit issues fetched (default 100) |
| `--non-interactive` | CI/CD mode — fail fast, no prompts |
| `--profile NAME` | Use specific GitHub token profile |

### `unified` — Multi-Source Combination

Combines multiple sources into a single skill with conflict detection.

```bash
skill-seekers unified --config unified-config.json
```

**Config format:**

```json
{
  "name": "my-skill",
  "description": "Combined docs + code skill",
  "merge_mode": "claude-enhanced",
  "sources": [
    {
      "type": "documentation",
      "base_url": "https://docs.example.com/",
      "max_pages": 300,
      "enhance_level": 3
    },
    {
      "type": "github",
      "repo": "owner/repo",
      "include_code": true,
      "code_analysis_depth": "full",
      "enhance_level": 3
    },
    {
      "type": "pdf",
      "path": "./docs/manual.pdf"
    },
    {
      "type": "local",
      "path": "./my-project",
      "analysis_depth": "deep"
    }
  ]
}
```

**Merge modes:** `rule-based` (default, fast) or `claude-enhanced` (AI-powered conflict resolution)

**Source types:** `documentation`, `github`, `pdf`, `local`, `word`, `video`

### `enhance` — AI-Powered Skill Enhancement

Takes a basic skill from ~3/10 quality to ~9/10.

```bash
# Auto-detects API vs LOCAL mode
skill-seekers enhance output/myskill/

# Explicit API mode (needs ANTHROPIC_API_KEY, GOOGLE_API_KEY, or OPENAI_API_KEY)
skill-seekers enhance output/myskill/ --target claude

# Use specific agent
skill-seekers enhance output/myskill/ --agent claude
skill-seekers enhance output/myskill/ --agent copilot
skill-seekers enhance output/myskill/ --agent custom --agent-cmd "my-tool {prompt_file}"
```

**Enhancement levels:**
- `0` — Disabled
- `1` — SKILL.md generation only
- `2` — Plus architecture/config docs (default)
- `3` — Full enhancement (all reference files)

### `package` — Platform-Specific Packaging

```bash
skill-seekers package output/myskill/                    # Claude (default)
skill-seekers package output/myskill/ --target gemini    # Google Gemini
skill-seekers package output/myskill/ --target openai    # OpenAI / ChatGPT
skill-seekers package output/myskill/ --target langchain # LangChain Documents
skill-seekers package output/myskill/ --target llama-index
skill-seekers package output/myskill/ --target markdown  # Universal
```

### `upload` — Deploy to Platform

```bash
skill-seekers upload output/myskill.zip                           # Claude
skill-seekers upload output/myskill-gemini.tar.gz --target gemini # Gemini
skill-seekers upload output/myskill-openai.zip --target openai    # OpenAI
```

Requires the appropriate API key as env var (`ANTHROPIC_API_KEY`, `GOOGLE_API_KEY`, `OPENAI_API_KEY`).

### `install-agent` — Install to Local Agent Directory

```bash
skill-seekers install-agent output/myskill/ --agent claude   # ~/.claude/skills/
skill-seekers install-agent output/myskill/ --agent cursor   # Project .cursorrules
skill-seekers install-agent output/myskill/ --agent vscode
skill-seekers install-agent output/myskill/ --agent all      # All agents
```

### `quality` — Score Skill Quality

```bash
skill-seekers quality output/myskill/
skill-seekers quality output/myskill/ --report --threshold 7
```

### `config` — Configuration Management

```bash
skill-seekers config --show      # Display current config
skill-seekers config --github    # Set up GitHub tokens
skill-seekers config --api-keys  # Set up API keys
skill-seekers config --test      # Test all connections
```

Config location: `~/.config/skill-seekers/config.json`

### `workflows` — Enhancement Workflow Management

```bash
skill-seekers-workflows list                    # List all available workflows
skill-seekers-workflows show security-focus     # View workflow YAML
skill-seekers-workflows copy minimal            # Copy to user dir for editing
skill-seekers-workflows add my-workflow.yaml    # Add custom workflow
skill-seekers-workflows validate my-workflow    # Validate workflow
```

**Built-in workflow presets (selected):**
- `minimal` — Lightweight, SKILL.md only
- `api-documentation` — Comprehensive API docs
- `architecture-comprehensive` — Deep architectural analysis
- `security-focus` — Security-focused review
- `testing-focus` — Testing documentation
- `performance-optimization` — Bottleneck identification
- `migration-guide` — Version migration docs
- `troubleshooting-guide` — Common errors and debugging

### Other Source Commands

| Command | Source Type |
|---------|------------|
| `skill-seekers pdf --pdf FILE --name NAME` | PDF files |
| `skill-seekers word --file FILE --name NAME` | Word docs (.docx) |
| `skill-seekers epub --file FILE --name NAME` | EPUB e-books |
| `skill-seekers video --url URL --name NAME` | YouTube / local video |
| `skill-seekers jupyter --file FILE --name NAME` | Jupyter notebooks |
| `skill-seekers openapi --file FILE --name NAME` | OpenAPI/Swagger specs |
| `skill-seekers confluence --space SPACE --name NAME` | Confluence wikis |
| `skill-seekers notion --database-id ID --name NAME` | Notion pages |
| `skill-seekers chat --export-dir DIR --name NAME` | Slack/Discord exports |
| `skill-seekers manpage --name NAME` | Man pages |
| `skill-seekers rss --url URL --name NAME` | RSS/Atom feeds |
| `skill-seekers html --file FILE --name NAME` | Local HTML files |
| `skill-seekers asciidoc --file FILE --name NAME` | AsciiDoc documents |
| `skill-seekers pptx --file FILE --name NAME` | PowerPoint presentations |

## Common Workflows

### Quick skill from docs URL

```bash
skill-seekers create https://docs.example.com/ -p quick --name myskill
skill-seekers package output/myskill/
skill-seekers install-agent output/myskill/ --agent claude
```

### Comprehensive skill from GitHub + docs

```bash
# Create unified config
cat > config.json << 'EOF'
{
  "name": "myframework",
  "description": "Complete framework skill",
  "merge_mode": "claude-enhanced",
  "sources": [
    { "type": "documentation", "base_url": "https://docs.example.com/", "enhance_level": 3 },
    { "type": "github", "repo": "owner/repo", "include_code": true, "code_analysis_depth": "full", "enhance_level": 3 }
  ]
}
EOF

skill-seekers unified --config config.json --enhance-level 3
skill-seekers quality output/myframework/ --report
skill-seekers package output/myframework/
```

### Enhance an existing skill with custom workflow

```bash
# Apply security-focused enhancement
skill-seekers enhance output/myskill/ --enhance-workflow security-focus

# Chain multiple workflows
skill-seekers enhance output/myskill/ \
  --enhance-workflow architecture-comprehensive \
  --enhance-workflow testing-focus

# Add inline custom stage
skill-seekers enhance output/myskill/ \
  --enhance-stage 'perf:Identify performance bottlenecks and optimization opportunities'
```

### Custom workflow YAML

```yaml
name: "my-custom-workflow"
description: "Custom enhancement workflow"
stages:
  - name: "Security Audit"
    prompt: "Analyze for security issues, authentication patterns, and data handling"
  - name: "API Documentation"
    prompt: "Generate comprehensive API documentation with examples"
```

```bash
skill-seekers-workflows add my-workflow.yaml
skill-seekers create https://docs.example.com/ --enhance-workflow my-custom-workflow
```

## Environment Variables

| Variable | Purpose |
|----------|---------|
| `ANTHROPIC_API_KEY` | Claude API key (for enhancement + upload) |
| `GOOGLE_API_KEY` | Gemini API key |
| `OPENAI_API_KEY` | OpenAI API key |
| `GITHUB_TOKEN` | GitHub PAT (higher rate limits, private repos) |
| `ANTHROPIC_BASE_URL` | Custom Claude-compatible API endpoint |
| `SKILL_SEEKER_AGENT` | Default local agent for enhancement |

## Output Structure

After creating a skill, the output directory contains:

```
output/myskill/
├── SKILL.md              # Main skill file (the agent reads this)
├── references/           # Detailed reference documentation
│   ├── index.md          # Table of contents
│   ├── api.md            # API documentation
│   ├── getting-started.md
│   ├── tutorials.md
│   └── ...               # Category-organized reference files
├── scripts/              # Helper scripts
└── assets/               # Templates, boilerplate
```

## Key Concepts

### AI Skills
Structured knowledge packages (SKILL.md + references/) that give AI systems deep expertise in specific domains. The SKILL.md is the entry point agents read; references/ contains detailed docs organized by category.

### Three-Stream Architecture
GitHub repos are analyzed across three streams: **Code** (AST parsing, patterns, examples via C3.x), **Docs** (README, CONTRIBUTING, docs/*.md), and **Insights** (issues, labels, stars, community knowledge).

### C3.x Codebase Analysis
Comprehensive Codebase Context Extraction — deep AST parsing for Python, JS, TS, Java, C++, Go that detects design patterns, extracts test examples, generates how-to guides, and maps architecture. Levels: `surface` (1-2 min), `deep`, `full`/`c3x` (20-60 min).

### Enhancement Workflows
Reusable YAML-defined AI processing pipelines with named stages. Each stage sends a prompt to an LLM to transform/improve the skill. Presets ship with the tool; custom ones go in `~/.config/skill-seekers/workflows/`.

### Merge Modes
When combining multiple sources via `unified`, conflicts between docs and code are detected. `rule-based` applies deterministic priority rules; `claude-enhanced` uses AI for intelligent conflict resolution.

## API Reference

### Python API (Programmatic Usage)

```python
from skill_seekers.cli.unified_codebase_analyzer import UnifiedCodebaseAnalyzer

analyzer = UnifiedCodebaseAnalyzer()
result = analyzer.analyze(
    source="https://github.com/owner/repo",
    depth="c3x",
    fetch_github_metadata=True
)

# Code stream
print(f"Patterns: {len(result.code_analysis['c3_1_patterns'])}")
print(f"Test examples: {result.code_analysis['c3_2_examples_count']}")

# Docs stream
print(f"README: {result.github_docs['readme'][:100]}")

# Insights stream
print(f"Stars: {result.github_insights['metadata']['stars']}")
```

### MCP Server (26 tools via Model Context Protocol)

Set up for Claude Code:
```bash
./setup_mcp.sh
# Or manually add to mcp.json:
```

```json
{
  "mcpServers": {
    "skill-seeker": {
      "command": "python",
      "args": ["-m", "skill_seekers.mcp.server_fastmcp"]
    }
  }
}
```

Key MCP tools: `scrape_docs`, `scrape_github`, `scrape_pdf`, `package_skill`, `upload_skill`, `enhance_skill`, `generate_config`, `list_configs`, `validate_config`, `estimate_pages`.

## Gotchas and Known Issues

- **Unified scraper bug (v3.2.0):** The `unified` command's internal docs temp config uses legacy format, causing docs sources to fail. Workaround: scrape docs and GitHub separately, then merge manually or use `create` for each source individually.
- **C3.x analysis bug (v3.2.0):** `analyze_codebase()` may fail with `unexpected keyword argument 'enhance_with_ai'` in unified mode. Works fine in standalone `github` mode.
- **`scrape` command goes interactive:** When using `scrape` with just a URL and no `--config`, it drops into interactive mode even with other flags set. Use `create <URL>` instead for non-interactive usage.
- **Language detection:** Code examples sometimes get wrong language labels (e.g., bash commands labeled as `go` or `lua`). This is cosmetic but affects syntax highlighting.
- **Config format:** All configs must use the new unified format with `sources` array. Legacy format (`base_url` at top level) was removed in v2.11.0.
- **Rate limits:** Without a GitHub token, you get 60 requests/hour. With a token: 5,000/hour. Always set `GITHUB_TOKEN` for GitHub scraping.
- **Enhancement modes:** If `ANTHROPIC_API_KEY` is set, enhancement uses API mode automatically. To force local (Claude Code), unset the env var or use `--agent claude`.

## Reference Files

Detailed documentation is available in `references/`:

- **references/github/** — Repository README, issues, releases, file structure
- **references/docs/** — Scraped documentation organized by category (cli, manual, tutorials, integrations, getting-started, reference)

Read specific reference files when you need detailed information about a particular command, integration, or workflow.

## Resources

- **Repository:** https://github.com/yusufkaraaslan/Skill_Seekers
- **Website:** https://skillseekersweb.com/
- **PyPI:** https://pypi.org/project/skill-seekers/
- **Community configs:** https://github.com/yusufkaraaslan/skill-seekers-configs
- **GitHub Action:** https://github.com/yusufkaraaslan/skill-seekers-action
