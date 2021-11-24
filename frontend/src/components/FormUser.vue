<template>
  <title-bar :title-stack="titleStack" />

  <main-section>
    <card-component
      title="Registrar Usuário"
      :icon="mdiAccountCircle"
      @submit.prevent="submit"
      form
    >
      <control v-model="form.id" name="id" hidden />
      <field label="Nome" help="Obrigatorio. Seu nome">
        <control
          :icon="mdiAccount"
          v-model="form.name"
          name="username"
          required
          autocomplete="username"
        />
      </field>
      <field label="E-mail" help="Obrigatório. Seu e-mail">
        <control
          :icon="mdiMail"
          type="email"
          name="email"
          v-model="form.email"
          required
          autocomplete="email"
        />
      </field>

      <field label="Senha" help="Obrigatório. Nova senha">
        <control
          :icon="mdiFormTextboxPassword"
          v-model="form.password"
          name="password"
          type="password"
          required
          autocomplete="new-password"
        />
      </field>

      <field
        label="Confirmação da senha"
        help="Obrigatório. Confirme a sua nova senha"
      >
        <control
          :icon="mdiFormTextboxPassword"
          v-model="form.password_confirmation"
          name="password_confirmation"
          type="password"
          required
          autocomplete="new-password"
        />
      </field>

      <field label="Checkbox" wrap-body>
        <check-radio-picker
          name="admin"
          v-model="form.admin"
          :options="{
            admin: 'Esse usuário deve ser registrado como Administrador',
          }"
        />
      </field>

      <jb-buttons>
        <jb-button color="info" type="submit" label="Confirmar" />
      </jb-buttons>
    </card-component>
  </main-section>
</template>

<script>
import { ref, reactive } from 'vue'
import {
  mdiAccount,
  mdiAccountCircle,
  mdiLock,
  mdiMail,
  mdiAsterisk,
  mdiFormTextboxPassword
} from '@mdi/js'
import MainSection from '@/components/MainSection'
import CardComponent from '@/components/CardComponent'
import TitleBar from '@/components/TitleBar'
import Field from '@/components/Field'
import Control from '@/components/Control'
import JbButton from '@/components/JbButton'
import JbButtons from '@/components/JbButtons'
import CheckRadioPicker from '@/components/CheckRadioPicker'

export default {
  name: 'Profile',
  components: {
    JbButtons,
    MainSection,
    TitleBar,
    CardComponent,
    Field,
    Control,
    JbButton,
    CheckRadioPicker
  },
  props: {
    id: { type: String, default: () => null },
    name: { type: String, default: () => null },
    email: { ype: String, default: () => null },
    password: { type: String, default: () => null },
    confirm_password: { type: String, default: () => null },
    admin: { type: Boolean, default: () => false }
  },
  emits: ['submit'],
  setup (props, { emit }) {
    const titleStack = ref(['Admin', 'Perfil'])

    const form = reactive({
      id: props.id,
      name: props.name,
      email: props.email,
      password: props.password,
      password_confirmation: props.password_confirmation,
      admin: props.admin
    })

    const reset = () => {
      form.name = null
      form.email = null
      form.password = null
      form.password_confirmation = null
      form.admin = false
    }

    const submit = () => {
      emit('submit', {
        id: form.id,
        name: form.name,
        email: form.email,
        password: form.password,
        confirm_password: form.password_confirmation,
        admin: form.admin
      })
      if (form.id === null) {
        reset()
      }
    }

    return {
      titleStack,
      form,
      submit,
      mdiAccount,
      mdiAccountCircle,
      mdiLock,
      mdiMail,
      mdiAsterisk,
      mdiFormTextboxPassword
    }
  }
}
</script>
