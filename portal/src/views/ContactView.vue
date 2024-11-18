<script>
  import Contact from '@/components/Contact.vue'

  export default {
  name: 'ContactView',
  components: {
    Contact,
  },
}

</script>

<template>
  <div class="contact">
    <h1>Contactanos</h1>
    <Contact />
  </div>
</template>

<style scoped>
.contact {
  padding: 20px;
}

@media (min-width: 1024px) {
  .contact {
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
  }
}
</style>
