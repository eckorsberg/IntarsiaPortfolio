// File: pattern-designer-loader-laser.js
// Purpose: Load pattern designer for laser detail pages under /ed/pages/ (and future /jane/laser if needed)

(function () {
  // Example path: "/ed/pages/laserdemo.html"
  const path = window.location.pathname.toLowerCase().replace(/^\//, "");
  const parts = path.split("/");           // ["ed", "pages", "laserdemo.html"]

  const section = parts[0] || "";          // "ed" or "jane"
  const relativePath = parts.slice(1).join("/"); // "pages/laserdemo.html"

  // Determine which laser.json to load
  let jsonPath;
  if (section === "ed" || section === "jane") {
    jsonPath = `/${section}/laser.json`;   // "/ed/laser.json"
  } else {
    jsonPath = "/laser.json";              // fallback for legacy paths
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
      const currentFile = relativePath;   // "pages/laserdemo.html"

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
      console.error("Error loading laser pattern designer:", error);
      designerElement.textContent = "Unknown";
    });
})();
