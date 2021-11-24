import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home'
import { loginRequired, refreshToken } from '@/middlewares/auth'

const routes = [
  {
    // Document title tag
    // We combine it with defaultDocumentTitle set in `src/main.js` on router.afterEach hook
    meta: {
      title: 'Dashboard'
    },
    path: '/',
    name: 'home',
    component: Home
  },
  {
    meta: {
      title: 'Caixa'
    },
    path: '/caixa/cadastro',
    name: 'create-balance',
    component: () => import('../views/CreateBalance')
  },
  {
    meta: {
      title: 'Caixa'
    },
    path: '/caixa/',
    name: 'view-balances',
    component: () => import('../views/ViewBalance')
  },
  {
    meta: {
      title: 'Cliente'
    },
    path: '/clientes/cadastro',
    name: 'create-client',
    component: () => import('../views/CreateClient')
  },
  {
    meta: {
      title: 'Cliente'
    },
    path: '/clientes/',
    name: 'view-clients',
    component: () => import('../views/ViewClient')
  },
  {
    meta: {
      title: 'Estoque'
    },
    path: '/produtos/',
    name: 'view-items',
    component: () => import('../views/ViewItem')
  },
  {
    meta: {
      title: 'Item'
    },
    path: '/produtos/cadastro',
    name: 'create-item',
    component: () => import('../views/CreateItem')
  },
  {
    meta: {
      title: 'Vendas'
    },
    path: '/vendas/cadastro',
    name: 'create-order',
    component: () => import('../views/CreateOrder')
  },
  {
    meta: {
      title: 'Vendas'
    },
    path: '/vendas/',
    name: 'view-orders',
    component: () => import('../views/ViewOrder')
  },
  {
    meta: {
      title: 'Perfil'
    },
    path: '/me',
    name: 'me',
    component: () => import('../views/Profile')
  },
  {
    meta: {
      title: 'Cadastro de Usuários'
    },
    path: '/usuarios/cadastro',
    name: 'new-user',
    component: () => import('../views/CreateUser')
  },
  {
    meta: {
      title: 'Login',
      fullScreen: true
    },
    path: '/login',
    name: 'login',
    component: () => import('../views/Login')
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior (to, from, savedPosition) {
    return savedPosition || { top: 0 }
  }
})

router.beforeEach(loginRequired)
router.beforeEach(refreshToken)

export default router
