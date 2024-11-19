<script setup>
import { usePostsStore } from '@/stores/posts'
import { storeToRefs } from 'pinia'
import { computed, onMounted } from 'vue'

const props = defineProps({
  id: {
    type: String,
    required: true,
  },
})

const postsStore = usePostsStore()
const { loading, error } = storeToRefs(postsStore)

// Asegurarse de que los datos están cargados
onMounted(async () => {
  if (!postsStore.posts.length) {
    await postsStore.fetchPosts()
  }
})


const post = computed(() => postsStore.getPostById(props.id))
</script>

<template>
  <div class="post-container">
    <div v-if="loading">
      <h2>Cargando...</h2>
    </div>
    <div v-else-if="error">
      <h2>{{ error }}</h2>
    </div>
    <div v-if="post == undefined">
      <h2>El post solicitado no existe</h2>
    </div>
    <div v-else>
      <div class="divition">
        <h1 class="post-title">{{ post.title }}</h1>
        <h2 class="post-summary">{{ post.summary }}</h2>
        <h4 class="post-author"><span>Por</span> {{ post.author }}</h4>
        <p class="post-posted_at">Publicado el {{ new Date(post.posted_at).toLocaleDateString() }}</p>
      </div>
      <div class="divition">
        <p class="post-content">{{ post.content }}</p>
      </div>
    </div>
  </div>

</template>

<style scoped>

  .post-container {
    background-color: whitesmoke;
    margin: 2%;
    padding: 2%;
    border-radius: 10px;
    height: 100%
  }

  .post-title {
    font-size: 2rem;
    color: black;
    text-align: center;
    font-weight: bold;
  }

  .post-summary {
    font-size: 1.5rem;
    color: rgb(107, 103, 103);
    margin-left: 2%;
    margin-right: 2%;
    margin-bottom: 2%;
  }

  .post-author {
    font-size: medium;
    color: black;
    margin-top: 2%;
    margin-left: 2%;
    margin-bottom: 0.5%;
  }

  .post-posted_at {
    font-size: small;
    color: black;
    margin-left: 2%;
  }

  .post-content {
    font-size: 1.2rem;
    color: black;
    text-align: left;
    margin-bottom: 2%;
    margin-left: 2%;
  }

  .divition {
    padding: 1.5rem; /* Espaciado interno para separar el contenido del borde */
    border-radius: 10px; /* Bordes redondeados */
    background-color: #ffffff; /* Fondo blanco para destacar sobre el fondo general */
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); /* Sombras sutiles para dar profundidad */
    border: 1px solid #e0e0e0; /* Línea sutil que define la separación */
  }

  h2 {
    color: black;
    font-size: 2rem;
  }

  
</style>
