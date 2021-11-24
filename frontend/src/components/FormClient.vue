<template>
  <main-section>
    <title-sub-bar :icon="mdiBallotOutline" :title="title" required />
    <card-component
      title="Registro"
      :icon="mdiBallot"
      @submit.prevent="submit"
      form
    >
      <control hidden v-model="id" />
      <field label="Nome">
        <control placeholder="Duno da Silva Sauro" v-model="name" required />
      </field>

      <field label="Email">
        <control placeholder="email@example.com" type="email" v-model="email" />
      </field>

      <field label="Telefone">
        <control type="number" placeholder="+5500912345678" v-model="phone" />
      </field>

      <field label="CEP">
        <control type="number" placeholder="000.000.000-00" v-model="zipCode" />
      </field>

      <field label="Endereço">
        <control placeholder="Rua dos bobos, N0" v-model="address" />
      </field>

      <divider />

      <jb-buttons>
        <jb-button color="info" type="submit" label="Confirmar" />
        <jb-button type="reset" color="info" outline label="Limpar" />
      </jb-buttons>
    </card-component>
  </main-section>
</template>

<script>
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
  name: 'FormClient',
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
    title: { type: String, default: () => 'Formulário de clientes' },
    id: { type: String, default: () => null },
    name: { type: String, default: () => null },
    email: { type: String, default: () => null },
    phone: { type: String, default: () => null },
    zipCode: { type: String, default: () => null },
    address: { type: String, default: () => null }
  },
  emits: ['submit'],

  setup (props, { emit }) {
    const reset = () => {
      props.id = null
      props.name = null
      props.email = null
      props.phone = null
      props.zipCode = null
      props.address = null
    }

    const submit = () => {
      const data = {
        id: props.id,
        name: props.name,
        email: props.email,
        phone: props.phone,
        address: props.address,
        zip_code: props.zipCode
      }

      emit('submit', data)
      if (props.id === null) {
        reset()
      }
    }
    return {
      submit,
      mdiBallot,
      mdiBallotOutline,
      mdiAccount,
      mdiMail,
      mdiCheck
    }
  }
}
</script>
