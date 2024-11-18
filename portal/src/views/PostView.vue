<script setup>
import Post from '@/components/Post.vue'
defineProps({
  id: {
    type: String,
    required: true,
  },
})

</script>

<template>
  <Post :id="id"/>
</template>