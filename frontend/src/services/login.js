import axios from 'axios'
import { buildApiUrl } from '@/config/api'

export async function login(username,password) {
    let response = await axios.post(buildApiUrl('/login'), {
        username: username,
        password: password
    })
    
    return response
}
