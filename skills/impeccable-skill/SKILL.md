---
name: impeccable-skill
description: Deterministic UI/UX design validation skill that enforces layout, spacing, accessibility, and anti-pattern checklists to eliminate generic visual slop.
triggers:
  - "impeccable"
  - "design review"
  - "ui audit"
  - "ux audit"
  - "anti-pattern check"
od:
  mode: design-system
  category: design-systems
  upstream: "https://github.com/Leonxlnx/taste-skill"
---

# Impeccable Skill — Deterministic Design Audit & Review

> An advanced UI/UX validation skill designed to perform strict, deterministic structural and visual audits on web layouts.

---

## 🔍 Validation Philosophy

* **Objective Aesthetics**: Beauty can be measured. Alignment, proportion, and contrast are treated as strict mathematical formulas.
* **Anti-Slop Detection**: Scans for and eliminates:
  * Floating decorative gradients with no structural anchor.
  * Over-rounded card borders (>12px) that ruin professional visual density.
  * Inconsistent margins across layout sections.
  * Purple/violet accents (strictly forbidden by default).
* **Base Tokens**: Warm parchment canvas (`#fbfaf5`), deep ink-blue text (`#0d1b2a`), forest green highlights (`#2d4a3e`).

---

## 📐 Deterministic Audit Checklist

| Phase | Metric | Acceptance Standard |
|---|---|---|
| **Alignment** | Grid Flow | Enforce exact alignment on an 8px grid. Zero fractional pixel values. |
| **Hierarchy** | Scale Scale | Headers must double body sizes (e.g., h1: 32px, h2: 24px, body: 16px). |
| **Breathing** | Section Gaps | Layout sections must have minimum 64px vertical margins. |
| **Accessibility** | Contrast | Minimum 4.5:1 for body and 3:1 for large headers (WCAG 2.2 AA). |

---

## 🧱 Visual & Interactive Component Gates

### 1. Interactive Tap Targets
* Buttons and links must provide a minimum tap target of **44px × 44px**.
* Standardize inputs to match primary button heights perfectly to maintain horizontal alignment rhythm.

### 2. Active Focus States
* Focus indicators must be visible, high-contrast, and provide a minimum 2px offset (`outline-offset: 2px`).
* Hover transitions must feel crisp and fast (`transition: 150ms ease-out`).

---

## 🏁 Post-Implementation Quality Verification
1. Run `scripts/ux_audit.py` to evaluate code against psychological laws (Miller's Law, Fitts' Law).
2. Confirm contrast ratios are mathematically compliant.
3. Test layout fluidity under variable responsive widths (320px, 768px, 1200px) and check for overflow leaks.
