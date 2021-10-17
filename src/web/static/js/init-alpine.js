function data() {
  function getThemeFromLocalStorage() {
    // if user already changed the theme, use it
    if (window.localStorage.getItem('dark')) {
      return JSON.parse(window.localStorage.getItem('dark'))
    }

    // else return their preferences
    return (
      !!window.matchMedia &&
      window.matchMedia('(prefers-color-scheme: dark)').matches
    )
  }

  function setThemeToLocalStorage(value) {
    window.localStorage.setItem('dark', value)
  }

  return {
    dark: getThemeFromLocalStorage(),
    toggleTheme() {
      this.dark = !this.dark
      setThemeToLocalStorage(this.dark)
    },
    isSideMenuOpen: false,
    toggleSideMenu() {
      this.isSideMenuOpen = !this.isSideMenuOpen
    },
    closeSideMenu() {
      this.isSideMenuOpen = false
    },
    isProfileMenuOpen: false,
    toggleProfileMenu() {
      this.isProfileMenuOpen = !this.isProfileMenuOpen
    },
    closeProfileMenu() {
      this.isProfileMenuOpen = false
    },
    isClientMenuOpen: false,
    toggleClientMenu() {
      this.isClientMenuOpen = !this.isClientMenuOpen
    },
    isPagesMenuOpen: false,
    togglePagesMenu() {
      this.isPagesMenuOpen = !this.isPagesMenuOpen
    },
    isSalesMenuOpen: false,
    toggleSalesMenu() {
      this.isSalesMenuOpen = !this.isSalesMenuOpen
    },
    isItemsMenuOpen: false,
    toggleItemsMenu() {
      this.isItemsMenuOpen = !this.isItemsMenuOpen
    },
    isFiscalNoteMenuOpen: false,
    toggleFiscalNoteMenu() {
      this.isFiscalNoteMenuOpen = !this.isFiscalNoteMenuOpen
    },
    isNotificationOpen: true,
    closeNotification() {
      this.isNotificationOpen = false
    },
    isFiscalNoteMenuOpen: false,
    toggleFiscalNoteMenu() {
      this.isFiscalNoteMenuOpen = !this.isFiscalNoteMenuOpen
    },
    isBalancesMenuOpen: false,
    toggleBalancesMenu() {
      this.isBalancesMenuOpen = !this.isBalancesMenuOpen
    },

    // Client
    targetClientId: null,
    targetClientName: null,
    setClientTarget(clientId, clientName) {
      this.targetClientId = clientId,
        this.targetClientName = clientName
    },

    deleteClient(clientId) {
      fetch(window.location.pathname.split(/\/\d$/)[0] + 'delete', {
        method: 'POST',
        body: new URLSearchParams({ 'id': clientId })
      })
        .then((response) => {
          if (response.status >= 400) {
            this.openModal('Ops!', 'Alguma coisa deu errado! x.x')
          }
          window.location.reload()
        })
        .catch(() => {
          this.openModal('Ops!', 'Alguma coisa deu errado! x.x')
        })
    },
    deleteFiscalNote(fiscalNoteId) {
      fetch(window.location.pathname.split(/\/\d$/)[0] + 'delete', {
        method: 'POST',
        body: new URLSearchParams({ 'id': fiscalNoteId })
      })
        .then((response) => {
          if (response.status >= 400) {
            this.openModal('Ops!', 'Alguma coisa deu errado! x.x')
          }
          window.location.reload()
        })
        .catch(() => {
          this.openModal('Ops!', 'Alguma coisa deu errado! x.x')
        })
    },
    deleteFiscalNoteItem(fiscalNoteItemId) {
      fetch(window.location.pathname.split(/\/\d$/)[0] + 'delete', {
        method: 'POST',
        body: new URLSearchParams({ 'id': fiscalNoteItemId })
      })
        .then((response) => {
          if (response.status >= 400) {
            this.openModal('Ops!', 'Alguma coisa deu errado! x.x')
          }
          window.location.reload()
        })
        .catch(() => {
          this.openModal('Ops!', 'Alguma coisa deu errado! x.x')
        })
    },
    deleteItem(itemId) {
      fetch('/produtos/delete', {
        method: 'POST',
        body: new URLSearchParams({ 'id': itemId })
      })
        .then((response) => {
          if (response.status >= 400) {
            this.openModal('Ops!', 'Alguma coisa deu errado! x.x')
          }
          window.location.reload()
        })
        .catch(() => {
          this.openModal('Ops!', 'Alguma coisa deu errado! x.x')
        })
    },
    deleteBalance(balanceId) {
      fetch('/caixa/delete', {
        method: 'POST',
        body: new URLSearchParams({ 'id': itemId })
      })
        .then((response) => {
          if (response.status >= 400) {
            this.openModal('Ops!', 'Alguma coisa deu errado! x.x')
          }
          window.location.reload()
        })
        .catch(() => {
          this.openModal('Ops!', 'Alguma coisa deu errado! x.x')
        })
    },

    // Modal
    isModalOpen: false,
    modalHeader: null,
    modalText: null,
    trapCleanup: null,
    closeModal() {
      this.isModalOpen = false
      this.trapCleanup()
    },
    modalAcceptCallback: function () {
      this.closeModal()
    },
    openModal(modalHeader, modalText, acceptCallback = null) {
      this.modalHeader = modalHeader
      this.modalText = modalText
      this.isModalOpen = true
      this.trapCleanup = focusTrap(document.querySelector('#modal'))

      if (acceptCallback == null) {
        acceptCallback = () => this.closeModal()

      } else {
        this.modalAcceptCallback = acceptCallback
      }
    },
  }
}

