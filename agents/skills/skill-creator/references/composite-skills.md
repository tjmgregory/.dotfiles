# Composite Skills

Skills can reference and recommend other skills to handle parts of a workflow. This enables modular, composable agent capabilities where each skill owns its domain completely.

## The Composability Principle

**A skill that references another skill MUST NOT include ANY implementation details about how the referenced skill works.**

This is the fundamental rule of skill composition. Each skill totally owns how it accomplishes its task. A referring skill should only describe:

1. **The situation** that demands the other skill
2. **When** to invoke it in the workflow
3. **What outcome** to expect (not how it achieves that outcome)

### Why This Matters

- **Single source of truth**: Implementation details live in one place only
- **Independent evolution**: Skills can be updated without cascading changes
- **No context bleeding**: Referencing skills stay lean and focused
- **Clear boundaries**: Each skill's responsibilities are unambiguous

## Pattern: Situational Triggers

When a skill's workflow reaches a point where another skill should take over, describe the situation explicitly:

**Good** - Describes the situation:
```markdown
## Data Visualization

When the analysis is complete and results need to be visualized:
- If the user has the `excel-charts` skill available, use it for chart generation
- The visualization step requires formatted data ready for charting

Hand off to the charting skill when visualization is needed.
```

**Bad** - Bleeds implementation:
```markdown
## Data Visualization

When the analysis is complete, use the excel-charts skill which works by:
1. Opening the workbook with openpyxl
2. Creating a ChartSheet object
3. Configuring the chart type and data range
4. ...
```

The bad example duplicates knowledge that belongs to `excel-charts`. If that skill changes its approach, the referring skill becomes wrong.

## Pattern: Conditional Skill References

Reference skills conditionally based on what the user has available:

```markdown
## Report Generation

After data processing:

1. **If generating PDF output**: The `pdf-processing` skill handles PDF creation
2. **If generating slides**: The `presentation-builder` skill handles slide decks
3. **If generating spreadsheets**: The `excel-analysis` skill handles workbook creation

Choose the appropriate output skill based on the user's requested format.
```

## Pattern: Workflow Handoff Points

Define clear handoff points where control transfers to another skill:

```markdown
## Customer Data Pipeline

This skill handles data extraction and transformation.

**Handoff points:**

- **After extraction, if data quality checks are needed**: Invoke `data-validation` skill
- **After transformation, if the data needs to be loaded**: Invoke `database-loader` skill
- **If errors occur that need incident tracking**: Invoke `incident-management` skill

Each handoff should include the context the receiving skill needs (file paths, data formats, etc.) but NOT instructions on how that skill should operate.
```

## Anti-Patterns

### Don't: Duplicate Workflows

```markdown
# Bad: Duplicates pdf-processing knowledge
When creating a PDF:
1. Use reportlab to create a canvas
2. Set the page size to A4
3. Add the header with company logo
4. ...
```

### Don't: Override Another Skill's Decisions

```markdown
# Bad: Makes decisions for another skill
Use the excel-charts skill but make sure it uses bar charts, not pie charts,
and always puts the legend on the right side.
```

### Don't: Assume Implementation Details

```markdown
# Bad: Assumes how another skill works internally
After the data-validation skill runs, check the validation_errors.json file
it creates in the temp directory.
```

## Describing Dependencies in Metadata

If a skill fundamentally requires another skill to function, mention this in the description:

```yaml
---
name: financial-reporting
description: Generates quarterly financial reports with charts and analysis.
  Requires excel-analysis skill for data processing and pdf-processing skill
  for final report generation. Use when creating financial reports, quarterly
  summaries, or board presentations.
---
```

This helps users understand what skills need to be available together.

## Testing Composite Skills

When testing a skill that references others:

1. **Test in isolation first**: Verify the skill's own logic works correctly
2. **Test with referenced skills available**: Verify handoffs work correctly
3. **Test with referenced skills missing**: Verify graceful handling or clear error messages
4. **Verify no context bleeding**: Check that updates to referenced skills don't require changes to the referring skill
