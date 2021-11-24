import { api } from '@/api'
import { context } from '@/store'

export const client = {
  async actionGetClients () {
    const response = await api.getClients(context.state.accessToken)
    context.commit('clients', response.data)
  },
  async actionRemoveClient (client) {
    const response = await api.deleteClient(context.state.accessToken, client.id)
    return response.data
  },
  async actionUpdateClient (payload) {
    const response = await api.updateClient(context.state.accessToken, payload)
    return response.data
  },
  async actionCreateClient (payload) {
    const response = await api.createClient(context.state.accessToken, payload)
    return response.data
  }
}
