<template>
    <div class="date-picker">
      <div class="block">
        <el-date-picker
          v-model="value1"
          type="date"
          placeholder="Pick a Date"
          format="YYYY-MM-DD"
          date-format="MMM DD, YYYY"
          editable = true
          size='large'
        />
      </div>
    </div>
  </template>
  
  <script lang="ts" setup>
    import { ref } from 'vue'
    
    const value1 = ref('')
  </script>
  <style scoped>
  </style>
  