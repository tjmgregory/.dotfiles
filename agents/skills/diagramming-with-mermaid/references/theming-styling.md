# Theming, Styling, and Configuration Reference

## Contents
- [Global Configuration](#global-configuration)
- [Theming](#theming)
- [CSS Classes and Styling](#css-classes-and-styling)
- [Interactions and Events](#interactions-and-events)
- [Common Pitfalls](#common-pitfalls)

---

# Global Configuration

## Frontmatter (Preferred, v10.5.0+)

```
---
config:
  theme: dark
  fontFamily: monospace
  logLevel: info
  flowchart:
    htmlLabels: true
    curve: linear
  sequence:
    mirrorActors: true
---
```

YAML wrapped in `---`. Indentation must be consistent. Case-sensitive.

## Legacy Directives (Deprecated from v10.5.0)

```
%%{init: {"theme": "dark", "fontFamily": "monospace"}}%%
```

`init` and `initialize` are interchangeable. Multiple directives merge.

## Top-Level Options

| Option | Values | Description |
|--------|--------|-------------|
| `theme` | `default`, `base`, `dark`, `forest`, `neutral` | Visual theme |
| `fontFamily` | any font name | Typography |
| `fontSize` | number (px) | Base font size |
| `logLevel` | 1-5 (debug to fatal) | Logging verbosity |
| `securityLevel` | `strict`, `loose`, `antiscript`, `sandbox` | Controls click events/HTML |
| `startOnLoad` | boolean | Auto-render on page load |

## Look and Layout

- `look: handDrawn` - Sketch-like appearance
- `look: classic` - Traditional Mermaid styling (default)
- `layout: dagre` - Default layout algorithm
- `layout: elk` - Advanced layout (better edge routing, complex diagrams)

## Comments

```
%% This is a comment
```

Must be on own line. Avoid curly braces `{}` in comments.

## Accessibility

```
accTitle: Diagram title for screen readers
accDescr: Single line description.
accDescr {
    Multi-line description.
}
```

Generates `<title>` and `<desc>` SVG elements with ARIA attributes.

## Text Formatting

- **Markdown**: `**bold**`, `*italic*` (in nodes using `"` quotes)
- **HTML**: `<br/>` for line breaks (when `htmlLabels: true`)
- **Unicode**: Supported in quoted strings
- **Entity codes**: `#35;` for `#`, `#59;` for `;`, `#colon;` for `:`

---

# Theming

## Built-in Themes

| Theme | Description |
|-------|-------------|
| `default` | Bright, colorful |
| `base` | Customizable via themeVariables |
| `dark` | Dark background |
| `forest` | Green tones |
| `neutral` | Black and white |

## Customizing with `base` Theme

Only `base` supports `themeVariables`:

```
---
config:
  theme: base
  themeVariables:
    primaryColor: '#4a90d9'
    primaryTextColor: '#ffffff'
    primaryBorderColor: '#2c5282'
    secondaryColor: '#48bb78'
    tertiaryColor: '#ed8936'
    lineColor: '#718096'
    fontFamily: 'Inter, sans-serif'
    fontSize: '14px'
    noteBkgColor: '#fefcbf'
    noteTextColor: '#744210'
    noteBorderColor: '#d69e2e'
---
```

## Color Derivation

Mermaid auto-derives related colors from primaries. Only hex colors supported (`#ff0000`, not `red`). Changing `primaryColor` adjusts `primaryBorderColor` and `primaryTextColor` if not explicitly set.

## Diagram-Specific Theme Variables

**Flowchart**: `nodeBorder`, `clusterBkg`, `clusterBorder`, `defaultLinkColor`, `titleColor`, `edgeLabelBackground`, `nodeTextColor`

**Sequence**: `actorBkg`, `actorBorder`, `actorTextColor`, `signalColor`, `labelBoxBkgColor`, `activationBorderColor`, `sequenceNumberColor`

**Pie**: `pie1`-`pie12`, `pieTitleTextSize`, `pieSectionTextSize`, `pieStrokeColor`, `pieOpacity`

**State**: `labelColor`, `altBackground`

**Class**: `classText`

**Journey**: `fillType0`-`fillType7`

**Gitgraph**: `git0`-`git7`, `gitBranchLabel0`-`gitBranchLabel7`, `commitLabelColor`, `commitLabelBackground`, `tagLabelColor`, `tagLabelBackground`, `tagLabelBorder`

**Timeline**: `cScale0`-`cScale11`, `cScaleLabel0`-`cScaleLabel11`

**Quadrant**: `quadrant1Fill`-`quadrant4Fill`, `quadrant1TextFill`-`quadrant4TextFill`, `quadrantPointFill`

---

# CSS Classes and Styling

## Defining Classes

```
classDef className property:value,property:value
```

## Common CSS Properties

| Property | Example | Description |
|----------|---------|-------------|
| `fill` | `#f9f` | Background |
| `stroke` | `#333` | Border color |
| `stroke-width` | `4px` | Border width |
| `stroke-dasharray` | `5 5` | Dashed border |
| `color` | `#000` | Text color |
| `font-size` | `14px` | Text size |
| `font-weight` | `bold` | Text weight |
| `font-style` | `italic` | Text style |
| `rx` | `10` | Border radius (x) |
| `ry` | `10` | Border radius (y) |
| `opacity` | `0.8` | Transparency |

## Applying Classes

```
class nodeA,nodeB className          %% explicit
nodeA:::className                    %% inline (at definition)
classDef default fill:#fff           %% default for all unclassed nodes
```

## Edge/Link Styling

```
linkStyle 0 stroke:#ff3,stroke-width:4px    %% by index (0-based)
linkStyle 0,1,2 stroke:#ff3                  %% multiple
linkStyle default stroke:#333                 %% all links
```

## Subgraph Styling

```
style subgraphId fill:#f0f0f0,stroke:#999
```

---

# Interactions and Events

## Flowchart Click Events

```
click nodeId href "https://example.com" _blank
click nodeId callback "Tooltip on hover"
click nodeId call myFunction()
```

## Gantt Click Events

```
click taskId href "https://example.com"
click taskId call myFunction()
```

## Class Diagram Interactions

```
click ClassName href "https://example.com"
click ClassName call myFunction()
```

## Sequence Diagram Actor Links

```
link Actor: Dashboard @ https://example.com/dashboard
links Actor: {"GitHub": "https://github.com", "Docs": "https://docs.example.com"}
```

## Requirements

- All click callbacks require `securityLevel: 'loose'`
- URL links work at any security level
- Tooltip text in double quotes after callback name
- Target window: `_self`, `_blank`, `_parent`, `_top`

---

# Common Pitfalls

## Reserved Words
- `end` in flowcharts: Capitalize (`End`, `END`) or quote `["end"]`
- `o`/`x` starting a node after `---`: Add space or capitalize

## Rendering Failures
- Typos break diagrams silently
- Missing spaces around operators
- Use Mermaid Live Editor (mermaid.live) for debugging

## Large Diagrams
- Break into multiple smaller diagrams
- Use `layout: elk` for complex edge crossings
- `displayMode: compact` for Gantt charts
- Subgraphs organize but add rendering complexity

## Security
- Click events/callbacks require `securityLevel: 'loose'`
- At `strict` level, click events fail silently
- `sandbox` mode uses iframes for isolation

## Text and Encoding
- Special characters in labels: Always quote
- Line breaks: `<br/>` in most contexts
- Markdown in nodes requires double-quote strings
- Entity codes: `#35;` = `#`, `#59;` = `;`, `#colon;` = `:`

## Config Gotchas
- Frontmatter YAML indentation must be consistent
- Theme variables only work with `base` theme
- `init` directives deprecated in v10.5.0+ (use frontmatter)
- Config is case-sensitive
