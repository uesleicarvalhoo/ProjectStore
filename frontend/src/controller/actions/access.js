import { api } from '@/api'
import { context } from '@/store'
import { dispatchNotification } from '..'
import { storage } from "../../helpers/storage"


export const access = {
  async actionLogin(email, password) {
    const response = await api.loginGetToken(email, password)
    const data = response.data

    if (data) {
      await this.actionLoggedIn(data)
    } else {
      dispatchNotification('Erro ao obter token', 'Ocorreu um problema ao obter o seu Token de acesso, por favor entre em contato com o administrador do sistema', 'danger')
    }
  },

  async actionLoggedIn(data) {
    context.commit('accessToken', data)
    context.commit('loggedIn', true)
    storage.setAccessToken(data)
  },

  async actionLogout() {
    context.commit('accessToken', {})
    context.commit('loggedIn', false)
    storage.removeAccessToken()
  },

  async actionRefresh() {
    const response = await api.refreshAcessToken(context.state.accessToken)
    const data = response.data

    if (data) {
      await this.actionLoggedIn(data)
    } else {
      this.actionLogout()
    }
  },

  async actionLoadLocalStorageToken() {
    return storage.getAccessToken()
  }
}
