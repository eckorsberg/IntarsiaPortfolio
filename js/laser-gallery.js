// laser-gallery.js
// -----------------------------------------------------------------------------
// Purpose
//   - Simple gallery loader for laser.html (no filters).
//   - Reads laser.json and renders clickable cards that navigate to item.file.
//
// Assumptions
//   - laser.html contains a container with class ".gallery".
//   - laser.json entries provide:
//       * item.thumbnail (image URL)
//       * item.title     (caption)
//       * item.file      (detail page URL)
//   - Clicking anywhere on the card should navigate to item.file.
//
// Safe modification points
//   - If you want to show optional metadata (artist/status), the commented-out
//     sections below are the intended place to re-enable.
//   - If you want the thumbnail itself to be a link instead of card click,
//     you would replace the card click handler with an <a> wrapper.
//
// Notes
//   - This file intentionally does not share filtering code with the main gallery
//     to keep laser.html extremely simple and robust.

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
