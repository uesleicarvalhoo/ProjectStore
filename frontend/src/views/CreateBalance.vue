<template>
  <form-balance v-on:submit="createBalane"></form-balance>
</template>

<script>
import FormBalance from '@/components/FormBalance'
import { dispatchCreateBalance } from '@/controller'

export default {
  name: 'CreateBalanceForm',
  components: {
    FormBalance
  },
  methods: {
    async createBalane (balance) {
      await dispatchCreateBalance(balance)
    }
  }
}
</script>
