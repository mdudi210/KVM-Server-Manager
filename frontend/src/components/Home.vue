<template>
  <div class="home-container">
    <TopBar :username="username" :role="role"/>
    <div class="body">
      <h2 class="page-title">Your Virtual Machines</h2>
      <div class="vm-grid">
        <VmItem 
          v-for="vm in vmlist"
          :key="vm.Id"
          :vm_name="vm.Name"
          :current_state="vm.State"
        />
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import VmItem from './VmItem.vue'
import TopBar from './TopBar.vue'

export default {
  name: 'VmHome',
  components: {
    VmItem,
    TopBar
  },
  data() {
    return {
      username: 'User',
      role: 'user',
      vmlist: []
    }
  },
  async mounted() {
    let user = sessionStorage.getItem('user-info')
    if (!user) {
      this.$router.push({name:'Login'})
    } else {
      const token = JSON.parse(user).access_token
      
      await axios.get("http://127.0.0.1:8000/check-token", {
        headers: { Authorization: `Bearer ${token}` }
      })
      .then(response => {
        if (response.data.valid === false) {
          sessionStorage.removeItem('user-info')
          this.$router.push({name:'Login'})
        }
      })
      .catch(error => {
        console.log('API call failed', error)
      })

      this.username = JSON.parse(user).username
      this.role = JSON.parse(user).role

      await axios.get("http://127.0.0.1:8000/vm", {
        headers: { Authorization: `Bearer ${token}` }
      })
      .then(response => {
        this.vmlist = response.data.Body.output
      })
      .catch(error => {
        console.log('API call failed', error)
      })
    }
  },
}
</script>

<style scoped>
.home-container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  background: linear-gradient(135deg, #f6f9fc, #e3f2fd);
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.body {
  flex: 1;
  padding: 2rem;
}

.page-title {
  font-size: 1.8rem;
  font-weight: bold;
  color: #1976d2;
  margin-bottom: 1.5rem;
  text-align: center;
}

.vm-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  justify-content: center;
  align-items: flex-start;
}

@media (max-width: 768px) {
  .body {
    padding: 1rem;
  }
  
  .page-title {
    font-size: 1.5rem;
  }
}
</style>
