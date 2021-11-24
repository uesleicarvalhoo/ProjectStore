import { context } from '@/store'

export const notification = {
  actionShowNotification (title, message, type) {
    context.commit('showNotification', true)
    context.commit('notification', { title: title, text: message, type: type })
  },
  actionHideNotification () {
    context.commit('showNotification', false)
  }
}
