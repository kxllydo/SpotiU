const getToken = async () => {
    const fs = require('fs').promises;
    const info = await fs.readFile('info.json', 'utf8');
    const json = JSON.parse(info);
    const id = json.CLIENT_ID;
    const secret = json.CLIENT_SECRET;
    const base64Encoded = btoa(id + ':' + secret);

    const result = await fetch('https://accounts.spotify.com/api/token', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': 'Basic ' + base64Encoded
        },
        body: 'grant_type=client_credentials'
    });

    const data = await result.json();
    return data.access_token;
    // console.log(data.access_token);
}



const getSongs = async (token, id) => {
    const result = await fetch(`https://api.spotify.com/v1/playlists/${id}/tracks`, {
        method: 'GET',
        headers: {'Authorization': 'Bearer ' + token}
    });

    const items = await result.json();
    const container = document.getElementsByClassName('container')[0];
    container.innerHTML = ''; // Clear container's contents

    items.items.forEach(item => {
        const songName = item.track.name;
        const pElement = document.createElement('p');
        pElement.textContent = songName; // Set song name as text content
        console.log(songName);
        container.appendChild(pElement); // Append <p> element to song container
    });

    // for (let i = 0; i < items.items.length; i++){
    //     console.log(items.items[i].track.name)
    // }
}

// getToken();

getToken()
  .then(data => getSongs(data, "2qjr8xuEYrLoJLgDe6iHbd"));