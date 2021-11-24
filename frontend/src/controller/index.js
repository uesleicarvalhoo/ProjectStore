import { access } from './actions/access'
import { user } from './actions/user'
import { order } from './actions/order'
import { client } from './actions/client'
import { balance } from './actions/balance'
import { item } from './actions/items'
import { notification } from './actions/notification'

import router from '@/router'
import { types } from './actions/types'

async function dispatchApiError(error) {
  let title = 'Erro no servidor'
  let message = 'Ocorreu um erro interno e não foi possível processar a sua solicitação!'
  const response = error.response
  console.log(error)

  if (response) {
    title = `${response.status} - ${title}`
    if (response.data.message) {
      message = response.data.message
    }
  }
  dispatchNotification(title, message, 'danger')
}

export function dispatchNotification(title, text, type) {
  notification.actionShowNotification(title, text, type)
}

export function dispatchConfirmNotification() {
  notification.actionHideNotification()
}

/* Constants */

export async function dispatchPaymentTypes() {
  await types.actionGetPaymentTypes()
}

export async function dispatchSaleTypes() {
  await types.actionGetSaleTypes()
}

export async function dispatchOperationTypes() {
  await types.actionGetOperationTypes()
}

/* Authorization */

export const dispatchLogout = async () => {
  await access.actionLogout()
}

export const dispatchLogin = async (email, password) => {
  try {
    await access.actionLogin(email, password)
    await dispatchGetMe()
    router.push({ name: 'home' })
  } catch (error) {
    dispatchApiError(error)
    await dispatchLogout()
  }
}

export const dispatchRefreshToken = async () => {
  try {
    await access.actionRefresh()
  } catch (error) {
    dispatchApiError(error)
    await dispatchLogout()
  }
}

/* Users */

export const dispatchGetMe = async () => {
  try {
    await user.actionGetUserData()
  } catch (error) {
    await dispatchApiError(error)
  }
}

export const dispatchUpdateUserPassword = async (payload) => {
  try {
    await user.actionUpdateUserPassword(payload)
  } catch (error) {
    await dispatchApiError(error)
  }
}

export const dispatchCreateUser = async (payload) => {
  try {
    await user.actionCreateUser(payload)
  } catch (error) {
    await dispatchApiError(error)
  }
}

export const dispatchUpdateUser = async (payload) => {
  try {
    await user.actionUpdateUserData(payload)
  } catch (error) {
    await dispatchApiError(error)
  }
}

/* Clients */

export const dispatchCreateClient = async (payload) => {
  try {
    await client.actionCreateClient(payload)
    dispatchNotification('Atualização do cliente', 'Cliente cadastrado com sucesso!', 'success')
    await dispatchGetClients()
  } catch (error) {
    await dispatchApiError(error)
  }
}

export const dispatchGetClients = async () => {
  try {
    await client.actionGetClients()
  } catch (error) {
    await dispatchApiError(error)
  }
}

export const dispatchUpdateClient = async (payload) => {
  try {
    await client.actionUpdateClient(payload)
    dispatchNotification('Atualização do cliente', 'Dados do cliente atualizados com sucesso!', 'success')
    await dispatchGetClients()
  } catch (error) {
    await dispatchApiError(error)
  }
}

export const dispatchRemoveClient = async (payload) => {
  try {
    await client.actionRemoveClient(payload)
    dispatchNotification('Atualização do cliente', 'Cliente excluido com sucesso!', 'success')
    await dispatchGetClients()
  } catch (error) {
    await dispatchApiError(error)
  }
}

/* Balances */

export const dispatchCreateBalance = async (payload) => {
  try {
    await balance.actionCreateBalance(payload)
    dispatchNotification('Atualização do Balanço', 'Balanço cadastrado com sucesso!', 'success')
    await dispatchGetBalances()
  } catch (error) {
    await dispatchApiError(error)
  }
}

export const dispatchGetBalances = async () => {
  try {
    await balance.actionGetBalances()
  } catch (error) {
    await dispatchApiError(error)
  }
}

export const dispatchRemoveBalance = async (payload) => {
  try {
    await balance.actionRemoveBalance(payload)
    dispatchNotification('Fluxo de caixa', 'Registro excluido com sucesso!', 'success')
    await dispatchGetBalances()
  } catch (error) {
    await dispatchApiError(error)
  }
}

/* Items */

export const dispatchCreateItem = async (payload) => {
  try {
    await item.actionCreateItem(payload)
    dispatchNotification('Produto cadastrado', 'Produto cadastrado com sucesso!', 'success')
    await dispatchGetItems()
  } catch (error) {
    await dispatchApiError(error)
  }
}

export const dispatchGetItems = async () => {
  try {
    await item.actionGetItems()
  } catch (error) {
    await dispatchApiError(error)
  }
}

export const dispatchUpdateItem = async (payload) => {
  try {
    await item.actionUpdateItem(payload)
    dispatchNotification('Atualização do produto', 'Dados do produto atualizados com sucesso!', 'success')
    await dispatchGetItems()
  } catch (error) {
    await dispatchApiError(error)
  }
}

export const dispatchRemoveItem = async (payload) => {
  try {
    await item.actionRemoveItem(payload)
    dispatchNotification('Atualização do produto', 'Produto excluido com sucesso!', 'success')
    await dispatchGetItems()
  } catch (error) {
    await dispatchApiError(error)
  }
}

/* Orders */

export const dispatchCreateOrder = async (payload) => {
  try {
    await order.actionCreateOrder(payload)
    dispatchNotification('Registro de venda', 'Venda registrada com sucesso!', 'success')
    await dispatchGetOrders()
  } catch (error) {
    await dispatchApiError(error)
  }
}

export const dispatchGetOrders = async () => {
  try {
    await order.actionGetOrders()
  } catch (error) {
    await dispatchApiError(error)
  }
}

export const dispatchUpdateOrder = async (payload) => {
  try {
    await order.actionUpdateOrder(payload)
    dispatchNotification('Atualização da venda', 'Dados da venda atualizados com sucesso!', 'success')
    await dispatchGetOrders()
  } catch (error) {
    await dispatchApiError(error)
  }
}

export const dispatchRemoveOrder = async (payload) => {
  try {
    await order.actionRemoveOrder(payload)
    dispatchNotification('Atualização da venda', 'Venda excluido com sucesso!', 'success')
    await dispatchGetOrders()
  } catch (error) {
    await dispatchApiError(error)
  }
}
