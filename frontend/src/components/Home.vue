<template>
  <div class="home-container">
    <TopBar :username="username" :role="role"/>
    <div class="body">
      <h2 class="page-title">Your Virtual Machines</h2>
      <AlertMsg ref="alertRef"></AlertMsg>
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
import AlertMsg from './Alert.vue'

export default {
  name: 'VmHome',
  components: {
    VmItem,
    TopBar,
    AlertMsg
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
    const token = JSON.parse(user).access_token

      await axios.get("http://127.0.0.1:8000/vm", {
        headers: { Authorization: `Bearer ${token}` }
      })
      .then(response => {
        this.vmlist = response.data.Body.output
        this.username = JSON.parse(user).username
        this.role = JSON.parse(user).role      
      })
      .catch(error => {
        const backendMsg = error.response.data?.detail || error.response.data?.message || "Something went wrong"
        console.log('API call failed', error)
        this.$refs.alertRef.show(backendMsg)
      })
    }
  // },
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
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
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
