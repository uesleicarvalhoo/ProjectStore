import { api } from '@/api'
import { context } from '@/store'

export const user = {
  async actionGetUserData () {
    const response = await api.getUserData(context.state.accessToken)
    context.commit('user', response.data)
  },
  async actionUpdateUserPassword (payload) {
    await api.updateUserPassword(context.state.accessToken, context.state.user.id, payload)
  },
  async actionUpdateUserData (payload) {
    const response = await api.updateUserData(context.state.accessToken, context.state.user.id, payload)
    context.commit('user', response.data)
  },
  async actionCreateUser (payload) {
    await api.createUser(context.state.accessToken, payload)
  }
}
