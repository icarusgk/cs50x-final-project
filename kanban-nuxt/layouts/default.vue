<script lang="ts" setup>
const headers = useRequestHeaders(['cookie']);
const baseURL = 'http://127.0.0.1:8000/api/';

const auth = useAuthStore();

interface IUser {
  user: string
}

const { data: user } = await useFetch<IUser>('me/', {
  baseURL,
  credentials: 'include',
  headers: {
    Cookie: headers.cookie!
  }
});

async function handleLogout() {
  const response = await $fetch.raw('http://127.0.0.1:8000/api/auth/logout/', {
    method: 'POST',
    credentials: 'include',
    headers: {
      Cookie: headers.cookie!
    }
  });
  if (response.status === 200) {
    auth.isAuthed = false;
  }
}
</script>

<template>
  <!-- Top nav bar -->
  <nav class="px-8 xl:px-16 pt-8">
    <div class="flex justify-between align-items items-end">
      <span @click="$router.push('/')" class="font-bold hover:cursor-pointer text-2xl xl:text-4xl align-baseline">CS50x KanBan</span>
      <div v-if="!auth.isAuthed">
        <button @click="$router.push('login')" class="btn btn-ghost mr-2 xl:mr-4">Login</button>
        <button @click="$router.push('register')" class="btn btn-accent">Register</button>
      </div>
      <div v-else>
        <span class="text-lg mr-5">Logged in as <span class="font-bold">{{ user?.user }}</span></span>
        <button @click="handleLogout" class="btn btn-error">Log out</button>
      </div>
    </div>
  </nav>
  <slot />
</template>