<template>
  <section class="px-6 sm:px-0 mb-6 flex items-center justify-between">
    <div class="flex items-center justify-start">
      <icon v-if="icon" :path="icon" class="mr-3"/>
      <h1 class="text-2xl">{{ title }}</h1>
    </div>

  </section>
</template>

<script>
import { mdiCog } from '@mdi/js'
import { computed } from 'vue'
import { useStore } from 'vuex'
import Icon from '@/components/Icon'

export default {
  name: 'TitleSubBar',
  components: {
    Icon
  },
  props: {
    icon: String,
    title: String
  },
  setup () {
    const store = useStore()

    const darkMode = computed(() => store.state.darkMode)

    return {
      darkMode,
      mdiCog
    }
  }
}
</script>
