<script setup>
// Grab the headers
const headers = useRequestHeaders(['cookie']);
const { public: { baseURL } } = useRuntimeConfig();

const auth = useAuthStore();
const alert = useAlertStore();

async function handleLogout() {
  const response = await $fetch.raw('auth/logout/', {
    method: 'POST',
    credentials: 'include',
    headers: {
      Cookie: headers.cookie
    },
    baseURL
  })
  if (response.status === 200) {
    auth.isAuthed = false;
    auth.user = null;
    await useRouter().push('/');
    alert.success("You've been logged out!")
  }
}
</script>

<template>
  <!-- Top nav bar -->
  <nav class="px-8 xl:px-16 pt-8">
    <div class="relative">
      <span @click="$router.push('/')" class="font-bold hover:cursor-pointer text-3xl xl:text-4xl align-baseline fixed left-8 top-8">CS50x KanBan</span>
      <div class="fixed right-4 top-4" v-if="!auth.isAuthed">
        <button @click="$router.push('/login')" class="btn btn-ghost mr-2 xl:mr-4">Login</button>
        <button @click="$router.push('/register')" class="btn btn-accent">Register</button>
      </div>
      <div class="fixed right-5 top-6" v-else>
        <!-- <span class="mr-4">Logged in as <span class="font-bold">{{ auth.user.user }}</span></span> -->
        <button @click="handleLogout" class="btn btn-error">Log out</button>
      </div>
    </div>
  </nav>
  <slot />
</template>