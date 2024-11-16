<script>
import { ref } from 'vue'

// esta es la funcion que esta en 'stores' que se encarga de enviar los datos a la api
import { useContactStore } from '@/stores/contact'

export default {
  name: 'Contact',
  setup() {
    const name = ref('')
    const lastName = ref('')
    const email = ref('')
    const message = ref('')
    const contactStore = useContactStore()

    const submitForm = () => {
      const contactData = {
        name: name.value,
        last_name: lastName.value,
        email: email.value,
        message: message.value,
      }
      // submitContact es la funcion del store que envia los datos del formulario
      contactStore.submitContact(contactData)
    }

    // se retornan las variables y la funcion que se usaran en el template
    return {
      name,
      lastName,
      email,
      message,
      submitForm,
    }
  },
}
</script>

<template>

    <!-- Defino el formulario con los campos necesarios
        Cuando se haga submit se ejecutara la funcion submitForm  
    -->
  <form @submit.prevent="submitForm">
    <div>
      <label for="name">Nombre:</label>
      <input id="name" v-model="name" type="text" required />
    </div>
    <div>
      <label for="lastName">Apellido:</label>
      <input id="lastName" v-model="lastName" type="text" required />
    </div>
    <div>
      <label for="email">Email:</label>
      <input id="email" v-model="email" type="email" required />
    </div>
    <div>
      <label for="message">Mensaje:</label>
      <textarea id="message" v-model="message" required></textarea>
    </div>
    <button type="submit">Enviar</button>
  </form>
</template>

<style scoped>
form {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

button {
  margin-top: 10px;
}
</style>
