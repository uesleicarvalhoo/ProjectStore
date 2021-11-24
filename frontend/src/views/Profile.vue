<template>
  <title-bar :title-stack="titleStack" />

  <main-section>
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <card-component
        title="Editar Perfil"
        :icon="mdiAccountCircle"
        @submit.prevent="submitProfile"
        form
      >
        <field label="Nome" help="Obrigatorio. Seu nome">
          <control
            :icon="mdiAccount"
            v-model="profileForm.name"
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
            v-model="profileForm.email"
            required
            autocomplete="email"
          />
        </field>

        <divider />

        <jb-buttons>
          <jb-button color="info" type="submit" label="Confirmar" />
        </jb-buttons>
      </card-component>

      <card-component
        title="Trocar a senha"
        :icon="mdiLock"
        @submit.prevent="submitPassword"
        form
      >
        <field label="Senha atual" help="Obrigatório. Sua senha atual">
          <control
            :icon="mdiAsterisk"
            v-model="passwordForm.password_current"
            name="password_current"
            type="password"
            required
            autocomplete="current-password"
          />
        </field>

        <divider />

        <field label="Nova senha" help="Obrigatório. Nova senha">
          <control
            :icon="mdiFormTextboxPassword"
            v-model="passwordForm.password"
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
            v-model="passwordForm.password_confirmation"
            name="password_confirmation"
            type="password"
            required
            autocomplete="new-password"
          />
        </field>

        <divider />

        <jb-buttons>
          <jb-button type="submit" color="info" label="Confirmar" />
        </jb-buttons>
      </card-component>
    </div>
  </main-section>
</template>

<script>
import { ref, reactive } from "vue";
import { useStore } from "vuex";
import {
  mdiAccount,
  mdiAccountCircle,
  mdiLock,
  mdiMail,
  mdiAsterisk,
  mdiFormTextboxPassword,
} from "@mdi/js";
import MainSection from "@/components/MainSection";
import CardComponent from "@/components/CardComponent";
import TitleBar from "@/components/TitleBar";
import Divider from "@/components/Divider";
import Field from "@/components/Field";
import Control from "@/components/Control";
import JbButton from "@/components/JbButton";
import JbButtons from "@/components/JbButtons";
import {
  dispatchUpdateUserPassword,
  dispatchUpdateUser,
  dispatchNotification,
} from "@/controller";

export default {
  name: "Profile",
  components: {
    JbButtons,
    MainSection,
    TitleBar,
    CardComponent,
    Divider,
    Field,
    Control,
    JbButton,
  },
  methods: {
    async submitPassword() {
      if (
        this.passwordForm.password !== this.passwordForm.password_confirmation
      ) {
        await dispatchNotification(
          "Senha invalida",
          "A senha e a confirmação não conferem!",
          "warning"
        );
      } else {
        await dispatchUpdateUserPassword({
          current_password: this.passwordForm.password_current,
          new_password: this.passwordForm.password,
        });
      }
    },
    async submitProfile() {
      await dispatchUpdateUser({
        name: this.profileForm.name,
        email: this.profileForm.email,
      });
    },
  },
  setup() {
    const store = useStore();

    const titleStack = ref(["Admin", "Perfil"]);

    const profileForm = reactive({
      name: store.state.user.name,
      email: store.state.user.email,
    });

    const passwordForm = reactive({
      password_current: "",
      password: "",
      password_confirmation: "",
    });

    return {
      titleStack,
      profileForm,
      passwordForm,
      mdiAccount,
      mdiAccountCircle,
      mdiLock,
      mdiMail,
      mdiAsterisk,
      mdiFormTextboxPassword,
    };
  },
};
</script>
