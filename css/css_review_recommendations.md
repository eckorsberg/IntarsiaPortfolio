# CSS/HTML Code Review & Recommendations

**Project:** Korsberg Crafts Portfolio  
**Review Date:** January 2026  
**Overall Grade:** B-

---

## Executive Summary

Your code is **functional and shows good organizational thinking**, but lacks consistency in execution. The structure (separating page-specific CSS from shared styles) is sound, but implementation needs standardization.

**Key Issues:**
- Mixing naming conventions
- CSS variables defined but not used
- Duplicate/conflicting styles across files
- Too many variations of similar components

**Good News:** These are all easy fixes that won't require HTML restructuring—just a CSS cleanup pass.

---

## Strengths 💪

### 1. Good Separation of Concerns
- Page-specific styles properly separated (`index.css`, `laser.css`, `animation-gallery.css`)
- Shared styles centralized in `style.css`

### 2. Semantic HTML
- Proper use of `<header>`, `<main>`, `<footer>` elements
- Meaningful class names

### 3. Mobile-First Thinking
- Responsive design with media queries
- Touch-friendly affordances (zoom indicators)

### 4. CSS Variables Defined
- Variables declared in `style.css` `:root`
- Shows forward-thinking planning

---

## Issues & Inconsistencies 🔍

### 1. Class Naming Conventions

**Problem:** Mixing different naming styles

```css
/* Found in your code: */
.gallery-link        /* kebab-case ✅ */
.gallery_caption     /* snake_case ❌ */
.gallery-caption     /* kebab-case ✅ */
.quick-links         /* kebab-case ✅ */
.quickLinks          /* camelCase ❌ */
```

**Recommendation:** Standardize on **kebab-case** throughout (CSS industry standard)

---

### 2. Duplicate/Conflicting Styles

**Problem:** Same elements styled differently

```css
/* In style.css */
.gallery-caption {
  margin-top: 0.5rem;
  text-align: center;
}

/* Also exists */
.gallery-title {
  font-size: 1.1em;
}
```

**Question:** Are these the same element? If so, consolidate.

**Also found:**
```css
/* style.css */
.back { margin: 1em 0; }

/* animation-gallery.css */
.back { margin-top: .75rem; }
```

**Recommendation:** Choose one definition per component.

---

### 3. Redundant Container Classes

**Problem:** Orphaned/unused styles at bottom of `style.css`

```css
.gallery-item {
  flex: 0 0 200px;
  margin: 15px;
}

.gallery-container {
  display: flex;
  flex-wrap: wrap;
}
```

But `.gallery` already uses CSS Grid layout.

**Recommendation:** Remove unused classes or clarify their purpose.

---

### 4. Inconsistent Spacing Units

**Problem:** Mixing `em`, `rem`, and `px` without pattern

```css
margin: 1em 0;        /* em */
padding: 1rem;        /* rem */
gap: 15px;            /* px */
border-radius: 8px;   /* px */
```

**Recommendation:**
- **`rem`** for most spacing (consistent, accessible)
- **`em`** for component-relative sizing (buttons, typography)
- **`px`** only for borders, shadows, and precise 1-2px adjustments

**Example refactor:**
```css
/* Before */
margin: 1em 0;
padding: 15px;

/* After */
margin: var(--spacing-md) 0;
padding: var(--spacing-md);
```

---

### 5. CSS Variables Not Implemented

**Problem:** Variables defined but hardcoded values still used everywhere

```css
/* Defined in :root */
--spacing-md: 1rem;
--radius-md: 12px;
--shadow-md: 0 4px 10px rgba(0,0,0,0.1);

/* But still using hardcoded: */
border-radius: 12px;
margin: 1rem;
box-shadow: 0 4px 10px rgba(0,0,0,0.1);
```

**Recommendation:** Replace all hardcoded values

```css
/* After */
border-radius: var(--radius-md);
margin: var(--spacing-md);
box-shadow: var(--shadow-md);
```

---

### 6. Conflicting Link/Button Styles

**Problem:** Four different button styles for similar purposes

```html
<a href="about.html" class="btn">Learn More</a>
<a href="index.html" class="back-link">Return</a>
<a class="button-link" href="...">Laser</a>
<a class="quick-pill" href="...">Animations</a>
```

**Recommendation:** Consolidate to 2-3 button types maximum

```css
/* Proposed structure */
.btn              /* Primary action button */
.btn-secondary    /* Secondary action */
.btn-pill         /* Pill-shaped variant */
```

---

### 7. Selector Specificity Issues

**Problem:** Overly specific selectors make maintenance harder

```css
/* Too specific */
.image-container a::after {
  content: "🔍";
  /* ... */
}

.gallery-link::after {
  content: "🔍";
  /* ... */
}
```

**Recommendation:** Create reusable utility class

```css
.zoom-indicator::after {
  content: "🔍";
  position: absolute;
  right: 10px;
  bottom: 10px;
  font-size: 22px;
  background: rgba(255, 255, 255, 0.85);
  border-radius: 999px;
  padding: 6px 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.15);
}

/* Usage */
.image-container a,
.gallery-link {
  position: relative;
}
```

---

### 8. Magic Numbers

**Problem:** Unexplained hardcoded values

```css
bottom: 32px;         /* Why 32? */
font-size: 22px;      /* Why 22? */
max-width: 600px;     /* Why 600? */
```

**Recommendation:** Use CSS variables with meaningful names

```css
:root {
  --zoom-icon-size: 22px;
  --zoom-icon-offset: 10px;
  --gallery-caption-height: 32px;
  --content-max-width: 600px;
}
```

---

## Action Plan 📋

