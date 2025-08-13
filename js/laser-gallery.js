
// laser-gallery.js
// Simple gallery loader for laser.html (no filters)

fetch('laser.json')
  .then(response => response.json())
  .then(data => {
    const galleryContainer = document.querySelector('.gallery');
    galleryContainer.innerHTML = '';

    data.forEach(item => {
      const card = document.createElement('div');
      card.className = 'gallery-item';

      const thumb = document.createElement('img');
      thumb.src = item.thumbnail;
      thumb.alt = item.title;
      thumb.className = 'gallery-thumb';
      card.appendChild(thumb);

      const title = document.createElement('p');
      title.className = 'gallery-title';
      title.textContent = item.title;
      card.appendChild(title);

      //if (item.artist) {
      //  const artist = document.createElement('p');
      //  artist.className = 'gallery-artist';
      //  artist.textContent = item.artist;
      //  card.appendChild(artist);
      //}

      //if (item.status && item.status.toLowerCase() !== "available") {
      //  const status = document.createElement('p');
      //  status.className = 'gallery-status';
      //  status.textContent = item.status;
      //  card.appendChild(status);
      //}

      card.addEventListener('click', () => {
        window.location.href = item.file;
      });

      galleryContainer.appendChild(card);
    });
  })
  .catch(error => {
    console.error('Failed to load laser gallery:', error);
  });
