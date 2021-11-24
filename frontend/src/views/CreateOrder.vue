<template>
  <form-order v-on:submit="createOrder"></form-order>
</template>

<script>
import FormOrder from '@/components/FormOrder'
import { dispatchCreateOrder } from '@/controller'

export default {
  name: 'CreateOrder',
  components: {
    FormOrder
  },
  methods: {
    async createOrder (order) {
      await dispatchCreateOrder(order)
    }
  }
}
</script>