function fiscalNoteForm() {
  return {
    formData: {
      imageData: null,
      description: null,
      purchase_date: null,
    },
    fileChosen(event) {
      console.log(event)
      this.fileToDataUrl(event, src => this.imageData = src)
    },
    fileToDataUrl(event, callback) {
      if (!event.target.files.length) return
      let file = event.target.files[0],
        reader = new FileReader()
      reader.readAsText(file)
      console.log(reader)
      reader.onload = e => callback(e.target.result)
    },
    submitData() {
      var form = new FormData();
      form.append("file", this.formData.imageData)
      form.append("description", this.formData.description)
      form.append("purchase_date", this.formData.purchase_date)

      fetch(window.location, {
        method: 'POST',
        headers: {
          'content-Type': 'multipart/form-data'
        },
        body: form
      })
        .then((response) => {
          window.location.reload()
        })
        .catch(() => {
          this.openModal('Ops!', 'Alguma coisa deu errado! x.x')
        })
    }
  }
}

function imageViewer() {
  return {
    imageUrl: '',

    fileChosen(event) {
      this.fileToDataUrl(event, src => this.imageUrl = src)
    },

    fileToDataUrl(event, callback) {
      if (!event.target.files.length) return

      let file = event.target.files[0],
        reader = new FileReader()

      reader.readAsDataURL(file)
      reader.onload = e => callback(e.target.result)
    },
  }
}

function orderForm() {
  return {
    items: [],
    clients: [],
    orderItems: [],
    itemAmount: 1,
    saleType: null,
    description: null,
    selectedItem: null,
    selectedClient: { "phone": "-", "email": "-" },
    clientData: { "id": "-", "phone": "-", "email": "-" },

    updateData(clients, items) {
      this.clients = clients
      this.items = items
    },
    removeSelectedItem(item) {
      this.items = this.items.filter(item => (!this.orderItems.includes(item)))
    },
    updateSelectedClient() {
      this.clientData = JSON.parse(this.selectedClient)
    },
    addItem() {
      if (this.selectedItem !== null && !this.orderItems.includes(this.selectedItem)) {
        item = Object.assign({}, JSON.parse(this.selectedItem))
        item.amount = this.itemAmount
        this.orderItems.push(item)
      }
    },
    removeItem(item) {
      this.orderItems = this.orderItems.filter(el => el != item)
    },
    submitData() {
      fetch(window.location, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          client: this.selectedClient,
          items: this.orderItems,
          description: this.description,
          operation_type: this.saleType
        })
      })
        .then((response) => {
          if (response.status >= 400) {
            window.location.reload()
          }
          window.location.replace(window.location.pathname.split(/\/\d$/)[0])
        })
    }
  }
}
