import { createStore } from 'vuex'

export const context = createStore({
  state: {
    /* User */
    user: {
      id: null,
      name: null,
      email: null
    },

    userAvatar: 'https://avatars.dicebear.com/api/avataaars/example.svg?options[top][]=shortHair&options[accessoriesChance]=93',
    accessToken: null,
    expireTokenTime: null,

    /* Constants */
    paymentTypes: [],

    saleTypes: [],

    operationTypes: [],

    /* Client */
    clients: [],

    /* Balance */
    balances: [],

    /* Item */
    items: [],

    /* Order */
    orders: [],

    /* Notification */
    showNotification: false,
    notification: {},

    /* Access info */
    loggedIn: false,

    /* fullScreen - fullscreen form layout (e.g. login page) */
    isFullScreen: false,

    /* Aside */
    isAsideMobileExpanded: false,
    isAsideLgActive: false,

    /* Dark mode */
    darkMode: false,

    /* Field focus with ctrl+k (to register only once) */
    isFieldFocusRegistered: false
  },
  mutations: {
    /* A fit-them-all commit */
    basic (state, payload) {
      state[payload.key] = payload.value
    },

    /* User */
    user (state, payload) {
      state.user = payload
    },
    loggedIn (state, paylolad) {
      state.loggedIn = paylolad
    },
    accessToken (state, payload) {
      state.accessToken = payload.accessToken
      state.expireTokenTime = payload.exp
    },
    orders (state, payload) {
      state.orders = payload
    },
    clients (state, payload) {
      state.clients = payload
    },
    balances (state, payload) {
      state.balances = payload
    },
    items (state, payload) {
      state.items = payload
    },
    notification (state, payload) {
      state.notification = payload
    },
    showNotification (state, payload) {
      state.showNotification = payload
    }
  },
  actions: {
    asideMobileToggle ({ commit, state }, payload = null) {
      const isShow = payload !== null ? payload : !state.isAsideMobileExpanded

      document.getElementById('app').classList[isShow ? 'add' : 'remove']('ml-60')

      document.documentElement.classList[isShow ? 'add' : 'remove']('m-clipped')

      commit('basic', {
        key: 'isAsideMobileExpanded',
        value: isShow
      })
    },

    asideLgToggle ({ commit, state }, payload = null) {
      commit('basic', { key: 'isAsideLgActive', value: payload !== null ? payload : !state.isAsideLgActive })
    },

    fullScreenToggle ({ commit, state }, value) {
      commit('basic', { key: 'isFullScreen', value })

      document.documentElement.classList[value ? 'add' : 'remove']('full-screen')
    },

    darkMode ({ commit, state }) {
      const value = !state.darkMode

      document.documentElement.classList[value ? 'add' : 'remove']('dark')

      commit('basic', {
        key: 'darkMode',
        value
      })
    }
  },
  modules: {
  }
})
