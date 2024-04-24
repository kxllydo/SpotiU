const baseURL = "http://127.0.0.1:5000"

async function getInfo(endpoint) {
    try{
        const response = await fetch('${baseURL}/${endpoint}');
        const data = await response.text();
        console.log(data)
    }catch (error) {
        console.error('Error:', error)
    }
}
        
getInfo()
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        // id=  "c584a76f0e49433ab86e6b25fcc3aa2b"
// key = "8bf8ac459e444362b38b6af8f1563a87"
// const url = "/token"

// fetch("https://api.spotify.com/v1/me", {
//     headers: {
//         'Authorization'
//     }
// })
// .then(res => res.json())
// .then(data => console.log(data)), 
// .catch(error => console.log("ERROR")) 

// async function getUserInfo() {
//     try {
//         // Fetch the access token from the Flask backend
//         const response = await fetch('/token');
//         const data = await response.json();
//         const accessToken = data.access_token;

//         // Make a fetch request to the Spotify API with the access token
//         const userInfoResponse = await fetch('https://api.spotify.com/v1/me', {
//             headers: {
//                 'Authorization': `Bearer ${accessToken}`
//             }
//         });

//         // Handle the response
//         const userInfo = await userInfoResponse.json();
//         console.log(userInfo);
//     } catch (error) {
//         console.error('Error:', error);
//     }
// }

// // Call the function to fetch user information
// getUserInfo();