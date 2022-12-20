<script setup>
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
  --popper-theme-background-color: #ffffff;
  --popper-theme-background-color-hover: #dbdbdb;
  --popper-theme-text-color: #ffffff;
  --popper-theme-border-width: 0px;
  --popper-theme-border-style: solid;
  --popper-theme-border-radius: 6px;
  --popper-theme-padding: 12px;
  --popper-theme-box-shadow: 0 30px 30px -6px rgba(28, 28, 28, 0.25);
}

@media (prefers-color-scheme: dark) {
  :root {
    --popper-theme-background-color: #282828;
    --popper-theme-background-color-hover: #252525;
  }
}
</style>
