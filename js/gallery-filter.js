// Load gallery data from a JSON file
fetch("gallery.json")
  .then(response => response.json()) // Parse the JSON response
  .then(data => {
    const galleryContainer = document.querySelector(".gallery"); // Target container for gallery

    // Cache UI elements
    const totalCountElement = document.getElementById("totalCount");
    const viewLabel = document.getElementById("viewLabel");
    const toggleBtn = document.getElementById("toggleView");
    const featuredToggle = document.getElementById("featuredToggle");

    // Compute featured set (items with featured:true)
    const featuredData = data.filter(item => item.featured === true);

    // Determine initial view mode:
    // - if there are featured items, default to "featured"
    // - otherwise default to "all"
    let viewMode = sessionStorage.getItem("viewMode") ||
      (featuredData.length > 0 ? "featured" : "all");

    // Display total number of pieces (always the full portfolio count)
    if (totalCountElement) {
      totalCountElement.textContent = `Total pieces in portfolio: ${data.length}`;
    }

    // Cache filter dropdown DOM elements
    const filters = {
      //artist: document.getElementById("artistFilter"),
      //theme: document.getElementById("themeFilter"),
      category: document.getElementById("categoryFilter"),
      //status: document.getElementById("statusFilter"),
    };

    // Keep only filters that actually exist on the page
    const activeFilters = Object.fromEntries(
      Object.entries(filters).filter(([_, el]) => el)
    );

    const searchBox = document.getElementById("searchBox");

    // Populate dropdowns with unique values from the dataset
    Object.keys(activeFilters).forEach(key => {
      const uniqueValues = [...new Set(data.map(item => item[key]).filter(Boolean))].sort();

      const defaultOption = document.createElement("option");
      defaultOption.value = "";
      defaultOption.textContent = "All";
      activeFilters[key].appendChild(defaultOption);

      uniqueValues.forEach(value => {
        const option = document.createElement("option");
        option.value = value;
        option.textContent = value;
        activeFilters[key].appendChild(option);
      });
    });

    // Restore session values (filters + search)
    Object.keys(activeFilters).forEach(key => {
      const saved = sessionStorage.getItem(`filter-${key}`);
      if (saved) activeFilters[key].value = saved;
    });

    const savedSearch = sessionStorage.getItem("searchTerm");
    if (savedSearch && searchBox) {
      searchBox.value = savedSearch;
    }

    function clearAllFiltersAndSearch() {
      // Clear UI
      if (searchBox) searchBox.value = "";
      Object.keys(activeFilters).forEach(key => {
        activeFilters[key].value = "";
      });

      // Clear session
      sessionStorage.removeItem("searchTerm");
      Object.keys(activeFilters).forEach(key => {
        sessionStorage.removeItem(`filter-${key}`);
      });
    }

    function updateViewUI() {
      if (!featuredToggle || !viewLabel || !toggleBtn) return;

      // Hide the toggle entirely if there are no featured items
      if (featuredData.length === 0) {
        featuredToggle.style.display = "none";
        return;
      }

      featuredToggle.style.display = ""; // show

      if (viewMode === "featured") {
        viewLabel.textContent = `Showing: Featured (${featuredData.length} of ${data.length})`;
        toggleBtn.textContent = "Show All";
      } else {
        viewLabel.textContent = `Showing: All (${data.length})`;
        toggleBtn.textContent = "Show Featured";
      }
    }

    // Render gallery based on current filters and search term
    function applyFilters() {
      galleryContainer.innerHTML = ""; // Clear gallery
      galleryContainer.className = "gallery"; // Ensure class remains for layout

      const searchTerm = (searchBox ? searchBox.value : "").trim().toLowerCase();

      // Get selected filter values
      const selected = {};
      Object.keys(activeFilters).forEach(key => {
        selected[key] = activeFilters[key].value;
      });

      const anyFilterActive = Object.values(selected).some(v => v);
      const anySearchActive = !!searchTerm;

      // Featured view is only meaningful as the "landing" (no filters/search).
      // If user starts filtering/searching, they get the full dataset automatically.
      const useFeaturedLanding =
        (viewMode === "featured") &&
        !anyFilterActive &&
        !anySearchActive &&
        featuredData.length > 0;

      const sourceData = useFeaturedLanding ? featuredData : data;

      let matchedCount = 0;

      // Loop through dataset and build elements for matches
      sourceData.forEach(item => {
        const matchFilters = Object.entries(selected).every(([key, val]) =>
          !val || item[key] === val
        );

        const match = matchFilters &&
          (!searchTerm || (item.title || "").toLowerCase().includes(searchTerm));

        if (match) {
          matchedCount++;

          // Create link for each matched item
          const link = document.createElement("a");
          link.href = item.file;
          link.className = "gallery-link";

          // Image thumbnail
          const img = document.createElement("img");
          img.src = item.thumbnail;
          img.alt = item.title;
          img.classList.add("gallery-img");

          // Caption (title)
          const caption = document.createElement("p");
          caption.className = "gallery-caption";
          caption.innerText = item.title;

          link.appendChild(img);
          link.appendChild(caption);

          galleryContainer.appendChild(link);
        }
      });

      // Handle empty results
      if (matchedCount === 0) {
        galleryContainer.innerHTML = "<p style='text-align:center;'>No items match the selected filters.</p>";
      }
    }

    // Toggle button behavior
    if (toggleBtn) {
      toggleBtn.addEventListener("click", () => {
        if (viewMode === "featured") {
          viewMode = "all";
          sessionStorage.setItem("viewMode", viewMode);
        } else {
          // Switching back to Featured should reset filters/search so Featured is actually visible.
          viewMode = "featured";
          sessionStorage.setItem("viewMode", viewMode);
          clearAllFiltersAndSearch();
        }
        updateViewUI();
        applyFilters();
      });
    }

    // Attach change listeners to all filters
    Object.entries(activeFilters).forEach(([key, select]) => {
      select.addEventListener("change", () => {
        sessionStorage.setItem(`filter-${key}`, select.value);

        // Any explicit filtering implies "All"
        if (viewMode !== "all") {
          viewMode = "all";
          sessionStorage.setItem("viewMode", viewMode);
          updateViewUI();
        }

        applyFilters();
      });
    });

    // Text input listener
    if (searchBox) {
      searchBox.addEventListener("input", () => {
        sessionStorage.setItem("searchTerm", searchBox.value);

        // Any explicit search implies "All"
        if (viewMode !== "all") {
          viewMode = "all";
          sessionStorage.setItem("viewMode", viewMode);
          updateViewUI();
        }

        applyFilters();
      });
    }

    updateViewUI();
    applyFilters(); // Initial rendering of gallery
  });
