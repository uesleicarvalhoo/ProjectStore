<template>
  <hero-bar>Vendas</hero-bar>
  <main-section>
    <card-component class="mb-6" has-table>
      <table-order v-on:view="viewOrder" v-on:remove="removeOrder" />
    </card-component>
  </main-section>
  <modal-view v-model="orderModal.active">
    <form-order v-on:submit="updateOrder" :data="orderModal.data" />
  </modal-view>
</template>

<script>
import { reactive } from 'vue'
import { mdiMonitorCellphone, mdiTableBorder } from '@mdi/js'
import MainSection from '@/components/MainSection'
import CardComponent from '@/components/CardComponent'
import HeroBar from '@/components/HeroBar'
import TableOrder from '@/components/TableOrder.vue'
import FormOrder from '@/components/FormOrder.vue'
import ModalView from '@/components/ModalView.vue'
import {
  dispatchGetOrders,
  dispatchRemoveOrder,
  dispatchUpdateOrder
} from '@/controller'

export default {
  name: 'ViewOrder',
  components: {
    MainSection,
    HeroBar,
    CardComponent,
    TableOrder,
    FormOrder,
    ModalView
  },
  methods: {
    async removeOrder (order) {
      await dispatchRemoveOrder(order)
    },

    async updateOrder (order) {
      await dispatchUpdateOrder(order)
    },

    viewOrder (order) {
      // TODO: Gerar/normalizar o tipo da ordem ou ajustar isso direto na fonte pra reconhecer a String(?)
      this.orderModal.active = true
      this.orderModal.data = order
    }
  },
  async created () {
    await dispatchGetOrders()
  },
  setup () {
    const orderModal = reactive({
      active: false,
      data: { client: {}, items: [] }
    })

    return {
      mdiMonitorCellphone,
      mdiTableBorder,
      orderModal
    }
  }
}
</script>
