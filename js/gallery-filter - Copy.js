
fetch("gallery.json")
  .then(response => response.json())
  .then(data => {
    const galleryContainer = document.querySelector(".gallery");

    const filters = {
      artist: document.getElementById("artistFilter"),
      theme: document.getElementById("themeFilter"),
      type: document.getElementById("typeFilter"),
    };

    Object.keys(filters).forEach(key => {
      const uniqueValues = [...new Set(data.map(item => item[key]).filter(Boolean))].sort();
      uniqueValues.forEach(value => {
        const option = document.createElement("option");
        option.value = value;
        option.textContent = value;
        filters[key].appendChild(option);
      });
    });

    function applyFilters() {
      galleryContainer.innerHTML = "";
      const selected = {
        artist: filters.artist.value,
        theme: filters.theme.value,
        type: filters.type.value,
      };

      data.forEach(item => {
        const match =
          (!selected.artist || item.artist === selected.artist) &&
          (!selected.theme || item.theme === selected.theme) &&
          (!selected.type || item.type === selected.type);

        if (match) {
          const link = document.createElement("a");
          link.href = item.file;
          link.className = "gallery-link";

          const img = document.createElement("img");
          img.src = item.thumbnail;
          img.alt = item.title;
          img.classList.add("gallery-thumb");

          const title = document.createElement("span");
          title.innerText = item.title;
          title.className = "gallery-title";

          link.appendChild(img);
          link.appendChild(title);
          galleryContainer.appendChild(link);
        }
      });
    }

    Object.values(filters).forEach(select => {
      select.addEventListener("change", applyFilters);
    });

    applyFilters();
  });
