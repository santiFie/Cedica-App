<script setup>
    import { usePostsStore } from '@/stores/posts'
    import { storeToRefs } from 'pinia'
    import { onMounted } from 'vue'

    const postsStore = usePostsStore()
    const { posts, loading, error, total_pages, page } = storeToRefs(postsStore)

    const fetchPosts = async () => {
        await postsStore.fetchPosts()
    }

    const changePage = async () => {
        await postsStore.changePage()
    }

    const goBackPage = async () => {
        await postsStore.goBackPage()
    }

    onMounted(() => {
        if (!posts.value.length){
            fetchPosts()
        }
    })

    
</script>

<template>
    <div class="wrapper">
        <div class="column1">
            <h2>Publicaciones y Actividades</h2>
            <p v-if="error">Error: {{ error }}</p>
        </div>
        <div class="column2">
            <ul v-if="posts.length > 0">
                <li v-for="post in posts" :key="post.id" class="post-item">
                    <h3 class="post-title">{{ post.title }}</h3>
                    <p class="post-summary">{{ post.summary }}</p>
                    <p class="post-posted_at">{{ post.posted_at }}</p>

                    <RouterLink :to="{ name: 'post', params: { id: post.id } }" class="post-button"> Ver más</RouterLink>
                </li>
            </ul>
            
            <p v-else>No hay publicaciones</p>
            <p v-if="loading">Cargando...</p>
            <div class="page-counter">
                <div>
                    <button v-if="page > 1" @click="goBackPage()" class="page-button">Anterior</button>
                </div>
                <div>
                    <p :style="{ fontSize: '1.3rem' }">Página {{ page }} de {{ total_pages }}</p>
                </div>
                <div>
                    <button v-if="page < total_pages" @click="changePage()" class="page-button">Siguiente</button>
                </div>
            </div>
        </div>
        
    </div>
</template>

<style scoped>

    p{
        color: black;
        font-size: 1.5rem;
        text-align: center;
    }

    h2 {
        color: black;
        font-size: 2rem;
    }

    .wrapper {
        display: flex;
        width: 100%;
    }

    .column1 {
        flex: 1;
        padding: 20px;
    }

    .column2 {
        flex: 3;
        padding: 2%;
        background-color: #ffffff;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }

    .post-item{
        margin-bottom: 20px;
        padding: 10px;
        border: 1px solid #f5f5f5;
        border-radius: 5px;
        background-color: #f5f5f5;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1); /* Sombras para dar profundidad */
        transition: transform 0.2s ease, b; /* Animación al hacer hover */
    }

    .post-item:hover {
        transform: scale(1.02); /* Efecto de zoom */
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2); /* Mayor sombra al hacer hover */
    }

    .post-title {
        font-size: 2rem;
        margin-bottom: 10px;
        text-align: center;
        color: black;
    }
    
    .post-summary {
        font-size: 1.5rem;
        margin-bottom: 10px;
        text-align: justify;
        color: black;
        padding-left: 1%;
        padding-right: 1%;
    }

    .post-posted_at {
        font-size: 1rem;
        margin-bottom: 10px;
        text-align: right;
        color: black;
    }

    .post-button {
        font-size: large;
        font-family: inherit;
        color: black;
        margin: auto;
        margin-left: 40px;
        padding: 0.8%;
        background-color: lightblue;
        border: none;
        border-radius: 5px; /* Added to make the button rounded */
        cursor: pointer;
        transition: background-color 0.3s ease, transform 0.3s ease, box-shadow 0.3s ease;
    }

    .post-button:hover {
        background-color: #58b7ee; /* Azul más oscuro */
        transform: translateY(-2px); /* Efecto de elevación */
    }

    .page-button {
        font-size: large;
        font-family: inherit;
        margin: 1%;
        padding: 14%;
        background-color: lightblue;
        border: none;
        border-radius: 5px; /* Added to make the button rounded */
        display: block;
        cursor: pointer;
        transition: background-color 0.3s ease, transform 0.3s ease, box-shadow 0.3s ease;
    }

    .page-counter {
        display: flex;
        justify-content: center;
        align-items: center;
    }

    .page-counter > div {
        margin: 2%;
    }


</style>