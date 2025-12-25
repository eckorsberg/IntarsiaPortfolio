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

	// keep only filters that actually exist on the page
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

    // Now that options exist, restore session values
	Object.keys(activeFilters).forEach(key => {
	  const saved = sessionStorage.getItem(`filter-${key}`);
	  if (saved) activeFilters[key].value = saved;
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
	const selected = {};
	Object.keys(activeFilters).forEach(key => {
	  selected[key] = activeFilters[key].value;
	});

      let matchedCount = 0;

      // Loop through dataset and build elements for matches
      data.forEach(item => {
		const matchFilters = Object.entries(selected).every(([key, val]) =>
		  !val || item[key] === val
		);

		const match = matchFilters &&
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
	Object.entries(activeFilters).forEach(([key, select]) => {
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
