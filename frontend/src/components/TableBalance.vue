<template>
  <table>
    <thead>
      <tr>
        <th class="text-center">Operação</th>
        <th class="text-center">Valor</th>
        <th class="text-center">Descrição</th>
        <th class="text-center">Data</th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="balance in itemsPaginated" :key="balance.id">
        <td data-label="Operação">{{ balance.operation }}</td>
        <td class="text-center" data-label="Valor">
          R$ {{ balance.value }}
        </td>
        <td class="text-center" data-label="Descrição">
          {{ balance.description }}
        </td>
        <td class="text-center" data-label="Data">
          {{ new Date(balance.created_at).toLocaleDateString() }}
        </td>
        <td class="actions-cell" v-if="actions">
          <jb-buttons type="justify-start lg:justify-end" no-wrap>
            <jb-button
              color="danger"
              :icon="mdiTrashCan"
              small
              @click="emitEvent('remove', balance)"
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
import { mdiTrashCan } from '@mdi/js'
import Level from '@/components/Level'
import JbButtons from '@/components/JbButtons'
import JbButton from '@/components/JbButton'
import { itemsPerPage } from '@//env'

export default {
  name: 'TableBalance',
  components: {
    Level,
    JbButtons,
    JbButton
  },
  props: {
    actions: { type: Boolean, default: true }
  },
  emits: ['remove'],

  setup (props, { emit }) {
    const context = useStore()

    const darkMode = computed(() => context.state.darkMode)

    const items = computed(() => context.state.balances)

    const perPage = ref(itemsPerPage)

    const currentPage = ref(0)

    const itemsPaginated = computed(() =>
      items.value.slice(
        perPage.value * currentPage.value,
        perPage.value * (currentPage.value + 1)
      )
    )

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

    const emitEvent = (event, data) => {
      emit(event, data)
    }

    return {
      darkMode,
      emitEvent,
      currentPage,
      currentPageHuman,
      numPages,
      itemsPaginated,
      pagesList,
      mdiTrashCan
    }
  }
}
</script>
