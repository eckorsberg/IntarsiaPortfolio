// Simple gallery loader for Jane's quilts.
// Expects to be used from /jane/index.html and read /jane/gallery.json.

document.addEventListener("DOMContentLoaded", () => {
  const galleryEl = document.querySelector(".gallery");
  const countEl = document.getElementById("totalCount");

  if (!galleryEl) {
    console.error("jane-gallery: .gallery element not found");
    return;
  }

  fetch("gallery.json")
    .then((response) => {
      if (!response.ok) {
        throw new Error("Failed to load gallery.json");
      }
      return response.json();
    })
    .then((items) => {
      if (!Array.isArray(items)) {
        throw new Error("gallery.json is not an array");
      }

      // Update piece count
      if (countEl) {
        countEl.textContent = `${items.length} pieces in Jane's quilt portfolio`;
      }

      // Build simple cards (reusing existing .card styling from Ed's gallery)
      items.forEach((item) => {
        const title = item.title || "Untitled";
        const thumb = item.thumbnail || "";
        const file = item.file || "#";
        const theme = item.theme || "";
        const status = item.status || "";

        const card = document.createElement("a");
        card.className = "card";
        card.href = file;

        card.innerHTML = `
          <div class="card-image">
            <img src="${thumb}" alt="${title}">
          </div>
          <div class="card-body">
            <h2 class="card-title">${title}</h2>
            ${theme || status ? `
              <p class="card-meta">
                ${theme ? `<span class="card-theme">${theme}</span>` : ""}
                ${status ? `<span class="card-status">${status}</span>` : ""}
              </p>
            ` : ""}
          </div>
        `;

        galleryEl.appendChild(card);
      });

      if (items.length === 0 && countEl) {
        countEl.textContent = "No pieces found in Jane's gallery yet.";
      }
    })
    .catch((err) => {
      console.error("Error loading Jane's gallery:", err);
      if (countEl) {
        countEl.textContent = "Error loading Jane's gallery.";
      }
    });
});
