export const useMyAuth = () => useState('auth', () => {
  const name = ref();
  useAuthedFetch('me').then((res) => {
    name.value = res.user;
  })
  return name;
})