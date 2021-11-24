<template>
  <main-section>
    <div class="grid grid-cols-1 gap-6 lg:grid-cols-3 mb-6">
      <card-widget
        color="text-green-500"
        :icon="mdiAccountMultiple"
        :number="totalClients"
        label="Total de clientes"
      />
      <card-widget
        color="text-blue-500"
        :icon="mdiCartOutline"
        prefix="R$"
        :number="totalSales"
        label="Total de vendas"
      />
      <card-widget
        color="text-red-500"
        :icon="mdiChartTimelineVariant"
        :number="balance"
        prefix="R$"
        label="Balanço geral"
      />
    </div>
    <card-component title="Movimentações do mês" has-table>
      <table-balance :actions="false" />
    </card-component>
  </main-section>
</template>

<script>
// @ is an alias to /src
import { computed } from 'vue'
import { useStore } from 'vuex'
import {
  mdiAccountMultiple,
  mdiCartOutline,
  mdiChartTimelineVariant
} from '@mdi/js'
import MainSection from '@/components/MainSection'
import CardWidget from '@/components/CardWidget'
import CardComponent from '@/components/CardComponent'
import TableBalance from '@/components/TableBalance'
import { dispatchGetOrders, dispatchGetClients, dispatchGetBalances } from '@/controller'
import { sum } from '@/helpers/functions'

export default {
  name: 'Home',
  components: {
    MainSection,
    CardComponent,
    TableBalance,
    CardWidget
  },
  async created () {
    await dispatchGetOrders()
    await dispatchGetClients()
    await dispatchGetBalances()
  },
  setup () {
    const context = useStore()

    const totalClients = computed(() => context.state.clients.length)

    const totalSales = computed(() => sum(context.state.orders, 'value'))

    const balance = computed(() => sum(context.state.balances, 'value'))

    const darkMode = computed(() => context.state.darkMode)
    return {
      totalClients,
      totalSales,
      balance,
      darkMode,
      mdiAccountMultiple,
      mdiCartOutline,
      mdiChartTimelineVariant
    }
  }
}
</script>
