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
  <div id=app class="wrapper">
    <header>
      <nav>
        <NavBar :pages="pages" />
      </nav>
    </header>
    <body>
      <h1> Bienvenido a la página de CEDICA </h1>
    </body>
    <RouterView />  
  </div>
</template>

<style scoped>
header {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  z-index: 1000;
  background-color: white;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  display: flex;
  align-items: center;
  padding: 0.5rem 1rem; /* Ajuste de padding para hacer la navbar más pequeña */
}
body {
  background-color: white;
}

.wrapper {
  margin-top: 3rem; /* Ajuste de margen para evitar que el contenido se solape con la navbar */
  padding: 1rem;
  font-family: Arial, sans-serif;
  line-height: 1.6;
  max-width: 800px;
  margin: 0 auto;

}
</style>
