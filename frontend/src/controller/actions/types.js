import { api } from '@/api'
import { context } from '@/store'

export const types = {
  async actionGetPaymentTypes () {
    const response = await api.getPaymentTypes()
    context.commit('basic', { key: 'paymentTypes', value: response.data })
  },
  async actionGetSaleTypes () {
    const response = await api.getSaleTypes()
    context.commit('basic', { key: 'saleTypes', value: response.data })
  },
  async actionGetOperationTypes () {
    const response = await api.getOperationTypes()
    context.commit('basic', { key: 'operationTypes', value: response.data })
  }
}
