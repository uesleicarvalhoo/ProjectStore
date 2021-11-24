<template>
  <card-component class="items-center" rounded="">
    <level type="justify-around lg:justify-center">
      <user-avatar class="lg:mx-12" button/>
      <div class="space-y-3 text-center md:text-left lg:mx-12">
        <div class="flex justify-center md:block">
          <check-radio-picker
            name="sample-switch"
            type="switch"
            v-model="userSwitchVal"
            :options="{ one: 'Notifications' }"/>
        </div>
        <h1 class="text-2xl">Olá, <b>{{ userName }}</b>!</h1>
      </div>
    </level>
  </card-component>
</template>

<script>
import { computed, ref, watch } from 'vue'
import { useStore } from 'vuex'
import { mdiCheckDecagram } from '@mdi/js'
import Level from '@/components/Level'
import UserAvatar from '@/components/UserAvatar'
import CardComponent from '@/components/CardComponent'

export default {
  name: 'UserCard',
  components: {
    Level,
    UserAvatar,
    CardComponent
  },
  setup () {
    const store = useStore()

    const userName = computed(() => store.state.user.name)

    const userSwitchVal = ref([])

    watch(userSwitchVal, value => {
      store.dispatch('pushMessage', value && value.indexOf('one') > -1 ? 'Success! Now active' : 'Done! Now inactive')
    })

    return {
      userName,
      userSwitchVal,
      mdiCheckDecagram
    }
  }
}
</script>
