// pattern-designer-loader.js

// Extract the current page path in lowercase (without leading slash)
const currentPage = window.location.pathname.toLowerCase().replace(/^\//, "");

// Fetch gallery metadata
fetch("/gallery.json")
  .then((response) => response.json())
  .then((data) => {
    // Find matching entry (case-insensitive match)
    const entry = data.find(
      (item) => item.file.toLowerCase() === currentPage
    );

    // Set designer name or fallback to 'Unknown'
    const designerElement = document.getElementById("patternDesigner");
    if (entry && entry.artist && designerElement) {
      designerElement.textContent = entry.artist;
    } else if (designerElement) {
      designerElement.textContent = "Unknown";
    }
  })
  .catch((error) => {
    console.error("Error loading gallery.json:", error);
  });
