<template>
  <div class="time-picker">
    <div class="block">
      <el-time-picker 
      v-model="value1" 
      placeholder="Enter time" 
      size="large"
      />
    </div>
  </div>
</template>
  
  <script lang="ts" setup>
  import { ref } from 'vue'
  const value1 = ref()
  const value2 = ref()
  </script>
  
  <style scoped>

  </style>