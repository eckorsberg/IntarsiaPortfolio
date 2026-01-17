Site Architecture Review
January 2026
(Supersedes site-review.txt – August 2025)

Overview
--------
This site is a handcrafted, static portfolio intended to showcase woodworking and laser
projects with minimal technical overhead. It prioritizes clarity, stability, and long-term
maintainability over framework adoption, automation, or aggressive abstraction.

The site has reached a mature, stable state. Recent changes have focused on reducing
duplication and improving structure without altering visual design or introducing new
dependencies.

This document reflects the current architecture and records intentional decisions so future
maintenance can proceed confidently without rediscovering prior reasoning.

---

Architecture Summary
--------------------

HTML
- Pages are hand-authored static HTML.
- No templating engine or CMS is used.
- Page structure favors readability and direct editability.
- Data-driven rendering is used selectively where repetition warranted it (animations gallery).

CSS
- `/style.css` contains site-wide base styles and is intentionally located at the repository root.
- Page- or feature-specific styles live in `/css/` (e.g., index.css, laser.css, animation-gallery.css).
- Embedded `<style>` blocks have been removed in favor of external CSS for readability and tooling.
- Naming conventions are consistent (kebab-case).
- No CSS framework or utility system is used by design.

JavaScript
- JavaScript is used sparingly.
- One-purpose scripts are favored over generalized libraries.
- A JSON + loader pattern is used selectively where it meaningfully reduces duplication
  (e.g., animation gallery).
- No build step, bundler, or transpiler is required.

Data
- JSON is used only where it improves maintainability (e.g., repeated gallery entries).
- Schema flexibility is handled in code, not enforced rigidly.

---

Design Principles (Intentional Decisions)
-----------------------------------------

The following are conscious design choices, not omissions:

- No frameworks (React, Vue, etc.)
- No build pipeline
- No CMS
- No global design system
- No aggressive abstraction
- No refactoring for symmetry alone

Cleanup and refactoring are incremental, evidence-driven, and only performed when they
reduce real maintenance cost or error risk.

Aesthetic consistency is valued, but not at the expense of stability or clarity.

---

Changes Since August 2025
-------------------------

The following material improvements have been made since the prior review:

- Introduced data-driven rendering for the animation gallery using JSON + a small loader script.
- Removed embedded CSS from HTML pages and externalized it into page-scoped stylesheets.
- Eliminated unused CSS files (e.g., card.css, map.css) after confirming they were not referenced.
- Clarified CSS organization into base vs page-specific roles.
- Avoided unnecessary refactors (e.g., relocating style.css) after evaluating cost vs benefit.
- Improved internal consistency while preserving the original visual design.

These changes reduce duplication, improve editor ergonomics, and lower the risk of
future inconsistencies without increasing complexity.

---

Explicitly Deferred or Declined Options
---------------------------------------

The following are intentionally not implemented:

- Full CSS variable conversion
- BEM or utility-first CSS methodologies
- CSS or JS minification
- Component frameworks
- Automated build or deployment tooling
- CMS integration
- Overgeneralized JavaScript utilities

These options were evaluated and declined as unnecessary for the site’s goals.

---

Verdict
-------

The site is considered functionally complete and architecturally stable.

Future changes should be driven by new content or clear functional needs, not by a desire
to further “clean up” existing structure.

Unless project goals change, the site is effectively in maintenance mode.

---

Historical Note
---------------
This document supersedes the August 2025 site review, which reflected an earlier phase of
active structural evolution. That document is retained for historical context but should not
be treated as current guidance.
