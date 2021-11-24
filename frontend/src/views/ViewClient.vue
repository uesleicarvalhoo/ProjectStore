<template>
  <hero-bar>Clientes</hero-bar>
  <main-section>
    <card-component class="mb-6" has-table>
      <table-clients v-on:remove="removeClient" v-on:view="viewClient" />
    </card-component>
  </main-section>
  <modal-view v-model="clientModal.active">
    <form-client
      :id="clientModal.clientData.id"
      :email="clientModal.clientData.email"
      :name="clientModal.clientData.name"
      :phone="clientModal.clientData.phone"
      :zipCode="clientModal.clientData.zip_code"
      :address="clientModal.clientData.address"
      v-on:submit="updateClient"
    />
  </modal-view>
</template>

<script>
import { reactive } from 'vue'
import { mdiMonitorCellphone, mdiTableBorder } from '@mdi/js'
import MainSection from '@/components/MainSection'
import TableClients from '@/components/TableClients'
import CardComponent from '@/components/CardComponent'
import HeroBar from '@/components/HeroBar'
import ModalView from '@/components/ModalView'
import FormClient from '@/components/FormClient'
import {
  dispatchGetClients,
  dispatchRemoveClient,
  dispatchUpdateClient
} from '@/controller'

export default {
  name: 'ViewClient',
  components: {
    MainSection,
    HeroBar,
    CardComponent,
    TableClients,
    ModalView,
    FormClient
  },
  methods: {
    viewClient (client) {
      this.clientModal.clientData = client
      this.clientModal.active = true
    },
    async removeClient (client) {
      await dispatchRemoveClient(client)
    },
    async updateClient (client) {
      await dispatchUpdateClient(client)
    }
  },
  async created () {
    await dispatchGetClients()
  },
  setup () {
    const clientModal = reactive({ active: false, clientData: {} })

    return {
      clientModal,
      mdiMonitorCellphone,
      mdiTableBorder
    }
  }
}
</script>
