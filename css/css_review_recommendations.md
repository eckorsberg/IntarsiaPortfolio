# CSS/HTML Maintenance Recommendations

**Project:** Korsberg Crafts Portfolio  
**Review Date:** January 2026  
**Context:** Mature, stable site in maintenance mode.
**Overall Grade:** A-

---

## Executive Summary

Your site architecture is **sound and appropriate for its goals**. After reviewing your site-review.md document, it's clear you've made intentional decisions to keep the codebase simple, stable, and maintainable without frameworks or aggressive abstraction.

This review respects those principles and identifies only **evidence-based issues** that represent actual maintenance risks or confusion points—not stylistic preferences.

**Total Issues Found:** 3 minor items  
**Estimated Fix Time:** 15-30 minutes  
**Priority Level:** Low (address when convenient)

---

## Your Architecture Strengths ✅

Based on your site-review.md, you've successfully achieved:

- ✅ Static HTML with no build pipeline
- ✅ Minimal, purpose-driven JavaScript
- ✅ Clear CSS organization (base vs page-specific)
- ✅ Consistent kebab-case naming throughout
- ✅ Data-driven rendering only where it reduces duplication
- ✅ External stylesheets (no embedded `<style>` blocks)
- ✅ No unnecessary dependencies or frameworks

**This is a well-executed static site.** The following items are genuine maintenance concerns, not refactoring suggestions.

---

## Issues Requiring Action

### Issue #1: Orphaned CSS Classes (Priority: Low)

**Location:** `/style.css` (bottom of file)

**Problem:** Two classes appear to be unused:

```css
.gallery-item {
    flex: 0 0 200px;
    margin: 15px;
    text-align: center;
}

.gallery-container {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
}
```

These don't match your current gallery architecture, which uses CSS Grid via the `.gallery` class.

**Evidence Needed:**
1. Search all HTML files for `gallery-item` and `gallery-container`
2. Check if these are legacy classes from a previous layout
3. Determine if they're intentional future hooks

**Recommended Actions:**

**If unused:**
```css
/* Delete these lines from style.css */
```

**If legacy/future hooks:**
```css
/* Legacy layout classes - retained for potential future use */
.gallery-item { /* ... */ }
.gallery-container { /* ... */ }
```

**If actively used somewhere:**
- Document where/why in a comment
- Consider renaming to avoid confusion with `.gallery`

---

### Issue #2: Conflicting `.back` Styles (Priority: Low)

**Locations:** 
- `/style.css`
- `/css/animation-gallery.css`

**Problem:** The `.back` class has different definitions in two files:

```css
/* style.css */
.back {
  margin: 1em 0;
  font-size: 0.9rem;
  text-align: left;
}

/* animation-gallery.css */
.back {
  display: inline-block;
  margin-top: .75rem;
}
```

**Impact:** Animation gallery back link will have merged styles, potentially causing unexpected spacing.

**Recommended Actions:**

**Option A - Namespace the override:**
```css
/* animation-gallery.css */
.back-anim {
  display: inline-block;
  margin-top: .75rem;
}
```

**Option B - Document the override:**
```css
/* animation-gallery.css */
/* Override base .back styles for tighter spacing in animation header */
.back {
  display: inline-block;
  margin-top: .75rem;
}
```

**Option C - Verify if override is necessary:**
- Test removing the animation-gallery.css override
- If base styles work fine, delete the duplicate definition

---

### Issue #3: Undocumented CSS Variables (Priority: Low)

**Location:** `/style.css` `:root` block

**Problem:** CSS variables are defined but never used:

```css
:root {
  --bg-warm: #f6f4f1;
  --text-primary: #222;
  /* ... etc ... */
}
```

Per your site-review.md, "Full CSS variable conversion" is explicitly deferred.

**Impact:** No functional issue, but creates ambiguity about their purpose.

**Recommended Action:** Document the decision

```css
/* 
  CSS Variables - Future Hooks
  ----------------------------
  These variables are available for incremental use but are not
  required for current functionality. Per site-review.md (Jan 2026),
  full CSS variable conversion is explicitly deferred.
  
  Use these variables when:
  - Adding new styles
  - Editing existing styles that would benefit from consistency
  
  Do NOT refactor existing working code to use these variables.
*/
:root {
  /* Colors */
  --bg-warm: #f6f4f1;
  --text-primary: #222;
  /* ... */
}
```

---

## Non-Issues (Clarifications)

These items from a typical code review are **NOT issues** in your context:

### ✅ Mixing `em`, `rem`, and `px`
**Status:** Acceptable variance in a mature codebase  
**Reasoning:** Consistent within each file; no functional problems; refactoring would violate your "no refactoring for symmetry alone" principle

