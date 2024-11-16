import { defineStore } from 'pinia'
import axios from 'axios'

export const usePostsStore = defineStore('posts', {
  state: () => ({
    posts: [],
    loading: false,
    error: null,
  }),

  actions: {
    async fetchPosts() {
      try {
        const response = await axios.get('http://127.0.0.1:5000/api/posts')
        this.posts = response.data

      } catch (error) {
        this.error = 'Error al obtener las publicaciones'
      } finally {
        this.loading = false
      }
    },
  },
})
