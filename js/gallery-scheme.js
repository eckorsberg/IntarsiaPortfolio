// /js/gallery-schema.js
// ----------------------------------------------------------------------------
// Purpose
//   - Centralize how we read common fields from gallery JSON items.
//   - This protects you from JSON schema drift over time (renames, old keys).
//
// Assumptions
//   - Gallery items might come from different eras/scripts and may use
//     different property names for the same concept.
//   - Callers want a consistent API: designer(), category(), title().
//
// Safe modification points
//   - If you rename fields in gallery.json (or Jane’s gallery.json), update
//     these fallbacks so older content keeps working.
//   - If you add new normalized fields, add a new method here rather than
//     sprinkling "item.foo || item.bar" throughout the codebase.
//
// Notes
//   - Exposed as window.GallerySchema to avoid module tooling; scripts can
//     reference it after it loads.

window.GallerySchema = {
  designer(item) {
    return (item.pattern_designer || item.patternDesigner || item.artist || "").trim();
  },
  category(item) {
    return (item.category || item.type || "").trim();
  },
  title(item) {
    return (item.title || "").trim();
  }
};
