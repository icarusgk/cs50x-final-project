<script setup>
const headers = useRequestHeaders();
const auth = useAuthStore();

const { data: isAuthed } = await useFetch('/api/isAuthed', { headers });
auth.isAuthed = isAuthed;

useHead({
  title: 'CS50x KanBan'
});
</script>

<template>
  <div>
    <NuxtLayout>
      <NuxtPage />
      <Alerts />
    </NuxtLayout>
  </div>
</template>

<style>
/* Popper styles */
:root {
  --popper-theme-background-color: #282828;
  --popper-theme-background-color-hover: #252525;
  --popper-theme-text-color: #ffffff;
  --popper-theme-border-width: 0px;
  --popper-theme-border-style: solid;
  --popper-theme-border-radius: 6px;
  --popper-theme-padding: 12px;
  --popper-theme-box-shadow: 0 6px 30px -6px rgba(28, 28, 28, 0.25);
}
</style>
