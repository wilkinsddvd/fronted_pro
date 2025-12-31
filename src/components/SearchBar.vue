<template>
  <div class="search-bar">
    <input
      v-model="keyword"
      @keyup.enter="emitSearch"
      placeholder="搜索博客..."
      class="search-input"
    />
    <button @click="emitSearch" class="search-btn">搜索</button>
  </div>
</template>

<script setup>
import { ref } from 'vue'
const keyword = ref('')
const emit = defineEmits(['search'])

function emitSearch() {
  emit('search', keyword.value)
}
</script>

<style scoped>
.search-bar {
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 32px auto 24px auto;
  max-width: 680px;
  background: #181920;
  box-shadow: 0 4px 24px #0001;
  border-radius: 16px;
  padding: 24px;
}

.search-input {
  flex: 1;
  padding: 12px 18px;
  font-size: 1em;
  margin-right: 20px;
  border: 1px solid #aaa;
  border-radius: 6px;
  background: #23242a;
  color: #fff;
  transition: border-color 0.2s;
}

.search-input:focus {
  border-color: #228be6;
}

.search-btn {
  padding: 10px 36px;
  border-radius: 6px;
  background: #228be6;
  color: #fff;
  border: none;
  cursor: pointer;
  font-weight: bold;
  box-shadow: 0 2px 8px #228be661;
  transition: background 0.2s;
}

.search-btn:hover {
  background: #025fbb;
}
</style>