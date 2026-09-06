# Design System: Germany Job Hunt Workbench (德国求职工作台)

> Calibrated via **Stitch Design Taste** (`labs.google/stitch`) & **GStack Design Methodology**.
> Serves as the authoritative single source of truth for semantic design tokens, component behaviors, anti-slop constraints, and theme calibrations across the workbench ecosystem.

---

## 1. Visual Theme & Atmosphere

- **Atmosphere & Mood**: A restrained, razor-sharp career cockpit engineered for high-velocity software engineers. The aesthetic bridges the tactile precision of a modern developer IDE (Linear, Raycast) with the warmth of a curated editorial studio (Notion).
- **Taste Spectrum Calibration**:
  - **Density**: `Cockpit Dense` (**8/10**) — Maximum informational throughput without perceptual fatigue. Prioritizes tabular scans, sticky navigational chrome, high-density monospace badges, and dense keyboard shortcuts.
  - **Variance**: `Offset Asymmetric` (**6/10**) — Balanced structural asymmetry. Left-weighted data hierarchy, responsive multi-lane kanban, and side-sheet drawer overlays.
  - **Motion**: `Fluid Spring CSS` (**6/10**) — Tactile, hardware-accelerated micro-interactions. Weighty spring-physics transitions (`cubic-bezier(0.16, 1, 0.3, 1)`), physical press states (`translateY(1px)`), and perpetual micro-interaction pulse loops.

---

## 2. Color Palette & Roles

The workbench supports 4 curated palettes. Every palette enforces a single primary chromatic accent with saturation strictly controlled below 80%, absolute neutral bases, zero neon glow artifacts, and strict WCAG AA contrast compliance. Pure black (`#000000`) is strictly banned across all themes.

### 2.1 Editorial Craft (Default — Warm Paper & Ink Workspace)
- **Canvas White** (`#ffffff`) — Primary card and table container surface
- **Warm Paper Canvas** (`#f7f6f5`) — Page backdrop and drawer body background
- **Charcoal Ink** (`#37352f`) — Primary text; warm signature charcoal (Zinc-950 depth)
- **Muted Slate** (`#787671`) — Secondary labels, timestamps, and table headers
- **Whisper Border** (`#e5e3df`) — 1px hairline dividers and structural borders
- **Strong Hairline** (`#c8c4be`) — Focused card edges and interactive borders
- **Editorial Purple Accent** (`#5645d4`) — Primary chromatic accent for CTAs, active indicators, and focus rings (Saturation: 62%)
- **Verified Fresh Green** (`#1aae39`, tint `#d9f3e1`) — High-freshness semantic indicator
- **Active Warning Amber** (`#dd5b00`, tint `#ffe8d4`) — Medium-fit and recent active semantic indicator

### 2.2 Dark Velocity (Dark — High-Contrast Cybernetic Engine)
- **Void Canvas** (`#010102`) — Deepest dark backdrop (never pure `#000000`)
- **Surface Elevation** (`#0f1011`) — Card bodies, table rows, and control bars
- **Surface Lift** (`#141516`) — Hover state and modal surface
- **High-Contrast Ink** (`#f7f8f8`) — Primary high-contrast light text
- **Muted Steel** (`#8a8f98`) — Secondary text, metadata, and column headers
- **Subtle Charcoal** (`#62666d`) — Faint shortcuts and placeholder text
- **Hairline Rule** (`#23252a`) — 1px card and divider borders; strong variant `#34343a`
- **Lavender-Blue Accent** (`#5e6ad2`) — Primary chromatic accent for active pills and focus rings (Saturation: 55%)
- **Semantic Green** (`#27a644`, bg `rgba(39, 166, 68, 0.16)`) — Verified job status indicator
- **Semantic Amber** (`#f59e0b`, bg `rgba(245, 158, 11, 0.16)`) — Active job status indicator

