import { defineStore } from 'pinia'
import axios, { all } from 'axios'

const limit = 10

export const usePostsStore = defineStore('posts', {
  state: () => ({
    posts: [],
    loading: false,
    error: null,
    total_pages: 0,
    page: 1,
    allPosts: []
  }),


  actions: {
    async fetchPosts() {
      try {
        const response = await axios.get('http://127.0.0.1:5000/api/posts/')
            
        this.allPosts = response.data
        this.total_pages = Math.ceil(this.allPosts.length / limit)
        
        const start = (this.page - 1) * limit
        const end = start + limit
        this.posts = this.allPosts.slice(start, end)

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
