<template>
  <div class="login-container">
    <div class="login-card">
      <h2 class="title">Login</h2>
      <input type="text" placeholder="Enter your Username" v-model="username" required>
      <input type="password" placeholder="Enter your Password" v-model="password" required>
      <button>Login</button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'LogIn',
  data () {
    return {
      token: '',
      username: '',
      password: '' 
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

/* Card styling */
.login-card {
  background: white;
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 6px 20px rgba(0,0,0,0.1);
  width: 300px;
  text-align: center;
}

/* Title */
.title {
  margin-bottom: 1.5rem;
  font-family: Arial, sans-serif;
  color: #333;
}

/* Inputs */
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

/* Button */
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
