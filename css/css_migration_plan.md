# CSS Variable Migration Plan

## Phase 1: Border Radius Standardization
**Time:** 15 minutes  
**Impact:** High visual consistency  
**Risk:** Very low

### Find & Replace Operations

#### In `/style.css`:
```css
/* Before → After */
border-radius: 8px;   → border-radius: var(--radius-sm);
border-radius: 12px;  → border-radius: var(--radius-md);
border-radius: 14px;  → border-radius: var(--radius-lg);
border-radius: 999px; → border-radius: var(--radius-pill);
border-radius: 6px;   → border-radius: var(--radius-sm); /* close enough */
```

#### In `/css/index.css`:
```css
border-radius: 14px;  → border-radius: var(--radius-lg);
border-radius: 999px; → border-radius: var(--radius-pill);
border-radius: 12px;  → border-radius: var(--radius-md);
```

#### In `/css/laser.css`:
```css
border-radius: 12px;  → border-radius: var(--radius-md);
```

#### In `/css/animation-gallery.css`:
```css
border-radius: 14px;  → border-radius: var(--radius-lg);
border-radius: 999px; → border-radius: var(--radius-pill);
```

### Testing After Phase 1
- Load each page (main, laser, animation)
- Verify all rounded corners look identical to before
- No visual changes expected

---

## Phase 2: Box Shadow Standardization
**Time:** 20 minutes  
**Impact:** Subtle depth consistency  
**Risk:** Low (may require visual comparison)

### Analysis Required First

Current shadows need mapping to your predefined variables:

```css
/* Your variables: */
--shadow-sm: 0 2px 6px rgba(0,0,0,0.08);
--shadow-md: 0 4px 10px rgba(0,0,0,0.1);
--shadow-lg: 0 6px 18px rgba(0,0,0,0.06);
```

**Problem:** Some current shadows don't exactly match:
```css
box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);  /* close to md, but different blur */
box-shadow: 0 2px 8px rgba(0,0,0,0.15);    /* between sm and md */
box-shadow: 0 2px 10px rgba(0,0,0,0.05);   /* custom */
```

### Recommended Approach

**Option A (Precise):** Adjust your variables to match most common actual usage
```css
:root {
  --shadow-sm: 0 2px 6px rgba(0,0,0,0.08);   /* keep as-is */
  --shadow-md: 0 4px 8px rgba(0,0,0,0.1);    /* change to match gallery-img */
  --shadow-lg: 0 6px 14px rgba(0,0,0,0.12);  /* change to match hover states */
}
```

**Option B (Simplify):** Round to your existing variables, accept slight visual changes
```css
/* Just replace all shadows with closest var() */
0 4px 8px rgba(0, 0, 0, 0.1) → box-shadow: var(--shadow-md);
```

### Replacements (if choosing Option B)

```css
/* In /style.css */
box-shadow: 0 4px 10px rgba(0,0,0,0.1);  → var(--shadow-md)
box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); → var(--shadow-md)
box-shadow: 0 2px 6px rgba(0,0,0,0.08);   → var(--shadow-sm)
box-shadow: 0 2px 8px rgba(0,0,0,0.15);   → var(--shadow-md) /* slightly lighter than before */

/* Leave contextual shadows alone: */
box-shadow: 0 1px 0 rgba(255,255,255,0.65) /* text-shadow effect, don't change */
```

