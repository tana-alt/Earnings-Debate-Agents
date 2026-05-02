---
name: design-system-audit
description: "Use when UI changes may violate the existing design system, spacing, typography, colors, component reuse, responsive behavior, or accessibility conventions."
---


## Purpose

Keep UI changes consistent without forcing a large redesign.

## Use when

- Adding or modifying visual components.
- Fixing UI polish, layout, or responsive behavior.
- Reviewing PRs that add new colors, spacing, typography, or component variants.

## Success conditions

- Existing components and tokens are reused when available.
- Spacing, typography, color, and layout match repo conventions.
- Responsive behavior is checked for affected surfaces.
- Accessibility basics are preserved.
- Issues are reported with specific file or route references.

## Constraints

- Do not invent a new design system.
- Do not add decorative complexity or generic AI-looking styling.
- Do not perform broad redesign during a local fix.
- Do not treat minor preference differences as blockers.

## Output

- Consistency verdict.
- Specific deviations.
- Minimal fix recommendation.
