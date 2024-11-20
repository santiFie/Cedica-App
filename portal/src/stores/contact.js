import { defineStore } from 'pinia'
import axios from 'axios'
import js from '@eslint/js'

export const useContactStore = defineStore('contactStore', {
  actions: {
    async submitContact(contactData) {
      try {
        // convertir contactData en un objeto JSON y enviar
        const response = await axios.post(`${import.meta.env.VITE_APP_API}/contacts/register`, contactData, {
            headers: {
              'Content-Type': 'application/json',
            },
        })
        console.log('Consulata enviada exitosamente:', response.data)
        alert('Tu consulta ha sido enviada!')
      } catch (error) {
        console.error('Error enviando consulta:', error)
        alert('Ocurrio un error al enviar la consulta. Por favor intenta nuevamente.')
      }
    },
  },
})
