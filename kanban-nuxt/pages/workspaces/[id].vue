<script setup>
const headers = useRequestHeaders(['cookie']);
const { id } = useRoute().params;
const { public: { baseURL } } = useRuntimeConfig();


const newBoard = reactive({
  name: '',
  opened: false
});

const { data: workspace } = await useFetch(`workspaces/${id}/`, {
  baseURL,
  credentials: 'include',
  headers
});

useHead({ title: `Workspace - ${workspace.value.name}` });

const alert = useAlertStore();

const move = async (cardInfo) => {
  const { from, to, cardID } = cardInfo;
  const { boards } = workspace.value;

  if (from === to) {
    return;
  }
  const fromBoard = boards.find(b => b.id === from);

  const toBoard = boards.find(b => b.id === to);

  const card = fromBoard.cards.find(c => c.id === cardID);

  const response = await $fetch.raw(`cards/${cardID}/move/`, {
    method: 'PATCH',
    body: { to },
    baseURL,
    credentials: 'include',
  })

  if (response.status === 200) {
    fromBoard.cards = fromBoard.cards.filter(c => c.id !== card.id);
    toBoard.cards.push(card);
    card.board = to;
  }
}

const deleteBoard = (boardId) => {
  workspace.value.boards = workspace.value.boards.filter(b => b.id !== boardId);
}

const addBoard = async () => {
  const res = await $fetch.raw('boards/', {
    method: 'POST',
    credentials: 'include',
    baseURL,
    body: { name: newBoard.name, workspace: parseInt(id) }
  });

  if (res.status === 201) {
    workspace.value.boards.push(res._data);
    alert.success(`${newBoard.name} added!`);
    resetBoard();
  }
}

const resetBoard = () => {
  newBoard.name = '';
  newBoard.opened = false;
}

let renamedWorkspace = "";

const renameWorkspace = async () => {
  if (renamedWorkspace !== "") {
    const res = await $fetch.raw(`workspaces/${id}/`, {
      method: "PATCH",
      body: { name: renamedWorkspace },
      credentials: "include",
      baseURL
    });

    if (res.status === 200) {
      useHead({ title: `Workspace - ${renamedWorkspace}` });
      alert.success("Workspace renamed successfully");
      renamedWorkspace = "";
    }
  }
}

</script>

<template>
  <div>
    <div class="mt-16 px-6">
      <input @focusout="renameWorkspace" :value="workspace.name" @input="(e) => renamedWorkspace = e.target.value" type="text" class="text-3xl font-extrabold input input-sm"/>
    </div>
    <div v-auto-animate class="flex gap-6 mt-6 px-8">
      <!-- Boards iterator -->
      <div v-for="board in workspace.boards">
        <Board @moveCard="move" @deleteBoard="deleteBoard" :board="board" />
      </div>
      <!-- New board form -->
      <div>
        <!-- Add new board button -->
        <div 
          @click="newBoard.opened = true"
          v-if="!newBoard.opened"
          class="flex items-center cursor-pointer bg-slate-200 dark:bg-gray-800 h-min w-80 w-min-full p-4 mr-4 rounded-md"
        >
          <Icon name="carbon:add" />
          <span class="ml-1 font-bold">Add new board</span>
        </div>
        <!-- Form -->
        <div v-if="newBoard.opened" class="flex flex-col w-80 p-4 rounded-md mr-4 bg-slate-200 dark:bg-gray-800">
          <input
            v-model="newBoard.name"
            @keyup.enter="addBoard"
            type="text" placeholder="Name" class="input input-sm w-full max-w-xs my-3"
          />
          <div class="flex gap-4 justify-end">
            <button class="btn btn-error btn-sm" @click="resetBoard">Close</button>
            <button class="btn btn-success btn-sm" @click="addBoard">Add</button>
          </div>
        </div>
      </div>
    </div>
  </div>
  
</template>