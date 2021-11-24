<template>
  <overlay v-show="show" @overlay-click="confirm">
    <card-component
      v-show="show"
      :title="title"
      class="shadow-lg w-full max-h-modal md:w-3/5 lg:w-2/5 z-50"
      :header-icon="mdiClose"
      @header-icon-click="confirm"
    >
      <div class="space-y-3">
        <h1 v-if="largeTitle" class="text-2xl">{{ largeTitle }}</h1>
        <slot />
      </div>

      <divider />

      <jb-buttons>
        <jb-button :label="buttonLabel" :color="button" @click="confirm" />
      </jb-buttons>
    </card-component>
  </overlay>
</template>

<script>
import { computed } from 'vue'
import { mdiClose } from '@mdi/js'
import JbButton from '@/components/JbButton'
import JbButtons from '@/components/JbButtons'
import CardComponent from '@/components/CardComponent'
import Divider from '@/components/Divider'
import Overlay from '@/components/Overlay'
import { useStore } from 'vuex'

export default {
  name: 'ModalBox',
  components: {
    Overlay,
    JbButton,
    JbButtons,
    CardComponent,
    Divider
  },
  props: {
    title: String,
    largeTitle: String,
    button: {
      type: String,
      default: 'info'
    },
    buttonLabel: {
      type: String,
      default: 'Done'
    },
    modelValue: [String, Number, Boolean]
  },
  emits: ['confirm'],
  setup (props, { emit }) {
    const context = useStore()

    const show = computed(() => context.state.showNotification)

    const confirm = () => {
      emit('confirm')
    }

    return {
      show,
      confirm,
      mdiClose
    }
  }
}
</script>
