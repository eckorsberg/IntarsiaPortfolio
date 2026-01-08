// /js/pattern-designer-loader.js
// -----------------------------------------------------------------------------
// Purpose
//   - Detail pages contain a placeholder:
//       <span id="patternDesigner">Loading...</span>
//   - This script looks up the current page in the appropriate JSON file(s),
//     finds the matching entry, and replaces the text with the correct designer.
//
// Assumptions
//   - Detail page URL structure is:
//       /ed/pages/<something>.html
//       /jane/pages/<something>.html
//     (This script infers "section" from the first path segment.)
//   - JSON items use "file" values that match the page's relative path from the
//     section root, e.g. "pages/foo.html".
//   - For Ed, designer metadata may live in either:
//       /ed/gallery.json (wood portfolio)
//       /ed/laser.json   (laser portfolio)
//     so we search both and combine.
//   - For Jane, we only search /jane/gallery.json.
//
// Safe modification points
//   - If you change folder structure (e.g., move pages out of /pages/),
//     update how `relativePage` is computed.
//   - If you rename JSON fields (e.g., pattern_designer), update the fallback
//     lookup for `designer`.
//   - If you add more sections (e.g. /laser/), add a case in the jsonPaths block.
//
// Notes
//   - Matching is case-insensitive via norm() to be resilient to filename casing.
//   - If fetch fails or an entry is not found, we show "Unknown" (and log to console).

(function () {
  const designerEl = document.getElementById("patternDesigner");
  if (!designerEl) return;

  const path = window.location.pathname.replace(/^\//, "");
  const parts = path.split("/");

  const section = parts[0];                 // "ed", "jane", etc.
  const relativePage = parts.slice(1).join("/"); // "pages/foo.html"

  // Decide which JSON files to search
  // Key point: in /ed/, laser items live in /ed/laser.json but pages are still /ed/pages/...
  let jsonPaths = [];
  if (section === "ed") {
    jsonPaths = ["/ed/gallery.json", "/ed/laser.json"];
  } else if (section === "jane") {
    jsonPaths = ["/jane/gallery.json"];
  } else if (section === "laser") {
    // only relevant if you ever move laser to /laser/ URLs later
    jsonPaths = ["/laser/laser.json"];
  } else {
    return;
  }

  const norm = (s) => (s || "").toLowerCase();

  Promise.all(
    jsonPaths.map(p =>
      fetch(p).then(r => r.ok ? r.json() : Promise.reject({ path: p, status: r.status }))
    )
  )
    .then(arrays => {
      const combined = arrays.flat();

      const entry = combined.find(item => norm(item.file) === norm(relativePage));

      const designer =
        entry?.pattern_designer ||
        entry?.patternDesigner || // just in case
        entry?.artist ||
        "";

      designerEl.textContent = designer.trim() || "Unknown";
    })
    .catch(err => {
      console.error("Pattern designer load failed:", err);
      designerEl.textContent = "Unknown";
    });
})();
