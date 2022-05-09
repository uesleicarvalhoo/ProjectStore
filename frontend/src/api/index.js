import axios from 'axios'
import { apiUrl } from '@//env'

function authHeaders (token) {
  return {
    headers: {
      Authorization: `Bearer ${token}`
    }
  }
}

export const api = {
  /* Utils */
  async healthCheck(){
    return await axios.get(`${apiUrl}/health`)
  },
  /* Authentication */
  async loginGetToken (username, password) {
    const params = new URLSearchParams()
    params.append('username', username)
    params.append('password', password)
    console.log(apiUrl)
    console.log(params)
    return await axios.post(`${apiUrl}/auth/access-token`, params)
  },
  async refreshAcessToken (token) {
    return await axios.post(`${apiUrl}/auth/refresh-token`, {}, authHeaders(token))
  },
  /* Users */
  async getUserData (token) {
    return await axios.get(`${apiUrl}/v1/users/me`, authHeaders(token))
  },
  async updateUserPassword (token, userId, payload) {
    return await axios.post(`${apiUrl}/v1/users/password/${userId}`, payload, authHeaders(token))
  },
  async updateUserData (token, userId, payload) {
    return await axios.post(`${apiUrl}/v1/users/${userId}`, payload, authHeaders(token))
  },
  async createUser (token, payload) {
    return await axios.post(`${apiUrl}/v1/users/`, payload, authHeaders(token))
  },
  /* Orders */
  async createOrder (token, payload) {
    return await axios.post(`${apiUrl}/v1/orders/`, payload, authHeaders(token))
  },
  async getOrders (token) {
    return await axios.get(`${apiUrl}/v1/orders/`, authHeaders(token))
  },
  async updateOrder (token, payload) {
    return await axios.patch(`${apiUrl}/v1/orders/`, payload, authHeaders(token))
  },
  async deleteOrder (token, orderId) {
    return await axios.delete(`${apiUrl}/v1/orders/${orderId}`, authHeaders(token))
  },
  /* Clients */
  async createClient (token, payload) {
    return await axios.post(`${apiUrl}/v1/clients/`, payload, authHeaders(token))
  },
  async getClients (token) {
    return await axios.get(`${apiUrl}/v1/clients/`, authHeaders(token))
  },
  async updateClient (token, payload) {
    return await axios.patch(`${apiUrl}/v1/clients/`, payload, authHeaders(token))
  },
  async deleteClient (token, clientId) {
    return await axios.delete(`${apiUrl}/v1/clients/${clientId}`, authHeaders(token))
  },
  /* Balance */
  async createBalance (token, payload) {
    return await axios.post(`${apiUrl}/v1/balances/`, payload, authHeaders(token))
  },
  async getBalances (token) {
    return await axios.get(`${apiUrl}/v1/balances/`, authHeaders(token))
  },
  async deleteBalance (token, balanceId) {
    return await axios.delete(`${apiUrl}/v1/balances/${balanceId}`, authHeaders(token))
  },
  /* Items */
  async createItem (token, payload) {
    return await axios.post(`${apiUrl}/v1/items/`, payload, authHeaders(token))
  },
  async getItems (token) {
    return await axios.get(`${apiUrl}/v1/items/`, authHeaders(token))
  },
  async updateItem (token, payload) {
    return await axios.patch(`${apiUrl}/v1/items/`, payload, authHeaders(token))
  },
  async deleteItem (token, itemId) {
    return await axios.delete(`${apiUrl}/v1/items/${itemId}`, authHeaders(token))
  },
  /* Types */
  async getPaymentTypes () {
    return await axios.get(`${apiUrl}/v1/types/payments`)
  },
  async getSaleTypes () {
    return await axios.get(`${apiUrl}/v1/types/sales`)
  },
  async getOperationTypes () {
    return await axios.get(`${apiUrl}/v1/types/operations`)
  }
}
