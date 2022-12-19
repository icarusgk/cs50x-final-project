<script lang="ts" setup>
const form = reactive({
  username: '',
  password: '',
  passwordConfirmation: ''
});

const { public: { baseURL } } = useRuntimeConfig();

const alert = useAlertStore();
const auth = useAuthStore();

async function handleRegister() { 
  if (form.password === form.passwordConfirmation) {
    try {
      const response = await $fetch.raw('auth/register/', {
        method: 'POST',
        body: form,
        baseURL,
      });

      if (response.ok) {
        alert.success('Registered successfully');
        auth.user = form.username;
        await auth.login({ username: form.username, password: form.password });
      }
    } catch (e) {
      alert.error(`There was an error registering you: ${e}`);
    }
  } else {
    alert.error("Your password doesn't match with your password confirmation");
  }
}
</script>

<template>
  <div class="flex flex-col h-max items-center mt-20 2xl:mt-32">
    <!-- Title -->
    <span class="text-3xl font-bold mb-5">Register</span>
    <!-- Form -->
    <div class="flex flex-col w-64">
      <FormKit
        type="form"
        @submit="handleRegister"
        :config="{ validationVisibility: 'submit' }"
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
        <FormKit 
          type="password"
          name="passwordConfirmation"
          label="Password confirmation"
          validation="required"
          :classes="{
            outer: 'mb-3',
            input: 'input input-bordered input-md w-full max-w-xs mb-2',
            message: 'text-center text-red-400'
          }"
        />
        <button class="btn btn-success w-full mt-5" type="submit">Register</button>
      </FormKit>
    </div>
    <!-- Login redirect -->
    <span class="text-xl mt-8">Already have an account? <NuxtLink class="font-bold" to="/login">Log in!</NuxtLink></span>
  </div>
</template>
