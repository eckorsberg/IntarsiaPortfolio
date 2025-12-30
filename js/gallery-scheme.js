// /js/gallery-schema.js
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