### Testing After Phase 2
- Load all pages side-by-side with before/after screenshots
- Verify depth hierarchy feels consistent
- Some subtle changes expected (that's the point)

---

## Phase 3: Spacing Standardization (Optional)
**Time:** 30 minutes  
**Impact:** Low (internal consistency only)  
**Risk:** Medium (easy to over-apply)

### Only Replace Repeated Structural Spacing

**Good candidates (repeated patterns):**
```css
margin: 1rem 0;     → margin: var(--spacing-md) 0;
padding: 1rem;      → padding: var(--spacing-md);
gap: 1rem;          → gap: var(--spacing-md);
margin-top: 0.75rem; → margin-top: var(--spacing-sm); /* or create --spacing-3/4 */
```

**Bad candidates (contextual, leave alone):**
```css
padding: 1.5rem;              /* specific to .intro-text */
padding: 0.4em 0.8em;         /* optical balance for .button-link */
margin: 0.5em 0;              /* em-based, intentionally relative to font-size */
```

### Key Rule
**Only replace spacing values that:**
1. Appear 3+ times across multiple files
2. Represent the same conceptual spacing unit
3. Would change together if you adjusted your spacing scale

---

## What NOT to Migrate

### Colors
Your color variables are **aspirational** but not worth forcing:

```css
/* Leave these as-is - they're contextual */
color: #222;                   /* text-primary exists, but this is fine */
background-color: #f6f4f1;     /* bg-warm exists, but hardcoded is clearer here */
color: #3498db;                /* link-color exists, but this is Ed-specific */
```

**Why:** Your site has intentional color variations. Forcing everything through variables would require:
- Naming every single color variation
- Indirection without clarity benefit
- Potential for "variable soup"

**Exception:** If you add new interactive elements (buttons, cards, etc.), use variables there.

### Typography
```css
/* Leave alone - these are responsive and contextual */
font-size: clamp(1rem, 2.5vw, 1.2rem);
font-size: 0.9em;
font-size: 1.8em;
```

**Why:** Font sizing is intentionally contextual and relative. Variables would obscure the responsive logic.

---

## Migration Workflow

### For Each Phase

1. **Make a backup commit**
   ```bash
   git add .
   git commit -m "Pre-migration snapshot: [Phase name]"
   ```

2. **Do find-replace in one file at a time**
   - Don't bulk-replace across all files
   - Review each change before saving

3. **Test immediately after each file**
   - Load the relevant page
   - Compare to before

4. **Commit after each file**
   ```bash
   git add style.css
   git commit -m "Migrate border-radius to variables in style.css"
   ```

5. **If something looks wrong, revert just that file**
   ```bash
   git checkout HEAD -- style.css
   ```

### Stop Conditions

**Stop if:**
- You find yourself creating new variables for one-off values
- Changes feel arbitrary rather than clarifying
- You're replacing values that never appear together

**This is a success signal:** You've hit the natural boundary between "shared design tokens" and "contextual values."

---

## Expected Outcomes

### After Phase 1 (Border Radius)
✅ All rounded corners use consistent values  
✅ Changing corner rounding site-wide requires editing 4 variables, not 20+ instances  
✅ Zero visual changes (exact replacement)

### After Phase 2 (Box Shadows)
✅ Depth hierarchy becomes consistent  
✅ Hover effects have uniform "lift" feeling  
⚠️ Minor visual changes possible (subtle depth adjustments)

### After Phase 3 (Spacing - if done)
✅ Structural rhythm becomes more consistent  
✅ Responsive spacing adjustments easier  
⚠️ Risk of over-application if not disciplined

---

## Long-Term Maintenance

### When to Add New Variables
**Only when:**
- A new design token appears 3+ times
- It represents a design decision (not a one-off tweak)
- Future you would want to adjust all instances together

**Examples:**
```css
/* Yes - design token */
--card-padding: 1.5rem;  /* if you use this pattern for multiple card types */

/* No - one-off */
--article-thumb-max-width: 600px;  /* specific to one element */
```

### When to Use Existing Variables
- When adding new styles
- When editing existing styles you're already touching
- When you notice a hardcoded value matches an existing variable

### When NOT to Use Variables
- Don't refactor working code just to use variables
- Don't create variables for single-use values
- Don't replace contextual values with semantic variables

---

## Estimated Total Time

- **Phase 1 (Recommended):** 15 minutes
- **Phase 2 (Nice to have):** 20 minutes  
- **Phase 3 (Optional):** 30 minutes

**Total if doing all:** ~65 minutes  
**Recommended start:** Phase 1 only, evaluate if Phase 2 is worth it

---

## Success Criteria

You'll know the migration was successful if:

1. **No visual changes** (or only intentional improvements)
2. **Easier future adjustments** (e.g., "make corners rounder" is now 1 variable change)
3. **No new confusion** (variables are clearer than magic numbers, not more obscure)
4. **Stop naturally** (you don't force everything into variables)

You'll know to stop/revert if:

1. You're creating variables for single-use values
2. Code becomes less clear than before
3. You're changing visual design unintentionally
4. Variables feel like indirection rather than abstraction

---

## Final Recommendation

**Do Phase 1 now** (border-radius): Clear win, zero risk, 15 minutes.

**Evaluate Phase 2** (shadows) after seeing Phase 1: Probably worth it, but compare before/after carefully.

**Skip Phase 3** (spacing) unless you find yourself repeatedly adjusting the same spacing values: Not worth the time investment for current site scale.

This respects your "evidence-driven improvement" philosophy while getting real consistency benefits.
