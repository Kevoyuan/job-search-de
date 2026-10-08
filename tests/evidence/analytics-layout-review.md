# Analytics layout review — 2026-10-06

PASS. Frontend Design Premium and its installed upstream guidance were used for
the product layout refinement. Lieflat F5/L4 encodings remain the chart owners;
Better Design was not used, following the user's explicit instruction.

The public preview serves the exact generated fictional source. SHA-256, measured
SVG scale and geometry are recorded in the adjacent JSON; six screenshots
are retained as adjacent image files. Screenshots at 390, 1440 and 1728 were inspected: labels are
horizontal, SVG text retains physical font sizes, controls reflow, chart regions
scroll locally, and no horizontal document overflow occurs. The small-sample tick
pitch is capped to prevent widely separated unit marks. Phone cross charts expose
an overflow-specific horizontal browsing hint.

Real local data were independently checked without publishing screenshots or
candidate information. At 1440, all eight distribution rows occupy a 1120×396px
SVG; the default six-by-six cross view occupies a 1120×384px SVG. At 390, ranking
SVG width is 326px and matrix width is preserved inside its own scroll region.

Validation completed:

- 4 analytics and 6 existing workbench unit tests passed.
- Analytics and existing workbench browser regression checks passed.
- Configuration editor preservation/draft/validation checks passed.
- Layout checks passed for 3 locales × 5 themes × 4 widths, all five rankings and
  both cross views; SVG label bounds, keyboard scrolling and 200% reflow passed.
- Strict source-template audit: zero findings (`premium-audit.json`). Historical
  documentation demos are outside this product-source audit scope.
- DESIGN.md lint: zero errors; one pre-existing prose-only/YAML warning. The
  existing document format was preserved and the scoped analytics rules appended.
