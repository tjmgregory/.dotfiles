# Evaluation-Driven Development

Build evaluations BEFORE writing extensive documentation. This ensures the skill solves real problems rather than documenting imagined ones.

## Process

1. **Identify gaps**: Run Claude on representative tasks without the skill. Document specific failures or missing context.
2. **Create evaluations**: Build at least three scenarios that test these gaps.
3. **Establish baseline**: Measure Claude's performance without the skill.
4. **Write minimal instructions**: Create just enough content to address the gaps and pass evaluations.
5. **Iterate**: Execute evaluations, compare against baseline, and refine.

## Evaluation Structure

```json
{
  "skills": ["pdf-processing"],
  "query": "Extract all text from this PDF file and save it to output.txt",
  "files": ["test-files/document.pdf"],
  "expected_behavior": [
    "Successfully reads the PDF file using an appropriate library",
    "Extracts text content from all pages without missing any",
    "Saves the extracted text to output.txt in clear, readable format"
  ]
}
```

## Test with Multiple Models

Skills act as additions to models, so effectiveness depends on the underlying model. Test with all models you plan to use:

- **Claude Haiku** (fast, economical): Does the skill provide enough guidance?
- **Claude Sonnet** (balanced): Is the skill clear and efficient?
- **Claude Opus** (powerful reasoning): Does the skill avoid over-explaining?

What works perfectly for Opus might need more detail for Haiku. If you plan to use the skill across multiple models, aim for instructions that work well with all of them.

## Iteration Based on Observation

1. Use the skill on real tasks
2. Notice struggles or inefficiencies
3. Identify how SKILL.md or bundled resources should be updated
4. Implement changes and test again

Watch for:
- **Unexpected exploration paths**: Does Claude read files in an order you didn't anticipate?
- **Missed connections**: Does Claude fail to follow references to important files?
- **Overreliance on certain sections**: If Claude repeatedly reads the same file, move content to main SKILL.md
- **Ignored content**: If Claude never accesses a bundled file, it might be unnecessary

Iterate based on observed behavior, not assumptions.
