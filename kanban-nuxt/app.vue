<script setup>
const headers = useRequestHeaders();
const auth = useAuthStore();

// Fetch whether the user is the user is authed
const { data: isAuthed, refresh: refreshAuthed } = await useFetch('/api/isAuthed', { headers });
auth.isAuthed = isAuthed;
</script>

<template>
  <div>
    <NuxtLayout>
      <NuxtPage />
    </NuxtLayout>
  </div>
</template>
