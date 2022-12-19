<script setup lang="ts">
import ICard from '@/types/ICard';
const props = defineProps<{
  card: ICard
}>();
const emit = defineEmits(['deleteCard']);

const { public: { baseURL } } = useRuntimeConfig();

const open = ref(false);
const alert = useAlertStore();

let body: { name?: string, description?: string } = {};

function startDrag (event: any, card: ICard): void {
  event.dataTransfer.dropEffect = 'move';
  event.dataTransfer.effectAllowed = 'move';
  event.dataTransfer.setData('cardID', card.id);  
  event.dataTransfer.setData('from', card.board);
}

function handleInput(event: any): void {
  body.name = event.target.value;
}

function handleDescription(event: any): void {
  body.description = event.target.value;
}

async function updateCard() {  
  if (Object.keys(body).length !== 0) {
    try {
      const res = await $fetch.raw(`cards/${props.card.id}/`, {
        method: 'PATCH',
        body,
        credentials: 'include',
        baseURL
      });

      if (res.status === 200) {
        if (body?.name) props.card.name = body?.name
        if (body?.description) props.card.description = body.description
        body = {};
        alert.success(`Successfully updated the card`);
      }
      closeCard();
    } catch (e) {
      alert.error(`There was an error updating the card: ${e}`);
    }
  }
}

async function deleteCard(id: number) {
  try {
    const res = await $fetch.raw(`cards/${id}/`, {
      method: "DELETE",
      credentials: 'include',
      baseURL
    });
    
    if (res.status === 204) {
      emit('deleteCard', id);
      alert.success('Successfully deleted the card');
    }
    
  } catch (e) {
    alert.error(`There was an error deleting the card: ${e}`);
  }
}

const closeCard = () => open.value = false;
</script>

<template>
  <!-- Individual card -->
  <div @dragstart="startDrag($event, card)" :draggable="!open" class="p-2 rounded my-2 dark:bg-zinc-900 bg-white">
    <!-- Card name -->
    <div class="w-full cursor-pointer" @click="open = true" v-if="!open">
      <span class="cursor-pointer">{{ card.name }}</span>
    </div>
    <!-- Edit card form -->
    <div v-if="open" class="p-0">
      <input 
        :value="card.name"
        @input="handleInput"
        type="text" placeholder="Name" class="input input-sm w-full max-w-xs input-bordered"
      />
      <textarea
        :value="card.description"
        @input="handleDescription"
        class="textarea textarea-bordered w-full max-w-xs mt-3 mb-2" placeholder="Description"
      ></textarea>
      <div class="flex gap-4 justify-center">
        <button class="btn btn-info btn-sm" @click="deleteCard(card.id)">Delete</button>
        <button class="btn btn-error btn-sm" @click="closeCard">Close</button>
        <button class="btn btn-success btn-sm" @click="updateCard">Save</button>
      </div>
    </div>
  </div>
</template>
