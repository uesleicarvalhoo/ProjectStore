<template>
  <form-item v-on:submit="createItem"></form-item>
</template>

<script>
import FormItem from '@/components/FormItem'
import { dispatchCreateItem } from '@/controller'

export default {
  name: 'CreateItemForm',
  components: {
    FormItem
  },
  methods: {
    async createItem (item) {
      await dispatchCreateItem(item)
    }
  }
}
</script>
