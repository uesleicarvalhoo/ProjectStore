export const storage = {
    getAccessToken() {
        const token = localStorage.getItem("accessToken")
        return JSON.parse(token)
    },
    setAccessToken(token) {
        localStorage.setItem("accessToken", JSON.stringify(token))
    },
    removeAccessToken() {
        localStorage.removeItem("accessToken")
    },
}