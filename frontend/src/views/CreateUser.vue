<template>
  <form-user v-on:submit="createUser" />
</template>

<script>
import FormUser from '@/components/FormUser'
import { dispatchCreateUser } from '@/controller'

export default {
  name: 'CreateUser',
  components: {
    FormUser
  },
  methods: {
    async createUser (user) {
      await dispatchCreateUser(user)
    }
  }
}
</script>
