<script setup>
const headers = useRequestHeaders(['cookie']);
const { public: { baseURL } } = useRuntimeConfig();

const { data: isAuthed, refresh: refreshAuthed } = await useFetch('/api/isAuthed', { headers });

const { data: workspaces } = await useFetch('workspaces/', {
  baseURL,
  credentials: 'include',
  headers
});

const auth = useAuthStore();

const newWorkspace = reactive({
  name: "",
  open: false
});

const alert = useAlertStore();

function closeWorkspaceForm() { 
  newWorkspace.open = false;
  newWorkspace.name = "";
}

async function addWorkspace() {
  if (newWorkspace.name) {
    try {
      const response = await $fetch.raw('workspaces/', {
        method: "POST",
        body: { name: newWorkspace.name },
        credentials: 'include',
        baseURL
      });
      if (response.status === 201) {
        alert.success("Successfully added new workspace");
        workspaces.value.push(response._data);
      }
    } catch (e) {
      alert.error(`There was an error adding the workspace: ${e}`);
    }
  } else {
    alert.info("The workspace's name is missing");
  }
  closeWorkspaceForm();
}

async function deleteWorkspace(id) {
  if (window.confirm('Are you sure?')) {
    try {
      const res = await $fetch.raw(`workspaces/${id}/`, {
        method: "DELETE",
        credentials: "include",
        baseURL
      });

      if (res.status === 204) {
        alert.success("Successfully deleted workspace");
        workspaces.value = workspaces.value.filter(ws => ws.id !== id);
      }
    } catch (e) {
      alert.error(`There was an error deleting the workspace: ${e}`);
    }
  }
}
</script>

<template>
  <div>
    <!-- Authed view -->
    <div class="flex flex-col px-8 py-8 xl:px-10 mt-10" v-if="auth.isAuthed">
      <!-- Workspaces container -->
      <div class="flex justify-between">
        <span class="text-2xl font-bold mb-5">Your Workspaces</span>
      </div>
      <!-- The workspaces iterator -->
      <div v-auto-animate class="flex flex-wrap gap-6">
        <div v-for="workspace in workspaces" :key="workspace.id" class="card w-64 bg-base-100 shadow-xl flex flex-col">
          <!-- Individual workspace card -->
          <div class="card-body">
            <span class="font-bold text-lg">{{ workspace.name }}</span>
            <div class="card-actions justify-end mt-2">
              <Popper arrow>
                <button class="btn btn-info btn-sm"><Icon name="carbon:menu"/> </button>
                <template #content>
                  <div class="flex flex-col gap-2">
                    <button @click="deleteWorkspace(workspace.id)" class="btn btn-warning btn-sm">Delete</button>
                  </div>
                </template>
              </Popper>
              <button @click="$router.push(`/workspaces/${workspace.id}`)" class="btn btn-sm btn-success">Open</button>
            </div>
          </div>
        </div>
        <div>
          <div v-if="!newWorkspace.open" @click="newWorkspace.open = true" class="flex items-center justify-center h-full btn btn-success">
            <Icon name="carbon:add-alt" />
            <span class="ml-2" v-if="workspaces.length === 0">Add a new workspace</span>
          </div>
          <!-- New workspace form -->
          <div class="p-6 w-72 h-full bg-base-100 shadow-xl rounded-xl flex flex-col" v-else>
            <div>
              <input 
                v-model="newWorkspace.name"
              @keyup.enter="addWorkspace"
                type="text" placeholder="Name" class="input input-sm w-full max-w-xs font-bold text-lg"
              />
            <div class="flex gap-4 justify-end mt-5">
              <button class="btn btn-error btn-sm" @click="closeWorkspaceForm">Cancel</button>
              <button class="btn btn-success btn-sm" @click="addWorkspace">Save</button>
            </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <!-- Unauthed view -->
    <div class="flex items-center justify-center xl:h-96" v-else>
      <!-- The flex row container -->
      <div class="flex flex-col items-center xl:justify-between xl:flex-row xl:mt-44 xl:mx-24">
        <!-- Show hero section -->
        <div class="flex flex-col justify-center mt-20 w-11/12 xl:w-9/12">
          <span class="text-6xl font-bold text-center justify-center xl:text-7xl xl:text-left">Manage your projects easily with this KanBan board</span>
          <button @click="$router.push('/register')" class="btn btn-success w-36 mt-12 self-center xl:self-start">Get Started</button>
        </div>
        <div class="flex justify-center">
          <img class="w-9/12 xl:w-10/12 mt-16" src="/img/hero-image.png" alt="Hand holding a construction plane">
        </div>
      </div>
    </div>
  </div>
</template>