// Load gallery data from a JSON file
fetch("gallery.json")
  .then(response => response.json()) // Parse the JSON response
  .then(data => {
    const galleryContainer = document.querySelector(".gallery"); // Target container for gallery

    // Display total number of pieces
    const totalCountElement = document.getElementById("totalCount");
    if (totalCountElement) {
      totalCountElement.textContent = `Total pieces in portfolio: ${data.length}`;
    }

    // Cache filter dropdown DOM elements
    const filters = {
      artist: document.getElementById("artistFilter"),
      theme: document.getElementById("themeFilter"),
      type: document.getElementById("typeFilter"),
      status: document.getElementById("statusFilter"),
    };

    const searchBox = document.getElementById("searchBox");

    // Populate dropdowns with unique values from the dataset
    Object.keys(filters).forEach(key => {
      const uniqueValues = [...new Set(data.map(item => item[key]).filter(Boolean))].sort();

      // Add default "All" option
      const defaultOption = document.createElement("option");
      defaultOption.value = "";
      defaultOption.textContent = "All";
      filters[key].appendChild(defaultOption);

      // Add individual option values
      uniqueValues.forEach(value => {
        const option = document.createElement("option");
        option.value = value;
        option.textContent = value;
        filters[key].appendChild(option);
      });
    });

    // Now that options exist, restore session values
    Object.keys(filters).forEach(key => {
      const saved = sessionStorage.getItem(`filter-${key}`);
      if (saved && filters[key]) {
        filters[key].value = saved;
      }
    });

    const savedSearch = sessionStorage.getItem("searchTerm");
    if (savedSearch) {
      searchBox.value = savedSearch;
    }

    // Render gallery based on current filters and search term
    function applyFilters() {
      galleryContainer.innerHTML = ""; // Clear gallery
      galleryContainer.className = "gallery"; // Ensure class remains for layout

      const searchTerm = searchBox.value.trim().toLowerCase();

      // Get selected filter values
      const selected = {
        artist: filters.artist.value,
        theme: filters.theme.value,
        type: filters.type.value,
        status: filters.status.value,
      };

      let matchedCount = 0;

      // Loop through dataset and build elements for matches
      data.forEach(item => {
        const match =
          (!selected.artist || item.artist === selected.artist) &&
          (!selected.theme || item.theme === selected.theme) &&
          (!selected.type || item.type === selected.type) &&
          (!selected.status || item.status === selected.status) &&
          (!searchTerm || item.title.toLowerCase().includes(searchTerm));

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

          //// Optional cost line
          //if (item.status === "Available" && item.cost) {
          //  const costLine = document.createElement("p");
          //  costLine.className = "gallery-cost";
          //  costLine.innerText = item.cost;
          //  link.appendChild(costLine);
          //}

          galleryContainer.appendChild(link);
        }

      });

      // Handle empty results
      if (matchedCount === 0) {
        galleryContainer.innerHTML = "<p style='text-align:center;'>No items match the selected filters.</p>";
      }
    }

    // Attach change listeners to all filters
    Object.entries(filters).forEach(([key, select]) => {
      select.addEventListener("change", () => {
        sessionStorage.setItem(`filter-${key}`, select.value);
        applyFilters();
      });
    });

    // Text input listener
    searchBox.addEventListener("input", () => {
      sessionStorage.setItem("searchTerm", searchBox.value);
      applyFilters();
    });

    applyFilters(); // Initial rendering of gallery
  });
