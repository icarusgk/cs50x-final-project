export default defineNuxtRouteMiddleware(async (to, from) => {
  const headers = useRequestHeaders(['cookie']);  
  
  if (Object.keys(headers)?.length !== 0) {
    if (to.name === 'login' || to.name === 'register') {
      return navigateTo('/');
    }
  }
})