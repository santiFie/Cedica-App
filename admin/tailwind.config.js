/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    
    "./src/web/templates/auth/login.html",
    './src/web/templates/**/*.html', // Verifica esta ruta
    './static/js/**/*.js',
  ],
  theme: {
    extend: {
      screens: {
      xs: '480px', // Define tu propio valor para xs
      xxs: '300px'
      },
    },
  },
  plugins: [],
}