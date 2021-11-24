<template>
  <footer v-show="isFooterBarVisible" class="bg-white py-2 px-6 dark:bg-gray-900">
    <level>
      <div>
        <b>&copy; Desenvolvido por Ueslei Carvalho.</b>
        Para entrar em contato comigo use meu <a href="https://www.instagram.com/uesleicarvalhoo/" target="_blank" class="text-blue-500">Instagram</a>
      </div>
      <div class="md:py-2">
      </div>
    </level>
  </footer>
</template>

<script>
import { computed } from 'vue'
import { useStore } from 'vuex'
import Level from '@/components/Level'

export default {
  name: 'FooterBar',
  components: {
    Level
  },
  setup () {
    const store = useStore()
    const isFooterBarVisible = computed(() => !store.state.isFullScreen)

    return {
      isFooterBarVisible
    }
  }
}
</script>
