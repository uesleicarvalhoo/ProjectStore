export const itemsPerPage = process.env.ITEMS_PER_PAGE || 10

// let envApiUrl = process.env.API_URL || `${window.location.protocol}//${window.location.host}/api`;
let envApiUrl = "http://localhost:5000/api"

export const apiUrl = envApiUrl;
