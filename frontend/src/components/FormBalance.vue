<template>
  <main-section>
    <title-sub-bar :icon="mdiBallotOutline" title="Novo registro de Caixa" />
    <card-component
      title="Registro"
      :icon="mdiBallot"
      @submit.prevent="submit"
      form
    >
      <field label="Tipo de Operação">
        <control :options="operationTypes" v-model="operationType" />
      </field>

      <field label="Valor">
        <control
          type="number"
          placeholder="00.00"
          v-model="value"
          step="0.01"
          required
        />
      </field>

      <divider />

      <field label="Descrição da movimentação">
        <control type="textarea" v-model="description" required />
      </field>

      <divider />

      <jb-buttons>
        <jb-button type="submit" color="info" label="Confirmar" />
        <jb-button type="reset" color="info" outline label="Limpar" />
      </jb-buttons>
    </card-component>
  </main-section>
  <modal-box
    v-model="warningModal.active"
    large-title="Ops!"
    button="warning"
    buttonLabel="Ok"
    shake
  >
    <p v-text="warningModal.text"></p>
  </modal-box>
</template>

<script>
import { computed, reactive } from 'vue'
import {
  mdiBallot,
  mdiBallotOutline,
  mdiAccount,
  mdiMail,
  mdiCheck
} from '@mdi/js'
import MainSection from '@/components/MainSection'
import CardComponent from '@/components/CardComponent'
import Divider from '@/components/Divider.vue'
import JbButton from '@/components/JbButton'
import JbButtons from '@/components/JbButtons'
import Field from '@/components/Field'
import Control from '@/components/Control'
import TitleSubBar from '@/components/TitleSubBar'
import ModalBox from '@/components/ModalBox'
import { dispatchOperationTypes } from '@/controller'
import { useStore } from 'vuex'

export default {
  name: 'FormBalance',
  components: {
    TitleSubBar,
    Divider,
    MainSection,
    CardComponent,
    ModalBox,
    Field,
    Control,
    JbButton,
    JbButtons
  },
  props: {
    operationType: { type: Object, default: () => {} },
    value: { type: Number, default: null },
    description: { type: String, default: '' }
  },
  emits: ['submit'],
  async created () {
    await dispatchOperationTypes()
  },

  setup (props, { emit }) {
    const context = useStore()

    const operationTypes = computed(() => context.state.operationTypes)

    const warningModal = reactive({
      active: false,
      text: ''
    })

    const submit = () => {
      if (!props.operationType) {
        warningModal.active = true
        warningModal.text = 'Informe o tipo de movimentação!'
      } else {
        const data = {
          operation: props.operationType,
          value: props.value,
          description: props.description
        }
        emit('submit', data)

        if (props.id === null) {
          reset()
        }
      }
    }

    const reset = () => {
      props.operationType = null
      props.value = null
      props.description = null
    }

    return {
      operationTypes,
      submit,
      warningModal,
      mdiBallot,
      mdiBallotOutline,
      mdiAccount,
      mdiMail,
      mdiCheck
    }
  }
}
</script>
