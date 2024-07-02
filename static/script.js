async function searchArtist() {
    const artistName = document.getElementById('artistName').value;
    const songsList = document.getElementById('songsList');
    songsList.innerHTML = '';
    
    try {
        const response = await fetch(`/search?artist_name=${artistName}`);
        if (!response.ok) {
            const errorData = await response.json();
            songsList.innerHTML = `<p>${errorData.error}</p>`;
            return;
        }
        const data = await response.json();
        
        if (data.error) {
            songsList.innerHTML = `<p>${data.error}</p>`;
        } else {
            data.songs.forEach((song, index) => {
                const songItem = document.createElement('li');
                songItem.textContent = `${index + 1}. ${song}`;
                songsList.appendChild(songItem);
            });
        }
    } catch (error) {
        songsList.innerHTML = `<p>Error: ${error.message}</p>`;
    }
}

document.getElementById('searchBtn').addEventListener('click', searchArtist);


