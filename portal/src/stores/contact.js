import { defineStore } from 'pinia'
import axios from 'axios'
import js from '@eslint/js'

export const useContactStore = defineStore('contactStore', {
  actions: {
    async submitContact(contactData) {
        console.log('ADENTRO DE LA FUNCION SUBMIT CONTACT EN STORE')
        console.log('CONTACT DATA:', contactData)
      try {
        // convertir contactData en un objeto JSON y enviar
        const response = await axios.post('http://127.0.0.1:5000/api/contacts/register', contactData, {
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
