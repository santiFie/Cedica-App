import { defineStore } from 'pinia'
import axios, { all } from 'axios'

const limit = 10

export const usePostsStore = defineStore('posts', {
  state: () => ({
    posts: [],
    loading: false,
    error: null,
    hasNextPage: false,
    totalPages: 1,
    page: 1,
  }),

  getters: {
    getPostById: (state) => (id) => {
      return state.posts.find(post => post.id == id)
    }
  },

  actions: {
    async fetchPosts() {
      try {
        const params = {
          page: this.page,
          per_page: limit
        };
        console.log(import.meta.env.VITE_APP_API)
        const response = await axios.get(`${import.meta.env.VITE_APP_API}/posts`, { params })
        this.posts = response.data.data
        this.hasNextPage = response.data.meta.has_next_page
        this.totalPages = response.data.meta.total_pages

      } catch (error) {
        this.error = error
      } finally {
        this.loading = false
      }
    },

    async changePage() {
      this.loading = true
      this.page++
      await this.fetchPosts()
    },

    async goBackPage() {
      this.loading = true
      this.page--
      await this.fetchPosts()
    },
  },

  
})

