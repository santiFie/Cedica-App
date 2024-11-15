<template>
  <!-- Bienvenida e Introducción -->
  <section class="hero">
    <h1>Bienvenidos a CEDICA</h1>
    <p>
      Trabajamos por la inclusión, la igualdad de oportunidades y el bienestar integral 
      de las personas con discapacidad, gracias a la conexión única con los caballos.
    </p>
    <!--<img src="path-to-hero-image.jpg" alt="Jinete con un caballo" />-->
  </section>

  <!-- ¿Quiénes somos? -->
  <section class="hero" id="about">
    <h2>¿Quiénes somos?</h2>
    <p>
      CEDICA es una asociación civil sin fines de lucro fundada en 1994 en La Plata, Argentina. 
      Nuestro objetivo es igualar oportunidades y mejorar la calidad de vida a través de las 
      Terapias y Actividades asistidas con caballos (TACAs).
    </p>
    <p>
      Somos un equipo multidisciplinario comprometido con la inclusión, trabajando en cinco áreas 
      clave: Técnica, Ecuestre, Voluntariado, Gestión y Capacitación.
    </p>
    <button @click="goTo('aboutDetails')">Conocer más</button>
  </section>
  
</template>

<script>
export default {
  data() {
    return {
      contact: {
        name: "",
        email: "",
        message: "",
      },
    };
  },
  methods: {
    goTo(section) {
      // Navega a una sección específica
      const element = document.getElementById(section);
      if (element) element.scrollIntoView({ behavior: "smooth" });
    },
    sendContact() {
      alert("Formulario enviado. ¡Gracias por contactarnos!");
      this.contact = { name: "", email: "", message: "" };
    },
  },
};
</script>

<style scoped>

.continer {
  width: 100%;
  height: 100;
  max-width: 800px;
  margin: 0 auto;
  padding: 1rem;
}

.home {
  font-family: Arial, sans-serif;
  line-height: 1.6;
}
.hero {
  text-align: center;
  padding: 2rem;
  background-color: #f3ecec;
}
.about,
.activities,
.news,
.team,
.contact {
  padding: 2rem;
  border-bottom: 1px solid #ccc;
}
h1, h2 {
  color: #2c3e50;
}
button {
  background-color: #3498db;
  color: #fff;
  border: none;
  padding: 0.5rem 1rem;
  cursor: pointer;
}
button:hover {
  background-color: #2980b9;
}

p {
  color: #000;
}
</style>
