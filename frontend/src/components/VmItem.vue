<template>
  <div class="item" :class="{ colorr: current_state === 'shut off', colorg : current_state === 'running' }">
    <div class="info">
      <p><strong>{{ vm_name }}</strong></p>
      <div>
        <p id="status">Status: {{ current_state }}</p>
      </div>
    </div>
    <div>
      <button 
        @click="changestate('start')" 
        :disabled="current_state !== 'shut off'">
        Start
      </button>
      <button 
        @click="changestate('shutdown')" 
        :disabled="current_state !== 'running'">
        Shut Down
      </button>
      <button 
        @click="changestate('reboot')" 
        :disabled="current_state !== 'running'">
        Reboot
      </button>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'VmItem',
  props: {
    vm_name: String,
    current_state: String
  },
  methods: {
    async changestate(state) {
      try {
        const token = JSON.parse(sessionStorage.getItem('user-info')).access_token;
        this.username = JSON.parse(atob(token.split('.')[1])).sub;

        const response = await axios.post("http://127.0.0.1:8000/vm/state", {
          state: state,
          name: this.vm_name
        }, {
          headers: {
            Authorization: `Bearer ${token}`
          }
        });

        console.log(response.data.Body.output);
        this.$router.go(0);
      } catch (error) {
        console.error('API call failed', error);
      }
    }
  }
};
</script>

<style scoped>
.item {
  width: 100%;
  min-height: 60px;
  border: 1px solid #ccc;
  border-radius: 8px;
  padding: 12px 16px;
  margin-bottom: 12px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-sizing: border-box;
  background-color: #f9f9f9;
}

.info {
  display: flex;
}

.info p {
  margin: 2px 0;
}

button {
  margin: 12px;
  padding: 4px 12px;
  cursor: pointer;
  background-color: #007bff;
  border: none;
  border-radius: 4px;
  color: white;
}

button:hover:enabled {
  background-color: #0056b3;
}

button:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}

.item.colorr {
  background-color: rgba(255, 72, 0, 0.767);
}

.item.colorg {
  background-color: rgba(0, 128, 53, 0.623);
}
</style>
