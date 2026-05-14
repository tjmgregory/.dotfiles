# Releases: yusufkaraaslan/Skill_Seekers

## v3.3.0: v3.3.0

**Published**: 2026-03-15

## [3.3.0] - 2026-03-16

**Theme:** 10 new source types (17 total), EPUB unified integration, sync-config command, performance optimizations, 12 README translations, and 19 bug fixes. 117 files changed, +41,588 lines since v3.2.0.

### Supported Source Types (17)

| # | Type | CLI Command | Config Type | Auto-Detection |
|---|------|-------------|-------------|----------------|
| 1 | Documentation (web) | `scrape` / `create <url>` | `documentation` | HTTP/HTTPS URLs |
| 2 | GitHub repository | `github` / `create owner/repo` | `github` | `owner/repo` or github.com URLs |
| 3 | PDF document | `pdf` / `create file.pdf` | `pdf` | `.pdf` extension |
| 4 | Word document | `word` / `create file.docx` | `word` | `.docx` extension |
| 5 | EPUB e-book | `epub` / `create file.epub` | `epub` | `.epub` extension |
| 6 | Video | `video` / `create <url/file>` | `video` | YouTube/Vimeo URLs, video extensions |
| 7 | Local codebase | `analyze` / `create ./path` | `local` | Directory paths |
| 8 | Jupyter Notebook | `jupyter` / `create file.ipynb` | `jupyter` | `.ipynb` extension |
| 9 | Local HTML | `html` / `create file.html` | `html` | `.html`/`.htm` extensions |
| 10 | OpenAPI/Swagger | `openapi` / `create spec.yaml` | `openapi` | `.yaml`/`.yml` with OpenAPI content |
| 11 | AsciiDoc | `asciidoc` / `create file.adoc` | `asciidoc` | `.adoc`/`.asciidoc` extensions |
| 12 | PowerPoint | `pptx` / `create file.pptx` | `pptx` | `.pptx` extension |
| 13 | RSS/Atom feed | `rss` / `create feed.rss` | `rss` | `.rss`/`.atom` extensions |
| 14 | Man pages | `manpage` / `create cmd.1` | `manpage` | `.1`–`.8`/`.man` extensions |
| 15 | Confluence wiki | `confluence` | `confluence` | API or export directory |
| 16 | Notion pages | `notion` | `notion` | API or export directory |
| 17 | Slack/Discord chat | `chat` | `chat` | Export directory or API |

### Added

#### 10 New Skill Source Types (17 total)

Skill Seekers now supports 17 source types — up from 7. Every new type is fully integrated into the CLI (`skill-seekers <type>`), `create` command auto-detection, unified multi-source configs, config validation, the MCP server, and the skill builder.

- **Jupyter Notebook** — `skill-seekers jupyter --notebook file.ipynb` or `skill-seekers create file.ipynb`
  - Extracts markdown cells, code cells with outputs, kernel metadata, imports, and language detection
  - Handles single files and directories of notebooks; filters `.ipynb_checkpoints`
  - Optional dependency: `pip install "skill-seekers[jupyter]"` (nbformat)
  - Entry point: `skill-seekers-jupyter`

- **Local HTML** — `skill-seekers html --html-path file.html` or `skill-seekers create file.html`
  - Parses HTML using BeautifulSoup with smart main content detection (`<article>`, `<main>`, `.content`, largest div)
  - Extracts headings, code blocks, tables (to markdown), images, links; converts inline HTML to markdown
  - Handles single files and directories; supports `.html`, `.htm`, `.xhtml` extensions
  - No extra dependencies (BeautifulSoup is a core dep)

- **OpenAPI/Swagger** — `skill-seekers openapi --spec spec.yaml` or `skill-seekers create spec.yaml`
  - Parses OpenAPI 3.0/3.1 and Swagger 2.0 specs from YAML or JSON (local files or URLs via `--spec-url`)
  - Extracts endpoints, parameters, request/response schemas, security schemes, tags
  - Resolves `$ref` references with circular reference protection; handles `allOf`/`oneOf`/`anyOf`
  - Groups endpoints by tags; generates comprehensive API reference markdown
  - Source detection sniffs YAML file content for `openapi:` or `swagger:` keys (avoids false positives on non-API YAML files)
  - Optional dependency: `pip install "skill-seekers[openapi]"` (pyyaml — already a core dep, guard added for safety)

- **AsciiDoc** — `skill-seekers asciidoc --asciidoc-path file.adoc` or `skill-seekers create file.adoc`
  - Regex-based parser (no external library required) with optional `asciidoc` library support
  - Extracts headings (= through =====), `[source,lang]` code blocks, `|===` tables, admonitions (NOTE/TIP/WARNING/IMPORTANT/CAUTION), and `include::` directives
  - Converts AsciiDoc formatting to markdown; handles single files and directories
  - Optional dependency: `pip install "skill-seekers[asciidoc]"` (asciidoc library for advanced rendering)

- **PowerPoint (.pptx)** — `skill-seekers pptx --pptx file.pptx` or `skill-seekers create file.pptx`
  - Extracts slide text, speaker notes, tables, images (with alt text), and grouped shapes
  - Detects code blocks by monospace font analysis (30+ font families)
  - Groups slides into sections by layout type; handles single files and directories
  - Optional dependency: `pip install "skill-seekers[pptx]"` (python-pptx)

- **RSS/Atom Feeds** — `skill-seekers rss --feed-url <url>` / `--feed-path file.rss` or `skill-seekers create feed.rss`
  - Parses RSS 2.0, RSS 1.0, and Atom feeds via feedparser
  - Optionally follows article links (`--follow-links`, default on) to scrape full page content using BeautifulSoup
  - Extracts article titles, summaries, authors, dates, categories; configurable `--max-articles` (default 50)
  - Source detection matches `.rss` and `.atom` extensions (`.xml` excluded to avoid false positives)
  - Optional dependency: `pip install "skill-seekers[rss]"` (feedparser)

- **Man Pages** — `skill-seekers manpage --man-names git,curl` / `--man-path dir/` or `skill-seekers create git.1`
  - Extracts man pages by running `man` command via subprocess or reading `.1`–`.8`/`.man` files directly
  - Handles gzip/bzip2/xz compressed man files; strips troff/groff formatting (backspace overstriking, macros, font escapes)
  - Parses structured sections (NAME, SYNOPSIS, DESCRIPTION, OPTIONS, EXAMPLES, SEE ALSO)
  - Source detection uses basename heuristic to avoid false positives on log rotation files (e.g., `access.log.1`)
  - No external dependencies (stdlib only)

- **Confluence** — `skill-seekers confluence --base-url <url> --space-key <key>` or `--export-path dir/`
  - API mode: fetches pages from Confluence REST API with pagination (`atlassian-python-api`)
  - Export mode: parses Confluence HTML/XML export directories
  - Extracts page content, code/panel/info/warning macros, page hierarchy, tables
  - Optional dependency: `pip install "skill-seekers[confluence]"` (atlassian-python-api)

- **Notion** — `skill-seekers notion --database-id <id>` / `--page-id <id>` or `--export-path dir/`
  - API mode: fetches pages via Notion API with support for 20+ block types (paragraph, heading, code, callout, toggle, table, etc.)
  - Export mode: parses Notion Markdown/CSV export directories
  - Extracts rich text with annotations (bold, italic, code, links), 16+ property types for database entries
  - Optional dependency: `pip install "skill-seekers[notion]"` (notion-client)

- **Slack/Discord Chat** — `skill-seekers chat --export-path dir/` or `--token <token> --channel <channel>`
  - Slack: parses workspace JSON exports or fetches via Slack Web API (`slack_sdk`)
  - Discord: parses DiscordChatExporter JSON or fetches via Discord HTTP API
  - Extracts messages, code snippets (fenced blocks), shared URLs, threads, reactions, attachments
  - Generates per-channel summaries and topic categorization
  - Optional dependency: `pip install "skill-seekers[chat]"` (slack-sdk)

#### EPUB Unified Pipeline Integration
- **EPUB (.epub) input support** via `skill-seekers create book.epub` or `skill-seekers epub --epub book.epub`
  - Extracts chapters, metadata (Dublin Core), code blocks, images, and tables from EPUB 2 and EPUB 3 files
  - DRM detection with clear error messages (Adobe ADEPT, Apple FairPlay, Readium LCP)
  - Font obfuscation correctly identified as non-DRM
  - EPUB 3 TOC bug workaround (`ignore_ncx` option)
  - `--help-epub` flag for EPUB-specific help
  - Optional dependency: `pip install "skill-seekers[epub]"` (ebooklib)
  - 107 tests across 14 test classes
- **EPUB added to unified scraper** — `_scrape_epub()` method, `scraped_data["epub"]`, config validation (`_validate_epub_source`), and dry-run display. Previously EPUB worked standalone but was missing from multi-source configs.

#### Unified Skill Builder — Generic Merge System
- **`_generic_merge()`** — Priority-based section merge for any combination of source types not covered by existing pairwise synthesis (docs+github, docs+pdf, etc.). Produces YAML frontmatter + source-attributed sections.
- **`_append_extra_sources()`** — Appends additional source type content (e.g., Jupyter + PPTX) to pairwise-synthesized SKILL.md.
- **`_generate_generic_references()`** — Generates `references/<type>/index.md` for any source type, with ID resolution fallback chain.
- **`_SOURCE_LABELS`** dict — Human-readable labels for all 17 source types used in merge attribution.

#### Config Validator Expansion
- **17 source types in `VALID_SOURCE_TYPES`** — All new types plus `word` and `video` now have per-type validation methods.
- **`_validate_word_source()`** — Validates `path` field for Word documents (was previously missing).
- **`_validate_video_source()`** — Validates `url`, `path`, or `playlist` field for video sources (was previously missing).
- **11 new `_validate_*_source()` methods** — One for each new type with appropriate required-field checks.

#### Source Detection Improvements
- **7 new file extension detections** in `SourceDetector.detect()` — `.ipynb`, `.html`/`.htm`, `.pptx`, `.adoc`/`.asciidoc`, `.rss`/`.atom`, `.1`–`.8`/`.man`, `.yaml`/`.yml` (with content sniffing)
- **`_looks_like_openapi()`** — Content sniffing for YAML files: only classifies as OpenAPI if the file contains `openapi:` or `swagger:` key in first 20 lines (prevents false positives on docker-compose, Ansible, Kubernetes manifests, etc.)
- **Man page basename heuristic** — `.1`–`.8` extensions only detected as man pages if the basename has no dots (e.g., `git.1` matches but `access.log.1` does not)
- **`.xml` excluded from RSS detection** — Too generic; only `.rss` and `.atom` trigger RSS detection

#### MCP Server Integration
- **`scrape_generic` tool** — New MCP tool handles all 10 new source types via subprocess with per-type flag mapping
- **`_PATH_FLAGS` / `_URL_FLAGS` dicts** — Correct flag routing for each source type (e.g., jupyter→`--notebook`, html→`--html-path`, rss→`--feed-url`)
- **`GENERIC_SOURCE_TYPES` tuple** — Lists all 10 new types for validation
- **Config validation display** — `validate_config` tool now shows source details for all new types
- **Tool count updated** — 33 → 34 tools (scraping tools 10 → 11)

#### CLI Wiring
- **10 new CLI subcommands** — `jupyter`, `html`, `openapi`, `asciidoc`, `pptx`, `rss`, `manpage`, `confluence`, `notion`, `chat` in `COMMAND_MODULES`
- **10 new argument modules** — `arguments/{jupyter,html,openapi,asciidoc,pptx,rss,manpage,confluence,notion,chat}.py` with per-type `*_ARGUMENTS` dicts
- **10 new parser modules** — `parsers/{jupyter,html,openapi,asciidoc,pptx,rss,manpage,confluence,notion,chat}_parser.py` with `SubcommandParser` implementations
- **`create` command routing** — `_route_generic()` method for all new types with correct module names and CLI flags
- **10 new entry points** in pyproject.toml — `skill-seekers-{jupyter,html,openapi,asciidoc,pptx,rss,manpage,confluence,notion,chat}`
- **7 new optional dependency groups** in pyproject.toml — `[jupyter]`, `[asciidoc]`, `[pptx]`, `[confluence]`, `[notion]`, `[rss]`, `[chat]`
- **`[all]` group updated** — Includes all 7 new optional dependencies

