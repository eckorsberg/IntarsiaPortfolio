// pattern-designer-loader.js
// Automatically inserts the pattern designer name based on current page

document.addEventListener("DOMContentLoaded", () => {
  const fileName = location.pathname.split("/").pop(); // e.g., "standingpug.html"

  fetch("/gallery.json")
    .then(res => res.json())
    .then(data => {
      const match = data.find(item => item.file.includes(fileName));
      const target = document.getElementById("patternDesigner");
      if (target) {
        if (match && match.artist) {
          target.textContent = match.artist;
        } else {
          target.textContent = "(unknown)";
        }
      }
    })
    .catch(() => {
      const target = document.getElementById("patternDesigner");
      if (target) target.textContent = "(error)";
    });
});
