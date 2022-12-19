// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  modules: [
    '@nuxtjs/tailwindcss',
    'nuxt-icon',
    ['@pinia/nuxt', {
      autoImports: ['defineStore', 'acceptHMRUpdate']
    }],
    '@vueuse/nuxt',
    '@formkit/nuxt',
  ],
  imports: {
    dirs: ['stores']
  },
  runtimeConfig: {
    public: {
      baseURL: 'http://127.0.0.1:8000/api/'
    }
  },
  vite: {
    ssr: {
      noExternal: ['vue3-popper']
    }
  }
})
