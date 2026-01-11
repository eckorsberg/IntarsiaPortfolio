/**
 * /js/animation_loader.js
 * -----------------------------------------------------------------------------
 * Renders animation cards from a JSON file into an element with class "grid".
 *
 * Usage:
 *   <main class="grid" data-json="./animations.json"></main>
 *   <script src="/js/animation-loader.js"></script>
 *
 * If data-json is omitted, defaults to "animations.json" (same folder as the page).
 */

(() => {
  const grid = document.querySelector(".grid");
  if (!grid) return;

  const jsonPath = grid.dataset.json || "animations.json";

  // Small loading hint (nice on slow networks)
  grid.innerHTML =
    '<p style="text-align:center;color:#666;padding:1rem;">Loading animations…</p>';

  fetch(jsonPath)
    .then((response) => {
      if (!response.ok) {
        throw new Error(`HTTP ${response.status} loading ${jsonPath}`);
      }
      return response.json();
    })
    .then((data) => {
      if (!Array.isArray(data) || data.length === 0) {
        grid.innerHTML =
          '<p style="text-align:center;color:#666;padding:1rem;">No animations found.</p>';
        return;
      }

      grid.innerHTML = "";

      data.forEach((item) => {
        if (!item || !item.video) return;

        const titleText = (item.title || "Untitled").trim();

        const article = document.createElement("article");
        article.className = "card";

        // Thumbnail opens video
        const thumbLink = document.createElement("a");
        thumbLink.className = "thumb";
        thumbLink.href = item.video;
        thumbLink.target = "_blank";
        thumbLink.rel = "noopener";
        thumbLink.setAttribute("aria-label", `Play ${titleText} video`);

        const img = document.createElement("img");
        img.src = item.thumbnail || "";
        img.alt = `${titleText} animation thumbnail`;
        img.loading = "lazy";
        thumbLink.appendChild(img);

        // Content
        const content = document.createElement("div");
        content.className = "content";

        const title = document.createElement("div");
        title.className = "title";
        title.textContent = titleText;

        const actions = document.createElement("div");
        actions.className = "actions";

        // Optional: View piece page
        if (item.detailPage) {
          const detailBtn = document.createElement("a");
          detailBtn.className = "btn";
          detailBtn.href = item.detailPage;
          detailBtn.textContent = "View piece";
          detailBtn.setAttribute("aria-label", `View ${titleText} details`);
          actions.appendChild(detailBtn);
        }

        // Open video
        const videoBtn = document.createElement("a");
        videoBtn.className = "btn";
        videoBtn.href = item.video;
        videoBtn.target = "_blank";
        videoBtn.rel = "noopener";
        videoBtn.textContent = "Open video";
        videoBtn.setAttribute("aria-label", `Open ${titleText} video in new tab`);
        actions.appendChild(videoBtn);

        content.appendChild(title);
        content.appendChild(actions);

        article.appendChild(thumbLink);
        article.appendChild(content);

        grid.appendChild(article);
      });
    })
    .catch((error) => {
      console.error("Failed to load animations:", error);
      grid.innerHTML =
        '<p style="text-align:center;color:#666;padding:2rem;">Unable to load animations. Please refresh the page.</p>';
    });
})();
