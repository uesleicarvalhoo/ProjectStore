<template>
  <hero-bar>Fluxo de Caixa</hero-bar>
  <main-section>
    <card-component class="mb-6" has-table>
      <table-balances v-on:remove="removeBalance" />
    </card-component>
  </main-section>
</template>

<script>
import { mdiMonitorCellphone, mdiTableBorder } from '@mdi/js'
import MainSection from '@/components/MainSection'
import TableBalances from '@/components/TableBalance'
import CardComponent from '@/components/CardComponent'
import HeroBar from '@/components/HeroBar'
import { dispatchGetBalances, dispatchRemoveBalance } from '@/controller'

export default {
  name: 'ViewItem',
  components: {
    MainSection,
    HeroBar,
    CardComponent,
    TableBalances
  },
  methods: {
    async removeBalance (balance) {
      await dispatchRemoveBalance(balance)
    }
  },
  async created () {
    await dispatchGetBalances()
  },
  setup () {
    return {
      mdiMonitorCellphone,
      mdiTableBorder
    }
  }
}
</script>
