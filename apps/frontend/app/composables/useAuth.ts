export const useAuth = () => {
  const token = useState<string | null>('auth-token', () => null)

  const isAuthenticated = computed(() => Boolean(token.value))

  const hydrate = () => {
    if (!process.client) return
    token.value = localStorage.getItem('access_token')
  }

  const saveToken = (value: string) => {
    token.value = value
    if (process.client) {
      localStorage.setItem('access_token', value)
    }
  }

  const getAuthHeaders = (): Record<string, string> => {
    return token.value ? { Authorization: `Bearer ${token.value}` } : {}
  }

  const logout = async () => {
    const { clearRuntimeState } = useChat()
    clearRuntimeState()
    token.value = null
    if (process.client) {
      localStorage.removeItem('access_token')
    }
    await navigateTo('/login')
  }

  return { token, isAuthenticated, hydrate, saveToken, getAuthHeaders, logout }
}
