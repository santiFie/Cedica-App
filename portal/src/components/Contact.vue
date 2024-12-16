<script>
import { ref, onMounted, onUnmounted } from 'vue'

// esta es la funcion que esta en 'stores' que se encarga de enviar los datos a la api
import { useContactStore } from '@/stores/contact'

export default {
  name: 'Contact',
  methods: {
      adjustHeight(event) {
      const textarea = event.target;
      textarea.style.height = 'auto';  // Restablece la altura antes de recalcularla
      textarea.style.height = `${textarea.scrollHeight}px`;  // Ajusta la altura al contenido
      }
    },
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
  <h2 class="contact-title">Contactanos</h2>

  <form @submit.prevent="submitForm">
    <div class="form-field">
      <input id="name" class="form-input" v-model="name" type="text" placeholder="Nombre" required />
    </div>
    <div class="form-field">
      <input id="lastName" class="form-input" v-model="lastName" type="text" placeholder="Apellido" required />
    </div>
    <div class="form-field">
      <input id="email" class="form-input" v-model="email" type="email" placeholder="Correo Electrónico" required />
    </div>
    <div class="form-field">
      <textarea id="message" class="form-message" v-model="message" placeholder="Mensaje" required @input="adjustHeight"></textarea>
    </div>
    <div class="g-recaptcha" 
         :data-sitekey="import.meta.env.VITE_RECAPTCHA_SITE_KEY" 
         data-callback="onCaptchaSuccess">
    </div>
    <button type="submit">Enviar</button>
  </form>
</template>



<style scoped>

.contact-title {
  color: black;
  margin-left: 6%;
  margin-top: 5%;
  font-size: 2em;
  margin-bottom: 0.5%;
  font-family: 'Roboto', sans-serif;
}

form {
  display: flex;
  flex-direction: column;
  gap: 10px;
  padding: 6%;
  margin-bottom: 5%;
  margin-left: 5%;
  margin-right: 5%;
  background-color: white;
  border-radius: 10px;
  box-shadow: 0 0 10px rgba(201, 169, 169, 0.1);
}

.form-field {
  display: flex;
  padding: 13px;
  width: 100%;
}

.form-input {
  padding: 13px;
  border: 1px solid #ccc;
  width: 100%;
  font-size: inherit;
}

textarea {
  font-family: sans-serif;
  font-size: inherit;
  padding: 13px;
  border: 1px solid #ccc;
  width: 100%;
  font-size: inherit;
  resize: vertical; 
  overflow-y: hidden; 
}
button {
  margin-top: 10px;
  width: 10%;
  text-align: center;
  font-size: inherit;
  justify-content: center;
  align-self: center;
  padding: 8px;
  background-color: #385668;
  border: none;
  border-radius: 5%;
  color: white;
}

button:hover {
  background-color: #2b3b4e;
}

.g-recaptcha {
  margin-top: 10px;
  margin-bottom: 10px;
  display: flex;
  justify-content: center;
}

</style>
