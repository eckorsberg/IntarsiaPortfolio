// File: pattern-designer-loader.js
// Purpose: Load pattern designer for detail pages under /ed/pages and /jane/pages
// Works for both Ed and Jane by using the first path segment (ed/jane) as the base.

(function () {
  // e.g. "/ed/pages/babydragon.html" or "/jane/pages/EncantoQuilt.html"
  const path = window.location.pathname.toLowerCase().replace(/^\//, "");
  const parts = path.split("/"); // ["ed", "pages", "babydragon.html"]

  const section = parts[0] || "";              // "ed" or "jane"
  const relativePath = parts.slice(1).join("/"); // "pages/babydragon.html"

  // Decide which gallery.json to load
  let jsonPath;
  if (section === "ed" || section === "jane") {
    jsonPath = `/${section}/gallery.json`;     // "/ed/gallery.json" or "/jane/gallery.json"
  } else {
    // Fallback if you ever use this on a root-level page
    jsonPath = "/gallery.json";
  }

  const designerElement = document.getElementById("patternDesigner");
  if (!designerElement) {
    return;
  }

  fetch(jsonPath)
    .then((response) => {
      if (!response.ok) {
        throw new Error(`Failed to load ${jsonPath}: ${response.status}`);
      }
      return response.json();
    })
    .then((data) => {
      const currentFile = relativePath; // "pages/babydragon.html"

      const entry = data.find(
        (item) => (item.file || "").toLowerCase() === currentFile
      );

      if (entry && entry.artist) {
        designerElement.textContent = entry.artist;
      } else {
        designerElement.textContent = "Unknown";
      }
    })
    .catch((error) => {
      console.error("Error loading pattern designer:", error);
      designerElement.textContent = "Unknown";
    });
})();
