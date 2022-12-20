<script setup lang="ts">
import IBoard from '@/types/IBoard';
import ICard from '@/types/ICard';

const props = defineProps<{
  board: IBoard
}>();

const emit = defineEmits(['moveCard', 'deleteBoard']);

const { public: { baseURL } } = useRuntimeConfig();

const alert = useAlertStore();

const newCard = reactive({
  body: {
    name: '',
    description: ''
  },
  opened: false
});


const resetCard = () => {
  newCard.body.name = '';
  newCard.body.description = '';
}

async function addCard() {
  // Check for name existence  
  if (newCard.body.name) {
    try {
      const res = await $fetch.raw('cards/', {
        method: 'POST',
        body: {
          ...newCard.body,
          board: props.board.id
        },
        credentials: 'include',
        baseURL
      });
      console.log(res);
      
      if (res.status === 201) {
        props.board.cards.push(res._data as ICard);
        alert.success('Added the new card successfully!');
      }
      resetCard();
    } catch (e) {
      alert.error(`There was an error adding the card: ${e}`);
    }
  } else {
    // Alert the user the card needs a name
    alert.info('The card needs a name');
  }
};

const closeCard = () => {
  newCard.opened = false;
  resetCard();
}

function onDrop(event: any) {
  const cardID = parseInt(event.dataTransfer.getData('cardID'));
  const from = parseInt(event.dataTransfer.getData('from'));
  const to = props.board.id;

  emit('moveCard', { from, to, cardID });
}

function deleteCard(cardID: number) {
  props.board.cards = props.board.cards.filter((card: ICard) => card.id !== cardID);
}

async function deleteBoard() {
  const id = props.board.id;
  
  if (window.confirm('Are you sure?')) {
    try {
      const res = await $fetch.raw(`boards/${id}/`, {
        method: "DELETE",
        credentials: "include",
        baseURL
      });

      if (res.status === 204) {
        alert.success('Board successfully deleted');
        emit('deleteBoard', id);
      }
    } catch (e) {
      alert.error(`There was an error deleting the board: ${e}`);
    }
  }
}

let renamedBoard = "";

async function renameBoard() {
  if (renamedBoard !== "") {
    try {
      const res = await $fetch.raw(`boards/${props.board.id}/`, {
        method: "PATCH",
        body: { name: renamedBoard },
        credentials: "include",
        baseURL,
      });

      if (res.status === 200) {
        alert.success(`Board renamed to '${renamedBoard}'`);
        props.board.name = renamedBoard;
        renamedBoard = "";
      }
    } catch (e) {
      alert.error(`There was an error renaming the board: ${e}`); 
    }
  }
}
</script>

<template>
  <div @drop="onDrop" @dragenter.prevent @dragover.prevent class="flex flex-col w-80 min-w-full p-4 rounded-lg dark:bg-gray-800 bg-slate-200">
    <!-- Title and button -->
    <div class="flex justify-between">
      <input 
        @focusout="renameBoard"
        :value="board.name"
        @input="(e) => renamedBoard = (e.target as HTMLInputElement).value"
        class="font-bold text-2xl input input-sm w-full mr-4 pl-0 bg-transparent"
      />
      <Popper arrow>
        <button class="btn btn-sm btn-success"><Icon name="carbon:overflow-menu-vertical" /></button>
        <template #content>
          <button @click="deleteBoard" class="btn btn-warning btn-sm">Delete</button>
        </template>
      </Popper>
    </div>
    <!-- Cards -->
    <div v-auto-animate class="mt-4">
      <Card @deleteCard="deleteCard" v-for="card in board.cards" :card="card" />
    </div>
    <!-- New Card button -->
    <div>
      <!-- New card form -->
      <div v-if="newCard.opened" class="mt-2">
        <input 
          v-model="newCard.body.name"
          @keyup.ctrl.enter="addCard"
          type="text" placeholder="Name" class="input input-sm w-full max-w-xs"
        />
        <textarea
          v-model="newCard.body.description"
          @keyup.ctrl.enter="addCard"
          class="textarea w-full max-w-xs my-3" placeholder="Description"
        >
        </textarea>
        <div class="flex gap-4 justify-end">
          <button class="btn btn-error btn-sm" @click="closeCard">Close</button>
          <button class="btn btn-success btn-sm" @click="addCard">Add</button>
        </div>
      </div>
      <!-- Toggle new card form -->
      <div 
        @click="newCard.opened = true" v-if="!newCard.opened"
        class="flex items-center cursor-pointer mt-2"
      >
        <Icon name="carbon:add" />
        <span class="ml-1">Add new card</span>
      </div>
    </div>
  </div>
</template>