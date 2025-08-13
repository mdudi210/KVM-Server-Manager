<template>
  <div class="login-container">
    <div class="login-card">
      <h2 class="title">Login</h2>
      <input type="text" placeholder="Enter your Username" v-model="username" required>
      <input type="password" placeholder="Enter your Password" v-model="password" required>
      <button @click="login">Login</button>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'LogIn',
  data () {
    return {
      token: '',
      username: '',
      password: '' 
    }
  },
  methods: {
    async login() {
    try {
      let response = await axios.post("http://127.0.0.1:8000/login",{
        username: this.username,
        password: this.password
      })
      if(response.status==200){
        sessionStorage.setItem('user-info',JSON.stringify(response.data))
        this.token = response.data.access_token; 
        this.username = JSON.parse(atob(this.token.split('.')[1])).sub;
        console.log("Login successful:", this.username);
        this.$router.push({name:'VmHome'})
      }
    } catch (error) {
        console.error("Login failed:", error.response?.data || error.message);
    }
    },
  },
  mounted(){
    let user = sessionStorage.getItem('user-info')
    if(user){
      this.$router.push({name:'VmHome'})
    }
  }
}
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background: linear-gradient(120deg, #f6f9fc, #e3f2fd);
}

.login-card {
  background: white;
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 6px 20px rgba(0,0,0,0.1);
  width: 300px;
  text-align: center;
}

.title {
  margin-bottom: 1.5rem;
  font-family: Arial, sans-serif;
  color: #333;
}

input {
  width: 100%;
  padding: 10px;
  margin-bottom: 1rem;
  border: 1px solid #ccc;
  border-radius: 8px;
  font-size: 14px;
  outline: none;
  transition: border-color 0.2s;
}

input:focus {
  border-color: #1976d2;
}

button {
  width: 100%;
  padding: 10px;
  background: #1976d2;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  cursor: pointer;
  transition: background 0.2s;
}

button:hover {
  background: #125aa1;
}
</style>
