const getTokenAndLog = async () => {
    const id = "c584a76f0e49433ab86e6b25fcc3aa2b";
    const key = "8bf8ac459e444362b38b6af8f1563a87";

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
        console.log(data.access_token);
    } catch (error) {
        console.error('Error fetching token:', error);
    }
};

getTokenAndLog();
