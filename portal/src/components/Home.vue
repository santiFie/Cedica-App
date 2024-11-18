<template>
  <div class="home-container">
    <section class="hero-section">
      <div class="welcome-section">
        <h1>Bienvenidos a CEDICA</h1>
        <p>Trabajamos por la inclusión, la igualdad de oportunidades y el bienestar integral de las personas con discapacidad, gracias a la conexión única con los caballos.</p>
      </div>
      
      <div class="about-section">
        <h2>¿Quiénes somos?</h2>
        <p>CEDICA es una asociación civil sin fines de lucro fundada en 1994 en La Plata, Argentina. Nuestro objetivo es igualar oportunidades y mejorar la calidad de vida a través de las Terapias y Actividades asistidas con caballos (TACAs).</p>
        <p>Somos un equipo multidisciplinario comprometido con la inclusión, trabajando en cinco áreas clave: Técnica, Ecuestre, Voluntariado, Gestión y Capacitación.</p>
      </div>
    </section>
  </div>
</template>

<style scoped>
.home-container {
  min-height: calc(100vh - 120px); /* Ajusta según la altura de tu navbar */
  padding: 2rem;
  box-sizing: border-box;
}

.hero-section {
  max-width: 1200px;
  margin: auto;
  gap: 2rem;
  align-items: start;
}

.welcome-section, .about-section {
  background: #f5f5f5;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  margin: 2%;
}

h1, h2 {
  color: #2c3e50;
  margin-bottom: 1rem;
  text-align: center;
}

p {
  margin-bottom: 1rem;
  line-height: 1.6;
  text-align: justify;
  color: black;
  font-family: 'Trebuchet MS', 'Lucida Sans Unicode', 'Lucida Grande', 'Lucida Sans', Arial, sans-serif ;
  font-size: 1.4rem;
}

.cta-button {
  background-color: #42b983;
  color: white;
  border: none;
  padding: 0.8rem 1.5rem;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 500;
  display: block;
  margin: 1.5rem auto 0;
  transition: background-color 0.3s ease;
}

.cta-button:hover {
  background-color: #3aa876;
}

@media (max-width: 768px) {
  .home-container {
    padding: 1rem;
  }
  
  .hero-section {
    grid-template-columns: 1fr;
  }
}
</style>

<script>
export default {
  data() {
    return {
      contact: {
        name: "Augusto Dominguez",
        email: "augusto@gmail.com",
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
