<script setup>
import { RouterLink, RouterView } from 'vue-router'
import Home from './components/Home.vue'
import Posts from './components/Posts.vue'
</script>

<template>
  <header>
    <img alt="Vue logo" class="logo" src="@/assets/logoCEDICA.png" width="350" height="250"/>

    <nav class="wrapper">
        <RouterLink to="/">Home</RouterLink>
        <RouterLink to="/contact">Contacto</RouterLink>
        <RouterLink to="/posts">Actividades y Noticias</RouterLink>
    </nav>
    
  </header>

  <RouterView  />
  
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

.logo {
  width: 120px; /* Tamaño reducido del logo */
  height: auto;
  margin-right: 1rem;
}

nav {
  margin-top: auto;
  display: flex;
  gap: 0.5rem; /* Menor espacio entre los enlaces */
  justify-content: center; /* Centra los botones horizontalmente */
  width: 100%; /* Asegura que el nav ocupe todo el ancho disponible */
}

nav a {
  text-decoration: none;
  color: #333;
  font-weight: bold;
  font-size: 1.3rem; /* Tamaño de fuente reducido */
  padding: .40rem 0.50rem; /* Padding más pequeño en los enlaces */
  margin-block: 0.5rem; /* Espacio entre los enlaces */
  border-radius: 3px;
  justify-content: center;
  transition: background-color 0.3s, color 0.3s;

}

nav a.router-link-exact-active {
  background-color: #3498db;
  color: white;
}

nav a:hover {
  background-color: #2980b9;
  color: white;
}

/* Ajustes para el contenido debajo del header */
.wrapper {
  margin-top: 80px; /* Deja espacio para el header fijo más pequeño */
}

@media (min-width: 1024px) {
  header {
    padding: 0.5rem 2rem;
  }

  nav {
    gap: 1rem;
  }
}
</style>
