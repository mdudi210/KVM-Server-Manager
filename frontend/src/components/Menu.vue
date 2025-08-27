<template>
  <div v-if="isVisible" class="side-panel-overlay" @click.self="closePanel">
    <div class="side-panel-content">
      <div class="side-panel-header">
        <button class="close-btn" @click="closePanel">✕</button>
        <div class="user-info">
          <span class="username">{{ username[0].toUpperCase() + username.substring(1) }}</span>
          <img :src="profilePhoto" alt="Profile" class="profile-photo" />
        </div>
      </div>

      <div class="side-panel-body">
        <div v-if="role === '6f057cf8-93c7-4335-9729-3c92404c95f1'">
          <h4>Admin Dashboard</h4>
        </div>
        <div v-else>
          <h4>User Dashboard</h4>
        </div>
        <div></div>
      </div>

      <div class="side-panel-footer">
        <button @click="logout">Logout</button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ProfileMenu',
  props: {
    isVisible: {
      type: Boolean,
      required: true
    },
    username: {
      type: String,
    },
    profilePhoto: {
      type: String,
    },
    role: {
      type: String,
    }
  },
  data() {
    return {
      // role: JSON.parse(sessionStorage.getItem('user-info')).role
    }
  },
  methods: {
    closePanel() {
      this.$emit('close');
    },
    logout() {
      sessionStorage.removeItem('user-info');
      this.$router.push({ name: 'Login' });
    }
  }
};
</script>

<style scoped>
.side-panel-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: flex-end;
  z-index: 1000;
}

.side-panel-content {
  width: 300px;
  background-color: white;
  box-shadow: -2px 0 5px rgba(0, 0, 0, 0.2);
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: space-between; 
}

.side-panel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 15px;
  border-bottom: 1px solid #ddd;
}

.close-btn {
  background: none;
  border: none;
  font-size: 20px;
  cursor: pointer;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 8px;
}

.username {
  font-weight: 600;
  color: #d21919;
}

.profile-photo {
  width: 35px;
  height: 35px;
  border-radius: 50%;
  object-fit: cover;
}

.side-panel-body {
  flex: 1; 
  padding: 20px;
  overflow-y: auto;
  color: black;
}

.side-panel-footer {
  padding: 15px;
  border-top: 1px solid #ddd;
  display: flex;
  justify-content: center;
}

.side-panel-footer button {
  width: 100%;
  padding: 10px;
  background-color: #007bff;
  border: none;
  border-radius: 4px;
  color: white;
  cursor: pointer;
}
</style>
