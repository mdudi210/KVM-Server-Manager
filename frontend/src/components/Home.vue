<template>
  <div class="home-container">
    <TopBar :username="username" :role="role" />
    <div class="body">
      <h2 class="page-title">Your Virtual Machines</h2>
      <AlertMsg ref="alertRef" />
      <div class="vm-grid">
        <VmItem
          v-for="vm in vmlist"
          :key="vm.Id"
          :vm="vm"
          @vm-updated="applyVmStateUpdate"
          @refresh-requested="fetchVmList"
        />
      </div>
    </div>
  </div>
</template>

<script>
import VmItem from './VmItem.vue';
import TopBar from './TopBar.vue';
import AlertMsg from './Alert.vue';
import { apiClient, buildWsUrl } from '@/config/api';

export default {
  name: 'VmHome',
  components: {
    VmItem,
    TopBar,
    AlertMsg,
  },
  data() {
    return {
      username: 'User',
      role: 'user',
      vmlist: [],
      socket: null,
      reconnectTimer: null,
      pollTimer: null,
    };
  },
  async mounted() {
    const userInfo = this.getUserInfo();
    this.username = userInfo?.username || 'User';
    this.role = userInfo?.role || 'user';

    await this.fetchVmList();
    this.connectRealtimeUpdates();
    this.startFallbackPolling();
  },
  beforeUnmount() {
    if (this.socket) {
      this.socket.close();
      this.socket = null;
    }
    if (this.reconnectTimer) {
      clearTimeout(this.reconnectTimer);
      this.reconnectTimer = null;
    }
    if (this.pollTimer) {
      clearInterval(this.pollTimer);
      this.pollTimer = null;
    }
  },
  methods: {
    getUserInfo() {
      const raw = sessionStorage.getItem('user-info');
      if (!raw) {
        return null;
      }
      try {
        return JSON.parse(raw);
      } catch (error) {
        return null;
      }
    },
    getToken() {
      return this.getUserInfo()?.access_token || '';
    },
    async fetchVmList() {
      const token = this.getToken();
      if (!token) {
        this.$router.push({ name: 'Login' });
        return;
      }

      try {
        const response = await apiClient.get('/vm', {
          headers: { Authorization: `Bearer ${token}` },
        });
        this.vmlist = response.data.Body.output || [];
      } catch (error) {
        const backendMsg =
          error.response?.data?.detail ||
          error.response?.data?.message ||
          'Unable to fetch VM list';
        this.$refs.alertRef.show(String(backendMsg));
      }
    },
    applyVmStateUpdate(payload) {
      const index = this.vmlist.findIndex((vm) => vm.Name === payload.vm_name);
      if (index >= 0) {
        this.vmlist[index].State = payload.current_state;
      }
    },
    connectRealtimeUpdates() {
      const token = this.getToken();
      if (!token) {
        return;
      }

      const wsUrl = `${buildWsUrl('/ws/vm-updates')}?token=${encodeURIComponent(token)}`;
      this.socket = new WebSocket(wsUrl);

      this.socket.onmessage = (event) => {
        try {
          const message = JSON.parse(event.data);
          if (message.event === 'connected') {
            return;
          }

          if (message.event === 'vm_state_changed') {
            this.applyVmStateUpdate(message);
            this.$refs.alertRef.show(
              `${message.vm_name} is now ${message.current_state} (updated by ${message.updated_by})`
            );
            return;
          }

          if (message.event === 'vm_created' || message.event === 'vm_cloned') {
            this.fetchVmList();
            this.$refs.alertRef.show(`${message.vm_name} is ready in the list`);
            return;
          }

          if (message.event === 'vm_operation_in_progress') {
            this.$refs.alertRef.show(
              `Another operation is running on ${message.vm_name}. Please retry in a moment.`
            );
          }
        } catch (error) {
          console.error('Failed to parse websocket payload', error);
        }
      };

      this.socket.onclose = () => {
        this.socket = null;
        this.reconnectTimer = setTimeout(() => {
          this.connectRealtimeUpdates();
        }, 2500);
      };

      this.socket.onerror = () => {
        if (this.socket) {
          this.socket.close();
        }
      };
    },
    startFallbackPolling() {
      this.pollTimer = setInterval(() => {
        this.fetchVmList();
      }, 30000);
    },
  },
};
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
