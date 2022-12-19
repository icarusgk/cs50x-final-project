import Popper from 'vue3-popper';
import { autoAnimatePlugin } from '@formkit/auto-animate/vue';

export default defineNuxtPlugin(nuxtApp => {
  nuxtApp.vueApp.component('Popper', Popper);
  nuxtApp.vueApp.use(autoAnimatePlugin);
})