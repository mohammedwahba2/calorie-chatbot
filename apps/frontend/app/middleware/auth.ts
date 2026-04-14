export default defineNuxtRouteMiddleware((to) => {
  if (!process.client) return

  const token = localStorage.getItem('access_token')
  const isAuthPage = to.path === '/login' || to.path === '/register'

  if (!token && !isAuthPage) {
    return navigateTo('/login')
  }

  if (token && isAuthPage) {
    return navigateTo('/chat')
  }
})
