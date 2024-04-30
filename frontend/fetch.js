async function getToken () {
    try {
        const result = await fetch('https://accounts.spotify.com/api/token', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Authorization': 'Basic ' + Buffer.from(process.env.CLIENT_ID + ':' + process.env.CLIENT_SECRET).toString('base64')
            },
            body: 'grant_type=client_credentials'
        });

        const data = await result.json();
        return data.access_token;
    } catch (error) {
        console.error('Error fetching token:', error);
    }
}

async function refreshToken(refreshToken) {
    const requestBody = new URLSearchParams();
    requestBody.append('grant_type', 'refresh_token');
    requestBody.append('refresh_token', refreshToken);

    try {
        const result = await fetch('https://accounts.spotify.com/api/token', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Authorization': 'Basic ' + Buffer.from(process.env.CLIENT_ID + ':' + process.env.CLIENT_SECRET).toString('base64')
            },
            body: requestBody
        });

        const data = await result.json();
        console.log(data);
    } catch (error) {
        console.error('Error refreshing token:', error);
    }
}



async function getUserID (token) {
    console.log(token);
    try{
        const items = await fetch("https://api.spotify.com/v1/me", {
            method: "GET",
            headers: {
                'Authorization': 'Bearer ' + token,
                "Content-Type": "application/json"
            }
        });
        const result = await items.json();
        console.log(result);
    } catch (error) {
        console.error('Oopsies', error);
    }
}

getToken().then(data => getUserID(data));