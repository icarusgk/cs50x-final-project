<script setup>
const headers = useRequestHeaders(['cookie']);
const { id } = useRoute().params
const baseURL = 'http://127.0.0.1:8000/api/';


const { data: info } = await useFetch(`workspace/${id}/`, {
  baseURL,
  credentials: 'include',
  headers
})
</script>
<template>
  <div class="p-16">
    <span>{{ id }}</span>
    <span>{{ info }}</span>
  </div>
</template>