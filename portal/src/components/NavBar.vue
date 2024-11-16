<script setup>
import { defineProps } from 'vue'
import { ref } from 'vue';
import NavBarLink from '@/components/NavBarLink.vue'
defineProps({
  pages: {
    type: Array,
    required: true,
  },
})

// Reactividad
const highlightedButton = ref(null);

// Métodos
function highlight(id) {
  highlightedButton.value = id; // Resalta el botón actual
}

function unhighlight(id) {
  if (highlightedButton.value === id) {
    highlightedButton.value = null; // Quita el resaltado
  }
}
</script>

<template>    
  <div class="header">
    <img alt="Vue logo" class="logo" src="@/assets/logoCEDICA.png" width="150" height="100"/>
  
    <ul class="nav">
      <li 
        v-for="page in pages"
        :key="page.name"
        @mouseover="highlight(page.name)"
        @mouseleave="unhighlight(page.name)"
        :class="{ highlighted: highlightedButton === page.name }"
      >
        <NavBarLink
            :link="page.link"
            :name="page.name">
        </NavBarLink>
      </li>
    </ul>
  </div>
  
</template>

<style scoped>
.header {
  background-color: #42b983;
  color: white;
  padding: 1rem;
  text-align: center;
  width: 100%;
  display: flex;}


.nav {
  margin-top: auto;
  display: flex; /* Alinea los enlaces horizontalmente */
  gap: 3.5rem; /* Menor espacio entre los enlaces */
  justify-content: center; /* Centra los botones horizontalmente */
  width: 100%; /* Asegura que el nav ocupe todo el ancho disponible */
}

.logo {
  width: 120px; /* Tamaño reducido del logo */
  height: auto;
  padding: auto;
  margin: auto;
}

li {
  display: inline;
  background-color: #58b7ee;
  justify-content: center;
  padding: 0.7rem 1rem; /* Aumenta el tamaño del padding */
  border-radius: 5px;
  margin: 0.7rem; /* Aumenta el tamaño del margen */
  cursor: pointer;
  font-size: 1.2rem; /* Aumenta el tamaño de la fuente */
}

li.highlighted {
  background-color: #42a5f5; /* Color resaltado */
  transform: scale(1.05); /* Efecto de zoom */
}




</style>