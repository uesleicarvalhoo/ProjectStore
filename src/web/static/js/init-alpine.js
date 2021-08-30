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

    // Client
    targetClientId: null,
    targetClientName: null,
    setClientTarget(clientId, clientName) {
      this.targetClientId = clientId,
        this.targetClientName = clientName
    },

    deleteClient(clientId) {
      console.log(clientId)
      fetch(window.location.pathname.split(/\/\d$/)[0] + 'delete', {
        method: 'POST',
        body: new URLSearchParams({ 'id': clientId })
      })
        .then((response) => {
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
        console.log('tenho callback!')
        this.modalAcceptCallback = acceptCallback
      }
    },
  }
}
