import { api } from '@/api'
import { context } from '@/store'

export const item = {
  async actionCreateItem (payload) {
    const response = await api.createItem(context.state.accessToken, payload)
    return response.data
  },
  async actionGetItems () {
    const response = await api.getItems(context.state.accessToken)
    context.commit('items', response.data)
  },
  async actionUpdateItem (payload) {
    const response = await api.updateItem(context.state.accessToken, payload)
    return response.data
  },
  async actionRemoveItem (item) {
    const response = await api.deleteItem(context.state.accessToken, item.id)
    return response.data
  }
}