### ✅ Multiple button/link styles
**Status:** Appropriate for different contexts  
**Found:**
- `.btn` - primary action buttons
- `.button-link` - laser portfolio links
- `.quick-pill` - navigation pills
- `.back` / `.back-link` - navigation links

**Reasoning:** Each serves a distinct purpose; consolidation would be refactoring for symmetry without evidence of confusion or maintenance burden

### ✅ No utility classes or BEM
**Status:** Intentional architectural decision  
**Reasoning:** Per site-review.md, BEM is explicitly declined; current approach is maintainable

### ✅ Lack of CSS minification
**Status:** Intentional decision  
**Reasoning:** Site is static and small; readability prioritized over optimization

---

## Action Checklist

When you have 15-30 minutes:

- [ ] **Search for orphaned classes**
  ```bash
  # In your project directory:
  grep -r "gallery-item" . --include="*.html"
  grep -r "gallery-container" . --include="*.html"
  ```

- [ ] **Delete or document orphaned CSS**
  - If no results: delete `.gallery-item` and `.gallery-container` from style.css
  - If found: document their purpose

- [ ] **Resolve `.back` conflict**
  - Choose Option A, B, or C from Issue #2
  - Test animation gallery page after change

- [ ] **Document CSS variables**
  - Add explanatory comment above `:root` block
  - Clarifies they're future hooks, not required features

- [ ] **Update site-review.md**
  - Add line: "Addressed orphaned CSS and conflicting selectors (Jan 2026)"

---

## Testing After Changes

Minimal testing required since changes are documentation or deletion:

1. **Load all pages** - verify no broken styles
2. **Check animation gallery** - verify back link spacing acceptable
3. **Visual regression** - nothing should look different

**Expected result:** Zero visual changes, improved code clarity.

---

## Long-Term Guidance

### When to Use CSS Variables

Since you've created them but deferred conversion, here's when to use them:

**✅ Use variables for:**
- New styles you're adding
- Existing styles you're already modifying
- Colors that appear in multiple new components

**❌ Don't use variables for:**
- Working code you're not otherwise touching
- "Cleanup" refactoring sessions
- Achieving visual consistency (it already exists)

**Example:**
```css
/* If you're adding a new card style */
.new-feature-card {
  background: var(--bg-warm);        /* ✅ Use variable */
  border-radius: var(--radius-md);   /* ✅ Use variable */
}

/* Don't refactor existing working code */
.gallery-img {
  border-radius: 8px;  /* ✅ Leave as-is */
}
```

### When to Consolidate Styles

Only consolidate when you have **evidence** of:
- Confusion about which class to use
- Actual duplicate code causing maintenance burden
- Visual inconsistencies you want to fix

**Not valid reasons:**
- "It would be cleaner"
- "Best practices say so"
- "Other sites do it this way"

### File Organization Principles

Your current structure is sound:
```
/style.css              ← Site-wide base styles
/css/index.css          ← Index page specifics
/css/laser.css          ← Laser page specifics
/css/animation-gallery.css ← Animation page specifics
```

**Maintain this pattern** when adding new pages:
1. Put shared styles in `/style.css`
2. Put page-specific styles in `/css/[page-name].css`
3. Link both in the page HTML

---

## Architectural Affirmations

Based on your site-review.md principles:

### ✅ You're doing well by:
- Keeping HTML hand-editable
- Using JavaScript sparingly and purposefully
- Avoiding framework adoption
- Maintaining visual consistency without rigid design systems
- Making incremental, evidence-driven improvements
- Prioritizing stability over trends

### ✅ Continue to:
- Resist refactoring working code
- Add features only when needed for content
- Keep the build pipeline nonexistent
- Value clarity over abstraction
- Document architectural decisions (like you did in site-review.md)

### ❌ Avoid:
- Converting to a framework "because everyone uses them"
- Adding build tools for minification
- Refactoring for symmetry or consistency alone
- Implementing design systems
- Over-generalizing one-off solutions

---

## Conclusion

Your codebase is in excellent shape for a static portfolio site. The three issues identified are minor and can be addressed in under 30 minutes.

**Key Takeaway:** Your architecture is appropriate for your goals. The temptation to "modernize" or "clean up" should be resisted unless driven by actual content needs or measurable maintenance burden.

**Recommendation:** Address the three minor issues when convenient, then continue in maintenance mode as planned. Future changes should be driven by new content (additional woodworking projects, new galleries) rather than structural improvements.

---

## Questions for Future Consideration

Only if/when these become actual problems:

1. **If the site grows significantly** (100+ projects), would JSON + loaders help other galleries?
2. **If multiple people contribute**, would a style guide document be useful?
3. **If load times become an issue**, would image optimization be worth pursuing?

Otherwise, maintain current architecture. It's working well.

---

**Review Status:** Complete  
**Next Review:** Only if site goals change or functional issues arise  
**Confidence Level:** High - architecture is mature and well-documented