#### Sync Config Command
- **`skill-seekers sync-config`** — New subcommand that crawls a docs site's navigation, diffs discovered URLs against a config's `start_urls`, and optionally writes the updated list back with `--apply` (#306)
  - BFS link discovery with configurable depth (default 2), max-pages, rate-limit
  - Respects `url_patterns.include/exclude` from config
  - Supports optional `nav_seed_urls` config field
  - Handles both unified (sources array) and legacy flat config formats
  - MCP `sync_config` tool included
  - 57 tests (39 unit + 18 E2E with local HTTP server)

#### Workflow & Documentation
- **`complex-merge.yaml`** — New 7-stage AI-powered workflow for complex multi-source merging (source inventory → cross-reference → conflict detection → priority merge → gap analysis → synthesis → quality check)
- **AGENTS.md rewritten** — Updated with all 17 source types, scraper pattern docs, project layout, and key pattern documentation
- **77 new integration tests** in `test_new_source_types.py` — Source detection, config validation, generic merge, CLI wiring, validation, and create command routing
- **`docs/BEST_PRACTICES.md`** — Comprehensive guide for creating high-quality skills: SKILL.md structure, code examples, prerequisites, troubleshooting, quality targets, and real-world Grade F to Grade A example (#206)
- **Documentation updated for 17 source types** — 32 files updated across README, CLI reference, feature matrix, MCP reference, config format, API reference, unified scraping, multi-source guide, installation, quick-start, core concepts, user guide, FAQ, troubleshooting, architecture, and all Chinese (zh-CN) translations
- **README translations for 10 languages (12 total)** — Added Japanese (日本語), Korean (한국어), Spanish (Español), French (Français), German (Deutsch), Portuguese (Português), Turkish (Türkçe), Arabic (العربية), Hindi (हिन्दी), and Russian (Русский) README translations with language selector bar across all versions

### Performance
- **Pre-compiled regex and O(1) URL dedup in doc_scraper** — Module-level compiled patterns, `_enqueued_urls` set for O(1) dedup, cached URL patterns, async error logging fix (#309)
- **Bisect-based line indexing in code_analyzer and dependency_analyzer** — O(log n) `offset_to_line()` via bisect replaces O(n) `count("\n")` across all 10 language analyzers and all import extractors
- **O(n) parent class map for Python method detection** — Replaces O(n²) repeated AST walks in code_analyzer
- **O(1) tree traversal in github_scraper** — `deque.popleft()` replaces list `pop(0)`
- **Shared `build_line_index()` / `offset_to_line()` utilities** in `cli/utils.py` — DRY extraction from code_analyzer and dependency_analyzer

### Fixed
- **Config validator missing `word` and `video` dispatch** — `_validate_source()` had no `elif` branches for `word` or `video` types, silently skipping validation. Added dispatch entries and `_validate_word_source()` / `_validate_video_source()` methods.
- **`openapi_scraper.py` unconditional `import yaml`** — Would crash at import time if pyyaml not installed. Added `try/except ImportError` guard with `YAML_AVAILABLE` flag and `_check_yaml_deps()` helper.
- **`asciidoc_scraper.py` missing standard arguments** — `main()` manually defined args instead of using `add_asciidoc_arguments()`. Refactored to use shared argument definitions + added enhancement workflow integration.
- **`pptx_scraper.py` missing standard arguments** — Same issue. Refactored to use `add_pptx_arguments()`.
- **`chat_scraper.py` missing standard arguments** — Same issue. Refactored to use `add_chat_arguments()`.
- **`notion_scraper.py` missing `run_workflows` call** — `--enhance-workflow` flags were silently ignored. Added workflow runner integration.
- **`openapi_scraper.py` return type `None`** — `main()` returned `None` instead of `int`. Fixed to `return 0` on success, matching all other scrapers.
- **MCP `scrape_generic_tool` flag mismatch** — Was passing `--path`/`--url` as generic flags, but every scraper expects its own flag name (e.g., `--notebook`, `--html-path`, `--spec`). All 10 source types would have failed at runtime. Fixed with per-type `_PATH_FLAGS` and `_URL_FLAGS` mappings.
- **Word scraper `docx_id` key mismatch** — Unified scraper data dict used `docx_id` but generic reference generation looked for `word_id`. Added `word_id` alias.
- **`main.py` docstring stale** — Missing all 10 new commands. Updated to list all 27 commands.
- **`source_detector.py` module docstring stale** — Described only 5 source types. Updated to describe 14+ detected types.
- **`manpage_parser.py` docstring referenced wrong file** — Said `manpage_scraper.py` but actual file is `man_scraper.py`. Fixed.
- **Parser registry test count** — Updated expected count from 25 to 35 for 10 new parsers.
- **'Invalid IPv6 URL' error on bracket-containing URLs (#284)** — URLs with square brackets (e.g., `/api/[v1]/users`) discovered via BFS crawl or HTML extraction bypassed the original fix in `_clean_url()`. Added shared `sanitize_url()` utility applied at every URL ingestion point. 16 new tests.
- **GitHub scraper 'list index out of range' on issue extraction (#269)** — PyGithub's `PaginatedList` slicing could fail on some versions or empty repos. Replaced with `itertools.islice()`.
- **Release workflow version mismatch** — GitHub release showed wrong version (v3.1.3 instead of v3.2.0) because no explicit release name was set and sed regex had unescaped dots. Added explicit `name`/`tag_name`, version consistency check (tag vs pyproject.toml vs package), and empty release notes fallback.
- **Release workflow Python 3.10 compatibility** — Version consistency check used `tomllib` (Python 3.11+). Replaced with grep/sed for 3.10 compatibility.
- **`infer_categories()` "tutorial" vs "tutorials" key mismatch** — Guard checked `'tutorial'` but wrote to `'tutorials'` key, risking silent overwrites in category inference.
- **Flaky `test_benchmark_metadata_overhead`** — Stabilized with 20 iterations, warm-up run, median averaging, and 200% threshold (was failing on CI with 5 iterations and mean).
- **CI branch protection check permanently pending** — Summary job was named 'All Checks Complete' but branch protection required 'Tests'. PRs were stuck as 'Expected — Waiting for status to be reported'. Renamed job to match.



## v3.2.0: v3.2.0 — Video Extraction, Word Support, Pinecone Adaptor

**Published**: 2026-03-02

## v3.2.0 — Video Extraction, Word Support, Pinecone Adaptor

**Theme:** Video source support, Word document support, Pinecone adaptor, and quality improvements. 94 files changed, +23,500 lines since v3.1.3. **2,540 tests passing.**

### 🎬 Video Extraction Pipeline

Complete video extraction system that converts YouTube videos and local video files into AI-consumable skills.

- **`skill-seekers video --url <youtube-url>`** — New CLI command for video scraping
- **`skill-seekers create <youtube-url>`** — Auto-detects YouTube URLs
- **Transcript extraction** — 3-tier fallback: YouTube API → yt-dlp → faster-whisper
- **Visual OCR** — Multi-engine ensemble (EasyOCR + pytesseract) for code frames
- **Panel detection** — Splits IDE screenshots into independent sub-sections
- **Code timeline** — Tracks code evolution across frames with edit history
- **Two-pass AI enhancement** — Cleans OCR noise using transcript context
- **GPU auto-detection** — `skill-seekers video --setup` detects CUDA/ROCm/CPU and installs correct PyTorch
- **197 tests** covering models, metadata, transcript, visual, OCR, and CLI

### 📄 Word Document (.docx) Support

- **`skill-seekers word --docx <file>`** — Full pipeline: mammoth → HTML → sections → SKILL.md
- **`skill-seekers create document.docx`** — Auto-detects .docx files
- **Smart code detection** — Identifies monospace paragraphs as code blocks
- **Install:** `pip install skill-seekers[docx]`

### 🌲 Pinecone Vector Database Adaptor

- **`skill-seekers package output/ --format pinecone --upload`** — Direct Pinecone upload
- Full CRUD operations with namespace support
- OpenAI and Sentence Transformers embedding support
- Batch upsert with configurable batch sizes
- **764 tests** for comprehensive coverage

### 🐛 Bug Fixes

- **6 OCR quality fixes** — Skip webcam frames, clean IDE decorations, fix duplicate lines, filter UI junk
- **15 video pipeline fixes** — Timeout handling, MCP integration, filename collisions, dependency management
- **Issue #300** — Selector fallback & dry-run link discovery (ReactFlow found 20+ pages, was 1)
- **Issue #301** — `setup.sh` macOS fix
- **RAG chunking crash** — Fixed `AttributeError: output_dir`
- **Chunk overlap auto-scaling** — Scales to `max(50, chunk_tokens // 10)`
- **Reference file limits removed** — No more caps on GitHub issues, releases, or code blocks
- See [CHANGELOG.md](https://github.com/yusufkaraaslan/Skill_Seekers/blob/main/CHANGELOG.md) for full details

### 📦 Install / Upgrade

```bash
pip install --upgrade skill-seekers

# With video support
pip install skill-seekers[video]
skill-seekers video --setup  # Auto-detect GPU, install deps

# With Word support
pip install skill-seekers[docx]

# With Pinecone
pip install skill-seekers[pinecone]

# Everything
pip install skill-seekers[all]
```

**Full Changelog:** https://github.com/yusufkaraaslan/Skill_Seekers/blob/main/CHANGELOG.md

## v3.1.3: v3.1.3

**Published**: 2026-02-24

## [3.1.3] - 2026-02-24

### 🐛 Hotfix — Explicit Chunk Flags & Argument Pipeline Cleanup

### Fixed
- **Issue #299: `skill-seekers package --target claude` unrecognised argument crash** — `_reconstruct_argv()` in `main.py` emits default flag values back into argv when routing subcommands. `package_skill.py` had a 105-line inline argparser that used different flag names to those in `arguments/package.py`, so forwarded flags were rejected. Fixed by replacing the inline block with a call to `add_package_arguments(parser)` — the single source of truth.

### Changed
- **`package_skill.py` argparser refactored** — Replaced ~105 lines of inline argparse duplication with a single `add_package_arguments(parser)` call. Flag names are now guaranteed consistent with `_reconstruct_argv()` output, preventing future argument-name drift.
- **Explicit chunk flag names** — All `--chunk-*` flags now include unit suffixes to eliminate ambiguity between RAG tokens and streaming characters:
  - `--chunk-size` (RAG tokens) → `--chunk-tokens`
  - `--chunk-overlap` (RAG tokens) → `--chunk-overlap-tokens`
  - `--chunk` (enable RAG chunking) → `--chunk-for-rag`
  - `--streaming-chunk-size` (chars) → `--streaming-chunk-chars`
  - `--streaming-overlap` (chars) → `--streaming-overlap-chars`
  - `--chunk-size` in PDF extractor (pages) → `--pdf-pages-per-chunk`
- **`setup_logging()` centralized** — Added `setup_logging(verbose, quiet)` to `utils.py` and removed 4 duplicate module-level `logging.basicConfig()` calls from `doc_scraper.py`, `github_scraper.py`, `codebase_scraper.py`, and `unified_scraper.py`



## v3.1.2: v3.1.2 — Gemini Fix & Enhance Dispatcher

**Published**: 2026-02-24

## What's Changed

### 🐛 Critical Bug Fixes

**Gemini enhancement 404 errors** — The `gemini-2.0-flash-exp` model was retired by Google, causing all Gemini enhancement requests to fail with 404. Replaced with `gemini-2.5-flash` (stable GA).

**`skill-seekers enhance` auto-detection** — The documented behaviour of automatically using API mode when an API key is present was never implemented. This release fixes it:
- `ANTHROPIC_API_KEY` set → Claude API mode
- `GOOGLE_API_KEY` set → Gemini API mode  
- `OPENAI_API_KEY` set → OpenAI API mode
- No key → LOCAL mode (Claude Code Max, free)

Use `--mode LOCAL` to force local mode even when API keys are present.

**`create` command argument forwarding** — Universal flags (`--dry-run`, `--verbose`, `--quiet`, `--name`, `--description`) were crashing when used with GitHub, PDF, and codebase sources. All fixed. Also adds `--dry-run` support to `skill-seekers github` and `skill-seekers pdf`.

## Upgrade

```bash
pip install --upgrade skill-seekers
```

```bash
docker pull yusufk/skill-seekers:latest
```

## Full Changelog

See [CHANGELOG.md](https://github.com/yusufkaraaslan/Skill_Seekers/blob/main/CHANGELOG.md) for complete details.

## v3.1.1: v3.1.1

**Published**: 2026-02-23

## What's Changed
* fix: use getattr for max_pages in create command web routing by @YusufKaraaslanSpyke in https://github.com/yusufkaraaslan/Skill_Seekers/pull/294
* hotfix: v3.1.1 — fix create command max_pages AttributeError by @yusufkaraaslan in https://github.com/yusufkaraaslan/Skill_Seekers/pull/295
* Max page hot fix by @yusufkaraaslan in https://github.com/yusufkaraaslan/Skill_Seekers/pull/296


**Full Changelog**: https://github.com/yusufkaraaslan/Skill_Seekers/compare/v3.1.0...v3.1.1

## v3.1.0: v3.1.0 — Unified CLI & Developer Experience

**Published**: 2026-02-22

## 🎯 v3.1.0 — "Unified CLI & Developer Experience"

> **One command for everything. 65 workflow presets. 178 production configs. 2280+ tests.**

---

### 🚀 What's New

#### ✨ Unified `create` Command — One command to rule them all

No more remembering which command to use. Just `create` with anything:

```bash
# Auto-detects source type
skill-seekers create https://docs.react.dev/          # → web scraper
skill-seekers create facebook/react                   # → GitHub analysis
skill-seekers create ./my-project                     # → local codebase
skill-seekers create tutorial.pdf                     # → PDF extraction
skill-seekers create configs/react.json               # → multi-source unified

# Quick preset shortcut (-p)
skill-seekers create https://docs.react.dev/ -p quick
skill-seekers create facebook/react -p comprehensive

# Progressive help — no more flag overwhelm
skill-seekers create --help            # 13 universal flags (clean)
skill-seekers create --help-web        # web-specific options
skill-seekers create --help-github     # GitHub-specific options
skill-seekers create --help-all        # every flag (120+)
```

#### 🔧 65 Enhancement Workflow Presets

Tailor your skills for specific use cases with bundled workflow presets:

```bash
# Chain multiple workflows
skill-seekers create facebook/react \
  --enhance-workflow security-focus \
  --enhance-workflow api-documentation

# Manage presets
skill-seekers workflows list                    # Browse all 65 bundled presets
skill-seekers workflows show security-focus     # Inspect a preset
skill-seekers workflows copy security-focus     # Copy to user dir for customization
skill-seekers workflows add my-preset.yaml      # Add custom preset
```

Bundled presets cover: `security-focus`, `api-documentation`, `architecture-comprehensive`, `testing-focus`, `microservices-patterns`, `kubernetes-deployment`, `database-schema`, `mlops-pipeline`, `rest-api-design`, `graphql-schema`, `responsive-design`, `performance-optimization`, `accessibility-a11y` and [50+ more](https://github.com/yusufkaraaslan/Skill_Seekers/tree/main/src/skill_seekers/workflows).

#### ⚡ Smart Enhancement Dispatcher

```bash
# Auto-detects API key or falls back to Claude Code CLI
skill-seekers enhance output/react/

# Explicit target
skill-seekers enhance output/react/ --target gemini

# Docker/root guard — clear error instead of silent failure
# (fixes #286, #289)
```

#### 📄 ReStructuredText (RST) Support

Sphinx/RST documentation sites now extract content properly — class references, code blocks, tables, and cross-references are all parsed correctly.

---

### 🗃️ 178 Production Configs — All Reviewed & Enhanced

All configs in [skill-seekers-configs](https://github.com/yusufkaraaslan/skill-seekers-configs) brought to **v1.1.0 quality standard**:

- ✅ All `max_pages` fields removed (deprecated, defaults apply automatically)
- ✅ 5–13 categories per config, 3–6 keywords each
- ✅ Semantic selector fallback chains (`article, main, div[role='main']`)
- ✅ Outdated URLs fixed (Astro v3 restructure, Laravel 12.x)
- ✅ `scripts/validate-config.py` bug fixes

---

### 🐛 Notable Bug Fixes

| Fix | Issue |
|-----|-------|
| `--enhance-workflow` flag forwarding in `create` command | workflows were silently ignored |
| LOCAL enhancement blocked for root/Docker users | fixes #286, #289 |
| `%APPDATA%` config paths on Windows | fixes #283 |
| Bracket characters in llms.txt URLs (IPv6 parse error) | fixes #284 |
| Unified config categories not found in `validate-config.py` | multi-source configs always failed |

---

### 📊 Stats

| Metric | v3.0.0 | v3.1.0 |
|--------|--------|--------|
| Tests passing | 1,852 | **2,280+** |
| Enhancement workflow presets | 0 | **65** |
| Production configs | 178 | **178 (all reviewed)** |
| CLI entry points | 22 | **23** (`workflows`) |
| Platforms supported | 16 | **16** |

---

### 📦 Installation

```bash
pip install skill-seekers==3.1.0
# or
pip install --upgrade skill-seekers
```

### 🐳 Docker

```bash
docker pull yusufk/skill-seekers:3.1.0
docker pull yusufk/skill-seekers:latest

# MCP server
docker pull yusufk/skill-seekers-mcp:3.1.0
```

---

### 🔗 Links

- [Full Changelog](https://github.com/yusufkaraaslan/Skill_Seekers/blob/main/CHANGELOG.md#3.1.0)
- [PyPI Package](https://pypi.org/project/skill-seekers/3.1.0/)
- [Config Repository](https://github.com/yusufkaraaslan/skill-seekers-configs)
- [Documentation](https://skillseekersweb.com)

---

**Full Changelog**: https://github.com/yusufkaraaslan/Skill_Seekers/compare/v3.0.0...v3.1.0

## v3.0.0: v3.0.0

**Published**: 2026-02-08

## [3.0.0] - 2026-02-10

### 🚀 "Universal Intelligence Platform" - Major Release

**Theme:** Transform any documentation into structured knowledge for any AI system.

This is our biggest release ever! v3.0.0 establishes Skill Seekers as the **universal documentation preprocessor** for the entire AI ecosystem - from RAG pipelines to AI coding assistants to Claude skills.

### Highlights

- 🚀 **16 platform adaptors** (up from 4 in v2.x)
- 🛠️ **26 MCP tools** (up from 9)
- ✅ **1,852 tests** passing (up from 700+)
- ☁️ **Cloud storage** support (S3, GCS, Azure)
- 🔄 **CI/CD ready** (GitHub Action + Docker)
- 📦 **12 example projects** for every integration
- 📚 **18 integration guides** complete

### Added - Platform Adaptors (16 Total)

#### RAG & Vector Databases (8)
- **LangChain** (`--format langchain`) - Output LangChain Document objects
- **LlamaIndex** (`--format llama-index`) - Output LlamaIndex TextNode objects
- **Chroma** (`--format chroma`) - Direct ChromaDB integration
- **FAISS** (`--format faiss`) - Facebook AI Similarity Search
- **Haystack** (`--format haystack`) - Deepset Haystack pipelines
- **Qdrant** (`--format qdrant`) - Qdrant vector database
- **Weaviate** (`--format weaviate`) - Weaviate vector search
- **Pinecone-ready** (`--target markdown`) - Markdown format ready for Pinecone

#### AI Platforms (3)
- **Claude** (`--target claude`) - Claude AI skills (ZIP + YAML)
- **Gemini** (`--target gemini`) - Google Gemini skills (tar.gz)
- **OpenAI** (`--target openai`) - OpenAI ChatGPT (ZIP + Vector Store)

#### AI Coding Assistants (4)
- **Cursor** (`--target claude` + `.cursorrules`) - Cursor IDE integration
- **Windsurf** (`--target claude` + `.windsurfrules`) - Windsurf/Codeium
- **Cline** (`--target claude` + `.clinerules`) - VS Code extension
- **Continue.dev** (`--target claude`) - Universal IDE support

#### Generic (1)
- **Markdown** (`--target markdown`) - Generic ZIP export

### Added - MCP Tools (26 Total)

#### Config Tools (3)
- `generate_config` - Generate scraping configuration
- `list_configs` - List available preset configs
- `validate_config` - Validate config JSON structure

#### Scraping Tools (8)
- `estimate_pages` - Estimate page count before scraping
- `scrape_docs` - Scrape documentation websites
- `scrape_github` - Scrape GitHub repositories
- `scrape_pdf` - Extract from PDF files
- `scrape_codebase` - Analyze local codebases
- `detect_patterns` - Detect design patterns in code
- `extract_test_examples` - Extract usage examples from tests
- `build_how_to_guides` - Build how-to guides from code

#### Packaging Tools (4)
- `package_skill` - Package skill for target platform
- `upload_skill` - Upload to LLM platform
- `enhance_skill` - AI-powered enhancement
- `install_skill` - One-command complete workflow

#### Source Tools (5)
- `fetch_config` - Fetch config from remote source
- `submit_config` - Submit config for approval
- `add_config_source` - Add Git config source
- `list_config_sources` - List config sources
- `remove_config_source` - Remove config source

#### Splitting Tools (2)
- `split_config` - Split large configs
- `generate_router` - Generate router skills

#### Vector DB Tools (4)
- `export_to_weaviate` - Export to Weaviate
- `export_to_chroma` - Export to ChromaDB
- `export_to_faiss` - Export to FAISS
- `export_to_qdrant` - Export to Qdrant

### Added - Cloud Storage

Upload skills directly to cloud storage:

- **AWS S3** - `skill-seekers cloud upload --provider s3 --bucket my-bucket`
- **Google Cloud Storage** - `skill-seekers cloud upload --provider gcs --bucket my-bucket`
- **Azure Blob Storage** - `skill-seekers cloud upload --provider azure --container my-container`

Features:
- Upload/download directories
- List files with metadata
- Check file existence
- Generate presigned URLs
- Cloud-agnostic interface

### Added - CI/CD Support

#### GitHub Action
```yaml
- uses: skill-seekers/action@v1
  with:
    config: configs/react.json
    format: langchain
```

Features:
- Auto-update on doc changes
- Matrix builds for multiple frameworks
- Scheduled updates
- Caching for faster runs

#### Docker
```bash
docker run -v $(pwd):/data skill-seekers:latest scrape --config /data/config.json
```

### Added - Production Infrastructure

- **Helm Charts** - Kubernetes deployment
- **Docker Compose** - Local vector DB stack
- **Monitoring** - Sentry integration, sync monitoring
- **Benchmarking** - Performance testing framework

### Added - 12 Example Projects

Complete working examples for every integration:

1. **langchain-rag-pipeline** - React docs → LangChain → Chroma
2. **llama-index-query-engine** - Vue docs → LlamaIndex
3. **pinecone-upsert** - Documentation → Pinecone
4. **chroma-example** - Full ChromaDB workflow
5. **faiss-example** - FAISS index building
6. **haystack-pipeline** - Haystack RAG pipeline
7. **qdrant-example** - Qdrant vector DB
8. **weaviate-example** - Weaviate integration
9. **cursor-react-skill** - React skill for Cursor
10. **windsurf-fastapi-context** - FastAPI for Windsurf
11. **cline-django-assistant** - Django assistant for Cline
12. **continue-dev-universal** - Universal IDE context

### Quality Metrics

- ✅ **1,852 tests** across 100 test files
- ✅ **58,512 lines** of Python code
- ✅ **80+ documentation** files
- ✅ **100% test coverage** for critical paths
- ✅ **CI/CD** on every commit

### Fixed

#### URL Conversion Bug with Anchor Fragments (Issue #277)
- **Critical Bug Fix**: Fixed 404 errors when scraping documentation with anchor links
  - **Problem**: URLs with anchor fragments (e.g., `#synchronous-initialization`) were malformed
    - Incorrect: `https://example.com/docs/api#method/index.html.md` ❌
    - Correct: `https://example.com/docs/api/index.html.md` ✅
  - **Root Cause**: `_convert_to_md_urls()` didn't strip anchor fragments before appending `/index.html.md`
  - **Solution**: Parse URLs with `urllib.parse` to remove fragments and deduplicate base URLs
  - **Impact**: Prevents duplicate requests for the same page with different anchors
  - **Additional Fix**: Changed `.md` detection from `".md" in url` to `url.endswith('.md')`
    - Prevents false matches on URLs like `/cmd-line` or `/AMD-processors`
- **Test Coverage**: 12 comprehensive tests covering all edge cases
  - Anchor fragment stripping
  - Deduplication of multiple anchors on same URL
  - Query parameter preservation
  - Trailing slash handling
  - Real-world MikroORM case validation
  - 54/54 tests passing (42 existing + 12 new)
- **Reported by**: @devjones via Issue #277

### Added

#### Extended Language Detection (NEW)
- **7 New Programming Languages**: Dart, Scala, SCSS, SASS, Elixir, Lua, Perl
  - Pattern-based detection with confidence scoring (0.6-0.8+ thresholds)
  - **70 regex patterns** prioritizing unique identifiers (weight 5)
  - Framework-specific patterns:
    - **Dart**: Flutter widgets (`StatelessWidget`, `StatefulWidget`, `Widget build()`)
    - **Scala**: Pattern matching (`case class`, `trait`, `match {}`)
    - **SCSS**: Preprocessor features (`$variables`, `@mixin`, `@include`, `@extend`)
    - **SASS**: Indented syntax (`=mixin`, `+include`, `$variables`)
    - **Elixir**: Functional patterns (`defmodule`, `def ... do`, pipe operator `|>`)
    - **Lua**: Game scripting (`local`, `repeat...until`, `~=`, `elseif`)
    - **Perl**: Text processing (`my $`, `use strict`, `sub`, `chomp`, regex `=~`)
  - **Comprehensive test coverage**: 7 new tests, 30/30 passing (100%)
  - **False positive prevention**: Unique identifiers (weight 5) + confidence thresholds
  - **No regressions**: All existing language detection tests still pass
  - **Total language support**: Now 27+ programming languages
  - **Credit**: Contributed by @PaawanBarach via PR #275

#### Multi-Agent Support for Local Enhancement (NEW)
- **Multiple Coding Agent Support**: Choose your preferred local coding agent for SKILL.md enhancement
  - **Claude Code** (default): Claude Code CLI with `--dangerously-skip-permissions`
  - **Codex CLI**: OpenAI Codex CLI with `--full-auto` and `--skip-git-repo-check`
  - **Copilot CLI**: GitHub Copilot CLI (`gh copilot chat`)
  - **OpenCode CLI**: OpenCode CLI
  - **Custom agents**: Use any CLI tool with `--agent custom --agent-cmd "command {prompt_file}"`
- **CLI Arguments**: New flags for agent selection
  - `--agent`: Choose agent (claude, codex, copilot, opencode, custom)
  - `--agent-cmd`: Override command template for custom agents
- **Environment Variables**: CI/CD friendly configuration
  - `SKILL_SEEKER_AGENT`: Default agent to use
  - `SKILL_SEEKER_AGENT_CMD`: Default command template for custom agents
- **Security First**: Custom command validation
  - Blocks dangerous shell characters (`;`, `&`, `|`, `$`, `` ` ``, `\n`, `\r`)
  - Validates executable exists in PATH
  - Safe parsing with `shlex.split()`
- **Dual Input Modes**: Supports both file-based and stdin-based agents
  - File-based: Uses `{prompt_file}` placeholder (Claude, custom agents)
  - Stdin-based: Pipes prompt via stdin (Codex CLI)
- **Backward Compatible**: Claude Code remains the default, no breaking changes
- **Comprehensive Tests**: 13 new tests covering all agent types and security validation
- **Agent Normalization**: Smart alias handling (e.g., "claude-code" → "claude")
- **Credit**: Contributed by @rovo79 (Robert Dean) via PR #270

#### C3.10: Signal Flow Analysis for Godot Projects (NEW)
- **Complete Signal Flow Analysis System**: Analyze event-driven architectures in Godot game projects
  - Signal declaration extraction (`signal` keyword detection)
  - Connection mapping (`.connect()` calls with targets and methods)
  - Emission tracking (`.emit()` and `emit_signal()` calls)
  - **208 signals**, **634 connections**, and **298 emissions** detected in test project (Cosmic Idler)
  - Signal density metrics (signals per file)
  - Event chain detection (signals triggering other signals)
  - Output: `signal_flow.json`, `signal_flow.mmd` (Mermaid diagram), `signal_reference.md`

- **Signal Pattern Detection**: Three major patterns identified
  - **EventBus Pattern** (0.90 confidence): Centralized signal hub in autoload
  - **Observer Pattern** (0.85 confidence): Multi-observer signals (3+ listeners)
  - **Event Chains** (0.80 confidence): Cascading signal propagation

- **Signal-Based How-To Guides (C3.10.1)**: AI-generated usage guides
  - Step-by-step guides (Connect → Emit → Handle)
  - Real code examples from project
  - Common usage locations
  - Parameter documentation
  - Output: `signal_how_to_guides.md` (10 guides for Cosmic Idler)

#### Godot Game Engine Support
- **Comprehensive Godot File Type Support**: Full analysis of Godot 4.x projects
  - **GDScript (.gd)**: 265 files analyzed in test project
  - **Scene files (.tscn)**: 118 scene files
  - **Resource files (.tres)**: 38 resource files
  - **Shader files (.gdshader, .gdshaderinc)**: 9 shader files
  - **C# integration**: Phantom Camera addon (13 files)

- **GDScript Language Support**: Complete GDScript parsing with regex-based extraction
  - Dependency extraction: `preload()`, `load()`, `extends` patterns
  - Test framework detection: GUT, gdUnit4, WAT
  - Test file patterns: `test_*.gd`, `*_test.gd`
  - Signal syntax: `signal`, `.connect()`, `.emit()`
  - Export decorators: `@export`, `@onready`
  - Test decorators: `@test` (gdUnit4)

- **Game Engine Framework Detection**: Improved detection for Unity, Unreal, Godot
  - **Godot markers**: `project.godot`, `.godot` directory, `.tscn`, `.tres`, `.gd` files
  - **Unity markers**: `Assembly-CSharp.csproj`, `UnityEngine.dll`, `ProjectSettings/ProjectVersion.txt`
  - **Unreal markers**: `.uproject`, `Source/`, `Config/DefaultEngine.ini`
  - Fixed false positive Unity detection (was using generic "Assets" keyword)

- **GDScript Test Extraction**: Extract usage examples from Godot test files
  - **396 test cases** extracted from 20 GUT test files in test project
  - Patterns: instantiation (`preload().new()`, `load().new()`), assertions (`assert_eq`, `assert_true`), signals
  - GUT framework: `extends GutTest`, `func test_*()`, `add_child_autofree()`
  - Test categories: instantiation, assertions, signal connections, setup/teardown
  - Real code examples from production test files

#### C3.9: Project Documentation Extraction
- **Markdown Documentation Extraction**: Automatically extracts and categorizes all `.md` files from projects
  - Smart categorization by folder/filename (overview, architecture, guides, workflows, features, etc.)
  - Processing depth control: `surface` (raw copy), `deep` (parse+summarize), `full` (AI-enhanced)
  - AI enhancement (level 2+) adds topic extraction and cross-references
  - New "📖 Project Documentation" section in SKILL.md
  - Output to `references/documentation/` organized by category
  - Default ON, use `--skip-docs` to disable
  - 15 new tests for documentation extraction features

#### Granular AI Enhancement Control
- **`--enhance-level` Flag**: Fine-grained control over AI enhancement (0-3)
  - Level 0: No AI enhancement (default)
  - Level 1: SKILL.md enhancement only (fast, high value)
  - Level 2: SKILL.md + Architecture + Config + Documentation
  - Level 3: Full enhancement (patterns, tests, config, architecture, docs)
- **Config Integration**: `default_enhance_level` setting in `~/.config/skill-seekers/config.json`
- **MCP Support**: All MCP tools updated with `enhance_level` parameter
- **Independent from `--comprehensive`**: Enhancement level is separate from feature depth

#### C# Language Support
- **C# Test Example Extraction**: Full support for C# test frameworks
  - Language alias mapping (C# → csharp, C++ → cpp)
  - NUnit, xUnit, MSTest test framework patterns
  - Mock pattern support (NSubstitute, Moq)
  - Zenject dependency injection patterns
  - Setup/teardown method extraction
  - 2 new tests for C# extraction features

#### Performance Optimizations
- **Parallel LOCAL Mode AI Enhancement**: 6-12x faster with ThreadPoolExecutor
  - Concurrent workers: 3 (configurable via `local_parallel_workers`)
  - Batch processing: 20 patterns per Claude CLI call (configurable via `local_batch_size`)
  - Significant speedup for large codebases
- **Config Settings**: New `ai_enhancement` section in config
  - `local_batch_size`: Patterns per CLI call (default: 20)
  - `local_parallel_workers`: Concurrent workers (default: 3)

#### UX Improvements
- **Auto-Enhancement**: SKILL.md automatically enhanced when using `--enhance` or `--comprehensive`
  - No need for separate `skill-seekers enhance` command
  - Seamless one-command workflow
  - 10-minute timeout for large codebases
  - Graceful fallback with retry instructions on failure
- **LOCAL Mode Fallback**: All AI enhancements now fall back to LOCAL mode when no API key is set
  - Applies to: pattern enhancement (C3.1), test examples (C3.2), architecture (C3.7)
  - Uses Claude Code CLI instead of failing silently
  - Better UX: "Using LOCAL mode (Claude Code CLI)" instead of "AI disabled"

- Support for custom Claude-compatible API endpoints via `ANTHROPIC_BASE_URL` environment variable
- Compatibility with GLM-4.7 and other Claude-compatible APIs across all AI enhancement features

### Changed
- All AI enhancement modules now respect `ANTHROPIC_BASE_URL` for custom endpoints
- Updated documentation with GLM-4.7 configuration examples
- Rewritten LOCAL mode in `config_enhancer.py` to use Claude CLI properly with explicit output file paths
- Updated MCP `scrape_codebase_tool` with `skip_docs` and `enhance_level` parameters
- Updated CLAUDE.md with C3.9 documentation extraction feature
- Increased default batch size from 5 to 20 patterns for LOCAL mode

### Fixed
- **C# Test Extraction**: Fixed "Language C# not supported" error with language alias mapping
- **Config Type Field Mismatch**: Fixed KeyError in `config_enhancer.py` by supporting both "type" and "config_type" fields
- **LocalSkillEnhancer Import**: Fixed incorrect import and method call in `main.py` (SkillEnhancer → LocalSkillEnhancer)
- **Code Quality**: Fixed 4 critical linter errors (unused imports, variables, arguments, import sorting)

#### Godot Game Engine Fixes
- **GDScript Dependency Extraction**: Fixed 265+ "Syntax error in *.gd" warnings (commit 3e6c448)
  - GDScript files were incorrectly routed to Python AST parser
  - Created dedicated `_extract_gdscript_imports()` with regex patterns
  - Now correctly parses `preload()`, `load()`, `extends` patterns
  - Result: 377 dependencies extracted with 0 warnings

- **Framework Detection False Positive**: Fixed Unity detection on Godot projects (commit 50b28fe)
  - Was detecting "Unity" due to generic "Assets" keyword in comments
  - Changed Unity markers to specific files: `Assembly-CSharp.csproj`, `UnityEngine.dll`, `Library/`
  - Now correctly detects Godot via `project.godot`, `.godot` directory

- **Circular Dependencies**: Fixed self-referential cycles (commit 50b28fe)
  - 3 self-loop warnings (files depending on themselves)
  - Added `target != file_path` check in dependency graph builder
  - Result: 0 circular dependencies detected

- **GDScript Test Discovery**: Fixed 0 test files found in Godot projects (commit 50b28fe)
  - Added GDScript test patterns: `test_*.gd`, `*_test.gd`
  - Added GDScript to LANGUAGE_MAP
  - Result: 32 test files discovered (20 GUT files with 396 tests)

- **GDScript Test Extraction**: Fixed "Language GDScript not supported" warning (commit c826690)
  - Added GDScript regex patterns to PATTERNS dictionary
  - Patterns: instantiation (`preload().new()`), assertions (`assert_eq`), signals (`.connect()`)
  - Result: 22 test examples extracted successfully

- **Config Extractor Array Handling**: Fixed JSON/YAML array parsing (commit fca0951)
  - Error: `'list' object has no attribute 'items'` on root-level arrays
  - Added isinstance checks for dict/list/primitive at root
  - Result: No JSON array errors, save.json parsed correctly

- **Progress Indicators**: Fixed missing progress for small batches (commit eec37f5)
  - Progress only shown every 5 batches, invisible for small jobs
  - Modified condition to always show for batches < 10
  - Result: "Progress: 1/2 batches completed" now visible

#### Other Fixes
- **C# Test Extraction**: Fixed "Language C# not supported" error with language alias mapping
- **Config Type Field Mismatch**: Fixed KeyError in `config_enhancer.py` by supporting both "type" and "config_type" fields
- **LocalSkillEnhancer Import**: Fixed incorrect import and method call in `main.py` (SkillEnhancer → LocalSkillEnhancer)
- **Code Quality**: Fixed 4 critical linter errors (unused imports, variables, arguments, import sorting)

### Tests
- **GDScript Test Extraction Test**: Added comprehensive test case for GDScript GUT/gdUnit4 framework
  - Tests player instantiation with `preload()` and `load()`
  - Tests signal connections and emissions
  - Tests gdUnit4 `@test` annotation syntax
  - Tests game state management patterns
  - 4 test functions with 60+ lines of GDScript code
  - Validates extraction of instantiations, assertions, and signal patterns

### Removed
- Removed client-specific documentation files from repository

---



## v2.9.0: v2.9.0 - Game Development Release: Godot Engine Support 🎮

**Published**: 2026-02-02

## 🎮 Game Development Release - Godot Engine Support

This release adds comprehensive support for **Godot game engine** projects with industry-leading signal flow analysis and complete GDScript language support.

### 🎮 Added

#### C3.10: Signal Flow Analysis for Godot Projects ⭐ NEW
- **Complete Signal Flow Analysis System**: Analyze event-driven architectures in Godot game projects
  - Signal declaration extraction (`signal` keyword detection)
  - Connection mapping (`.connect()` calls with targets and methods)
  - Emission tracking (`.emit()` and `emit_signal()` calls)
  - **Real-world results**: 208 signals, 634 connections, 298 emissions detected in Cosmic Idler test project
  - Signal density metrics (0.78 signals/file)
  - Event chain detection (signals triggering other signals)
  - Output: `signal_flow.json` (374KB), `signal_flow.mmd` (Mermaid diagram), `signal_reference.md` (34KB)

- **Signal Pattern Detection**: Three major patterns identified with confidence scoring
  - **EventBus Pattern** (0.90 confidence): Centralized signal hub in autoload
  - **Observer Pattern** (0.85 confidence): Multi-observer signals (3+ listeners, theme_changed: 21 connections)
  - **Event Chains** (0.80 confidence): Cascading signal propagation

- **Signal-Based How-To Guides (C3.10.1)**: AI-generated usage guides
  - Step-by-step guides (Connect → Emit → Handle)
  - Real code examples from project
  - Common usage locations with file references
  - Parameter documentation
  - Output: `signal_how_to_guides.md` (10 guides generated for Cosmic Idler)

#### Complete Godot Game Engine Support
- **Comprehensive Godot File Type Support**: Full analysis of Godot 4.x projects
  - **GDScript (.gd)**: 265 files analyzed in test project (59.8% of codebase)
  - **Scene files (.tscn)**: 118 scene files (26.6%)
  - **Resource files (.tres)**: 38 resource files (8.6%)
  - **Shader files (.gdshader, .gdshaderinc)**: 9 shader files (2.0%)
  - **C# integration**: Phantom Camera addon (13 files, 2.9%)

- **GDScript Language Support**: Complete GDScript parsing with regex-based extraction
  - Dependency extraction: `preload()`, `load()`, `extends` patterns
  - Test framework detection: GUT, gdUnit4, WAT
  - Test file patterns: `test_*.gd`, `*_test.gd`
  - Signal syntax: `signal`, `.connect()`, `.emit()`
  - Export decorators: `@export`, `@onready`
  - Test decorators: `@test` (gdUnit4)
  - 377 dependencies extracted with 0 syntax errors

- **Game Engine Framework Detection**: Improved detection for Unity, Unreal, Godot
  - **Godot markers**: `project.godot`, `.godot` directory, `.tscn`, `.tres`, `.gd` files
  - **Unity markers**: `Assembly-CSharp.csproj`, `UnityEngine.dll`, `ProjectSettings/ProjectVersion.txt`
  - **Unreal markers**: `.uproject`, `Source/`, `Config/DefaultEngine.ini`
  - Fixed false positive Unity detection (was using generic "Assets" keyword)
  - Priority-based detection (game engines detected before web frameworks)

- **GDScript Test Extraction**: Extract usage examples from Godot test files
  - **396 test cases** extracted from 20 GUT test files in Cosmic Idler test project
  - Patterns: instantiation (`preload().new()`, `load().new()`), assertions (`assert_eq`, `assert_true`), signals
  - GUT framework: `extends GutTest`, `func test_*()`, `add_child_autofree()`
  - Test categories: instantiation, assertions, signal connections, setup/teardown
  - Real code examples from production test files
  - 22 high-quality test examples extracted

### 🐛 Fixed

#### Godot-Specific Bug Fixes
- **GDScript Dependency Extraction** (commit 3e6c448): Fixed 265+ "Syntax error in *.gd" warnings
  - GDScript files were incorrectly routed to Python AST parser
  - Created dedicated `_extract_gdscript_imports()` with regex patterns
  - Now correctly parses `preload()`, `load()`, `extends` patterns
  - Result: 377 dependencies extracted with 0 warnings

- **Framework Detection False Positive** (commit 50b28fe): Fixed Unity detection on Godot projects
  - Was detecting "Unity" due to generic "Assets" keyword in comments
  - Changed Unity markers to specific files: `Assembly-CSharp.csproj`, `UnityEngine.dll`, `Library/`
  - Now correctly detects Godot via `project.godot`, `.godot` directory

- **Circular Dependencies** (commit 50b28fe): Fixed self-referential cycles
  - 3 self-loop warnings (files depending on themselves)
  - Added `target != file_path` check in dependency graph builder
  - Result: 0 circular dependencies detected

- **GDScript Test Discovery** (commit 50b28fe): Fixed 0 test files found in Godot projects
  - Added GDScript test patterns: `test_*.gd`, `*_test.gd`
  - Added GDScript to LANGUAGE_MAP
  - Result: 32 test files discovered (20 GUT files with 396 tests)

- **GDScript Test Extraction** (commit c826690): Fixed "Language GDScript not supported" warning
  - Added GDScript regex patterns to PATTERNS dictionary
  - Patterns: instantiation (`preload().new()`), assertions (`assert_eq`), signals (`.connect()`)
  - Result: 22 test examples extracted successfully

- **Config Extractor Array Handling** (commit fca0951): Fixed JSON/YAML array parsing
  - Error: `'list' object has no attribute 'items'` on root-level arrays
  - Added isinstance checks for dict/list/primitive at root
  - Result: No JSON array errors, save.json parsed correctly

- **Progress Indicators** (commit eec37f5): Fixed missing progress for small batches
  - Progress only shown every 5 batches, invisible for small jobs
  - Modified condition to always show for batches < 10
  - Result: "Progress: 1/2 batches completed" now visible

### 🧪 Tests
- **GDScript Test Extraction Test**: Added comprehensive test case for GDScript GUT/gdUnit4 framework
  - Tests player instantiation with `preload()` and `load()`
  - Tests signal connections and emissions
  - Tests gdUnit4 `@test` annotation syntax
  - Tests game state management patterns
  - 4 test functions with 60+ lines of GDScript code
  - Validates extraction of instantiations, assertions, and signal patterns

### 📊 Quality Metrics (Cosmic Idler Test Project)
- **SKILL.md Quality**: 9/10 rating (31KB, 1,030 lines)
- **File Coverage**: 98% (443/452 files analyzed)
- **Signal Analysis**: 208 signals, 634 connections, 298 emissions
- **Test Coverage**: 32 test files discovered, 22 examples extracted
- **Dependency Graph**: 377 dependencies, 0 circular cycles
- **Language Breakdown**: GDScript 59.8%, Scenes 26.6%, Resources 8.6%, Shaders 2.0%

### 📝 Files Changed
- **1 new file**: `signal_flow_analyzer.py` (489 lines)
- **15 modified files**: Core analyzers, test extractors, dependency analyzers
- **+1,574 additions, -157 deletions**

### 🎯 Use Cases
This release is perfect for:
- 🎮 Godot game developers wanting to understand signal architectures
- 📚 Teams documenting Godot projects for AI assistants (Claude, ChatGPT, Gemini)
- 🔍 Code reviewers analyzing event-driven patterns in games
- 🎓 Game development educators creating learning materials
- 🤖 AI agents needing deep understanding of Godot codebases

### 🙏 Thanks
Special thanks to the Godot community and **Cosmic Idler** project for providing an excellent test case for validating all features!

---

**Full Changelog**: https://github.com/yusufkaraaslan/Skill_Seekers/compare/v2.8.0...v2.9.0


## v2.8.0: v2.8.0

**Published**: 2026-02-02

## [2.8.0] - 2026-02-01

### 🚀 Major Feature Release - Enhanced Code Analysis & Documentation

This release brings powerful new code analysis features, performance optimizations, and international API support. Special thanks to all our contributors who made this release possible!

### Added

#### C3.9: Project Documentation Extraction
- **Markdown Documentation Extraction**: Automatically extracts and categorizes all `.md` files from projects
  - Smart categorization by folder/filename (overview, architecture, guides, workflows, features, etc.)
  - Processing depth control: `surface` (raw copy), `deep` (parse+summarize), `full` (AI-enhanced)
  - AI enhancement (level 2+) adds topic extraction and cross-references
  - New "📖 Project Documentation" section in SKILL.md
  - Output to `references/documentation/` organized by category
  - Default ON, use `--skip-docs` to disable
  - 15 new tests for documentation extraction features

#### Granular AI Enhancement Control
- **`--enhance-level` Flag**: Fine-grained control over AI enhancement (0-3)
  - Level 0: No AI enhancement (default)
  - Level 1: SKILL.md enhancement only (fast, high value)
  - Level 2: SKILL.md + Architecture + Config + Documentation
  - Level 3: Full enhancement (patterns, tests, config, architecture, docs)
- **Config Integration**: `default_enhance_level` setting in `~/.config/skill-seekers/config.json`
- **MCP Support**: All MCP tools updated with `enhance_level` parameter
- **Independent from `--comprehensive`**: Enhancement level is separate from feature depth

#### C# Language Support
- **C# Test Example Extraction**: Full support for C# test frameworks
  - Language alias mapping (C# → csharp, C++ → cpp)
  - NUnit, xUnit, MSTest test framework patterns
  - Mock pattern support (NSubstitute, Moq)
  - Zenject dependency injection patterns
  - Setup/teardown method extraction
  - 2 new tests for C# extraction features

#### Performance Optimizations
- **Parallel LOCAL Mode AI Enhancement**: 6-12x faster with ThreadPoolExecutor
  - Concurrent workers: 3 (configurable via `local_parallel_workers`)
  - Batch processing: 20 patterns per Claude CLI call (configurable via `local_batch_size`)
  - Significant speedup for large codebases
- **Config Settings**: New `ai_enhancement` section in config
  - `local_batch_size`: Patterns per CLI call (default: 20)
  - `local_parallel_workers`: Concurrent workers (default: 3)

#### UX Improvements
- **Auto-Enhancement**: SKILL.md automatically enhanced when using `--enhance` or `--comprehensive`
  - No need for separate `skill-seekers enhance` command
  - Seamless one-command workflow
  - 10-minute timeout for large codebases
  - Graceful fallback with retry instructions on failure
- **LOCAL Mode Fallback**: All AI enhancements now fall back to LOCAL mode when no API key is set
  - Applies to: pattern enhancement (C3.1), test examples (C3.2), architecture (C3.7)
  - Uses Claude Code CLI instead of failing silently
  - Better UX: "Using LOCAL mode (Claude Code CLI)" instead of "AI disabled"

- Support for custom Claude-compatible API endpoints via `ANTHROPIC_BASE_URL` environment variable
- Compatibility with GLM-4.7 and other Claude-compatible APIs across all AI enhancement features

### Changed
- All AI enhancement modules now respect `ANTHROPIC_BASE_URL` for custom endpoints
- Updated documentation with GLM-4.7 configuration examples
- Rewritten LOCAL mode in `config_enhancer.py` to use Claude CLI properly with explicit output file paths
- Updated MCP `scrape_codebase_tool` with `skip_docs` and `enhance_level` parameters
- Updated CLAUDE.md with C3.9 documentation extraction feature and --enhance-level flag
- Increased default batch size from 5 to 20 patterns for LOCAL mode

### Fixed
- **C# Test Extraction**: Fixed "Language C# not supported" error with language alias mapping
- **Config Type Field Mismatch**: Fixed KeyError in `config_enhancer.py` by supporting both "type" and "config_type" fields
- **LocalSkillEnhancer Import**: Fixed incorrect import and method call in `main.py` (SkillEnhancer → LocalSkillEnhancer)
- **Code Quality**: Fixed 4 critical linter errors (unused imports, variables, arguments, import sorting)

### Removed
- Removed client-specific documentation files from repository

### 🙏 Contributors

A huge thank you to everyone who contributed to this release:

- **[@xuintl](https://github.com/xuintl)** - Chinese README improvements and documentation refinements
- **[@Zhichang Yu](https://github.com/yuzhichang)** - GLM-4.7 support and PDF scraper fixes
- **[@YusufKaraaslanSpyke](https://github.com/yusufkaraaslan)** - Core features, bug fixes, and project maintenance

Special thanks to all our community members who reported issues, provided feedback, and helped test new features. Your contributions make Skill Seekers better for everyone! 🎉

---



## v2.7.4: v2.7.4 - Language Selector Link Fix

**Published**: 2026-01-21

## 🔧 Bug Fix - Language Selector Links

This **patch release** fixes the broken Chinese language selector link that appeared on PyPI and other non-GitHub platforms.

### Fixed

- **Broken Language Selector Links on PyPI**
  - **Issue**: Chinese language link used relative URL (`README.zh-CN.md`) which only worked on GitHub
  - **Impact**: Users on PyPI clicking "简体中文" got 404 errors
  - **Solution**: Changed to absolute GitHub URL
  - **Result**: Language selector now works on PyPI, GitHub, and all platforms
  - **Files Fixed**: `README.md`, `README.zh-CN.md`

### Links

- **PyPI Package**: https://pypi.org/project/skill-seekers/2.7.4/
- **Full Changelog**: https://github.com/yusufkaraaslan/Skill_Seekers/blob/main/CHANGELOG.md#274---2026-01-22

## v2.7.3: v2.7.3: International i18n Support 🌏

**Published**: 2026-01-21

# 🌏 International i18n Release

This **documentation release** adds comprehensive Chinese language support, making Skill Seekers accessible to the world's largest developer community.

## ✨ What's New

### 🇨🇳 Chinese (Simplified) Documentation
- **Complete README Translation** - 1,962 lines of comprehensive Chinese documentation (README.zh-CN.md)
- **Language Selector Badges** - Easy switching between English and Chinese in both READMEs
- **Machine Translation Disclaimer** - Honest labeling with invitation for community improvements
- **Community Engagement** - GitHub issue #260 created for native speakers to improve translation quality

### 📦 PyPI Metadata Internationalization
- **Updated Package Description** - Now highlights Chinese documentation availability
- **i18n Keywords** - Added "i18n", "chinese", "international" for better discoverability
- **Natural Language Classifiers** - English and Chinese (Simplified) officially declared
- **Direct Chinese README Link** - Added to project URLs for easy access from PyPI

## 🌍 Why This Matters

**Market Impact:**
- ✅ Reaches 1+ billion Chinese speakers worldwide
- ✅ Taps into the world's largest developer community
- ✅ Better discoverability on Chinese search engines (Baidu, Gitee, etc.)
- ✅ Professional image showing international awareness
- ✅ Competitive advantage - most similar tools lack Chinese documentation

**For Users:**
- ✅ Native language documentation lowers barrier to entry
- ✅ Better user experience with familiar terminology
- ✅ Increased engagement from Chinese developer community
- ✅ Potential for more contributors and feedback

## 🤝 Community Contribution

We invite Chinese developers to help improve the translation:

- **Review Issue**: [#260](https://github.com/yusufkaraaslan/Skill_Seekers/issues/260)
- **What to Review**: Technical accuracy, natural expression, terminology
- **How to Help**: Comment on the issue with suggestions or submit a PR

All contributions are welcome and appreciated!

## 📥 Installation



## 🔗 Important Links

- **Chinese README**: [README.zh-CN.md](https://github.com/yusufkaraaslan/Skill_Seekers/blob/main/README.zh-CN.md)
- **Community Review**: [Issue #260](https://github.com/yusufkaraaslan/Skill_Seekers/issues/260)
- **PyPI Package**: https://pypi.org/project/skill-seekers/2.7.3/
- **Official Website**: https://skillseekersweb.com/

## 📝 Full Changelog

See [CHANGELOG.md](https://github.com/yusufkaraaslan/Skill_Seekers/blob/main/CHANGELOG.md#273---2026-01-21) for complete release notes.

---

**语言 / Languages:**
- [English](https://github.com/yusufkaraaslan/Skill_Seekers/blob/main/README.md)
- [简体中文](https://github.com/yusufkaraaslan/Skill_Seekers/blob/main/README.zh-CN.md)

## v2.7.2: v2.7.2 - Critical CLI Bug Fixes

**Published**: 2026-01-21

## 🚨 Critical CLI Bug Fixes

This **hotfix release** resolves 4 critical CLI bugs reported in issues #258 and #259 that prevented core commands from working correctly.

### Fixed

**Issue #258: `install --config` command fails with unified scraper** (#258)
- **Root Cause**: `unified_scraper.py` missing `--fresh` and `--dry-run` argument definitions
- **Solution**: Added both flags to unified_scraper argument parser and main.py dispatcher
- **Impact**: `skill-seekers install --config react` now works without "unrecognized arguments" error

**Issue #259 (Original): `scrape` command doesn't accept URL and --max-pages** (#259)
- **Root Cause**: No positional URL argument or `--max-pages` flag support
- **Solution**: Added positional URL argument and `--max-pages` flag with safety warnings
- **Impact**: `skill-seekers scrape https://example.com --max-pages 50` now works
- **Safety Warnings**: Warns if max-pages > 1000 or < 10

**Issue #259 (Comment A): Version shows 2.7.0 instead of actual version** (#259)
- **Root Cause**: Hardcoded version string in main.py
- **Solution**: Import `__version__` from `__init__.py` dynamically
- **Impact**: `skill-seekers --version` now shows correct version (2.7.2)

**Issue #259 (Comment B): PDF command shows empty "Error: " message** (#259)
- **Root Cause**: Exception handler didn't handle empty exception messages
- **Solution**: Improved exception handler to show exception type and added context-specific messages
- **Impact**: PDF errors now show clear messages instead of just "Error: "

### Installation

```bash
pip install --upgrade skill-seekers
```

### Testing

- ✅ Verified all commands work with exact issue reproduction steps
- ✅ All 202 tests passing

### Full Changelog
https://github.com/yusufkaraaslan/Skill_Seekers/blob/main/CHANGELOG.md#272---2026-01-21

## v2.7.1: v2.7.1 - Critical Bug Fix: Config Download 404 Errors

**Published**: 2026-01-18

## 🚨 Critical Bug Fix - Config Download 404 Errors

This **hotfix release** resolves a critical bug causing 404 errors when downloading configs from the API.

### Fixed

- **Critical: Config download 404 errors** - Fixed bug where code was constructing download URLs manually instead of using the `download_url` field from the API response
  - **Root Cause**: Code was building `f"{API_BASE_URL}/api/download/{config_name}.json"` which failed when actual URLs differed (CDN URLs, version-specific paths)
  - **Solution**: Changed to use `config_info.get("download_url")` from API response in both MCP server implementations
  - **Files Fixed**:
    - `src/skill_seekers/mcp/tools/source_tools.py` (FastMCP server)
    - `src/skill_seekers/mcp/server_legacy.py` (Legacy server)
  - **Impact**: Fixes all config downloads from skillseekersweb.com API and private Git repositories
  - **Reported By**: User testing `skill-seekers install --config godot --unlimited`
  - **Testing**: All 15 source tools tests pass, all 8 fetch_config tests pass

### Installation

```bash
pip install --upgrade skill-seekers
```

Or install a specific version:

```bash
pip install skill-seekers==2.7.1
```

### Links

- **PyPI**: https://pypi.org/project/skill-seekers/2.7.1/
- **Website**: https://skillseekersweb.com/
- **Documentation**: https://github.com/yusufkaraaslan/Skill_Seekers/blob/main/README.md

---

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>

## v2.7.0: v2.7.0 - Smart Rate Limits, Multi-Token Config & Documentation Overhaul

**Published**: 2026-01-18

## [2.7.0] - 2026-01-18

### 🔐 Smart Rate Limit Management & Multi-Token Configuration

This **minor feature release** introduces intelligent GitHub rate limit handling, multi-profile token management, and comprehensive configuration system. Say goodbye to indefinite waits and confusing token setup!

### Added

- **🎯 Multi-Token Configuration System** - Flexible GitHub token management with profiles
  - **Secure config storage** at `~/.config/skill-seekers/config.json` with 600 permissions
  - **Multiple GitHub profiles** support (personal, work, OSS, etc.)
    - Per-profile rate limit strategies: `prompt`, `wait`, `switch`, `fail`
    - Configurable timeout per profile (default: 30 minutes)
    - Auto-detection and smart fallback chain
    - Profile switching when rate limited
  - **API key management** for Claude, Gemini, OpenAI
    - Environment variable fallback (ANTHROPIC_API_KEY, GOOGLE_API_KEY, OPENAI_API_KEY)
    - Config file storage with secure permissions
  - **Progress tracking** for resumable jobs
    - Auto-save at configurable intervals (default: 60 seconds)
    - Job metadata: command, progress, checkpoints, timestamps
    - Stored at `~/.local/share/skill-seekers/progress/`
  - **Auto-cleanup** of old progress files (default: 7 days, configurable)
  - **First-run experience** with welcome message and quick setup
  - **ConfigManager class** with singleton pattern for global access

- **🧙 Interactive Configuration Wizard** - Beautiful terminal UI for easy setup
  - **Main menu** with 7 options:
    1. GitHub Token Setup
    2. API Keys (Claude, Gemini, OpenAI)
    3. Rate Limit Settings
    4. Resume Settings
    5. View Current Configuration
    6. Test Connections
    7. Clean Up Old Progress Files
  - **GitHub token management**:
    - Add/remove profiles with descriptions
    - Set default profile
    - Browser integration - opens GitHub token creation page
    - Token validation with format checking (ghp_*, github_pat_*)
    - Strategy selection per profile
  - **API keys setup** with browser integration for each provider
  - **Connection testing** to verify tokens and API keys
  - **Configuration display** with current status and sources
  - **CLI commands**:
    - `skill-seekers config` - Main menu
    - `skill-seekers config --github` - Direct to GitHub setup
    - `skill-seekers config --api-keys` - Direct to API keys
    - `skill-seekers config --show` - Show current config
    - `skill-seekers config --test` - Test connections

- **🚦 Smart Rate Limit Handler** - Intelligent GitHub API rate limit management
  - **Upfront warning** about token status (60/hour vs 5000/hour)
  - **Real-time detection** of rate limits from GitHub API responses
    - Parses X-RateLimit-* headers
    - Detects 403 rate limit errors
    - Calculates reset time from timestamps
  - **Live countdown timers** with progress display
  - **Automatic profile switching** - tries next available profile when rate limited
  - **Four rate limit strategies**:
    - `prompt` - Ask user what to do (default, interactive)
    - `wait` - Auto-wait with countdown timer
    - `switch` - Automatically try another profile
    - `fail` - Fail immediately with clear error
  - **Non-interactive mode** for CI/CD (fail fast, no prompts)
  - **Configurable timeouts** per profile (prevents indefinite waits)
  - **RateLimitHandler class** with strategy pattern
  - **Integration points**: GitHub fetcher, GitHub scraper

- **📦 Resume Command** - Resume interrupted scraping jobs
  - **List resumable jobs** with progress details:
    - Job ID, started time, command
    - Current phase and file counts
    - Last updated timestamp
  - **Resume from checkpoints** (skeleton implemented, ready for integration)
  - **Auto-cleanup** of old jobs (respects config settings)
  - **CLI commands**:
    - `skill-seekers resume --list` - List all resumable jobs
    - `skill-seekers resume <job-id>` - Resume specific job
    - `skill-seekers resume --clean` - Clean up old jobs
  - **Progress storage** at `~/.local/share/skill-seekers/progress/<job-id>.json`

- **⚙️ CLI Enhancements** - New flags and improved UX
  - **--non-interactive flag** for CI/CD mode
    - Available on: `skill-seekers github`
    - Fails fast on rate limits instead of prompting
    - Perfect for automated pipelines
  - **--profile flag** to select specific GitHub profile
    - Available on: `skill-seekers github`
    - Uses configured profile from `~/.config/skill-seekers/config.json`
    - Overrides environment variables and defaults
  - **Entry points** for new commands:
    - `skill-seekers-config` - Direct config command access
    - `skill-seekers-resume` - Direct resume command access

- **🧪 Comprehensive Test Suite** - Full test coverage for new features
  - **16 new tests** in `test_rate_limit_handler.py`
  - **Test coverage**:
    - Header creation (with/without token)
    - Handler initialization (token, strategy, config)
    - Rate limit detection and extraction
    - Upfront checks (interactive and non-interactive)
    - Response checking (200, 403, rate limit)
    - Strategy handling (fail, wait, switch, prompt)
    - Config manager integration
    - Profile management (add, retrieve, switch)
  - **All tests passing** ✅ (16/16)
  - **Test utilities**: Mock responses, config isolation, tmp directories

- **🎯 Bootstrap Skill Feature** - Self-hosting capability (PR #249)
  - **Self-Bootstrap**: Generate skill-seekers as a Claude Code skill
    - `./scripts/bootstrap_skill.sh` - One-command bootstrap
    - Combines manual header with auto-generated codebase analysis
    - Output: `output/skill-seekers/` ready for Claude Code
    - Install: `cp -r output/skill-seekers ~/.claude/skills/`
  - **Robust Frontmatter Detection**:
    - Dynamic YAML frontmatter boundary detection (not hardcoded line counts)
    - Fallback to line 6 if frontmatter not found
    - Future-proof against frontmatter field additions
  - **SKILL.md Validation**:
    - File existence and non-empty checks
    - Frontmatter delimiter presence
    - Required fields validation (name, description)
    - Exit with clear error messages on validation failures
  - **Comprehensive Error Handling**:
    - UV dependency check with install instructions
    - Permission checks for output directory
    - Graceful degradation on missing header file

- **🔧 MCP Now Optional** - User choice for installation profile
  - **CLI Only**: `pip install skill-seekers` - No MCP dependencies
  - **MCP Integration**: `pip install skill-seekers[mcp]` - Full MCP support
  - **All Features**: `pip install skill-seekers[all]` - Everything enabled
  - **Lazy Loading**: Graceful failure with helpful error messages when MCP not installed
  - **Interactive Setup Wizard**:
    - Shows all installation options on first run
    - Stored at `~/.config/skill-seekers/.setup_shown`
    - Accessible via `skill-seekers-setup` command
  - **Entry Point**: `skill-seekers-setup` for manual access

- **🧪 E2E Testing for Bootstrap** - Comprehensive end-to-end tests
  - **6 core tests** verifying bootstrap workflow:
    - Output structure creation
    - Header prepending
    - YAML frontmatter validation
    - Line count sanity checks
    - Virtual environment installability
    - Platform adaptor compatibility
  - **Pytest markers**: @pytest.mark.e2e, @pytest.mark.venv, @pytest.mark.slow
  - **Execution modes**:
    - Fast tests: `pytest -k "not venv"` (~2-3 min)
    - Full suite: `pytest -m "e2e"` (~5-10 min)
  - **Test utilities**: Fixtures for project root, bootstrap runner, output directory

- **📚 Comprehensive Documentation Overhaul** - Complete v2.7.0 documentation update
  - **7 new documentation files** (~3,750 lines total):
    - `docs/reference/API_REFERENCE.md` (750 lines) - Programmatic usage guide for Python developers
    - `docs/features/BOOTSTRAP_SKILL.md` (450 lines) - Self-hosting capability documentation
    - `docs/reference/CODE_QUALITY.md` (550 lines) - Code quality standards and ruff linting guide
    - `docs/guides/TESTING_GUIDE.md` (750 lines) - Complete testing reference (1200+ test suite)
    - `docs/QUICK_REFERENCE.md` (300 lines) - One-page cheat sheet for quick command lookup
    - `docs/guides/MIGRATION_GUIDE.md` (400 lines) - Version upgrade guides (v1.0.0 → v2.7.0)
    - `docs/FAQ.md` (550 lines) - Comprehensive Q&A for common user questions
  - **10 existing files updated**:
    - `README.md` - Updated test count badge (700+ → 1200+ tests), v2.7.0 callout
    - `ROADMAP.md` - Added v2.7.0 completion section with task statuses
    - `CONTRIBUTING.md` - Added link to CODE_QUALITY.md reference
    - `docs/README.md` - Quick links by use case, recent updates section
    - `docs/guides/MCP_SETUP.md` - Fixed server_fastmcp references (PR #252)
    - `docs/QUICK_REFERENCE.md` - Updated MCP server reference (server.py → server_fastmcp.py)
    - `CLAUDE_INTEGRATION.md` - Updated version references
    - 3 other documentation files with v2.7.0 updates
  - **Version consistency**: All version references standardized to v2.7.0
  - **Test counts**: Standardized to 1200+ tests (was inconsistent 700+ in some docs)
  - **MCP tool counts**: Updated to 18 tools (from 17)

- **📦 Git Submodules for Configuration Management** - Improved config organization and API deployment
  - **Configs as git submodule** at `api/configs_repo/` for cleaner repository
  - **Production configs**: Added official production-ready configuration presets
  - **Duplicate removal**: Cleaned up all duplicate configs from main repository
  - **Test filtering**: Filtered out test-example configs from API endpoints
  - **CI/CD integration**: GitHub Actions now initializes submodules automatically
  - **API deployment**: Updated render.yaml to use git submodule for configs_repo
  - **Benefits**: Cleaner main repo, better config versioning, production/test separation

- **🔍 Config Discovery Enhancements** - Improved config listing
  - **--all flag** for estimate command: `skill-seekers estimate --all`
  - Lists all available preset configurations with descriptions
  - Helps users discover supported frameworks before scraping
  - Shows config names, frameworks, and documentation URLs

### Changed

- **GitHub Fetcher** - Integrated rate limit handler
  - Modified `github_fetcher.py` to use `RateLimitHandler`
  - Added upfront rate limit check before starting
  - Check responses for rate limits on all API calls
  - Automatic profile detection from config
  - Raises `RateLimitError` when rate limit cannot be handled
  - Constructor now accepts `interactive` and `profile_name` parameters

- **GitHub Scraper** - Added rate limit support
  - New `--non-interactive` flag for CI/CD mode
  - New `--profile` flag to select GitHub profile
  - Config now supports `interactive` and `github_profile` keys
  - CLI argument passing for non-interactive and profile options

- **Main CLI** - Enhanced with new commands
  - Added `config` subcommand with options (--github, --api-keys, --show, --test)
  - Added `resume` subcommand with options (--list, --clean)
  - Updated GitHub subcommand with --non-interactive and --profile flags
  - Updated command documentation strings
  - Version bumped to 2.7.0

- **pyproject.toml** - New entry points and dependency restructuring
  - Added `skill-seekers-config` entry point
  - Added `skill-seekers-resume` entry point
  - Added `skill-seekers-setup` entry point for setup wizard
  - **MCP moved to optional dependencies** - Now requires `pip install skill-seekers[mcp]`
  - Updated pytest markers: e2e, venv, bootstrap, slow
  - Version updated to 2.7.0

- **install_skill.py** - Lazy MCP loading
  - Try/except ImportError for MCP imports
  - Graceful failure with helpful error message when MCP not installed
  - Suggests alternatives: scrape + package workflow
  - Maintains backward compatibility for existing MCP users

### Fixed

- **Code Quality Improvements** - Fixed all 21 ruff linting errors across codebase
  - SIM102: Combined nested if statements using `and` operator (7 fixes)
  - SIM117: Combined multiple `with` statements into single multi-context `with` (9 fixes)
  - B904: Added `from e` to exception chaining for proper error context (1 fix)
  - SIM113: Removed unused enumerate counter variable (1 fix)
  - B007: Changed unused loop variable to `_` (1 fix)
  - ARG002: Removed unused method argument in test fixture (1 fix)
  - Files affected: config_extractor.py, config_validator.py, doc_scraper.py, pattern_recognizer.py (3), test_example_extractor.py (3), unified_skill_builder.py, pdf_scraper.py, and 6 test files
  - Result: Zero linting errors, cleaner code, better maintainability

- **Version Synchronization** - Fixed version mismatch across package (Issue #248)
  - All `__init__.py` files now correctly show version 2.7.0 (was 2.5.2 in 4 files)
  - Files updated: `src/skill_seekers/__init__.py`, `src/skill_seekers/cli/__init__.py`, `src/skill_seekers/mcp/__init__.py`, `src/skill_seekers/mcp/tools/__init__.py`
  - Ensures `skill-seekers --version` shows accurate version number
  - **Critical**: Prevents bug where PyPI shows wrong version (Issue #248)

- **Case-Insensitive Regex in Install Workflow** - Fixed install workflow failures (Issue #236)
  - Made regex patterns case-insensitive using `(?i)` flag
  - Patterns now match both "Saved to:" and "saved to:" (and any case variation)
  - Files: `src/skill_seekers/mcp/tools/packaging_tools.py` (lines 529, 668)
  - Impact: install_skill workflow now works reliably regardless of output formatting

- **Test Fixture Error** - Fixed pytest fixture error in bootstrap skill tests
  - Removed unused `tmp_path` parameter causing fixture lookup errors
  - File: `tests/test_bootstrap_skill.py:54`
  - Result: All CI test runs now pass without fixture errors

- **MCP Setup Modernization** - Updated MCP server configuration (PR #252, @MiaoDX)
  - Fixed 41 instances of `server_fastmcp_fastmcp` → `server_fastmcp` typo in docs/guides/MCP_SETUP.md
  - Updated all 12 files to use `skill_seekers.mcp.server_fastmcp` module
  - Enhanced setup_mcp.sh with automatic venv detection (.venv, venv, $VIRTUAL_ENV)
  - Updated tests to accept `-e ".[mcp]"` format and module references
  - Files: .claude/mcp_config.example.json, CLAUDE.md, README.md, docs/guides/*.md, setup_mcp.sh, tests/test_setup_scripts.py
  - Benefits: Eliminates "module not found" errors, clean dependency isolation, prepares for v3.0.0

- **Rate limit indefinite wait** - No more infinite waiting
  - Configurable timeout per profile (default: 30 minutes)
  - Clear error messages when timeout exceeded
  - Graceful exit with helpful next steps
  - Resume capability for interrupted jobs

- **Token setup confusion** - Clear, guided setup process
  - Interactive wizard with browser integration
  - Token validation with helpful error messages
  - Clear documentation of required scopes
  - Test connection feature to verify tokens work

- **CI/CD failures** - Non-interactive mode support
  - `--non-interactive` flag fails fast instead of hanging
  - No user prompts in non-interactive mode
  - Clear error messages for automation logs
  - Exit codes for pipeline integration

- **AttributeError in codebase_scraper.py** - Fixed incorrect flag check (PR #249)
  - Changed `if args.build_api_reference:` to `if not args.skip_api_reference:`
  - Aligns with v2.5.2 opt-out flag strategy (--skip-* instead of --build-*)
  - Fixed at line 1193 in codebase_scraper.py

### Technical Details

- **Architecture**: Strategy pattern for rate limit handling, singleton for config manager
- **Files Modified**: 6 (github_fetcher.py, github_scraper.py, main.py, pyproject.toml, install_skill.py, codebase_scraper.py)
- **New Files**: 6 (config_manager.py ~490 lines, config_command.py ~400 lines, rate_limit_handler.py ~450 lines, resume_command.py ~150 lines, setup_wizard.py ~95 lines, test_bootstrap_skill_e2e.py ~169 lines)
- **Bootstrap Scripts**: 2 (bootstrap_skill.sh enhanced, skill_header.md)
- **Tests**: 22 tests added, all passing (16 rate limit + 6 E2E bootstrap)
- **Dependencies**: MCP moved to optional, no new required dependencies
- **Backward Compatibility**: Fully backward compatible, MCP optionality via pip extras
- **Credits**: Bootstrap feature contributed by @MiaoDX (PR #249)

### Migration Guide

**Existing users** - No migration needed! Everything works as before.

**MCP users** - If you use MCP integration features:
```bash
# Reinstall with MCP support
pip install -U skill-seekers[mcp]

# Or install everything
pip install -U skill-seekers[all]
```

**New installation profiles**:
```bash
# CLI only (no MCP)
pip install skill-seekers

# With MCP integration
pip install skill-seekers[mcp]

# With multi-LLM support (Gemini, OpenAI)
pip install skill-seekers[all-llms]

# Everything
pip install skill-seekers[all]

# See all options
skill-seekers-setup
```

**To use new features**:
```bash
# Set up GitHub token (one-time)
skill-seekers config --github

# Add multiple profiles
skill-seekers config
# → Select "1. GitHub Token Setup"
# → Select "1. Add New Profile"

# Use specific profile
skill-seekers github --repo owner/repo --profile work

# CI/CD mode
skill-seekers github --repo owner/repo --non-interactive

# View configuration
skill-seekers config --show

# Bootstrap skill-seekers as a Claude Code skill
./scripts/bootstrap_skill.sh
cp -r output/skill-seekers ~/.claude/skills/
```

### Breaking Changes

None - this release is fully backward compatible.

---




## v2.6.0: v2.6.0 - Codebase Analysis Enhancements & Documentation Reorganization

**Published**: 2026-01-13

## 🚀 Complete C3.x Codebase Analysis Suite + Documentation Reorganization

This is a **major feature release** that delivers the complete C3.x codebase analysis suite (C3.1-C3.8), transforming Skill Seekers into a comprehensive code documentation and analysis tool. Also includes comprehensive documentation reorganization and quality-of-life improvements.

---

## 🎯 Complete C3.x Codebase Analysis Suite

### C3.1 Design Pattern Detection
- **10 Design Patterns**: Singleton, Factory, Observer, Strategy, Decorator, Builder, Adapter, Command, Template Method, Chain of Responsibility
- **9 Languages**: Python, JavaScript, TypeScript, C++, C, C#, Go, Rust, Java (plus Ruby, PHP)
- **3 Detection Levels**: Surface (fast), deep (balanced), full (thorough)
- **CLI**: `skill-seekers-patterns --file src/db.py`
- **87% precision, 80% recall** (tested on 100 real-world projects)

### C3.2 Test Example Extraction
- **Extracts real usage examples** from test files
- **5 Categories**: instantiation, method_call, config, setup, workflow
- **9 Languages**: Python (AST-based), JavaScript, TypeScript, Go, Rust, Java, C#, PHP, Ruby
- **Quality filtering** with confidence scoring
- **CLI**: `skill-seekers extract-test-examples tests/ --language python`

### C3.3 How-To Guide Generation with AI Enhancement ⭐
- **Transforms test workflows** into step-by-step educational guides
- **🆕 COMPREHENSIVE AI ENHANCEMENT** - 5 automatic improvements:
  1. Step Descriptions - Natural language explanations
  2. Troubleshooting Solutions - Diagnostic flows + solutions
  3. Prerequisites Explanations - Why needed + setup instructions
  4. Next Steps Suggestions - Related guides, learning paths
  5. Use Case Examples - Real-world scenarios
- **3 AI Modes**:
  - **API Mode**: Claude API (requires ANTHROPIC_API_KEY)
  - **LOCAL Mode**: Claude Code CLI (FREE, no API key needed!)
  - **AUTO Mode**: Automatic detection (default)
- **Quality Transformation**: 75-line templates → 500+ line professional tutorials
- **CLI**: `skill-seekers-how-to-guides test_examples.json --ai-mode auto`

### C3.4 Configuration Pattern Extraction with AI Enhancement
- **9 Config Formats**: JSON, YAML, TOML, ENV, INI, Python, JS/TS, Dockerfile, Docker Compose
- **7 Common Patterns**: Database, API, Logging, Cache, Email, Auth, Server configs
- **🆕 AI ENHANCEMENT** (optional):
  1. Explanations - What each setting does
  2. Best Practices - Suggested improvements
  3. Security Analysis - Identifies hardcoded secrets
  4. Migration Suggestions - Consolidation opportunities
  5. Context - Pattern explanations
- **CLI**: `skill-seekers-config-extractor --directory . --enhance-local`

### C3.5 Architectural Overview & Skill Integrator
- **ARCHITECTURE.md Generation** - Comprehensive architectural overview with 8 sections:
  1. Overview, 2. Architectural Patterns, 3. Technology Stack, 4. Design Patterns
  5. Configuration Overview, 6. Common Workflows, 7. Usage Examples, 8. Entry Points
- **Default ON** - Runs automatically when GitHub sources have `local_repo_path`
- **Organized outputs** in `references/codebase_analysis/`
- **Enhanced SKILL.md** with Architecture & Code Analysis summary

### C3.6 AI Enhancement
- **AI-powered insights** for patterns and test examples
- **Pattern Enhancement**: Explains why patterns detected, suggests improvements
- **Test Example Enhancement**: Adds context, groups into tutorials, identifies best practices
- **Batch processing** (5 items per call) for efficiency

### C3.7 Architectural Pattern Detection
- **Detects high-level patterns**: MVC, MVVM, MVP, Repository, Service Layer, Layered, Clean Architecture
- **Framework detection**: Django, Flask, Spring, ASP.NET, Rails, Laravel, Angular, React, Vue.js
- **Evidence-based** with confidence scoring
- **AI-enhanced** architectural recommendations

### C3.8 Standalone Codebase Scraper SKILL.md Generation
- **Generates comprehensive SKILL.md** (300+ lines) with all C3.x analysis integrated
- **Sections**: Description, When to Use, Quick Reference, Design Patterns, Architecture, Configuration
- **Perfect for**: Private codebases, offline analysis, local project documentation
- **CLI**: `skill-seekers-codebase-scraper --directory /path/to/code`

---

## ✨ Enhanced LOCAL Enhancement Modes

**4 Execution Modes** for different use cases:
- **Headless** (default): Foreground, waits for completion (perfect for CI/CD)
- **Background** (`--background`): Background thread, returns immediately
- **Daemon** (`--daemon`): Fully detached with `nohup`, survives parent exit
- **Terminal** (`--interactive-enhancement`): Opens new terminal window (macOS)

**Force Mode (Default ON)**: Skip all confirmations - perfect for CI/CD automation!

**Status Monitoring**: New `enhance-status` command for background/daemon processes
- `skill-seekers enhance-status output/react/` - Check status
- `skill-seekers enhance-status output/react/ --watch` - Real-time watch
- `skill-seekers enhance-status output/react/ --json` - JSON output

---

## 📚 Comprehensive Documentation Reorganization

**Complete overhaul** of documentation structure:
- **Removed 7** temporary/analysis files from root
- **Archived 14** historical documents to `docs/archive/`
- **Organized 29** files into clear subdirectories:
  - `docs/features/` (10 files) - Core features, AI enhancement, PDF tools
  - `docs/integrations/` (3 files) - Multi-LLM platform support
  - `docs/guides/` (6 files) - Setup, MCP, usage guides
  - `docs/reference/` (8 files) - Architecture, standards, technical reference
- **Created `docs/README.md`** - Navigation index with "I want to..." user-focused navigation

**Result**: 3x faster documentation discovery, scalable structure

---

## 🔧 Global Setup Script with FastMCP

- **New `setup.sh`** for global PyPI installation
- Sets up MCP server configuration for Claude Code Desktop
- Perfect for end users (no development setup needed)
- Separate from `setup_mcp.sh` (development setup)

---

## 💥 BREAKING CHANGES

### Analysis Features Now Default ON
- **All analysis features** now **enabled by default** for better UX
- **Old flags (DEPRECATED)**: `--build-api-reference`, `--build-dependency-graph`, `--detect-patterns`, `--extract-test-examples`
- **New flags**: `--skip-api-reference`, `--skip-dependency-graph`, `--skip-patterns`, `--skip-test-examples`
- **Migration**: Remove old `--build-*` flags (features are now ON by default)
- **Impact**: `codebase-scraper --directory .` now runs all analysis features automatically

---

## 🐛 Bug Fixes

- Fixed codebase scraper language stats dict format handling
- Fixed install-agent directory traversal edge case

---

## 📊 Release Statistics

- **160 files changed**
- **44,965 additions**
- **4,704 deletions**
- **56 new test files** for C3.x features
- **700+ tests passing** (100% test coverage for all C3.x features)

---

## 📦 Installation

```bash
pip install --upgrade skill-seekers
```

---

## 🔗 Links

- **PyPI Package**: https://pypi.org/project/skill-seekers/2.6.0/
- **Documentation**: https://github.com/yusufkaraaslan/Skill_Seekers#readme
- **Full Changelog**: https://github.com/yusufkaraaslan/Skill_Seekers/blob/main/CHANGELOG.md#260---2026-01-13
- **Feature Docs**:
  - [Pattern Detection](https://github.com/yusufkaraaslan/Skill_Seekers/blob/main/docs/features/PATTERN_DETECTION.md)
  - [Test Example Extraction](https://github.com/yusufkaraaslan/Skill_Seekers/blob/main/docs/features/TEST_EXAMPLE_EXTRACTION.md)
  - [How-To Guides](https://github.com/yusufkaraaslan/Skill_Seekers/blob/main/docs/features/HOW_TO_GUIDES.md)
  - [Enhancement Modes](https://github.com/yusufkaraaslan/Skill_Seekers/blob/main/docs/features/ENHANCEMENT_MODES.md)

---

## 🎉 What This Means for Users

This release transforms Skill Seekers from a documentation scraper into a **complete codebase analysis and documentation tool**. You can now:

1. **Analyze any codebase** and generate comprehensive documentation automatically
2. **Extract design patterns** from your code (87% precision)
3. **Generate how-to guides** from your tests (with AI enhancement!)
4. **Detect architectural patterns** (MVC, MVVM, Clean Architecture, etc.)
5. **Extract configuration patterns** with security analysis
6. **Get AI-powered insights** for all analysis (using Claude Code - FREE!)
7. **Run everything by default** - no flags needed for full analysis

**Perfect for**: Code reviews, onboarding, documentation generation, architectural analysis, security audits

---

**This is the most significant release in Skill Seekers history!** 🚀

## v2.5.1: v2.5.1

**Published**: 2025-12-30

## [2.5.1] - 2025-12-30

### 🐛 Critical Bug Fix - PyPI Package Broken

This **patch release** fixes a critical packaging bug that made v2.5.0 completely unusable for PyPI users.

### Fixed

- **CRITICAL**: Added missing `skill_seekers.cli.adaptors` module to packages list in pyproject.toml ([#221](https://github.com/yusufkaraaslan/Skill_Seekers/pull/221))
  - **Issue**: v2.5.0 on PyPI throws `ModuleNotFoundError: No module named 'skill_seekers.cli.adaptors'`
  - **Impact**: Broke 100% of multi-platform features (Claude, Gemini, OpenAI, Markdown)
  - **Cause**: The adaptors module was missing from the explicit packages list
  - **Fix**: Added `skill_seekers.cli.adaptors` to packages in pyproject.toml
  - **Credit**: Thanks to [@MiaoDX](https://github.com/MiaoDX) for finding and fixing this issue!

### Package Structure

The `skill_seekers.cli.adaptors` module contains the platform adaptor architecture:
- `base.py` - Abstract base class for all adaptors
- `claude.py` - Claude AI platform implementation
- `gemini.py` - Google Gemini platform implementation
- `openai.py` - OpenAI ChatGPT platform implementation
- `markdown.py` - Generic markdown export

**Note**: v2.5.0 is broken on PyPI. All users should upgrade to v2.5.1 immediately.

---



## v2.5.0: v2.5.0 - Multi-Platform Feature Parity

**Published**: 2025-12-28

# 🚀 Multi-Platform Feature Parity - 4 LLM Platforms Supported

This **major feature release** adds complete multi-platform support for **Claude AI**, **Google Gemini**, **OpenAI ChatGPT**, and **Generic Markdown** export. All features now work across all platforms with full feature parity.

## 🎯 Highlights

### Multi-LLM Platform Support
- ✅ **4 platforms supported**: Claude AI, Google Gemini, OpenAI ChatGPT, Generic Markdown
- ✅ **Complete feature parity**: All skill modes work with all platforms
- ✅ **Platform adaptors**: Clean architecture with platform-specific implementations
- ✅ **Unified workflow**: Same scraping output works for all platforms
- ✅ **Smart enhancement**: Platform-specific AI models (Claude Sonnet 4, Gemini 2.0 Flash, GPT-4o)

### Platform-Specific Capabilities

| Platform | Format | Upload | Enhancement | Unique Features |
|----------|--------|--------|-------------|----------------|
| **Claude AI** | ZIP + YAML | Skills API | Sonnet 4 | MCP integration |
| **Google Gemini** | tar.gz | Files API | Gemini 2.0 | 1M token context |
| **OpenAI ChatGPT** | ZIP + Vector | Assistants API | GPT-4o | Semantic search |
| **Generic Markdown** | ZIP | Manual | - | Universal compatibility |

### Complete Feature Parity

**All skill modes work with all platforms:**
- 📄 Documentation scraping → All 4 platforms
- 🐙 GitHub repository analysis → All 4 platforms
- 📕 PDF extraction → All 4 platforms
- 🔀 Unified multi-source → All 4 platforms
- 💻 Local repository analysis → All 4 platforms

### 18 MCP Tools with Multi-Platform Support
- `package_skill` - Now accepts `target` parameter (claude, gemini, openai, markdown)
- `upload_skill` - Now accepts `target` parameter (claude, gemini, openai)
- `enhance_skill` - **NEW** standalone tool with `target` parameter
- `install_skill` - Full multi-platform workflow automation

## 📦 Installation

```bash
# Core package (Claude support)
pip install skill-seekers==2.5.0

# With Gemini support
pip install skill-seekers[gemini]==2.5.0

# With OpenAI support
pip install skill-seekers[openai]==2.5.0

# With all platforms
pip install skill-seekers[all-llms]==2.5.0
```

## 🚀 Quick Start - Multi-Platform

```bash
# Scrape documentation (platform-agnostic)
skill-seekers scrape --config configs/react.json

# Package for different platforms
skill-seekers package output/react/ --target claude     # ZIP
skill-seekers package output/react/ --target gemini     # tar.gz
skill-seekers package output/react/ --target openai     # ZIP with vector
skill-seekers package output/react/ --target markdown   # ZIP universal

# Upload to platforms (requires API keys)
export ANTHROPIC_API_KEY=sk-ant-...
export GOOGLE_API_KEY=AIzaSy...
export OPENAI_API_KEY=sk-proj-...

skill-seekers upload output/react.zip --target claude
skill-seekers upload output/react-gemini.tar.gz --target gemini
skill-seekers upload output/react-openai.zip --target openai
```

## 📚 Documentation

- 📊 [Complete Feature Matrix](https://github.com/yusufkaraaslan/Skill_Seekers/blob/main/docs/FEATURE_MATRIX.md)
- 📤 [Multi-Platform Upload Guide](https://github.com/yusufkaraaslan/Skill_Seekers/blob/main/docs/UPLOAD_GUIDE.md)
- ✨ [Enhancement Guide](https://github.com/yusufkaraaslan/Skill_Seekers/blob/main/docs/ENHANCEMENT.md)
- 🔧 [MCP Setup](https://github.com/yusufkaraaslan/Skill_Seekers/blob/main/docs/MCP_SETUP.md)

## 📈 Stats

- **16 commits** since v2.4.0
- **700 tests** passing (up from 427, +273 new tests)
- **4 platforms** supported (was 1)
- **18 MCP tools** (up from 17)
- **5 documentation guides** updated/created
- **29 files changed**, 6,349 insertions(+), 253 deletions(-)

## 🎉 What's New

See [CHANGELOG.md](https://github.com/yusufkaraaslan/Skill_Seekers/blob/main/CHANGELOG.md) for complete details.

## 🙏 Contributors

- @yusufkaraaslan - Multi-platform architecture, all platform adaptors, comprehensive testing

---

**Full Changelog**: https://github.com/yusufkaraaslan/Skill_Seekers/compare/v2.4.0...v2.5.0

## v2.4.0: v2.4.0

**Published**: 2025-12-25

## [2.4.0] - 2025-12-25

### 🚀 MCP 2025 Upgrade - Multi-Agent Support & HTTP Transport

This **major release** upgrades the MCP infrastructure to the 2025 specification with support for 5 AI coding agents, dual transport modes (stdio + HTTP), and a complete FastMCP refactor.

### 🎯 Major Features

#### MCP SDK v1.25.0 Upgrade
- **Upgraded from v1.18.0 to v1.25.0** - Latest MCP protocol specification (November 2025)
- **FastMCP framework** - Decorator-based tool registration, 68% code reduction (2200 → 708 lines)
- **Enhanced reliability** - Better error handling, automatic schema generation from type hints
- **Backward compatible** - Existing v2.3.0 configurations continue to work

#### Dual Transport Support
- **stdio transport** (default) - Standard input/output for Claude Code, VS Code + Cline
- **HTTP transport** (new) - Server-Sent Events for Cursor, Windsurf, IntelliJ IDEA
- **Health check endpoint** - `GET /health` for monitoring
- **SSE endpoint** - `GET /sse` for real-time communication
- **Configurable server** - `--http`, `--port`, `--host`, `--log-level` flags
- **uvicorn-powered** - Production-ready ASGI server

#### Multi-Agent Auto-Configuration
- **5 AI agents supported**:
  - Claude Code (stdio)
  - Cursor (HTTP)
  - Windsurf (HTTP)
  - VS Code + Cline (stdio)
  - IntelliJ IDEA (HTTP)
- **Automatic detection** - `agent_detector.py` scans for installed agents
- **One-command setup** - `./setup_mcp.sh` configures all detected agents
- **Smart config merging** - Preserves existing MCP servers, only adds skill-seeker
- **Automatic backups** - Timestamped backups before modifications
- **HTTP server management** - Auto-starts HTTP server for HTTP-based agents

#### Expanded Tool Suite (17 Tools)
- **Config Tools (3)**: generate_config, list_configs, validate_config
- **Scraping Tools (4)**: estimate_pages, scrape_docs, scrape_github, scrape_pdf
- **Packaging Tools (3)**: package_skill, upload_skill, install_skill
- **Splitting Tools (2)**: split_config, generate_router
- **Source Tools (5)**: fetch_config, submit_config, add_config_source, list_config_sources, remove_config_source

### Added

#### Core Infrastructure
- **`server_fastmcp.py`** (708 lines) - New FastMCP-based MCP server
  - Decorator-based tool registration (`@safe_tool_decorator`)
  - Modular tool architecture (5 tool modules)
  - HTTP transport with uvicorn
  - stdio transport (default)
  - Comprehensive error handling

- **`agent_detector.py`** (333 lines) - Multi-agent detection and configuration
  - Detects 5 AI coding agents across platforms (Linux, macOS, Windows)
  - Generates agent-specific config formats (JSON, XML)
  - Auto-selects transport type (stdio vs HTTP)
  - Cross-platform path resolution

- **Tool modules** (5 modules, 1,676 total lines):
  - `tools/config_tools.py` (249 lines) - Configuration management
  - `tools/scraping_tools.py` (423 lines) - Documentation scraping
  - `tools/packaging_tools.py` (514 lines) - Skill packaging and upload
  - `tools/splitting_tools.py` (195 lines) - Config splitting and routing
  - `tools/source_tools.py` (295 lines) - Config source management

#### Setup & Configuration
- **`setup_mcp.sh`** (rewritten, 661 lines) - Multi-agent auto-configuration
  - Detects installed agents automatically
  - Offers configure all or select individual agents
  - Manages HTTP server startup
  - Smart config merging with existing configurations
  - Comprehensive validation and testing

- **HTTP server** - Production-ready HTTP transport
  - Health endpoint: `/health`
  - SSE endpoint: `/sse`
  - Messages endpoint: `/messages/`
  - CORS middleware for cross-origin requests
  - Configurable host and port
  - Debug logging support

#### Documentation
- **`docs/MCP_SETUP.md`** (completely rewritten) - Comprehensive MCP 2025 guide
  - Migration guide from v2.3.0
  - Transport modes explained (stdio vs HTTP)
  - Agent-specific configuration for all 5 agents
  - Troubleshooting for both transports
  - Advanced configuration (systemd, launchd services)

- **`docs/HTTP_TRANSPORT.md`** (434 lines, new) - HTTP transport guide
- **`docs/MULTI_AGENT_SETUP.md`** (643 lines, new) - Multi-agent setup guide
- **`docs/SETUP_QUICK_REFERENCE.md`** (387 lines, new) - Quick reference card
- **`SUMMARY_HTTP_TRANSPORT.md`** (360 lines, new) - Technical implementation details
- **`SUMMARY_MULTI_AGENT_SETUP.md`** (556 lines, new) - Multi-agent technical summary

#### Testing
- **`test_mcp_fastmcp.py`** (960 lines, 63 tests) - Comprehensive FastMCP server tests
  - All 17 tools tested
  - Error handling validation
  - Type validation
  - Integration workflows

- **`test_server_fastmcp_http.py`** (165 lines, 6 tests) - HTTP transport tests
  - Health check endpoint
  - SSE endpoint
  - CORS middleware
  - Argument parsing

- **All tests passing**: 602/609 tests (99.1% pass rate)

### Changed

#### MCP Server Architecture
- **Refactored to FastMCP** - Decorator-based, modular, maintainable
- **Code reduction** - 68% smaller (2200 → 708 lines)
- **Modular tools** - Separated into 5 category modules
- **Type safety** - Full type hints on all tool functions
- **Improved error handling** - Graceful degradation, clear error messages

#### Server Compatibility
- **`server.py`** - Now a compatibility shim (delegates to `server_fastmcp.py`)
- **Deprecation warning** - Alerts users to migrate to `server_fastmcp`
- **Backward compatible** - Existing configurations continue to work
- **Migration path** - Clear upgrade instructions in docs

#### Setup Experience
- **Multi-agent workflow** - One script configures all agents
- **Interactive prompts** - User-friendly with sensible defaults
- **Validation** - Config file validation before writing
- **Backup safety** - Automatic timestamped backups
- **Color-coded output** - Visual feedback (success/warning/error)

#### Documentation
- **README.md** - Added comprehensive multi-agent section
- **MCP_SETUP.md** - Completely rewritten for v2.4.0
- **CLAUDE.md** - Updated with new server details
- **Version badges** - Updated to v2.4.0

### Fixed
- Import issues in test files (updated to use new tool modules)
- CLI version test (updated to expect v2.3.0)
- Graceful MCP import handling (no sys.exit on import)
- Server compatibility for testing environments

### Deprecated
- **`server.py`** - Use `server_fastmcp.py` instead
  - Compatibility shim provided
  - Will be removed in v3.0.0 (6+ months)
  - Migration guide available

### Infrastructure
- **Python 3.10+** - Recommended for best compatibility
- **MCP SDK**: v1.25.0 (pinned to v1.x)
- **uvicorn**: v0.40.0+ (for HTTP transport)
- **starlette**: v0.50.0+ (for HTTP transport)

### Migration from v2.3.0

**Upgrade Steps:**
1. Update dependencies: `pip install -e ".[mcp]"`
2. Update MCP config to use `server_fastmcp`:
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
3. For HTTP agents, start HTTP server: `python -m skill_seekers.mcp.server_fastmcp --http`
4. Or use auto-configuration: `./setup_mcp.sh`

**Breaking Changes:** None - fully backward compatible

**New Capabilities:**
- Multi-agent support (5 agents)
- HTTP transport for web-based agents
- 8 new MCP tools
- Automatic agent detection and configuration

### Contributors
- Implementation: Claude Sonnet 4.5
- Testing & Review: @yusufkaraaslan

---



## v2.2.0: v2.2.0

**Published**: 2025-12-21

## [2.2.0] - 2025-12-21

### 🚀 Private Config Repositories - Team Collaboration Unlocked

This major release adds **git-based config sources**, enabling teams to fetch configs from private/team repositories in addition to the public API. This unlocks team collaboration, enterprise deployment, and custom config collections.

### 🎯 Major Features

#### Git-Based Config Sources (Issue [#211](https://github.com/yusufkaraaslan/Skill_Seekers/issues/211))
- **Multi-source config management** - Fetch from API, git URL, or named sources
- **Private repository support** - GitHub, GitLab, Bitbucket, Gitea, and custom git servers
- **Team collaboration** - Share configs across 3-5 person teams with version control
- **Enterprise scale** - Support 500+ developers with priority-based resolution
- **Secure authentication** - Environment variable tokens only (GITHUB_TOKEN, GITLAB_TOKEN, etc.)
- **Intelligent caching** - Shallow clone (10-50x faster), auto-pull updates
- **Offline mode** - Works with cached repos when offline
- **Backward compatible** - Existing API-based configs work unchanged

#### New MCP Tools
- **`add_config_source`** - Register git repositories as config sources
  - Auto-detects source type (GitHub, GitLab, etc.)
  - Auto-selects token environment variable
  - Priority-based resolution for multiple sources
  - SSH URL support (auto-converts to HTTPS + token)

- **`list_config_sources`** - View all registered sources
  - Shows git URL, branch, priority, token env
  - Filter by enabled/disabled status
  - Sorted by priority (lower = higher priority)

- **`remove_config_source`** - Unregister sources
  - Removes from registry (cache preserved for offline use)
  - Helpful error messages with available sources

- **Enhanced `fetch_config`** - Three modes
  1. **Named source mode** - `fetch_config(source="team", config_name="react-custom")`
  2. **Git URL mode** - `fetch_config(git_url="https://...", config_name="react-custom")`
  3. **API mode** - `fetch_config(config_name="react")` (unchanged)

### Added

#### Core Infrastructure
- **GitConfigRepo class** (`src/skill_seekers/mcp/git_repo.py`, 283 lines)
  - `clone_or_pull()` - Shallow clone with auto-pull and force refresh
  - `find_configs()` - Recursive *.json discovery (excludes .git)
  - `get_config()` - Load config with case-insensitive matching
  - `inject_token()` - Convert SSH to HTTPS with token authentication
  - `validate_git_url()` - Support HTTPS, SSH, and file:// URLs
  - Comprehensive error handling (auth failures, missing repos, corrupted caches)

- **SourceManager class** (`src/skill_seekers/mcp/source_manager.py`, 260 lines)
  - `add_source()` - Register/update sources with validation
  - `get_source()` - Retrieve by name with helpful errors
  - `list_sources()` - List all/enabled sources sorted by priority
  - `remove_source()` - Unregister sources
  - `update_source()` - Modify specific fields
  - Atomic file I/O (write to temp, then rename)
  - Auto-detect token env vars from source type

#### Storage & Caching
- **Registry file**: `~/.skill-seekers/sources.json`
  - Stores source metadata (URL, branch, priority, timestamps)
  - Version-controlled schema (v1.0)
  - Atomic writes prevent corruption

- **Cache directory**: `$SKILL_SEEKERS_CACHE_DIR` (default: `~/.skill-seekers/cache/`)
  - One subdirectory per source
  - Shallow git clones (depth=1, single-branch)
  - Configurable via environment variable

#### Documentation
- **docs/GIT_CONFIG_SOURCES.md** (800+ lines) - Comprehensive guide
  - Quick start, architecture, authentication
  - MCP tools reference with examples
  - Use cases (small teams, enterprise, open source)
  - Best practices, troubleshooting, advanced topics
  - Complete API reference

- **configs/example-team/** - Example repository for testing
  - `react-custom.json` - Custom React config with metadata
  - `vue-internal.json` - Internal Vue config
  - `company-api.json` - Company API config example
  - `README.md` - Usage guide and best practices
  - `test_e2e.py` - End-to-end test script (7 steps, 100% passing)

- **README.md** - Updated with git source examples
  - New "Private Config Repositories" section in Key Features
  - Comprehensive usage examples (quick start, team collaboration, enterprise)
  - Supported platforms and authentication
  - Example workflows for different team sizes

### Dependencies
- **GitPython>=3.1.40** - Git operations (clone, pull, branch switching)
  - Replaces subprocess calls with high-level API
  - Better error handling and cross-platform support

### Testing
- **83 new tests** (100% passing)
  - `tests/test_git_repo.py` (35 tests) - GitConfigRepo functionality
    - Initialization, URL validation, token injection
    - Clone/pull operations, config discovery, error handling
  - `tests/test_source_manager.py` (48 tests) - SourceManager functionality
    - Add/get/list/remove/update sources
    - Registry persistence, atomic writes, default token env
  - `tests/test_mcp_git_sources.py` (18 tests) - MCP integration
    - All 3 fetch modes (API, Git URL, Named Source)
    - Source management tools (add/list/remove)
    - Complete workflow (add → fetch → remove)
    - Error scenarios (auth failures, missing configs)

### Improved
- **MCP server** - Now supports 12 tools (up from 9)
  - Maintains backward compatibility
  - Enhanced error messages with available sources
  - Priority-based config resolution

### Use Cases

**Small Teams (3-5 people):**
```bash
# One-time setup
add_config_source(name="team", git_url="https://github.com/myteam/configs.git")

# Daily usage
fetch_config(source="team", config_name="react-internal")
```

**Enterprise (500+ developers):**
```bash
# IT pre-configures sources
add_config_source(name="platform", ..., priority=1)
add_config_source(name="mobile", ..., priority=2)

# Developers use transparently
fetch_config(config_name="platform-api")  # Finds in platform source
```

**Example Repository:**
```bash
cd /path/to/Skill_Seekers
python3 configs/example-team/test_e2e.py  # Test E2E workflow
```

### Backward Compatibility
- ✅ All existing configs work unchanged
- ✅ API mode still default (no registration needed)
- ✅ No breaking changes to MCP tools or CLI
- ✅ New parameters are optional (git_url, source, refresh)

### Security
- ✅ Tokens via environment variables only (not in files)
- ✅ Shallow clones minimize attack surface
- ✅ No token storage in registry file
- ✅ Secure token injection (auto-converts SSH to HTTPS)

### Performance
- ✅ Shallow clone: 10-50x faster than full clone
- ✅ Minimal disk space (no git history)
- ✅ Auto-pull: Only fetches changes (not full re-clone)
- ✅ Offline mode: Works with cached repos

### Files Changed
- Modified (2): `pyproject.toml`, `src/skill_seekers/mcp/server.py`
- Added (6): 3 source files + 3 test files + 1 doc + 1 example repo
- Total lines added: ~2,600

### Migration Guide

No migration needed! This is purely additive:

```python
# Before v2.2.0 (still works)
fetch_config(config_name="react")

# New in v2.2.0 (optional)
add_config_source(name="team", git_url="...")
fetch_config(source="team", config_name="react-custom")
```

### Known Limitations
- MCP async tests require pytest-asyncio (added to dev dependencies)
- Example repository uses 'master' branch (git init default)

### See Also
- [GIT_CONFIG_SOURCES.md](docs/GIT_CONFIG_SOURCES.md) - Complete guide
- [configs/example-team/](configs/example-team/) - Example repository
- [Issue #211](https://github.com/yusufkaraaslan/Skill_Seekers/issues/211) - Original feature request

---



## v2.1.1: v2.1.1 - GitHub Repository Analysis Enhancements

**Published**: 2025-11-30

## 🚀 GitHub Repository Analysis Enhancements

This release significantly improves GitHub repository scraping with unlimited local analysis, configurable directory exclusions, and numerous bug fixes.

### ✨ New Features

- **Configurable directory exclusions** for local repository analysis ([#203](https://github.com/yusufkaraaslan/Skill_Seekers/issues/203))
  - `exclude_dirs_additional`: Extend default exclusions with custom directories
  - `exclude_dirs`: Replace default exclusions entirely (advanced users)
  - 19 comprehensive tests covering all scenarios
  - Logging: INFO for extend mode, WARNING for replace mode
- **Unlimited local repository analysis** via `local_repo_path` configuration parameter
- **Auto-exclusion** of virtual environments, build artifacts, and cache directories
- **Support for analyzing repositories without GitHub API rate limits** (50 → unlimited files)
- **Skip llms.txt option** - Force HTML scraping even when llms.txt is detected ([#198](https://github.com/yusufkaraaslan/Skill_Seekers/pull/198))

### 🐛 Bug Fixes

- Fixed logger initialization error causing `AttributeError: 'NoneType' object has no attribute 'setLevel'` ([#190](https://github.com/yusufkaraaslan/Skill_Seekers/issues/190))
- Fixed 3 NoneType subscriptable errors in release tag parsing
- Fixed relative import paths causing `ModuleNotFoundError`
- Fixed hardcoded 50-file analysis limit preventing comprehensive code analysis
- Fixed GitHub API file tree limitation (140 → 345 files discovered)
- Fixed AST parser "not iterable" errors eliminating 100% of parsing failures (95 → 0 errors)
- Fixed virtual environment file pollution reducing file tree noise by 95%
- Fixed `force_rescrape` flag not checked before interactive prompt causing EOFError in CI/CD environments

### 📈 Improvements

- **Code analysis coverage:** 14% → 93.6% (+79.6 percentage points)
- **File discovery:** 140 → 345 files (+146%)
- **Class extraction:** 55 → 585 classes (+964%)
- **Function extraction:** 512 → 2,784 functions (+444%)
- **Test suite:** Expanded to 427 tests (up from 391)

### 📦 Installation

```bash
# Install from PyPI (recommended)
pip install skill-seekers==2.1.1

# Or upgrade existing installation
pip install --upgrade skill-seekers
```

### 📚 Documentation

- [CHANGELOG.md](https://github.com/yusufkaraaslan/Skill_Seekers/blob/main/CHANGELOG.md) - Full changelog
- [README.md](https://github.com/yusufkaraaslan/Skill_Seekers/blob/main/README.md) - Complete documentation
- [CLAUDE.md](https://github.com/yusufkaraaslan/Skill_Seekers/blob/main/CLAUDE.md) - Technical architecture

**Full Changelog:** https://github.com/yusufkaraaslan/Skill_Seekers/compare/v2.1.0...v2.1.1

## v2.1.0: v2.1.0: Quality Assurance + Race Condition Fixes

**Published**: 2025-11-12

## 🎉 Major Enhancement: Quality Assurance + Race Condition Fixes

This release focuses on quality and reliability improvements, adding comprehensive quality checks and fixing critical race conditions in the enhancement workflow.

### 🚀 Key Features

#### Comprehensive Quality Checker
- ✅ Automatic quality validation before packaging
- ✅ Quality scoring system (0-100 score with A-F grades)
- ✅ Enhancement verification (checks for template text, code examples, sections)
- ✅ Structure validation (SKILL.md, references/ directory)
- ✅ Content quality checks (YAML frontmatter, language tags, "When to Use" section)
- ✅ Link validation (validates internal markdown links)
- ✅ Detailed reporting with errors, warnings, and info messages

#### Headless Enhancement Mode (Default)
- ✅ No terminal windows - runs enhancement in background by default
- ✅ Proper waiting - main console waits for enhancement to complete
- ✅ Timeout protection - 10-minute default timeout (configurable)
- ✅ Verification - checks that SKILL.md was actually updated
- ✅ Progress messages - clear status updates during enhancement
- ✅ Interactive mode available - use `--interactive-enhancement` flag

### 📊 Statistics

- **391 tests passing** (up from 379 in v2.0.0)
- **+12 quality checker tests** - comprehensive validation testing
- **0 test failures** - all tests green
- **5 commits** in this release

### 🔄 Breaking Changes

- **Headless mode default** - Enhancement now runs in background by default
  - Use `--interactive-enhancement` if you want the old terminal mode
  - Affects: `skill-seekers-enhance` and `skill-seekers scrape --enhance-local`

### 📦 Installation

```bash
# PyPI (recommended)
pip install skill-seekers==2.1.0

# Or with uv
uv tool install skill-seekers==2.1.0
```

### 🔧 Migration Guide

**If you want the old terminal mode behavior:**
```bash
# Old (v2.0.0): Default was terminal mode
skill-seekers-enhance output/react/

# New (v2.1.0): Use --interactive-enhancement
skill-seekers-enhance output/react/ --interactive-enhancement
```

**If you want to skip quality checks:**
```bash
# Add --skip-quality-check to package command
skill-seekers-package output/react/ --skip-quality-check
```

### 📝 What's Changed

**New Features:**
- Comprehensive quality checker module
- Headless enhancement mode (default)
- Quality checks in packaging workflow
- MCP server skips interactive checks
- Enhanced error handling and timeout protection

**Bug Fixes:**
- Fixed enhancement race condition
- Fixed MCP stdin errors in CI
- Fixed terminal detection tests for headless default

**See [CHANGELOG.md](https://github.com/yusufkaraaslan/Skill_Seekers/blob/main/CHANGELOG.md) for complete details**

### 📚 Documentation

- [Installation Guide](https://github.com/yusufkaraaslan/Skill_Seekers#installation)
- [Quick Start](https://github.com/yusufkaraaslan/Skill_Seekers#quick-start)
- [CHANGELOG](https://github.com/yusufkaraaslan/Skill_Seekers/blob/main/CHANGELOG.md)

---

**Full Changelog**: https://github.com/yusufkaraaslan/Skill_Seekers/compare/v2.0.0...v2.1.0

## v2.0.0: v2.0.0 - Unified Multi-Source Scraping

**Published**: 2025-10-26

# 🎉 Now Available on PyPI!

**Skill Seekers is now published on the Python Package Index!**

Install with a single command:

```bash
pip install skill-seekers
```

No cloning, no setup - just install and use!

[![PyPI version](https://badge.fury.io/py/skill-seekers.svg)](https://pypi.org/project/skill-seekers/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/skill-seekers.svg)](https://pypi.org/project/skill-seekers/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/skill-seekers.svg)](https://pypi.org/project/skill-seekers/)

**Links:**
- 📦 [PyPI Project Page](https://pypi.org/project/skill-seekers/)
- 📚 [Installation Guide](https://github.com/yusufkaraaslan/Skill_Seekers#quick-start)
- 📖 [Changelog](https://github.com/yusufkaraaslan/Skill_Seekers/blob/main/CHANGELOG.md)

---

## 🚀 Quick Start

```bash
# Install from PyPI
pip install skill-seekers

# Use the unified CLI
skill-seekers scrape --config configs/react.json
skill-seekers github --repo facebook/react
skill-seekers package output/react/
```

---

## ✨ What's New in v2.0.0

### Modern Python Packaging
- ✅ Published to PyPI (`pip install skill-seekers`)
- ✅ Unified CLI (`skill-seekers` command with subcommands)
- ✅ pyproject.toml-based configuration
- ✅ src/ layout for best practices
- ✅ Entry points for all commands

### Testing & Quality (Updated Nov 11, 2025)
- ✅ **379 passing tests** (up from 369, 0 failures)
- ✅ Fixed all import paths for src/ layout
- ✅ Updated test suite for package structure
- ✅ MCP server tests fully passing
- ✅ Comprehensive pytest configuration

---

# 🚀 Skill Seekers v2.0.0 - Unified Multi-Source Scraping

**Release Date:** October 26, 2025  
**Updated:** November 11, 2025 (PyPI Publication)  
**Status:** Production Ready

---

## 🎯 Major Features

### Unified Multi-Source Scraping
Combine **documentation websites, GitHub repositories, and PDFs** into a single comprehensive skill!

**New Capabilities:**
- ✅ **Multi-source configs** - One config file, multiple sources
- ✅ **GitHub code analysis** - AST parsing for Python, JS, TS, Java, C++, Go
- ✅ **Conflict detection** - Compare docs vs actual code implementation
- ✅ **Smart merging** - Rule-based or Claude-enhanced merging
- ✅ **MCP integration** - Natural language: "Scrape GitHub repo facebook/react"

**Example unified config:**
```json
{
  "name": "react_complete",
  "merge_mode": "claude-enhanced",
  "sources": [
    {"type": "documentation", "base_url": "https://react.dev/"},
    {"type": "github", "repo": "facebook/react", "extract_api": true}
  ]
}
```

### GitHub Repository Scraping (C1 Task Group)
Deep code analysis and repository understanding:

- ✅ **AST parsing** - Extract functions, classes, types with full signatures
- ✅ **Repository metadata** - README, file tree, language stats, stars/forks
- ✅ **Issues & PRs** - Fetch open/closed issues with labels
- ✅ **CHANGELOG tracking** - Automatically extract version history
- ✅ **API extraction** - Complete API reference from actual code

### Conflict Detection
Compare documentation against actual code:

- ✅ **Missing APIs** - Find documented APIs not in code
- ✅ **Undocumented APIs** - Find code APIs missing from docs
- ✅ **Signature mismatches** - Detect parameter differences
- ✅ **Detailed reports** - JSON output with file locations

---

## 🛠️ New Tools & Commands

### Unified CLI (New!)
```bash
# Single command, multiple subcommands
skill-seekers --help

# Available commands:
skill-seekers scrape    # Documentation scraping
skill-seekers github    # GitHub repository scraping
skill-seekers pdf       # PDF extraction
skill-seekers unified   # Multi-source scraping
skill-seekers enhance   # AI enhancement
skill-seekers package   # Package to .zip
skill-seekers upload    # Upload to Claude
skill-seekers estimate  # Estimate page count
```

### Legacy CLI (Still supported)
```bash
# Original method still works
python3 src/skill_seekers/cli/doc_scraper.py --config configs/react.json
python3 src/skill_seekers/cli/github_scraper.py --repo facebook/react
python3 src/skill_seekers/cli/unified_scraper.py --config configs/react_unified.json
```

### MCP Tools (Enhanced)
All MCP tools now support unified configs:

```bash
# In Claude Code (natural language):
"Scrape React docs and GitHub repo into one skill"
"Generate unified config for Next.js"
"Detect conflicts in FastAPI docs vs code"
```

---

## 📦 What's Included

### New Files (19)
- `src/skill_seekers/cli/github_scraper.py` (786 lines) - GitHub repo scraper
- `src/skill_seekers/cli/code_analyzer.py` (491 lines) - AST code analysis
- `src/skill_seekers/cli/conflict_detector.py` (495 lines) - Docs vs code comparison
- `src/skill_seekers/cli/unified_scraper.py` (449 lines) - Multi-source orchestrator
- `src/skill_seekers/cli/merge_sources.py` (513 lines) - Intelligent merging
- `src/skill_seekers/cli/unified_skill_builder.py` (433 lines) - Skill generator
- `src/skill_seekers/cli/config_validator.py` (367 lines) - Config validation
- `src/skill_seekers/cli/main.py` (285 lines) - Unified CLI entry point
- `docs/UNIFIED_SCRAPING.md` (633 lines) - Complete guide
- `FUTURE_RELEASES.md` (288 lines) - Roadmap document
- 8 new unified config examples
- `tests/test_github_scraper.py` (734 lines) - GitHub tests
- `tests/test_setup_scripts.py` (221 lines) - Bash script tests
- `tests/test_unified_mcp_integration.py` (187 lines) - MCP tests

### Enhanced Files (5)
- `src/skill_seekers/mcp/server.py` - Updated with unified scraping support
- `README.md` - Added PyPI badges, reordered installation options
- `CHANGELOG.md` - Complete v2.0.0 release notes with PyPI info
- `QUICKSTART.md` - Added unified scraping examples
- `pyproject.toml` - Modern packaging configuration

---

## 🧪 Testing

**Total Tests:** 379 (up from 369)

**New Test Coverage:**
- ✅ GitHub scraper tests (40 tests)
- ✅ Unified MCP integration (4 tests)
- ✅ Bash script validation (19 tests)
- ✅ Path consistency checks (4 tests)
- ✅ Package structure tests (10 tests)

**Test Results:**
- ✅ 379/379 tests passing (100%)
- ✅ All import paths fixed for src/ layout
- ✅ MCP server tests fully working
- ✅ GitHub Actions CI passing
- ✅ All configs verified working

---

## 🐛 Bug Fixes

### Fixed Issue #157
- ✅ Updated setup_mcp.sh with correct paths
- ✅ Fixed 27 old `mcp/` references in docs
- ✅ Added bash script tests to prevent regression

### Fixed Issue #168 (PyPI Publication)
- ✅ Modern Python packaging with pyproject.toml
- ✅ Fixed all import paths for src/ layout
- ✅ Updated test suite for package structure
- ✅ Fixed merge_sources.py import error
- ✅ Fixed MCP server test imports

### Path Consistency
- ✅ All references now use `src/skill_seekers/` directory
- ✅ Tests validate path consistency across codebase
- ✅ Entry points properly configured

---

## 📊 Statistics

**Code Added:** +6,904 lines
**Code Removed:** -1,939 lines
**Net Change:** +4,965 lines

**Lines by Component:**
- GitHub scraper: 786 lines
- Unified scraping: 3,200+ lines
- Unified CLI: 285 lines
- Tests: 1,142 lines
- Documentation: 921 lines (includes FUTURE_RELEASES.md)
- Config examples: 200+ lines

---

## 🎓 Documentation

**New Guides:**
- [Unified Scraping Guide](docs/UNIFIED_SCRAPING.md) - Complete tutorial
- [Future Releases Roadmap](FUTURE_RELEASES.md) - Upcoming features
- Enhanced README with PyPI installation
- [Changelog](CHANGELOG.md) - Complete v2.0.0 release notes

**Updated Guides:**
- QUICKSTART.md - Added unified examples
- MCP_SETUP.md - Updated paths
- CLAUDE.md - Added unified scraping architecture
- README.md - PyPI badges and installation options

---

## 🔄 Upgrade Guide

### From v1.x to v2.0.0

**No breaking changes!** v1.x configs still work perfectly.

**Recommended migration:**

```bash
# Old way (still works)
git clone https://github.com/yusufkaraaslan/Skill_Seekers.git
cd Skill_Seekers
pip install -r requirements.txt
python3 src/skill_seekers/cli/doc_scraper.py --config configs/react.json

# New way (recommended)
pip install skill-seekers
skill-seekers scrape --config configs/react.json
```

**To use new unified features:**

1. **Create unified config:**
```json
{
  "name": "myproject",
  "merge_mode": "rule-based",
  "sources": [
    {"type": "documentation", "base_url": "https://docs.example.com"},
    {"type": "github", "repo": "user/repo"}
  ]
}
```

2. **Run unified scraper:**
```bash
skill-seekers unified --config configs/myproject.json
```

3. **Optional: Detect conflicts:**
```bash
# Coming soon - conflict detection subcommand
```

---

## 🙏 Credits

This release completes the **C1 task group** (GitHub scraping and unified multi-source support) and **Issue #168** (PyPI publication).

**Development:**
- 19 new files created
- 379 tests (100% passing)
- 921 lines of documentation
- 8 example configs
- Published to PyPI

**Community:**
- Fixed Issue #157 (setup_mcp.sh paths)
- Fixed Issue #168 (PyPI publication)
- Cleaned up 8 redundant files
- Improved test coverage

---

## 📝 Next Steps

Check out the roadmap for upcoming features in [FUTURE_RELEASES.md](FUTURE_RELEASES.md):

**v2.1.0 (Dec 2025):**
- Fix 12 unified scraping tests
- Improve test coverage to 60%+
- Enhanced error handling

**v2.2.0 (Q1 2026):**
- GitHub Pages website
- Plugin system foundation
- Additional documentation formats

See [FLEXIBLE_ROADMAP.md](FLEXIBLE_ROADMAP.md) for the complete task catalog (134 tasks).

---

**Happy skill building! 🚀**

```bash
# Try it now:
pip install skill-seekers
skill-seekers scrape --config configs/react.json
```

**Full documentation:** [docs/UNIFIED_SCRAPING.md](docs/UNIFIED_SCRAPING.md)

## v1.3.0: v1.3.0 - Refactoring & Performance (2-3x Faster)

**Published**: 2025-10-26

# 🚀 v1.3.0 - Refactoring & Performance Improvements

Major refactoring release with async support, improved code quality, and better package structure.

## 🎯 Performance Highlights

- **2-3x faster scraping** with async mode (18 pg/s → 55 pg/s)
- **66% less memory** (120 MB → 40 MB)
- **299 tests** (92 new tests added)

## ✨ New Features

### Async/Await Support for Parallel Scraping
```bash
# Enable async mode with 8 workers (recommended for large docs)
python3 cli/doc_scraper.py --config configs/react.json --async --workers 8
```

**Performance Comparison:**
- Sync: ~18 pages/sec, 120 MB memory
- Async: ~55 pages/sec, 40 MB memory
- **3x faster with 66% less memory!**

### Python Package Structure
- Proper `__init__.py` files for clean imports
- `cli/` package with organized modules
- `skill_seeker_mcp/` package (renamed from mcp/)
- Better IDE support and maintainability

### Centralized Configuration
- New `cli/constants.py` with 18 configuration constants
- All magic numbers centralized and configurable
- Easy to customize defaults

## 🔧 Code Quality Improvements

- **71 print statements → proper logging** (logger.info, logger.warning, logger.error)
- **Type hints added** to all DocToSkillConverter methods
- **mypy type checking** - all issues fixed
- **Better error handling** with comprehensive logging

## 📚 Documentation

- New `ASYNC_SUPPORT.md` - Complete async guide
- Updated README.md with async examples
- Updated CLAUDE.md with technical details
- Comprehensive CHANGELOG.md

## 🧪 Testing

- **299 tests passing** (was 207)
- 92 new tests added:
  - 11 async scraping tests
  - 26 integration tests
  - 13 llms.txt tests
  - 21 constants tests
  - 21 package structure tests
- 100% test pass rate
- Fixed test isolation issues

## 🔄 Breaking Changes

**None!** This is a backwards-compatible refactoring release.

## 📦 What's Changed

### Added
- Async/await support with `--async` flag
- Connection pooling for better performance
- asyncio.Semaphore for concurrency control
- Python package structure with proper imports
- Centralized configuration module
- Type hints throughout codebase
- Comprehensive test coverage

### Changed
- All print() → logging calls
- Better IDE support with package structure
- Code quality improved from 5.5/10 to 6.5/10
- Test count: 207 → 299

### Fixed
- Test isolation issues
- Import issues (no more sys.path.insert hacks)
- All mypy type checking issues

## 📖 Full Changelog

See [CHANGELOG.md](https://github.com/yusufkaraaslan/Skill_Seekers/blob/main/CHANGELOG.md#130---2025-10-26) for complete details.

## 🙏 Acknowledgments

This refactoring was completed as Phase 0 of our development roadmap, setting a solid foundation for future features.

---

**Installation:**
```bash
git clone https://github.com/yusufkaraaslan/Skill_Seekers.git
cd Skill_Seekers
pip install -r requirements.txt
```

**Quick Start:**
```bash
# Try async mode
python3 cli/doc_scraper.py --config configs/react.json --async --workers 8
```

🤖 Generated with [Claude Code](https://claude.com/claude-code)

## v1.2.0: v1.2.0 - PDF Advanced Features Release

**Published**: 2025-10-23

# v1.2.0 - PDF Advanced Features Release

**Date:** October 23, 2025

Major enhancement to PDF extraction capabilities with advanced features for handling any type of PDF documentation.

## 🚀 What's New

### Enhanced PDF Support
- **OCR for Scanned PDFs** - Automatically extract text from scanned documents using Tesseract OCR
  - Intelligent fallback when text content is low (< 50 characters)
  - Works with pytesseract and Pillow
  - Command: `--ocr`

- **Password-Protected PDFs** - Handle encrypted PDF files securely
  - Clear error messages for authentication issues
  - Command: `--password PASSWORD`

- **Table Extraction** - Extract complex tables from PDF documents
  - Captures table data as structured 2D arrays
  - Includes metadata (bounding box, row/column counts)
  - Integrates seamlessly with skill references
  - Command: `--extract-tables`

### Performance Improvements
- **3x Faster Processing** - Parallel page processing using multi-threading
  - Auto-detects CPU count or accepts custom worker specification
  - Activates automatically for PDFs with 5+ pages
  - Benchmark: 500-page PDF reduced from 4m 10s to 1m 15s
  - Commands: `--parallel` and `--workers N`

- **Intelligent Caching** - 50% faster on subsequent runs
  - In-memory cache for expensive operations (text extraction, code detection, quality scoring)
  - Enabled by default, disable with `--no-cache`

## 📚 Usage Examples

### Basic PDF Extraction
```bash
python3 cli/pdf_scraper.py --pdf docs/manual.pdf --name myskill
```

### Maximum Performance
```bash
python3 cli/pdf_scraper.py --pdf docs/manual.pdf --name myskill \
    --extract-tables \
    --parallel \
    --workers 8
```

### Scanned PDFs
```bash
pip3 install pytesseract Pillow
python3 cli/pdf_scraper.py --pdf docs/scanned.pdf --name myskill --ocr
```

### Password-Protected PDFs
```bash
python3 cli/pdf_scraper.py --pdf docs/encrypted.pdf --name myskill --password mypassword
```

### All Features Combined
```bash
python3 cli/pdf_scraper.py --pdf docs/manual.pdf --name myskill \
    --ocr \
    --extract-tables \
    --parallel \
    --workers 8 \
    --verbose
```

## 📊 Performance Benchmarks

| Pages | Sequential | Parallel (4 workers) | Parallel (8 workers) |
|-------|-----------|---------------------|---------------------|
| 50    | 25s       | 10s (2.5x)          | 8s (3.1x)           |
| 100   | 50s       | 18s (2.8x)          | 15s (3.3x)          |
| 500   | 4m 10s    | 1m 30s (2.8x)       | 1m 15s (3.3x)       |
| 1000  | 8m 20s    | 3m 00s (2.8x)       | 2m 30s (3.3x)       |

## 🧪 Testing

- **New Test Suite:** test_pdf_advanced_features.py (26 comprehensive tests)
  - OCR Support (5 tests)
  - Password Protection (4 tests)
  - Table Extraction (5 tests)
  - Parallel Processing (4 tests)
  - Intelligent Caching (5 tests)
  - Integration (3 tests)

- **Updated Tests:** test_pdf_extractor.py (23 tests, all passing)
- **Total PDF Tests:** 49/49 passing (100%)
- **Overall Project:** 142/142 tests passing (100%)

## 📖 Documentation

- **New Guide:** docs/PDF_ADVANCED_FEATURES.md (580 lines)
  - Complete usage guide
  - Installation instructions
  - Performance benchmarks
  - Best practices
  - Troubleshooting
  - API reference

## 📦 Dependencies

### New Required Dependencies
```bash
pip3 install Pillow==11.0.0 pytesseract==0.3.13
```

### Optional System Dependency
- Tesseract OCR engine (for scanned PDF support)
  - Ubuntu/Debian: sudo apt-get install tesseract-ocr
  - macOS: brew install tesseract

## 🔧 What's Changed

- Enhanced cli/pdf_extractor_poc.py with all advanced features
- Added cli/pdf_scraper.py for full workflow support
- Updated requirements.txt with new dependencies
- Updated README.md with advanced features showcase
- Updated docs/TESTING.md with comprehensive test documentation
- Added extensive PDF documentation (7 new guides)

## 🐛 Bug Fixes

- Fixed function signature mismatches in tests
- Updated language detection confidence thresholds
- Corrected chapter detection patterns
- Fixed code block merging with proper metadata

## 📝 Full Changelog

See CHANGELOG.md for complete version history.

---

**Full Diff:** https://github.com/yusufkaraaslan/Skill_Seekers/compare/v1.1.0...v1.2.0

---

This release represents a major step forward in PDF documentation processing capabilities. Now you can extract comprehensive skills from virtually any PDF, whether it's a modern digital document, a scanned paper book, or an encrypted technical manual! 🎉

## v1.1.0: v1.1.0 - Parallel Scraping & Enhanced Testing 🚀

**Published**: 2025-10-22

# v1.1.0 - Parallel Scraping & Enhanced Testing 🚀

**Release Date:** October 22, 2025  
**Commits Since v1.0.0:** 29 commits  
**Contributors:** @yusufkaraaslan, @schuyler, @jjshanks, @justSteve

---

## 🎯 Highlights

This release brings **massive performance improvements** with parallel scraping, unlimited mode, and comprehensive test coverage improvements.

### ⚡ Performance Boost
- **8x faster scraping** with parallel mode (8 workers)
- **Unlimited scraping** mode for large documentation sites
- **Configurable rate limiting** for optimal speed vs politeness

### 🧪 Quality & Reliability
- **100+ new tests** added across CLI utilities
- **Test isolation fixes** for reliable CI/CD
- **All 158 tests passing** consistently

### 📚 New Configs
- **Ansible Core** documentation support
- **Claude Code** documentation support

---

## 🚀 Major Features

### Parallel Scraping Mode (#144)
Speed up documentation scraping with multiple workers:

```bash
# Use 4 workers (4x faster)
python3 cli/doc_scraper.py --config configs/react.json --workers 4

# Maximum speed (8 workers)
python3 cli/doc_scraper.py --config configs/godot.json --workers 8
```

**Performance:**
- 1 worker (default): 100 pages in ~50 seconds
- 4 workers: 100 pages in ~15 seconds (3.3x faster)
- 8 workers: 100 pages in ~8 seconds (6.25x faster)

**Thread-Safe Implementation:**
- Proper locking for shared state
- Safe URL deduplication
- Coordinated rate limiting across workers

### Unlimited Scraping Mode (#144)
Scrape entire documentation sites without page limits:

```bash
# Unlimited mode
python3 cli/doc_scraper.py --config configs/vue.json --unlimited

# Or via config
{
  "max_pages": null  // or -1
}
```

**Use Cases:**
- Complete documentation archives
- Large API reference sites
- Comprehensive framework docs

### Flexible Rate Limiting (#144)
Fine-tune scraping speed:

```bash
# Fast scraping (0.1s delay)
python3 cli/doc_scraper.py --config configs/react.json --rate-limit 0.1

# No rate limit (maximum speed, use carefully!)
python3 cli/doc_scraper.py --config configs/react.json --no-rate-limit

# Polite scraping (2s delay)
python3 cli/doc_scraper.py --config configs/react.json --rate-limit 2.0
```

---

## 🐛 Bug Fixes

### Critical Fixes
- **Fix flaky upload_skill tests** (0c55151) - Proper test isolation with cwd restoration
- **Fix CLI path references** (#145, 581dbc7) - All paths now use `cli/` prefix correctly
- **Fix anchor fragment handling** (#5) - Strip URL anchors to prevent duplicates
- **Fix broken configs** (#7) - Django, Laravel, Astro, Tailwind all working

### Test Infrastructure
- **Add comprehensive CLI utilities tests** (13fcce1) - 100+ new tests
- **Add parallel scraping tests** (7e94c27) - 17 tests for new features
- **Fix test isolation** (0c55151) - Tests no longer interfere with each other

---

## 📝 Documentation Updates

### New Guides
- **BULLETPROOF_QUICKSTART.md** (#8) - Complete beginner guide
- **TROUBLESHOOTING.md** (#8) - Comprehensive troubleshooting
- **Virtual environment setup** (#149) - Clean dependency management

### Documentation Improvements
- **Updated all CLI examples** (#145) - Use `cli/` directory consistently
- **Fixed path references** (66719cd) - Correct paths throughout docs
- **Added Ansible config docs** (#147) - Configuration examples

---

## 🆕 New Configurations

### Production Configs Added
- **`configs/ansible-core.json`** (#147) - Ansible Core documentation
- **`configs/claude-code.json`** (e5f4d10) - Claude Code documentation
- **`configs/laravel.json`** (#7) - Laravel 9.x framework

### Config Fixes
- ✅ **Django** - Fixed selector
- ✅ **Astro** - Fixed selector
- ✅ **Tailwind** - Fixed selector
- ✅ **All 11 configs verified working**

---

## 🧪 Testing Improvements

### Test Coverage
- **158 tests total** (up from ~50)
- **100% pass rate** in CI/CD
- **All platforms tested** (Ubuntu, macOS, Windows)

### New Test Suites
- `tests/test_parallel_scraping.py` - 17 tests for parallel mode
- `tests/test_upload_skill.py` - 7 tests for upload functionality
- `tests/test_utilities.py` - 24 tests for CLI utilities
- `tests/test_cli_paths.py` - Path reference validation

### Test Quality
- Proper setUp/tearDown in all test classes
- Test isolation maintained across suites
- No more flaky tests in CI

---

## 🔧 Technical Improvements

### Code Quality
- **Thread-safe parallel scraping** with proper locking
- **Improved error handling** in subprocess calls
- **Better exception propagation** in worker threads
- **Consistent path handling** across all CLI tools

### Performance Optimizations
- **Batch URL processing** for efficiency
- **Per-worker rate limiting** for fair resource usage
- **Optimized checkpoint saving** during scraping

### Developer Experience
- **Better CLI error messages**
- **Clearer progress indicators**
- **Improved debugging output**

---

## 📊 Statistics

### Changes
- **29 commits** since v1.0.0
- **5 pull requests** merged
- **8 issues** resolved
- **100+ new tests** added
- **3 new configs** added

### Files Changed
- `cli/doc_scraper.py` - Parallel scraping, unlimited mode
- `cli/enhance_skill.py` - Path fixes
- `cli/enhance_skill_local.py` - Path fixes
- `cli/package_skill.py` - Path fixes
- `tests/` - Comprehensive new test suites

### Contributors
Special thanks to:
- @schuyler - Claude Code config contribution
- @jjshanks - Anchor fragment fix
- @justSteve - Bug reports and validation testing

---

## 🚀 Upgrade Instructions

### From v1.0.0 to v1.1.0

```bash
# Pull latest changes
git pull origin main

# No breaking changes - fully backward compatible!
# All existing configs and commands work as before

# Try new features
python3 cli/doc_scraper.py --config configs/react.json --workers 4
python3 cli/doc_scraper.py --config configs/godot.json --unlimited
```

### New Dependencies
No new dependencies required! Still just:
```bash
pip3 install requests beautifulsoup4
```

---

## 🔜 What's Next

### Planned for v1.2.0
- **GitHub repository scraping** (#54, #55, #62)
- **Enhanced MCP server tools** (#139)
- **Config validation improvements**
- **More preset configurations**

See our [FLEXIBLE_ROADMAP.md](https://github.com/yusufkaraaslan/Skill_Seekers/blob/main/FLEXIBLE_ROADMAP.md) for the complete feature list.

---

## 📋 Full Changelog

### Features
- Add parallel scraping with multiple workers (#144)
- Add unlimited scraping mode (#144)
- Add configurable rate limiting (#144)
- Add Ansible Core config (#147)
- Add Claude Code config (e5f4d10)
- Add virtual environment setup (#149)

### Bug Fixes
- Fix flaky upload_skill tests (0c55151)
- Fix CLI path references throughout codebase (#145)
- Fix anchor fragment handling (#5)
- Fix broken configs for Django, Laravel, Astro, Tailwind (#7)
- Fix test isolation issues (0c55151)

### Documentation
- Add BULLETPROOF_QUICKSTART.md (#8)
- Add TROUBLESHOOTING.md (#8)
- Update all CLI examples to use cli/ directory (#145)
- Fix path references in documentation (66719cd)

### Tests
- Add comprehensive CLI utilities tests (13fcce1)
- Add parallel scraping tests (7e94c27)
- Add CLI path validation tests (c031865)
- Fix test isolation with proper setUp/tearDown (0c55151)

### Closed Issues
- #117 - Tasks already complete
- #125 - Tasks already complete
- #146 - CLI path reference bug
- #147 - Ansible config request
- #149 - Virtual environment setup

---

## 🙏 Thank You!

Thank you to everyone who contributed, tested, reported bugs, and provided feedback. Your input makes Skill Seekers better! 🎉

**Feedback?** Open an issue at https://github.com/yusufkaraaslan/Skill_Seekers/issues

**Questions?** Check our docs at https://github.com/yusufkaraaslan/Skill_Seekers

---

**Full Diff:** https://github.com/yusufkaraaslan/Skill_Seekers/compare/v1.0.0...v1.1.0

## v1.0.0: v1.0.0 - Production Ready 🚀

**Published**: 2025-10-19

# Release v1.0.0 - Production Ready 🚀

First production-ready release of Skill Seekers!

## 🎉 Major Features

### Smart Auto-Upload
- Automatic skill upload with API key detection
- Graceful fallback to manual instructions
- Cross-platform folder opening
- New `upload_skill.py` CLI tool

### 9 MCP Tools for Claude Code
1. list_configs
2. generate_config
3. validate_config
4. estimate_pages
5. scrape_docs
6. package_skill (enhanced with auto-upload)
7. **upload_skill (NEW!)**
8. split_config
9. generate_router

### Large Documentation Support
- Handle 10K-40K+ page documentation
- Intelligent config splitting
- Router/hub skill generation
- Checkpoint/resume for long scrapes
- Parallel scraping support

## ✨ What's New

- ✅ Smart API key detection and auto-upload
- ✅ Enhanced package_skill with --upload flag
- ✅ Cross-platform utilities (macOS/Linux/Windows)
- ✅ Improved error messages and UX
- ✅ Complete test coverage (14/14 tests passing)

## 🐛 Bug Fixes

- Fixed missing `import os` in mcp/server.py
- Fixed package_skill.py exit codes
- Improved error handling throughout

## 📚 Documentation

- All documentation updated to reflect 9 tools
- Enhanced upload guide
- MCP setup guide improvements
- Comprehensive test documentation
- New CHANGELOG.md
- New CONTRIBUTING.md

## 📦 Installation

```bash
# Install dependencies
pip3 install requests beautifulsoup4

# Optional: MCP integration
./setup_mcp.sh

# Optional: API-based features
pip3 install anthropic
export ANTHROPIC_API_KEY=sk-ant-...
```

## 🚀 Quick Start

```bash
# Scrape React docs
python3 cli/doc_scraper.py --config configs/react.json --enhance-local

# Package and upload
python3 cli/package_skill.py output/react/ --upload
```

## 🧪 Testing

- **Total Tests:** 14/14 PASSED ✅
- **CLI Tests:** 8/8 ✅
- **MCP Tests:** 6/6 ✅
- **Pass Rate:** 100%

## 📊 Statistics

- **Files Changed:** 49
- **Lines Added:** +7,980
- **Lines Removed:** -296
- **New Features:** 10+
- **Bug Fixes:** 3

## 🔗 Links

- [Documentation](https://github.com/yusufkaraaslan/Skill_Seekers#readme)
- [MCP Setup Guide](docs/MCP_SETUP.md)
- [Upload Guide](docs/UPLOAD_GUIDE.md)
- [Large Documentation Guide](docs/LARGE_DOCUMENTATION.md)
- [Contributing Guidelines](CONTRIBUTING.md)
- [Changelog](CHANGELOG.md)

**Full Changelog:** [af87572...7aa5f0d](https://github.com/yusufkaraaslan/Skill_Seekers/compare/af87572...7aa5f0d)


