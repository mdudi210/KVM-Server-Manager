<template>
  <div>
    <TopBar :username="username" :role="role"/>
    <div class="body">
      <VmItem v-for="vm in vmlist"
      :key="vm.Id"
      :vm_name="vm.Name"
      :current_state="vm.State"/>
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
    if(!user){
      this.$router.push({name:'Login'})
    }
    else {
      const token = JSON.parse(sessionStorage.getItem('user-info')).access_token
      await axios.get("http://127.0.0.1:8000/check-token",{
        headers: {
          Authorization: `Bearer ${token}`
        }
      })
      .then(response => {
        console.log(response.data)
        if(response.data.valid === false){
          console.log(response)
          sessionStorage.removeItem('user-info')
          this.$router.push({name:'Login'})
        }
      })
      .catch(error => {
        console.log('API call failed',error)
      })

      this.username = JSON.parse(sessionStorage.getItem('user-info')).username
      this.role = JSON.parse(sessionStorage.getItem('user-info')).role
      await axios.get("http://127.0.0.1:8000/vms",{
        headers: {
          Authorization: `Bearer ${token}`
        }
      })
      .then(response => {
        this.vmlist = response.data.Body.output
        console.log(this.vmlist)
      })
      .catch(error => {
        console.log('API call failed',error)
      })
    }
  },
}
</script>

<style scoped>
li {
  list-style: none;
}
.header {
  margin: 10px;
}
.body {
  margin: 20px;
}
</style>