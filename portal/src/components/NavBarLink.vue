<script setup>
import { defineProps } from 'vue'
defineProps({
  link: {
    type: String,
    required: true,
  },
  name: {
    type: String,
    required: true,
  }
})
</script>

<template>
  <a :href="link" class="nav-link">
    <slot>{{ name }} </slot>
  </a>
</template>

<style scoped>
.nav-link {
  color: #42b983;
  font-weight: 500;
  text-decoration: none;
  margin-right: 1rem;
}
</style>