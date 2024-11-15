<script setup>
import { defineProps } from 'vue'
import NavBarLink from '@/components/NavBarLink.vue'
defineProps({
  pages: {
    type: Array,
    required: true,
  },
})
</script>

<template>
  
  <img alt="Vue logo" class="logo" src="@/assets/logoCEDICA.png" width="150" height="100"/>
    
  <ul class="nav">
    <li v-for="page in pages" :key="page.id">
      <NavBarLink
          :link="page.link"
          :name="page.name">
      </NavBarLink>
    </li>
  </ul>
  
</template>

<style scoped>
.header {
    background-color: #42b983;
    color: white;
    padding: 1rem;
    text-align: center;
    width: 100%;
    display: flex;}

.logo {
  width: 120px; /* Tamaño reducido del logo */
  height: auto;
  margin-right: 1rem;
}

.nav {
  margin-top: auto;
  display: flex;
  gap: 0.5rem; /* Menor espacio entre los enlaces */
  justify-content: center; /* Centra los botones horizontalmente */
  width: 100%; /* Asegura que el nav ocupe todo el ancho disponible */
}

</style>