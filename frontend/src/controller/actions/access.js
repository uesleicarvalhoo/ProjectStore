import { api } from '@/api'
import { context } from '@/store'
import { dispatchNotification } from '..'

export const access = {
  async actionLogin (email, password) {
    const response = await api.loginGetToken(email, password)
    const data = response.data
    if (data) {
      context.commit('accessToken', data)
      context.commit('loggedIn', true)
    } else {
      dispatchNotification('Erro ao obter token', 'Ocorreu um problema ao obter o seu Token de acesso, por favor entre em contato com o administrador do sistema', 'danger')
    }
  },
  async actionLogout () {
    context.commit('accessToken', null)
    context.commit('loggedIn', false)
  },
  async actionRefresh () {
    const response = await api.refreshAcessToken(context.state.accessToken)
    context.commit('accessToken', response.data)
  }
}
