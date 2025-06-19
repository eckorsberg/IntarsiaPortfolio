
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
      uniqueValues.forEach(value => {
        const option = document.createElement("option");  // Create <option> element
        option.value = value;                             // Set the value attribute
        option.textContent = value;                       // Set the text shown in dropdown
        filters[key].appendChild(option);                 // Add option to the corresponding <select>
      });
    });

    // Function to apply active filters and rebuild the gallery
    function applyFilters() {
      galleryContainer.innerHTML = "";                    // Clear existing gallery items
      galleryContainer.className = "gallery";             // Ensure container retains grid styling

      // Collect selected filter values
      const selected = {
        artist: filters.artist.value,
        theme: filters.theme.value,
        type: filters.type.value,
      };

      // Loop through all items in the dataset
      data.forEach(item => {
        // Determine if item matches selected filters
        const match =
          (!selected.artist || item.artist === selected.artist) &&
          (!selected.theme || item.theme === selected.theme) &&
          (!selected.type || item.type === selected.type);

        if (match) {
          // Create a link that wraps the image and caption
          const link = document.createElement("a");
          link.href = item.file;
          //link.target = "_blank";                         // Open in new tab
          link.className = "gallery-link";

          // Create the image element
          const img = document.createElement("img");
          img.src = item.thumbnail;                       // Set image source
          img.alt = item.title;                           // Set alt text
          img.classList.add("gallery-img");               // Add styling class
          console.log("Added class:", img.className, "to", img.src);  // Debug log

          // Create caption element
          const caption = document.createElement("p");
          caption.className = "gallery-caption";
          caption.innerText = item.title;

          // Append image and caption to the link
          link.appendChild(img);
          link.appendChild(caption);

          // Add the link to the gallery container
          galleryContainer.appendChild(link);
        }
      });
    }

    // Attach change listeners to all dropdowns to reapply filters on change
    Object.values(filters).forEach(select => {
      select.addEventListener("change", applyFilters);
    });

    applyFilters(); // Initial rendering on page load
  });
