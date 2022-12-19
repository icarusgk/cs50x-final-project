export default defineNuxtRouteMiddleware(async (to, from) => {
  // console.log(to.name);
  const headers = useRequestHeaders();
  // @ts-ignore
  const data = await $fetch('/api/isAuthed', { headers });
  if (data) {
    if (to.name === 'login' || to.name === 'register') {
      return navigateTo('/');
    }
  }
})