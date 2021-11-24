<template>
  <table>
    <thead>
      <tr>
        <th class="text-center">Nome</th>
        <th class="text-center">Email</th>
        <th class="text-center">Telefone</th>
        <th class="text-center">Endereço</th>
        <th class="text-center">CEP</th>
        <th class="text-center">Cliente desde</th>
        <th class="text-center"></th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="client in itemsPaginated" :key="client.id">
        <td data-label="Nome">{{ client.name }}</td>
        <td class="text-center" data-label="Email">{{ client.email }}</td>
        <td class="text-center" data-label="Telefone">{{ client.phone }}</td>
        <td class="text-center" data-label="Endereço">{{ client.address }}</td>
        <td class="text-center" data-label="CEP">{{ client.zip_code }}</td>
        <td class="text-center" data-label="Cliente desde">
          {{ new Date(client.created_at).toLocaleDateString() }}
        </td>
        <td class="actions-cell" v-if="actions">
          <jb-buttons type="justify-start lg:justify-end" no-wrap>
            <jb-button
              class="mr-3"
              color="success"
              :icon="mdiEye"
              small
              @click="emitEvent('view', client)"
            />
            <jb-button
              color="danger"
              :icon="mdiTrashCan"
              small
              @click="emitEvent('remove', client)"
            />
          </jb-buttons>
        </td>
      </tr>
    </tbody>
  </table>
  <div class="table-pagination">
    <level>
      <jb-buttons>
        <jb-button
          v-for="page in pagesList"
          @click="currentPage = page"
          :active="page === currentPage"
          :label="page + 1"
          :key="page"
          :outline="darkMode"
          small
        />
      </jb-buttons>
      <small>Pagina {{ currentPageHuman }} de {{ numPages }}</small>
    </level>
  </div>
</template>

<script>
import { computed, ref } from 'vue'
import { useStore } from 'vuex'
import { mdiEye, mdiTrashCan } from '@mdi/js'
import Level from '@/components/Level'
import JbButtons from '@/components/JbButtons'
import JbButton from '@/components/JbButton'
import { itemsPerPage } from '@//env'

export default {
  name: 'TableClients',
  components: {
    Level,
    JbButtons,
    JbButton
  },
  props: {
    data: { type: Array, default: () => [] },
    actions: { type: Boolean, default: true }
  },
  emits: ['view', 'remove'],

  setup (props, { emit }) {
    const context = useStore()

    const darkMode = computed(() => context.state.darkMode)

    const items = computed(() => context.state.clients)

    const perPage = ref(itemsPerPage)

    const currentPage = ref(0)

    const itemsPaginated = computed(() =>
      items.value.slice(
        perPage.value * currentPage.value,
        perPage.value * (currentPage.value + 1)
      )
    )

    const emitEvent = (event, data) => {
      emit(event, data)
    }

    const numPages = computed(() =>
      Math.ceil(items.value.length / perPage.value)
    )

    const currentPageHuman = computed(() => currentPage.value + 1)

    const pagesList = computed(() => {
      const pagesList = []

      for (let i = 0; i < numPages.value; i++) {
        pagesList.push(i)
      }

      return pagesList
    })

    return {
      emitEvent,
      darkMode,
      currentPage,
      currentPageHuman,
      numPages,
      itemsPaginated,
      pagesList,
      mdiEye,
      mdiTrashCan
    }
  }
}
</script>
