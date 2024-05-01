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
        const div = document.createElement('div');
        div.classList.add('track');

        const container = document.getElementsByClassName('flex-container')[0]
        container.appendChild(div);
        nameAndImg(songName, imgUrl, div);
    });
}

function nameAndImg (song, url, div){
    const img = document.createElement('img');
    img.src = url;
    div.appendChild(img);

    const p = document.createElement('p');
    p.textContent = song;
    div.appendChild(p)
}

const getID = async () => {
    const response = await fetch ("http://127.0.0.1:5000/home");
    const id = response.statusText;
    return id;
}


const run = async () => {
    const token = await getToken();
    const id = await getID();
    displaySongs(token, id);
}

run()