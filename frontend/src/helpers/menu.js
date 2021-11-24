import {
  mdiAccount,
  mdiCart,
  mdiChartTimelineVariant,
  mdiHome,
  mdiTableOfContents
} from '@mdi/js'

export default [
  '',
  [
    {
      to: { name: 'home' },
      icon: mdiHome,
      label: 'Dashboard'
    },
    {
      label: 'Clientes',
      icon: mdiAccount,
      menu: [
        {
          label: 'Visualizar',
          to: { name: 'view-clients' }
        },
        {
          label: 'Cadastrar cliente',
          to: { name: 'create-client' }
        }
      ]
    },
    {
      label: 'Financeiro',
      icon: mdiChartTimelineVariant,
      menu: [
        {
          label: 'Fluxo de caixa',
          to: { name: 'view-balances' }
        },
        {
          label: 'Novo registro',
          to: { name: 'create-balance' }
        }
      ]
    },
    {
      label: 'Produtos',
      icon: mdiTableOfContents,
      menu: [
        {
          label: 'Estoque',
          to: { name: 'view-items' }
        },
        {
          label: 'Novo produto',
          to: { name: 'create-item' }
        }
      ]
    },
    {
      label: 'Vendas',
      icon: mdiCart,
      menu: [
        {
          label: 'Visualizar',
          to: { name: 'view-orders' }
        },
        {
          label: 'Nova venda',
          to: { name: 'create-order' }
        }
      ]
    }
  ]
]
