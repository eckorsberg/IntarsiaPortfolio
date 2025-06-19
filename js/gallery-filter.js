
// Load gallery data from a JSON file
fetch("gallery.json")
  .then(response => response.json())                // Parse the JSON response
  .then(data => {
    const galleryContainer = document.querySelector(".gallery"); // Reference the gallery container in the DOM

    // Define filter dropdown elements
    const filters = {
      artist: document.getElementById("artistFilter"),
      theme: document.getElementById("themeFilter"),
      type: document.getElementById("typeFilter"),
    };

    // Populate each filter dropdown with unique sorted values from data
    Object.keys(filters).forEach(key => {
      const uniqueValues = [...new Set(data.map(item => item[key]).filter(Boolean))].sort();

      // Add an "All" option first
      const defaultOption = document.createElement("option");
      defaultOption.value = "";
      defaultOption.textContent = "All";
      filters[key].appendChild(defaultOption);

      // Add real values
      uniqueValues.forEach(value => {
        const option = document.createElement("option");
        option.value = value;
        option.textContent = value;
        filters[key].appendChild(option);
      });
    });

    // Function to apply active filters and rebuild the gallery
    function applyFilters() {
      galleryContainer.innerHTML = ""; // Clear existing gallery items
      const searchTerm = document.getElementById("searchBox").value.trim().toLowerCase();
      galleryContainer.className = "gallery"; // Ensure container retains grid styling

      // Collect selected filter values
      const selected = {
        artist: filters.artist.value,
        theme: filters.theme.value,
        type: filters.type.value,
      };

      let matchedCount = 0;

      data.forEach(item => {
        const match =
          (!selected.artist || item.artist === selected.artist) &&
          (!selected.theme || item.theme === selected.theme) &&
          (!selected.type || item.type === selected.type) &&
          (!searchTerm || item.title.toLowerCase().includes(searchTerm));

        if (match) {
          matchedCount++;
          const link = document.createElement("a");
          link.href = item.file;
          link.className = "gallery-link";

          const img = document.createElement("img");
          img.src = item.thumbnail;
          img.alt = item.title;
          img.classList.add("gallery-img");

          const caption = document.createElement("p");
          caption.className = "gallery-caption";
          caption.innerText = item.title;

          link.appendChild(img);
          link.appendChild(caption);
          galleryContainer.appendChild(link);
        }
      });

      if (matchedCount === 0) {
        galleryContainer.innerHTML = "<p style='text-align:center;'>No items match the selected filters.</p>";
      }
    }

    // Attach listeners
    Object.values(filters).forEach(select => {
      select.addEventListener("change", applyFilters);
    });

    document.getElementById("searchBox").addEventListener("input", applyFilters);

    applyFilters(); // Initial render
  });
