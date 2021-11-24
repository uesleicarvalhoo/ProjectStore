<template>
  <main-section>
    <title-sub-bar :icon="mdiBallotOutline" :title="title" />
    <card-component
      title="Registro"
      :icon="mdiBallot"
      @submit.prevent="submit"
      form
    >
      <control placeholder="Código do item" v-model="id" hidden />
      <field label="Código">
        <control placeholder="Código do item" v-model="code" required />
      </field>

      <field label="Descrição">
        <control
          placeholder="Descrição do produto"
          type="text"
          v-model="name"
          required
        />
      </field>

      <field label="Quantidade disponível">
        <control
          type="number"
          placeholder="0"
          v-model="amount"
          min="0"
          step="1"
          required
        />
      </field>

      <field label="Preço sugerido">
        <control
          type="number"
          placeholder="00.00"
          min="0"
          step="0.01"
          v-model="value"
          required
        />
      </field>

      <divider />

      <jb-buttons>
        <jb-button type="submit" color="info" label="Confirmar" />
        <jb-button type="reset" color="info" outline label="Limpar" />
      </jb-buttons>
    </card-component>
  </main-section>
</template>

<script>
import { reactive } from 'vue'
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

export default {
  name: 'FormItem',
  components: {
    TitleSubBar,
    Divider,
    MainSection,
    CardComponent,
    Field,
    Control,
    JbButton,
    JbButtons
  },
  props: {
    id: String,
    title: { type: String, default: () => 'Formulário de produtos' },
    code: { type: String, default: () => null },
    name: { type: String, default: () => null },
    amount: { type: Number, default: () => null },
    value: { type: Number, default: () => null }
  },
  emits: ['submit'],

  setup (props, { emit }) {
    const warningModal = reactive({
      active: false,
      text: ''
    })

    const submit = () => {
      const item = {
        id: props.id,
        code: props.code,
        name: props.name,
        amount: props.amount,
        value: props.value.toFixed(2)
      }
      emit('submit', item)
      if (props.id === null) {
        reset()
      }
    }

    const reset = () => {
      props.code = null
      props.name = null
      props.amount = null
      props.value = null
    }

    return {
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
