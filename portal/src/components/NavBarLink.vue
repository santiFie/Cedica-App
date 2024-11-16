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
  color: white;
  font-weight: 550; /* Cambiado de 500 a 600 para hacer la letra más gruesa */
  justify-content: center;
}
</style>