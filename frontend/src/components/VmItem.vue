<template>
   <div class="item" :class="{ colorr: state === 'shut off', colorg : state === 'running' }" >
    <div class="info">
      <p><strong>{{ name }}</strong></p>
      <div>
        <p id="status" >Status: {{ state }}</p>
      </div>
    </div>
    <div>
      <button value="start">Start</button>
      <button value="shut down">Shut Down</button>
      <button value="reboot">Reboot</button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'VmItem',
  props: {
    name: String,
    state: String
  },
  data() {
    return {
      selectedAction: ''
    };
  },
  methods: {
    emitAction() {
      this.$emit('action', {
        name: this.name,
        action: this.selectedAction
      });
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

.controls {
  display: flex;
  align-items: center;
  gap: 10px;
}

select {
  padding: 4px 8px;
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

button:hover {
  background-color: #0056b3;
}

.item.colorr {
    background-color: rgba(255, 72, 0, 0.767);
}
.item.colorg {
    background-color: rgba(0, 128, 53, 0.623);
}
</style>


