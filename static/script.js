async function searchArtist() {
    const artistName = document.getElementById('artistName').value;
    const response = await fetch(`/search?artist_name=${artistName}`);
    const data = await response.json();
    const songsList = document.getElementById('songsList');
    songsList.innerHTML = '';

    if (data.error) {
        songsList.innerHTML = `<p>${data.error}</p>`;
    } else {
        data.songs.forEach((song, index) => {
            const songItem = document.createElement('li');
            songItem.textContent = `${index + 1}. ${song}`;
            songsList.appendChild(songItem);
        });
    }
}

document.getElementById('searchBtn').addEventListener('click', searchArtist);