### 2.3 Industrial Precision (Functional Industrial Minimalism)
- **Technical Composite Resin** (`#ece9e2`) — Warm matte composite resin canvas
- **Anodized Aluminum Surface** (`#f7f6f3`) — Matte faceplate and container surface
- **Recessed Bay** (`#e2ded6`) — Sunken channel and drawer backdrop
- **Deep Carbon Ink** (`#191a1b`) — High-contrast precision dark ink
- **Hairline Seam** (`#c8c4bc`) — Crisp CNC precision dividers
- **Signal Amber Accent** (`#e8590c`) — Tuning dial and action key accent (Saturation: 75%)
- **Tactile Keycap Shadow** (`0 1px 2px rgba(0, 0, 0, 0.05), inset 0 1px 0 rgba(255, 255, 255, 0.85)`) — Mechanical tactile convex key relief

### 2.4 Spatial Quartz (Translucent Quartz Glassmorphism)
- **Ambient Quartz Canvas** (`#eef2f7`) — Fixed radial ambient light canvas
- **Frosted Quartz Surface** (`rgba(255, 255, 255, 0.72)`) — Multi-layer frosted glass with `backdrop-filter: blur(24px) saturate(180%)`
- **High-Contrast Charcoal** (`#1d1d1f`) — Ultra-crisp modern ink
- **Electric Action Blue** (`#0071e3`) — System accent with soft diffuse lighting
- **Quartz Specular Border** (`rgba(255, 255, 255, 0.85)`) — Crystal inner reflection (`inset 0 1px 0 rgba(255, 255, 255, 0.95)`)

---

## 3. Typography Rules

- **Display & Headlines**:
  - **Stack**: `Geist, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif`
  - **Scale**: `16px - 18px`, `font-weight: 700`, `letter-spacing: -0.015em`.
  - **Hierarchy**: Established strictly through font weight and subtle tonal value, never through screaming oversized headlines.
- **Body Text**:
  - **Stack**: Same as Display.
  - **Scale**: `13px - 14px`, `line-height: 1.5`, `font-weight: 400 - 500`.
  - **Measure**: Max 65 characters per line (`max-w-[65ch]`) for reading comfort.
- **Monospace & High-Density Tabular Data**:
  - **Stack**: `Geist Mono, JetBrains Mono, ui-monospace, "SF Mono", Menlo, Monaco, Consolas, monospace`
  - **Scale**: `11px - 12px`, `font-weight: 500 - 600`.
  - **Mandatory**: `font-variant-numeric: tabular-nums` across all dates, match scores, job IDs, and metrics.
- **Typography Bans**:
  - `Inter` is BANNED in favor of `Geist` to prevent generic AI interface monotony.
  - Generic serif fonts (`Times New Roman`, `Georgia`, `Garamond`) are strictly BANNED in dashboard software UIs.

---

## 4. Component Stylings & Interaction Behaviors

- **Buttons (`.btn`)**:
  - Flat, tactile push feedback. No outer glow or ungrounded drop shadows.
  - Geometry: Strict `border-radius: var(--radius-md)` (8px in Notion/Linear, 0px in Bauhaus, 12px in Bento).
  - Hover: Subtle background shift (`transform: translateY(-1px)`).
  - Active: Physical tactile depression (`transform: translateY(1px)`).
  - Focus: Dedicated `:focus-visible` ring (`2px solid var(--border-focus)`, `outline-offset: 2px`).
- **Cards & Rows (`.kanban-card`, `.job-row`)**:
  - Elevation communicates semantic hierarchy. Tinted whisper shadows matching background tone.
  - Micro-motion: `will-change: transform; transition: transform 0.15s cubic-bezier(0.16, 1, 0.3, 1), box-shadow 0.15s;`.
- **Inputs & Filters (`.search-input`, `.select-dropdown`)**:
  - Integrated SVG search icon, keyboard shortcut hint (<kbd>/</kbd>), and tactile clear button.
  - Label strictly above or contextual placeholder; zero floating label animations.
  - Focus state: Crisp 3px colored focus ring (`box-shadow: 0 0 0 3px var(--primary-bg)`).
- **Indicators & Micro-Interactions**:
  - **Perpetual Breathing Pulse**: High-freshness jobs feature `.status-dot-pulse` with an infinite keyframe loop (`pulse-ring 2.4s cubic-bezier(0.16, 1, 0.3, 1) infinite`).
  - **Dirty Status Dot**: Visual feedback on candidate config modifications.
