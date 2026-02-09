# Content Guidelines

## Avoid Time-Sensitive Information

Don't include information that will become outdated:

**Bad** (will become wrong):
```markdown
If you're doing this before August 2025, use the old API.
After August 2025, use the new API.
```

**Good** (use an "old patterns" section):
```markdown
## Current method
Use the v2 API endpoint: `api.example.com/v2/messages`

## Old patterns
<details>
<summary>Legacy v1 API (deprecated)</summary>
The v1 API used: `api.example.com/v1/messages`
</details>
```

## Use Consistent Terminology

Choose one term and use it throughout the skill:

**Good**: Always "API endpoint", always "field", always "extract"

**Bad**: Mix "API endpoint", "URL", "API route", "path"; mix "field", "box", "element"

Consistency helps Claude understand and follow instructions accurately.

## Avoid Offering Too Many Options

Don't present multiple approaches unless necessary:

**Bad** (confusing):
```markdown
You can use pypdf, or pdfplumber, or PyMuPDF, or pdf2image...
```

**Good** (provide a default with escape hatch):
```markdown
Use pdfplumber for text extraction:
[code example]

For scanned PDFs requiring OCR, use pdf2image with pytesseract instead.
```

## File Path Conventions

Always use forward slashes in file paths, even on Windows:

- **Correct**: `scripts/helper.py`, `references/guide.md`
- **Avoid**: `scripts\helper.py`, `references\guide.md`

Use paths relative to the skill directory. When referencing bundled files in SKILL.md, use relative paths like `scripts/analyze.py` or `references/schema.md`.

Name files descriptively to indicate content:
- **Good**: `form_validation_rules.md`, `database_schema.md`
- **Bad**: `doc2.md`, `file1.md`, `ref.md`
