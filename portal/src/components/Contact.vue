<script>
import { ref, onMounted, onUnmounted } from 'vue'

// esta es la funcion que esta en 'stores' que se encarga de enviar los datos a la api
import { useContactStore } from '@/stores/contact'

export default {
  name: 'Contact',
  setup() {
    const name = ref('')
    const lastName = ref('')
    const email = ref('')
    const message = ref('')
    const captchaToken = ref('')
    const contactStore = useContactStore()

    // se carga el script del captcha dinamicamente
    const loadCaptchaScript = () => {
      if (!document.getElementById('recaptcha-script')) {
        const script = document.createElement('script');
        script.id = 'recaptcha-script';
        script.src = 'https://www.google.com/recaptcha/api.js';
        script.async = true;
        script.defer = true;
        document.head.appendChild(script);
      }
    };

    const submitForm = () => {

      if(!captchaToken.value) {
        alert('Por favor, complete el captcha')
        return
      }

      const contactData = {
        name: name.value,
        last_name: lastName.value,
        email: email.value,
        message: message.value,
        captcha: captchaToken.value,
      }
      // submitContact es la funcion del store que envia los datos del formulario
      contactStore.submitContact(contactData)
    }

    const onCaptchaSuccess = (token) => {
        captchaToken.value = token  // guardo el token generado por el captcha
      }

    onMounted(() => {
      loadCaptchaScript(); // Carga el script al montar el componente

      // Define onCaptchaSuccess en el objeto global para que sea accesible por el navegador
      window.onCaptchaSuccess = onCaptchaSuccess;
    });

    onUnmounted(() => {
      // Limpia la referencia global al desmontar el componente
      delete window.onCaptchaSuccess;
    });

    // se retornan las variables y la funcion que se usaran en el template
    return {
      name,
      lastName,
      email,
      message,
      submitForm,
      onCaptchaSuccess,
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
    <div class="g-recaptcha" 
         data-sitekey="6LeGsYIqAAAAAHtkb8P22Xoyfc-lyulQsGU3Ryx_" 
         data-callback="onCaptchaSuccess">
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
