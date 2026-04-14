export default defineNuxtConfig({
  modules: ['@nuxtjs/tailwindcss'],
  css: ['~/assets/css/main.css'],
  runtimeConfig: {
    public: {
      apiGatewayUrl: 'http://127.0.0.1:8000'
    }
  }
})
