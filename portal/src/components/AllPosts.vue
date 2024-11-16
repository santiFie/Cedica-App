<script setup>
    import { usePostsStore } from '@/stores/posts'
    import { storeToRefs } from 'pinia'
    import { onMounted } from 'vue'

    const postsStore = usePostsStore()
    const { posts, loading, error } = storeToRefs(postsStore)

    const fetchPosts = async () => {
        await postsStore.fetchPosts()
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
            <p v-if="loading">Cargando...</p>
            <p v-else-if="error">Error: {{ error }}</p>
            <p v-else-if="!posts.length">No hay publicaciones</p>
        </div>
        <div v-if="posts.length>0" class="column2">
            <ul>
                <li v-for="post in posts" :key="post.id">
                    <h3 class="post-title">{{ post.title }}</h3>
                    <p class="post-summary">{{ post.summary }}</p>
                    <p class="post-posted_at">{{ post.posted_at }}</p>
                    <form action="/post" method="post">
                        <input type="hidden" name="id" :value="post.id">
                        <button type="submit">Ver más</button>
                    </form>
                </li>
            </ul>
        </div>
    </div>
</template>

<style scoped>

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
        padding: 20px;

    }

    li{
        margin-bottom: 20px;
        padding: 10px;
        border: 1px solid black;
        border-radius: 5px;
        background-color: #f5f5f5;
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
    }

    .post-posted_at {
        font-size: 1rem;
        margin-bottom: 10px;
        text-align: right;
        color: black;
    }


</style>