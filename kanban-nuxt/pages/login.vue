<script lang="ts" setup>
const form = reactive({
  username: '',
  password: ''
});

const auth = useAuthStore();

async function handleLogin() {
  await auth.login(form);
}
</script>

<template>
  <div class="flex flex-col h-max items-center mt-20 2xl:mt-48">
    <!-- Title -->
    <span class="text-3xl font-bold mb-5">Login</span>
    <!-- Form -->
    <div class="flex flex-col w-64">
      <FormKit
        type="form"
        :config="{ validationVisibility: 'submit' }"
        @submit="handleLogin"
        :classes="{ outer: 'm-5', message: 'text-center text-red-400' }"
        :actions="false"
        v-model="form"
      >
        <FormKit
          type="text"
          label="Username"
          name="username"
          validation="required"
          :classes="{
            outer: 'mb-3',
            input: 'input input-bordered input-md w-full max-w-xs mb-2',
            message: 'text-center text-red-400'
          }"
        />
        <FormKit 
          type="password"
          name="password"
          label="Password"
          validation="required"
          :classes="{
            outer: 'mb-3',
            input: 'input input-bordered input-md w-full max-w-xs mb-2',
            message: 'text-center text-red-400'
          }"
        />
        <button class="btn btn-info w-full" type="submit">Login</button>
      </FormKit>
    </div>
    <!-- Register redirect -->
    <span class="text-xl mt-8">Don't have an account yet? <NuxtLink class="font-bold" to="/register">Register!</NuxtLink></span>
  </div>
</template>

