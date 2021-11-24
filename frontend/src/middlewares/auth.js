import { context } from '@/store'
import { dispatchRefreshToken } from '@/controller'

export function loginRequired (to, from, next) {
  if (to.name !== 'login' && !context.state.loggedIn) {
    return next({ name: 'login' })
  } else {
    return next()
  }
}

export async function refreshToken (to, from, next) {
  if (to.name === 'login' || !context.state.loggedIn) {
    return next()
  } else {
    const now = Date.now() / 1000
    const refreshTime = (10 * 60)
    const timeUntilExpire = now - context.state.expireTokenTime

    if (timeUntilExpire <= refreshTime) {
      await dispatchRefreshToken()
    }

    return next()
  }
}
