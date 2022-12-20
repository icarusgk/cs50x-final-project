export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null as any,
    isAuthed: false as any
  }),
  actions: {
    async login(creds: { username: string, password: string }) {
      const response = await $fetch.raw('http://127.0.0.1:8000/api/auth/login/', {
        method: 'POST',
        credentials: 'include',
        body: creds,
      });
      if (response.status === 200) {
        this.isAuthed = true;
        await useRouter().push('/')
      }
    },
  }
});