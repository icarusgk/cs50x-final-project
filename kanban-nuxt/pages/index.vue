<script setup>
const headers = useRequestHeaders(['cookie']);
const baseURL = 'http://127.0.0.1:8000/api/';
const auth = useAuthStore();

// Internal server api call
const { data: isAuthed, refresh: refreshAuthed } = await useFetch('/api/isAuthed', { headers });

const { data: user } = await useFetch('me/', {
  baseURL,
  credentials: 'include',
  headers
});

const { data: workspaces } = await useFetch('workspace/', {
  baseURL,
  credentials: 'include',
  headers
});
</script>

<template>
  <div>
    <!-- Move to layout -->
    <div v-if="!auth.isAuthed" class="flex items-center justify-center xl:h-96">
      <div class="flex flex-col items-center xl:justify-around xl:flex-row xl:mt-64 xl:mx-24">
        <!-- Show hero section -->
        <div class="flex flex-col justify-center mt-20 w-11/12 xl:w-6/12">
          <span class="text-6xl font-bold text-center justify-center xl:text-7xl xl:text-left">Manage your projects easily with this KanBan board</span>
          <button @click="$router.push('/register')" class="btn btn-success w-36 mt-12 self-center xl:self-start">Get Started</button>
        </div>
        <div class="flex justify-center">
          <img class="w-9/12 xl:w-10/12 mt-16" src="/img/hero-image.png" alt="">
        </div>
      </div>
    </div>
    <div class="flex flex-col px-16 py-8" v-else>
      <div class="flex justify-between">
        <span class="text-2xl font-bold mb-5">Your Workspaces</span>
        <button class="btn btn-warning">Add a new workspace</button>
      </div>
      <div class="flex gap-6">
        <div class="card w-72 bg-base-100 shadow-xl flex flex-col" v-for="workspace in workspaces" :key="workspace.id">
          <div class="card-body">
            <span class="font-bold text-lg ">{{ workspace.name }}</span>
            <div class="card-actions justify-end">
              <button class="btn btn-sm">...</button>
              <button @click="$router.push(`/workspaces/${workspace.id}`)" class="btn btn-sm btn-success">Open</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>