- **Iconography (Open Design Standard)**:
  - Strict 14–16px geometric SVG stroke icons (`stroke-width: 1.75`, `stroke: currentColor`, `stroke-linecap: round`). Zero external CDN runtime dependencies.
- **Empty States**:
  - Composed, illustrated SVG composition paired with an explicit action button ("重置所有筛选条件"), never a broken string.

---

## 5. Layout Principles

- **Grid-First Cockpit Architecture**:
  - Max container width constrained to `1600px` centered with fluid gutters.
  - Multi-lane Kanban: 4-column desktop grid (`repeat(4, 1fr)`) -> 2-column tablet (`repeat(2, 1fr)`) -> single horizontal touch-snapping carousel (<768px).
- **No Overlapping Elements**:
  - Every element occupies its own clean spatial zone. No absolute-positioned content stacking or ungrounded floating chips.
- **Mobile-First Responsiveness (<768px)**:
  - Kanban transforms into a smooth horizontal touch-scroller (`scroll-snap-type: x mandatory`).
  - Control bar & search collapse vertically to full width.
  - Minimum touch target for all interactive elements: `44px` or accessible padding.
  - Zero horizontal page overflow (`overflow-x: hidden; max-width: 100vw;`).

---

## 6. Motion Philosophy & Spring Dynamics

- **Spring Physics Engine**: `cubic-bezier(0.16, 1, 0.3, 1)` provides weighty, organic acceleration without bouncy oscillations (`stiffness: 100, damping: 20` equivalent).
- **Hardware Acceleration**: Transitions strictly restricted to `transform` and `opacity`. Never animate `width`, `height`, `top`, `left`, or `margin`.
- **Perpetual Micro-Interactions**: Active status indicators feature infinite breathing micro-loops to signal live intelligence.
- **Performance Budget**: Zero external runtime JavaScript libraries; zero heavy CSS frameworks. 100% pure vanilla CSS variables and client-side ECMAScript.

---

## 7. Anti-Patterns (Banned AI Clichés)

- 🚫 **Banned: Cartoon Emoji Decoration** — Zero consumer emojis (🎯, 🚀, 💬, 📝, ⚙️, 🇩🇪, 🎨) in interface labels, buttons, or badge elements. All icons must be clean Open Design SVG glyphs.
- 🚫 **Banned: AI Neon Purple/Cyan Glows** — No uncalibrated gradients from `#6366f1` to `#ec4899`, no radial neon backdrops.
- 🚫 **Banned: Pure Black (`#000000`)** — Void canvas must use off-black (`#090a0c` or `#010102`), primary text must use charcoal ink (`#37352f`).
- 🚫 **Banned: `Inter` Font Monotony** — Use `Geist` and `Geist Mono` for distinctive, modern software character.
- 🚫 **Banned: Generic Serifs** — No `Times New Roman`, `Georgia`, or `Garamond` in dashboard interfaces.
- 🚫 **Banned: Unchecked Outline Stripping** — Never declare `outline: none` without providing an explicit `:focus-visible` replacement.
- 🚫 **Banned: Uniform Bubbly Border-Radius** — No applying the same 16px+ border radius to every button, tag, input, and card.
- 🚫 **Banned: Centered Everything** — No centering tabular data, job titles, or column layouts. Alignment must be functional.
- 🚫 **Banned: AI Marketing Copy Slop** — No empty buzzwords like "Unlock Next-Gen Potential", "Seamless Workflow Synergy", "Elevate Your Career". Keep all copy factual and concrete.
- 🚫 **Banned: Filler UI Text** — No "Scroll to explore", "Swipe down", scroll arrows, or bouncing chevrons.
- 🚫 **Banned: Layout-Shifting Sprites** — All icons and spinners must have fixed structural dimensions.
- 🚫 **Banned: Custom Mouse Cursors** — Native cursor interaction only.
- 🚫 **Banned: Overlapping Content Stacks** — Clean spatial zones only.
- 🚫 **Banned: Oversaturated Accents** — Color saturation strictly below 80%.
- 🚫 **Banned: Fake Precision Numbers** — No artificial `99.99%` claims. Factual score metrics only.