### Priority 1: Immediate Fixes (1-2 hours)

1. **Standardize class names to kebab-case**
   - Search and replace: `gallery_caption` → `gallery-caption`
   - Check all HTML files for consistency

2. **Remove orphaned styles**
   - Delete `.gallery-item` and `.gallery-container` if unused
   - Verify no HTML references exist

3. **Consolidate duplicate classes**
   - Merge `.back` and `.back-link` → choose one
   - Merge button variants → max 3 types

### Priority 2: Variable Implementation (2-3 hours)

4. **Replace hardcoded spacing**
   ```css
   /* Find & replace pattern */
   margin: 1rem     → margin: var(--spacing-md)
   gap: 1.5rem      → gap: var(--spacing-lg)
   padding: 0.5rem  → padding: var(--spacing-sm)
   ```

5. **Replace hardcoded border-radius**
   ```css
   border-radius: 8px   → var(--radius-sm)
   border-radius: 12px  → var(--radius-md)
   border-radius: 14px  → var(--radius-lg)
   border-radius: 999px → var(--radius-pill)
   ```

6. **Replace hardcoded shadows**
   ```css
   box-shadow: 0 2px 6px...  → var(--shadow-sm)
   box-shadow: 0 4px 10px... → var(--shadow-md)
   ```

### Priority 3: Structural Improvements (3-4 hours)

7. **Create utility classes for common patterns**
   ```css
   .zoom-indicator { /* Reusable zoom icon */ }
   .card { /* Reusable card component */ }
   .btn { /* Primary button */ }
   .btn-secondary { /* Secondary button */ }
   ```

8. **Group related styles in style.css**
   ```css
   /* === Typography === */
   /* === Layout === */
   /* === Gallery Components === */
   /* === Navigation === */
   /* === Buttons & Links === */
   /* === Utilities === */
   ```

9. **Consider BEM methodology for complex components**
   ```css
   /* Block */
   .gallery { }
   
   /* Elements */
   .gallery__item { }
   .gallery__caption { }
   .gallery__image { }
   
   /* Modifiers */
   .gallery__item--featured { }
   ```

---

## Code Examples

### Before & After: CSS Variables

**Before (style.css):**
```css
.card {
  border-radius: 14px;
  padding: 1rem;
  margin: 1.5rem 0;
  box-shadow: 0 4px 10px rgba(0,0,0,0.1);
}

.btn {
  padding: 0.45rem 0.8rem;
  border-radius: 999px;
}
```

**After:**
```css
.card {
  border-radius: var(--radius-lg);
  padding: var(--spacing-md);
  margin: var(--spacing-lg) 0;
  box-shadow: var(--shadow-md);
}

.btn {
  padding: var(--spacing-sm) var(--spacing-md);
  border-radius: var(--radius-pill);
}
```

### Before & After: Button Consolidation

**Before (scattered across files):**
```css
.btn { /* ... */ }
.button-link { /* ... */ }
.quick-pill { /* ... */ }
.back-link { /* ... */ }
```

**After (organized in style.css):**
```css
/* === Buttons & Links === */

/* Base button styles */
.btn {
  display: inline-block;
  padding: var(--spacing-sm) var(--spacing-md);
  border-radius: var(--radius-md);
  text-decoration: none;
  font-weight: 600;
  transition: all 0.2s ease;
}

/* Primary action button */
.btn-primary {
  background: var(--link-color);
  color: white;
  border: 1px solid var(--link-color);
}

/* Pill variant */
.btn-pill {
  border-radius: var(--radius-pill);
  background: #fff;
  border: 1px solid var(--border-medium);
  box-shadow: var(--shadow-sm);
}

/* Text link button */
.btn-text {
  background: transparent;
  color: var(--link-color);
  padding: 0;
}

.btn-text:hover {
  text-decoration: underline;
}
```

---

## Testing Checklist

After making changes, verify:

- [ ] All pages load without broken styles
- [ ] Mobile responsive design still works (< 768px)
- [ ] Dark mode styles still apply correctly
- [ ] No console errors in browser dev tools
- [ ] All buttons/links visually consistent
- [ ] Hover states work on all interactive elements
- [ ] Gallery grid layouts correctly on all screen sizes
- [ ] CSS file sizes haven't dramatically increased

---

## Additional Resources

### Recommended Reading
- [BEM Methodology](http://getbem.com/) - Naming convention for maintainable CSS
- [CSS Variables Guide](https://developer.mozilla.org/en-US/docs/Web/CSS/Using_CSS_custom_properties)
- [CSS Units Guide](https://www.w3.org/Style/Examples/007/units.en.html) - When to use rem vs em vs px

### Tools
- [CSS Lint](http://csslint.net/) - Check for issues
- [PurgeCSS](https://purgecss.com/) - Remove unused CSS (future optimization)

---

## Questions for Consideration

1. **Do you need all three button styles?** Consider consolidating to two (primary + text link)

2. **Are `.gallery-item` and `.gallery-container` used anywhere?** If not, remove them

3. **Should the zoom indicator (🔍) be consistent everywhere?** Currently has different positioning in gallery vs detail pages

4. **Dark mode: Complete or in progress?** The `@media (prefers-color-scheme: dark)` block is only in `animation-gallery.css`

---

## Conclusion

Your project has a solid foundation with good separation of concerns and semantic HTML. The main work needed is **consistency cleanup** rather than structural changes.

**Estimated effort:** 6-9 hours to complete all recommendations

**Biggest wins:**
1. Implementing CSS variables (improves maintainability)
2. Standardizing button/link styles (improves consistency)
3. Removing duplicate code (improves performance)

These changes will make your codebase much easier to maintain and extend in the future.