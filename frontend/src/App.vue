<template>
  <nav-bar v-on:logout="logout" />
  <aside-menu :menu="menu" />
  <router-view />
  <footer-bar />
  <overlay
    v-show="isAsideLgActive"
    z-index="z-30"
    @overlay-click="overlayClick"
  />
  <notification
    :large-title="notification.title"
    :button="notification.type"
    buttonLabel="Ok"
    v-on:confirm="confirmNotification"
    shake
  >
    <p v-text="notification.text"></p>
  </notification>
</template>

<script>
// @ is an alias to /src
import { computed } from 'vue'
import { useStore } from 'vuex'
import router from '@/router'
import menu from '@/helpers/menu.js'
import NavBar from '@/components/NavBar'
import AsideMenu from '@/components/AsideMenu'
import FooterBar from '@/components/FooterBar'
import Overlay from '@/components/Overlay'
import Notification from '@/components/Notification'
import { dispatchConfirmNotification, dispatchLogout, dispatchLoadContext } from '@/controller'

export default {
  name: 'Home',
  components: {
    Overlay,
    FooterBar,
    AsideMenu,
    Notification,
    NavBar
  },
  methods: {
    async logout(){
      await dispatchLogout()
      router.push({ name: 'login' })
    }
  },
  async created(){
    await dispatchLoadContext()
  },
  setup () {
  const context = useStore()

    const loggedIn = computed(() => context.state.loggedIn)

    const notification = computed(() => context.state.notification)

    const isAsideLgActive = computed(() => context.state.isAsideLgActive)

    const confirmNotification = () => {
      dispatchConfirmNotification()
    }

    const overlayClick = () => {
      context.dispatch('asideLgToggle', false)
    }

    return {
      menu,
      notification,
      confirmNotification,
      loggedIn,
      isAsideLgActive,
      overlayClick
    }
  }
}
</script>
