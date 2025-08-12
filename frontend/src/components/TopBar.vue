<template>
  <div class="topbar">
    <div class="logo">
      <h2>⚙ VM Manager</h2>
    </div>
    <div class="user-section">
      <button title="User Profile">{{ username }}</button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'TopBar',
  props: {
    username: {
      type: String,
      default: 'User'
    }
  }
}
</script>

<style scoped>
.topbar {
  width: auto;
  min-height: 60px;
  padding: 0 20px;
  
  display: flex;
  justify-content: space-between;
  align-items: center;

  background: linear-gradient(90deg, #d21919, #2196f3);
  color: white;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}

.logo h2 {
  margin: 0;
  font-weight: 600;
  font-size: 1.4rem;
}

.user-section button {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  background: white;
  color: rgb(221, 27, 27);
  border: none;
  font-weight: bold;
  font-size: 1.1rem;
  cursor: pointer;
  /* transition: background 0.2s, transform 0.2s; */
}

.user-section button:hover {
  background: #f0f0f0;
  transform: scale(1.05);
}
</style>
