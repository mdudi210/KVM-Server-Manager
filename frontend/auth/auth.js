export function isAuthenticated() {
  const token = sessionStorage.getItem('user-info')

  if (!token) return false

  try {
    const parts = token.split('.')
    if (parts.length !== 3) return false

    const payload = JSON.parse(atob(parts[1]))
    const now = Math.floor(Date.now() / 1000)

    if (payload.exp && payload.exp < now) {
      sessionStorage.removeItem('user-info')
      return false
    }

    return true
  } catch (err) {
    console.error('Invalid token format:', err)
    sessionStorage.removeItem('user-info')
    return false
  }
}
