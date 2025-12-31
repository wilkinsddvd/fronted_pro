<template>
  <div class="calendar-container">
    <button class="calendar-toggle" @click="toggleShow">
      📅
    </button>
    <div class="calendar-panel" v-if="show">
      <input type="date" v-model="selectedDate" @change="emitDate" />
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
const show = ref(false)
const selectedDate = ref('')
const emit = defineEmits(['select'])

function toggleShow() {
  show.value = !show.value
}
function emitDate() {
  emit('select', selectedDate.value)
}
</script>

<style scoped>
.calendar-container {
  position: fixed;
  top: 16px;
  right: 32px;
}
.calendar-toggle {
  background: #fff;
  border: 1px solid #eee;
  border-radius: 50%;
  width: 38px;
  height: 38px;
  font-size: 1.6em;
  cursor: pointer;
  box-shadow: 0 0 5px #eee;
}
.calendar-panel {
  position: absolute;
  top: 45px;
  right: 0;
  background: #fff;
  box-shadow: 0 0 10px #ddd;
  padding: 12px;
  border-radius: 10px;
}
</style>