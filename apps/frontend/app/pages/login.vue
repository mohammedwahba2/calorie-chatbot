<template>
  <section class="mx-auto mt-14 w-full max-w-md rounded-2xl border border-slate-800 bg-slate-900 p-6">
    <h2 class="mb-4 text-xl font-semibold">Login</h2>

    <div class="space-y-3">
      <input v-model="email" class="field" type="email" placeholder="Email" />
      <input v-model="password" class="field" type="password" placeholder="Password" />

      <button class="btn" :disabled="loading" @click="login">{{ loading ? 'Loading...' : 'Login' }}</button>
      <p class="text-sm text-slate-400">
        No account?
        <NuxtLink to="/register" class="text-blue-400 hover:text-blue-300">Create one</NuxtLink>
      </p>
      <p v-if="error" class="text-sm text-rose-400">{{ error }}</p>
    </div>
  </section>
</template>

<script setup lang="ts">
definePageMeta({ middleware: ['auth'] })

const config = useRuntimeConfig()
const { saveToken, hydrate, getAuthHeaders } = useAuth()
const { bindSessionToUser } = useChat()

const email = ref('')
const password = ref('')
const error = ref('')
const loading = ref(false)

onMounted(() => {
  hydrate()
})

const login = async () => {
  error.value = ''
  loading.value = true
  try {
    const data = await $fetch<{ access_token: string }>(`${config.public.apiGatewayUrl}/auth/login`, {
      method: 'POST',
      body: { email: email.value, password: password.value }
    })
    saveToken(data.access_token)
    const meRes = await fetch(`${config.public.apiGatewayUrl}/me`, {
      headers: {
        ...getAuthHeaders()
      }
    })
    if (meRes.ok) {
      const me = await meRes.json() as { email: string }
      bindSessionToUser(me.email, false)
    } else {
      bindSessionToUser(email.value.toLowerCase(), false)
    }
    await navigateTo('/chat')
  } catch (e: any) {
    error.value = e?.data?.detail || 'Login failed'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.field {
  width: 100%;
  border-radius: 0.75rem;
  border: 1px solid #334155;
  background: #0f172a;
  padding: 0.7rem 0.9rem;
}

.btn {
  width: 100%;
  border-radius: 0.75rem;
  background: #3b82f6;
  color: white;
  padding: 0.7rem;
  font-weight: 600;
}
</style>
