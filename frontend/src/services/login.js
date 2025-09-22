import axios from 'axios'

export async function login(username,password) {
    let response = await axios.post("http://127.0.0.1:8000/login", {
        username: username,
        password: password
    })
    
    return response
}