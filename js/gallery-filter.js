
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
	  galleryContainer.className = "gallery";

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
		  link.target = "_blank";
		  link.className = "gallery-link";

		  const img = document.createElement("img");
		  img.src = item.thumbnail;
		  img.alt = item.title;
		  img.classList.add("gallery-img");
		  console.log("Added class:", img.className, "to", img.src);


		  const caption = document.createElement("p");
		  caption.className = "gallery-caption";
		  caption.innerText = item.title;

		  link.appendChild(img);
		  link.appendChild(caption);
		  galleryContainer.appendChild(link); // direct child of .gallery
		}
	  });
	}

    Object.values(filters).forEach(select => {
      select.addEventListener("change", applyFilters);
    });

    applyFilters();
  });
