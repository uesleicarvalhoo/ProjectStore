<template>
  <form-client v-on:submit="createClient"></form-client>
</template>

<script>
import FormClient from '@/components/FormClient'
import { dispatchCreateClient } from '@/controller'

export default {
  name: 'CreateClientForm',
  methods: {
    async createClient (client) {
      await dispatchCreateClient(client)
    }
  },
  components: {
    FormClient
  }
}
</script>
