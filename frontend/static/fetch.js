const getToken = async () => {
    id = config.id;
    secret = config.secret;
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

}

const displaySongs= async(token, id) => {
    const result = await fetch(`https://api.spotify.com/v1/playlists/${id}/tracks`, {
        method: 'GET',
        headers: {'Authorization': 'Bearer ' + token}
    });

    const info = await result.json();
    info.items.forEach(item => {
        const songName = item.track.name;
        const imgUrl = item.track.album.images[2].url
        console.log(imgUrl);
        // const imgUrl = imgUrlList[0].url;
        const div = document.createElement('div');
        div.classList.add('track');
        document.body.appendChild(div);
        nameAndImg(songName, imgUrl, div);
    });
}

function nameAndImg (song, url, div){
    const p = document.createElement('p');
    p.textContent = song;
    div.appendChild(p)

    // const img = document.createElement('img');
}
// getToken();

getToken()
  .then(data => displaySongs(data, "2qjr8xuEYrLoJLgDe6iHbd"));