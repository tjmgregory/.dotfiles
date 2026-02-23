---
name: diagramming-with-mermaid
description: Generates and edits Mermaid diagrams with correct syntax across all 19 diagram types including flowcharts, sequence diagrams, class diagrams, state diagrams, ER diagrams, Gantt charts, pie charts, quadrant charts, XY charts, Sankey diagrams, mindmaps, timelines, gitgraphs, block diagrams, packet diagrams, architecture diagrams, kanban boards, requirement diagrams, and user journeys. Use when asked to create a diagram, visualize something, make a chart, draw a flowchart, model a database, or any request involving Mermaid syntax. Triggers include "mermaid", "diagram", "flowchart", "sequence diagram", "class diagram", "ER diagram", "gantt", "chart", "visualize", "draw", "graph".
---

# Mermaid Diagrams

Generate syntactically correct Mermaid diagrams. Always wrap output in a ` ```mermaid ` fenced code block.

## Diagram Type Selector

Match the user's need to the right diagram type:

| Need | Diagram Type | Declaration |
|------|-------------|-------------|
| Process flow, decision trees, system overview | **Flowchart** | `flowchart TD` |
| API calls, service interactions, message passing | **Sequence** | `sequenceDiagram` |
| OOP design, interfaces, inheritance | **Class** | `classDiagram` |
| Lifecycle, transitions, FSM | **State** | `stateDiagram-v2` |
| Database schema, table relationships | **ER** | `erDiagram` |
| Project schedule, task dependencies | **Gantt** | `gantt` |
| Proportions, distribution | **Pie** | `pie` |
| 2x2 matrix, prioritization | **Quadrant** | `quadrantChart` |
| Trends, bar/line data | **XY Chart** | `xychart-beta` |
| Flow quantities, budgets | **Sankey** | `sankey-beta` |
| Brainstorm, topic hierarchy | **Mindmap** | `mindmap` |
| Historical events, roadmap | **Timeline** | `timeline` |
| Git branching strategy | **Gitgraph** | `gitGraph` |
| Grid layout, infrastructure | **Block** | `block-beta` |
| Network protocol headers | **Packet** | `packet-beta` |
| Cloud/infra topology | **Architecture** | `architecture-beta` |
| Task board, sprint planning | **Kanban** | `kanban` |
| Specs traceability | **Requirement** | `requirementDiagram` |
| Customer experience mapping | **User Journey** | `journey` |

## Reference Files

Read the appropriate reference file for full syntax before generating a diagram:

- **Flowchart**: [references/flowchart.md](references/flowchart.md) -- All shapes (14 classic + 40+ new v11.3.0), edge types, subgraphs, icon/image nodes, styling, interactions
- **Sequence diagram**: [references/sequence.md](references/sequence.md) -- Arrow types, participant shapes, activation, control flow (loop/alt/par/critical/break), boxes, create/destroy
- **Class, State, ER diagrams**: [references/class-state-er.md](references/class-state-er.md) -- Class visibility/generics/namespaces, state composites/fork/join/concurrency, ER crow's foot notation/attributes
- **Gantt, Timeline, Kanban, User Journey, Requirement**: [references/project-planning.md](references/project-planning.md) -- Gantt task syntax/excludes/milestones, timeline sections, kanban metadata, journey scoring, requirement types/relationships
- **Pie, Quadrant, XY, Sankey charts**: [references/data-visualization.md](references/data-visualization.md) -- Pie showData, quadrant point styling, XY bar/line series, Sankey CSV format
- **Block, Packet, Architecture, Mindmap, Gitgraph**: [references/layout-diagrams.md](references/layout-diagrams.md) -- Block column spans, packet bit ranges, architecture groups/services/edges, mindmap indentation, gitgraph commit/branch/merge
- **Theming, styling, config, pitfalls**: [references/theming-styling.md](references/theming-styling.md) -- Frontmatter config, base theme customization, classDef, linkStyle, click events, common pitfalls

## Global Configuration

Apply via frontmatter at the top of any diagram:

```
---
config:
  theme: default
  look: handDrawn
  layout: elk
---
flowchart TD
    ...
```

Key options: `theme` (default/base/dark/forest/neutral), `look` (classic/handDrawn), `layout` (dagre/elk).

Comments: `%% comment text` on own line.

Accessibility: `accTitle: ...` and `accDescr: ...` after declaration.

## Generation Guidelines

1. **Read the reference first** -- Consult the relevant reference file before writing any non-trivial diagram to get exact syntax right.
2. **Choose the simplest diagram type** that conveys the information. A flowchart can often replace a more complex type.
3. **Use meaningful node IDs** -- `Auth["Auth Service"]` not `A["Auth Service"]`. Aids readability and styling.
4. **Quote text with special characters** -- Always use `["text"]` when text contains parentheses, brackets, or reserved words like `end`.
5. **Keep diagrams focused** -- If a diagram exceeds ~30 nodes, split into multiple diagrams or use subgraphs.
6. **Apply styling sparingly** -- Use `classDef` for consistent color schemes. Prefer 2-4 classes max.
7. **Use subgraphs/groups** to organize related nodes in flowcharts, blocks, and architecture diagrams.
8. **Direction matters** -- `LR` for wide/horizontal flows, `TD` for tall/vertical hierarchies.
9. **Avoid `layout: elk`** unless the diagram has complex edge crossings -- `dagre` (default) is faster and sufficient for most cases.
10. **Test edge cases** -- The word `end`, nodes starting with `o`/`x`, and unclosed quotes are common syntax breakers.
