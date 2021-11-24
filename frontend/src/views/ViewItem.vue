<template>
  <hero-bar>Estoque de Produtos</hero-bar>
  <main-section>
    <card-component class="mb-6" has-table>
      <table-items
        v-on:view="viewItem"
        v-on:remove="removeItem"
      />
    </card-component>
  </main-section>
  <modal-view v-model="itemModal.active">
    <form-item
      :id="itemModal.data.id"
      :code="itemModal.data.code"
      :name="itemModal.data.name"
      :value="itemModal.data.value"
      :amount="itemModal.data.amount"
      v-on:submit="updateItem"
    />
  </modal-view>
</template>

<script>
import { reactive } from 'vue'
import { mdiMonitorCellphone, mdiTableBorder } from '@mdi/js'
import MainSection from '@/components/MainSection'
import TableItems from '@/components/TableItem'
import CardComponent from '@/components/CardComponent'
import HeroBar from '@/components/HeroBar'
import FormItem from '@/components/FormItem'
import ModalView from '@/components/ModalView'
import { dispatchGetItems, dispatchRemoveItem, dispatchUpdateItem } from '@/controller'

export default {
  name: 'ViewItem',
  components: {
    MainSection,
    HeroBar,
    CardComponent,
    TableItems,
    FormItem,
    ModalView
  },
  methods: {
    viewItem (item) {
      this.itemModal.active = true
      this.itemModal.data = item
    },
    async removeItem (item) {
      await dispatchRemoveItem(item)
    },
    async updateItem (item) {
      await dispatchUpdateItem(item)
    }
  },
  async created () {
    await dispatchGetItems()
  },
  setup () {
    const itemModal = reactive({ active: false, data: {} })

    return {
      itemModal,
      mdiMonitorCellphone,
      mdiTableBorder
    }
  }
}
</script>
