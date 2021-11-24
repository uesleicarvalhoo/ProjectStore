import { api } from '@/api'
import { context } from '@/store'

export const order = {
  async actionGetOrders () {
    const response = await api.getOrders(context.state.accessToken)
    context.commit('orders', response.data)
  },
  async actionRemoveOrder (order) {
    const response = await api.deleteOrder(context.state.accessToken, order.id)
    return response.data
  },
  async actionUpdateOrder (payload) {
    const response = await api.updateOrder(context.state.accessToken, payload)
    return response.data
  },
  async actionCreateOrder (payload) {
    const response = await api.createOrder(context.state.accessToken, payload)
    return response.data
  }
}
