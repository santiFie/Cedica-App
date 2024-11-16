<script setup>

import { RouterLink, RouterView } from 'vue-router'
import NavBar from './components/NavBar.vue'
const pages = [
  { name: 'Home', link: '/' },
  { name: 'Contacto', link: '/contact' },
  { name: 'Actividades y Noticias', link: '/posts' },
]

</script>

<template>
  <div class="app-container">
    <header class="header">
      <NavBar :pages="pages" />
    </header>
    
    <main class="main-content">
      <RouterView />
    </main>
  </div>
</template>

<style>
/* Estilos globales */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: Arial, sans-serif;
  line-height: 1.6;
  background-color: #ffffff;
}
</style>

<style scoped>

.app-container {
  min-height: 100vh;
  flex-direction: column;
}

.header {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  background-color: white;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  z-index: 1000;
}

.main-content {
  flex: 1;
  margin-top: 120px; /* Ajusta esto según la altura de tu navbar */
  width: 100%;
}
</style>