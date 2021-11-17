function deleteOrder(orderId) {
  fetch(window.location.pathname.split(/\/\d$/)[0] + '/delete', {
    method: 'POST',
    body: new URLSearchParams({ 'id': orderId })
  })
    .then((response) => {
      window.location.reload()
    })
    .catch(() => {
      this.openModal('Ops!', 'Alguma coisa deu errado! x.x')
    })
}

function confirmOrder(orderId) {
  fetch(window.location.pathname.split(/\/\d$/)[0] + "/status", {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      "order_id": orderId,
      'status': 2
    })
  })
    .then((response) => {
      window.location.reload()
    })
    .catch(() => {
      this.openModal('Ops!', 'Alguma coisa deu errado! x.x')
    })
}

function cancelOrder(orderId) {
  fetch(window.location.pathname.split(/\/\d$/)[0] + "/status", {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      "order_id": orderId,
      'status': 3
    })
  })
    .then((response) => {
      window.location.reload()
    })
    .catch(() => {
      this.openModal('Ops!', 'Alguma coisa deu errado! x.x')
    })
}
