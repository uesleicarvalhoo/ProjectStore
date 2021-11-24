<template>
  <overlay v-show="value" @overlay-click="cancel">
    <card-component
      v-show="value"
      :title="title"
      class="shadow-lg w-full max-h-modal overflow-y-scroll md:w-4/5 z-50"
      :header-icon="mdiClose"
      @header-icon-click="cancel"
    >
      <slot />
      <divider />
    </card-component>
  </overlay>
</template>

<script>
import { mdiClose } from '@mdi/js'
import CardComponent from '@/components/CardComponent'
import Divider from '@/components/Divider'
import Overlay from '@/components/Overlay'
import { computed } from '@vue/reactivity'

export default {
  name: 'ModalView',
  components: {
    Overlay,
    CardComponent,
    Divider
  },
  props: {
    title: String,
    modelValue: [String, Number, Boolean]
  },
  emits: ['update:modelValue', 'cancel', 'confirm'],
  setup (props, { emit }) {
    const value = computed({
      get: () => props.modelValue,
      set: value => emit('update:modelValue', value)
    })

    const confirmCancel = mode => {
      value.value = false
      emit(mode)
    }

    const confirm = () => confirmCancel('confirm')

    const cancel = () => confirmCancel('cancel')

    return {
      value,
      confirm,
      cancel,
      mdiClose
    }
  }
}
</script>
