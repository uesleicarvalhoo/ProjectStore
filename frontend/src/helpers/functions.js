export function sum (data, key) {
  const total = []

  Object.entries(data).forEach(([_, val]) => {
    total.push(val[key])
  })

  return total.reduce(function (total, num) { return total + num }, 0)
}
