import { api } from '@/api'
import { context } from '@/store'

export const balance = {
  async actionCreateBalance (payload) {
    const response = await api.createBalance(context.state.accessToken, payload)
    return response.data
  },
  async actionGetBalances () {
    const response = await api.getBalances(context.state.accessToken)
    context.commit('balances', response.data)
  },
  async actionRemoveBalance (balance) {
    const response = await api.deleteBalance(context.state.accessToken, balance.id)
    return response.data
  },
  async actionUpdateBalance (payload) {
    const response = await api.updateBalance(context.state.accessToken, payload)
    return response
  }
}
