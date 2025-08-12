<template>
  <div>
    <!-- <TopBar :username="username"/> -->
    <Login/>
    <!-- <div class="body">
      <VmItem v-for="vm in vmlist"
      :key="vm.Id"
      :name="vm.Name"
      :state="vm.State"
      @action="handleAction"/>
    </div> -->
  </div>
</template>

<script>
import axios from 'axios'
// import VmItem from './components/VmItem.vue'
// import TopBar from './components/TopBar.vue'
import Login from './components/Login.vue'

export default {
  name: 'App',
  components: {
    // VmItem,
    // TopBar,
    Login
  },
  data() {
    return {
      username: String,
      vmlist: NodeList,
      vmList: [
        { id: 1, Name: 'VM1', State: 'Running'},
        { id: 2, name: 'VM2', state: 'Stopped'},
        { id: 2, name: 'VM2', state: 'Running'},
      ]
    }
  },
  async mounted() {
    const token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ0ZXN0YWRtaW4iLCJpYXQiOjE3NTQ5OTU4ODcsIm5iZiI6MTc1NDk5NTg4NywianRpIjoiMmE0Yzk3YzktMDk0Yi00MTFmLTg3MzQtNDZlMzY0ZDlhNjEyIiwiZXhwIjoxNzU0OTk2Nzg3LCJ0eXBlIjoiYWNjZXNzIiwiZnJlc2giOmZhbHNlLCJpZCI6IjUzMTkyMGE0LTQyN2ItNDVmOC1iN2MyLWQzYzg1Njc2YjNmYyIsInJvbGUiOiJhZG1pbiJ9.AayNbVRBI4FCiKDGNI1nPiaG83VAgrt7KXzw_bOswwc'
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
  },
  methods: {
    handleAction({ name, action }) {
      console.log(`Action "${action}" triggered for ${name}`);
    }
  },

}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 0px;
}
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