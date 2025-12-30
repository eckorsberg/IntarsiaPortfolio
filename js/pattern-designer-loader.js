// /js/pattern-designer-loader.js
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
