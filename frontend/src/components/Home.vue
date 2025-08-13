<template>
  <div>
    <TopBar :username="username"/>
    <div class="body">
      <VmItem v-for="vm in vmlist"
      :key="vm.Id"
      :name="vm.Name"
      :state="vm.State"
      @action="handleAction"/>
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
      username: '',
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
        this.username = JSON.parse(atob(token.split('.')[1])).sub
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
  methods: {
    handleAction({ name, action }) {
      console.log(`Action "${action}" triggered for ${name}`);
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