<template>
  <main-section>
    <title-sub-bar :icon="mdiBallotOutline" :title="title" />
    <card-component
      title="Registro"
      :icon="mdiBallot"
      @submit.prevent="submit"
      form
    >
      <control v-model="data.id" hidden />
      <field label="Cliente">
        <control :options="clients" v-model="data.client" required />
      </field>

      <field label="Telefone">
        <control v-model="data.client.phone" :disabled="true" required />
      </field>

      <field label="Email">
        <control v-model="data.client.email" :disabled="true" required />
      </field>

      <field label="Tipo de Pagamento">
        <control :options="saleTypes" v-model="data.saleType" required />
      </field>

      <field label="Descrição">
        <control
          placeholder="Descrição do produto"
          type="textarea"
          v-model="data.description"
          required
        />
      </field>

      <divider />

      <field label="Produtos">
        <control :options="products" v-model="data.product" />
        <control
          v-model="data.amount"
          placeholder="Quantidade do produto"
          type="number"
          min="1"
          step="1"
        />
        <jb-button
          color="success"
          label="Adicionar"
          :icon="mdiCheck"
          small
          @click="addItem()"
        />
      </field>

      <table>
        <thead>
          <tr>
            <th class="text-center">Descrição</th>
            <th class="text-center">Código</th>
            <th class="text-center">Valor</th>
            <th class="text-center">Quantidade</th>
            <th class="text-center">Ações</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in data.items" v-bind:key="item.id">
            <td data-label="Descrição" class="text-center">{{ item.name }}</td>
            <td data-label="Código" class="text-center">{{ item.code }}</td>
            <td data-label="Valor" class="text-center">{{ item.value }}</td>
            <td data-label="Quantidade" class="text-center">
              {{ item.amount }}
            </td>
            <td class="actions-cell items-center justify-between">
              <jb-buttons no-wrap>
                <jb-button
                  color="danger"
                  :icon="mdiTrashCan"
                  small
                  @click="removeItem(item.id)"
                />
              </jb-buttons>
            </td>
          </tr>
        </tbody>
      </table>

      <divider />

      <jb-buttons>
        <jb-button color="info" type="submit" label="Confirmar" />
        <jb-button type="reset" color="info" outline label="Limpar" />
      </jb-buttons>
    </card-component>
  </main-section>

  <modal-box
    v-model="warningModal.active"
    large-title="Ops!"
    button="warning"
    buttonLabel="Ok"
    shake
  >
    <p v-text="warningModal.text"></p>
  </modal-box>
</template>

<script>
import { computed, reactive } from 'vue'
import { mdiBallot, mdiBallotOutline, mdiCheck, mdiTrashCan } from '@mdi/js'
import MainSection from '@/components/MainSection'
import CardComponent from '@/components/CardComponent'
import Divider from '@/components/Divider.vue'
import JbButton from '@/components/JbButton'
import JbButtons from '@/components/JbButtons'
import Field from '@/components/Field'
import Control from '@/components/Control'
import TitleSubBar from '@/components/TitleSubBar'
import ModalBox from '@/components/ModalBox'
import {
  dispatchGetClients,
  dispatchGetItems,
  dispatchSaleTypes
} from '@/controller'
import { useStore } from 'vuex'

export default {
  name: 'FormOrder',
  components: {
    TitleSubBar,
    Divider,
    MainSection,
    CardComponent,
    ModalBox,
    Field,
    Control,
    JbButton,
    JbButtons
  },
  props: {
    title: { type: String, default: () => 'Formulário de vendas' },
    data: {
      type: Object,
      default: () =>
        reactive({
          id: null,
          client: {},
          saleType: null,
          description: null,
          product: null,
          amount: 1,
          items: []
        })
    }
  },
  emits: ['submit'],
  async created () {
    await dispatchGetClients()
    await dispatchGetItems()
    await dispatchSaleTypes()
  },
  setup (props, { emit }) {
    const context = useStore()

    const clients = computed(() => context.state.clients)

    const products = computed(() => context.state.items)

    const saleTypes = computed(() => context.state.saleTypes)

    const warningModal = reactive({
      active: false,
      text: ''
    })

    const getItemFromForm = (itemId) => {
      const filtredItems = props.data.items.filter((el) => el.id === itemId)
      if (filtredItems.length > 0) {
        return filtredItems[0]
      } else {
        return null
      }
    }

    const addItem = () => {
      if (!props.data.amount | (props.data < 1)) {
        warningModal.active = true
        warningModal.text = 'A quantidade do produto precisa ser maior que 0!'
        return
      }

      if (props.data.product.id) {
        const product = Object.assign(props.data.product)
        const item = getItemFromForm(product.id)

        if (item !== null) {
          item.amount = item.amount + Number(props.data.amount)
        } else {
          product.amount = Number(props.data.amount)
          props.data.items.push(product)
        }
      }
    }

    const removeItem = (itemId) => {
      const item = getItemFromForm(itemId)

      const index = props.data.items.indexOf(item)

      if (index > -1) {
        props.data.items.splice(index, 1)
      }
    }

    const submit = () => {
      if (props.data.items.length === 0) {
        warningModal.active = true
        warningModal.text = 'Adicione pelo menos um item ao carrinho!'
      } else {
        const details = []

        props.data.items.forEach((el) => {
          details.push({
            item_id: el.id,
            item_name: el.name,
            item_value: el.value,
            item_amount: el.amount,
            value: el.value
          })
        })

        const data = {
          id: props.data.id,
          client_id: props.data.client.id,
          sale_type: props.data.saleType,
          description: props.data.description,
          items: details
        }
        emit('submit', data)
        if (data.id === null) {
          reset()
        }
      }
    }

    const reset = () => {
      props.data.client = {}
      props.data.saleType = null
      props.data.description = null
      props.data.product = null
      props.data.items = []
    }

    return {
      submit,
      clients,
      products,
      addItem,
      removeItem,
      warningModal,
      saleTypes,
      mdiBallot,
      mdiBallotOutline,
      mdiCheck,
      mdiTrashCan
    }
  }
}
</script>
