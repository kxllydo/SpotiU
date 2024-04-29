

// async function getInfo(endpoint) {
//     const baseURL = "http://127.0.0.1:5000"

//     try{
//         const before = await fetch("http://127.0.0.1:5000/home", {
//             method: 'POST',
//             headers: {
//                 "Content-Type": "application/json"
//             }
//         }) //`${baseURL}/${endpoint}`)
//         const huh = before.json()
//         console.log(huh)
//         // const tokenInfo = await token.json();
//         // const final = tokenInfo.access_token

//     }catch (error) {
//         console.error('Error:', error)
//     }
// }

// getInfo("home")

        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
// const getToken = async() => {

//     id =  "c584a76f0e49433ab86e6b25fcc3aa2b"
//     key = "8bf8ac459e444362b38b6af8f1563a87"
//     const result = await fetch('https://accounts.spotify.com/api/token', {
//         method: 'POST',
//         headers: {
//             'Content-Type' : 'application/x-www-form-urlencoded',
//             'Authorization' : 'Basic' + btoa(id + ':' + key)
//         },
//         body: 'grant_type-client_credentials'
//     });

//     const data = await result.json();
//     return data.access_token;

// } 
        

// console.log(getToken())

const getToken = async () => {
    const id = "c584a76f0e49433ab86e6b25fcc3aa2b";
    const key = "8bf8ac459e444362b38b6af8f1563a87";

    const result = await fetch('https://accounts.spotify.com/api/token', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': 'Basic ' + Buffer.from(id + ':' + key).toString('base64')
        },
        body: 'grant_type=client_credentials' // Fixed the body format
    });

    const data = await result.json();
    return data.access_token;
};

// Use async/await to wait for the promise to resolve
const main = async () => {
    const token = await getToken();
    console.log(token);
};

// Call the main function to start the asynchronous operation
main();
