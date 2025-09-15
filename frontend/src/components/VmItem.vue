<template>
  <div class="vm-card" :class="[statusClass,statusChangeClass]">
    <div class="vm-info">
      <p class="vm-name"><strong>{{ vm_name }}</strong></p>
      <p class="vm-status">Status: <span :class="statusTextClass">{{ current_state }}</span></p>
    </div>
    <div class="vm-actions">
      <button 
        v-if="current_state === 'shut off'"
        class="action-btn start-btn"
        :disabled="changing_state"
        @click="changestate('start')">
        <span v-if="!changing_state">Start</span>
        <span v-else>⏳ Changing...</span>
      </button>
      <button 
        v-if="current_state === 'running'"
        class="action-btn shutdown-btn"
        :disabled="changing_state"
        @click="changestate('shutdown')">
        <span v-if="!changing_state">Shut Down</span>
        <span v-else>⏳ Changing...</span>
      </button>

      <button 
        v-if="current_state === 'running'"
        class="action-btn reboot-btn"
        :disabled="changing_state"
        @click="changestate('reboot')">
        <span v-if="!changing_state">Reboot</span>
        <span v-else>⏳ Changing...</span>
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
  data() {
    return {
      changing_state: false
    }
  },
  computed: {
    statusClass() {
      return this.current_state === 'running' ? 'status-running' : 'status-stopped';
    },
    statusTextClass() {
      return this.current_state === 'running' ? 'text-green' : 'text-red';
    },
    statusChangeClass() {
      return this.changing_state === true ? 'disable-status' : 'enable-status';
    }
  },
  methods: {
    async changestate(state) {
      try {
        this.changing_state = true
        const token = JSON.parse(sessionStorage.getItem('user-info')).access_token;
        this.username = JSON.parse(atob(token.split('.')[1])).sub;

        const response = await axios.post("http://127.0.0.1:8000/vm/state", 
          { state: state, name: this.vm_name },
          { headers: { Authorization: `Bearer ${token}` } }
        );
        console.log(response.data.Body.output);
        
        await setTimeout(() => {
          console.log("One minute has passed!");

          axios.get("http://127.0.0.1:8000/vm", {
            params: {
              vm_name : this.vm_name
            },
            headers: { Authorization: `Bearer ${token}` }
          })
          .then(response => {
            console.log("hello")
            console.log(response.data.Body.output)
          })
          .catch(error => {
            console.log('API call failed', error)
          })

          this.$parent.vmlist.forEach(element => {
          if(element.Name === this.vm_name){
            if(state === "shutdown"){
              state = "shut off"
            }else if(state === "start"){
              state = "running"
            }else if(state == 'reboot'){
              state = 'running'
            }
            element.State = state
          } 
        });

        this.changing_state = false

        }, 60000);
        
      } catch (error) {
        console.error('API call failed', error);
      }
    }
  }
};
</script>

<style scoped>
.vm-card {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
  padding: 16px;
  margin-bottom: 16px;
  transition: all 0.3s ease;
  border-left: 6px solid transparent;
}

.status-running {
  border-left-color: #28a745;
}

.status-stopped {
  border-left-color: #dc3545;
}

.disable-status {
  background: #aca7a7;
}

.enable-status {
  background: white;
}

.changing-status {
   display: flex;
}

.vm-info {
  margin-bottom: 12px;
}

.vm-name {
  font-size: 1.1rem;
  color: #1976d2;
  margin: 0 0 4px 0;
}

.vm-status {
  font-size: 0.9rem;
  color: #666;
  margin: 0;
}

.text-green {
  color: #28a745;
  font-weight: 600;
}

.text-red {
  color: #dc3545;
  font-weight: 600;
}

.vm-actions {
  display: flex;
  gap: 8px;
}

.action-btn {
  flex: 1;
  min-width: 80px;
  padding: 8px 12px;
  font-size: 0.9rem;
  font-weight: 500;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.start-btn {
  background: #28a745;
  color: white;
}

.shutdown-btn {
  background: #dc3545;
  color: white;
}

.reboot-btn {
  background: #ffc107;
  color: #333;
}

.action-btn:hover:enabled {
  opacity: 0.85;
  transform: translateY(-1px);
}

.action-btn:disabled {
  background: #ccc;
  cursor: not-allowed;
}

@media (max-width: 600px) {
  .vm-card {
    padding: 12px;
  }

  .vm-actions {
    flex-direction: column;
  }

  .action-btn {
    width: 100%;
  }
}
</style>
