/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    
    "./src/web/templates/auth/login.html",
    './src/web/templates/**/*.html', // Verifica esta ruta
    './static/js/**/*.js',
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}