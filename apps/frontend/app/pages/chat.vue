<template>
  <div class="space-y-4">
    <div class="flex flex-wrap items-center gap-2">
      <NuxtLink to="/dashboard" class="rounded-lg border border-slate-700 px-3 py-2 text-xs hover:bg-slate-800">Dashboard</NuxtLink>
      <NuxtLink to="/profile" class="rounded-lg border border-slate-700 px-3 py-2 text-xs hover:bg-slate-800">Profile</NuxtLink>
      <NuxtLink to="/meals" class="rounded-lg border border-slate-700 px-3 py-2 text-xs hover:bg-slate-800">Meals</NuxtLink>
      <NuxtLink to="/progress" class="rounded-lg border border-slate-700 px-3 py-2 text-xs hover:bg-slate-800">Progress</NuxtLink>
      <button class="rounded-lg border border-blue-500 px-3 py-2 text-xs text-blue-300 hover:bg-blue-500/10" @click="startFresh">
        Start New Chat
      </button>
    </div>
    <div class="max-h-44 overflow-y-auto rounded-xl border border-slate-800 bg-slate-900/40 p-2">
      <div class="flex flex-wrap gap-2">
      <button
        v-for="session in sessions"
        :key="session.session_id"
        class="rounded-lg border px-3 py-2 text-left text-xs"
        :class="session.session_id === selectedSession ? 'border-blue-500 bg-blue-500/10 text-blue-200' : 'border-slate-700 text-slate-300 hover:bg-slate-800'"
        @click="onSessionPick(session.session_id)"
      >
        <p class="font-medium">{{ formatDate(session.updated_at) }}</p>
        <p class="max-w-[210px] truncate text-slate-400">{{ session.last_message || 'New chat' }}</p>
      </button>
      </div>
      <div class="mt-2 flex justify-center" v-if="hasMore">
        <button class="rounded border border-slate-700 px-3 py-1 text-xs text-slate-300 hover:bg-slate-800" @click="loadMore">
          Load More
        </button>
      </div>
    </div>
    <ChatBox />
  </div>
</template>

<script setup lang="ts">
definePageMeta({ middleware: ['auth'] })

const config = useRuntimeConfig()
const { hydrate, getAuthHeaders } = useAuth()
const { sessionId, startNewChatForCurrentUser, switchSessionForCurrentUser } = useChat()

const sessions = ref<Array<{ session_id: string; updated_at: string; last_message: string }>>([])
const selectedSession = ref('')
const totalSessions = ref(0)
const pageSize = 20

const formatDate = (value: string) => value ? new Date(value).toLocaleString() : 'No date'
const hasMore = computed(() => sessions.value.length < totalSessions.value)

const loadSessions = async (append = false) => {
  hydrate()
  const offset = append ? sessions.value.length : 0
  const res = await fetch(
    `${config.public.apiGatewayUrl}/chat/sessions?limit=${pageSize}&offset=${offset}`,
    { headers: { ...getAuthHeaders() } }
  )
  if (!res.ok) return
  const payload = await res.json() as {
    items: Array<{ session_id: string; updated_at: string; last_message: string }>
    total: number
  }
  totalSessions.value = payload.total || 0
  sessions.value = append ? [...sessions.value, ...payload.items] : payload.items
  selectedSession.value = sessionId.value || ''
}

const loadMore = async () => {
  await loadSessions(true)
}

const onSessionPick = (session: string) => {
  selectedSession.value = session
  switchSessionForCurrentUser(session)
}

const startFresh = async () => {
  const newSessionId = startNewChatForCurrentUser()
  if (newSessionId) {
    await fetch(`${config.public.apiGatewayUrl}/chat/sessions`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        ...getAuthHeaders()
      },
      body: JSON.stringify({ session_id: newSessionId })
    })
  }
  await loadSessions(false)
}

onMounted(loadSessions)
watch(sessionId, () => {
  selectedSession.value = sessionId.value || ''
})
</script>
