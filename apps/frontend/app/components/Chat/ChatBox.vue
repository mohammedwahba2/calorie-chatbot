<template>
  <section class="mx-auto flex h-[78vh] w-full max-w-4xl flex-col rounded-2xl border border-slate-800 bg-slate-950/80">
    <div ref="scrollContainer" class="flex-1 space-y-3 overflow-y-auto p-4">
      <MessageBubble v-for="(msg, index) in messages" :key="index" :role="msg.role" :direction="msg.direction" :timestamp="msg.timestamp">
        <p class="whitespace-pre-wrap">{{ msg.text }}</p>
      </MessageBubble>

      <TypingLoader v-if="loading" />
    </div>

    <div class="border-t border-slate-800 p-3">
      <div class="flex gap-2">
        <input
          v-model="input"
          class="w-full rounded-xl border border-slate-700 bg-slate-900 px-4 py-3 text-sm outline-none focus:border-blue-500"
          :dir="direction"
          :placeholder="placeholder"
          @keyup.enter="send"
        >
        <button
          class="rounded-xl bg-blue-500 px-5 py-3 text-sm font-semibold text-white transition hover:bg-blue-400 disabled:cursor-not-allowed disabled:opacity-50"
          :disabled="loading || !input.trim()"
          @click="send"
        >
          Send
        </button>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import MessageBubble from './MessageBubble.vue'
import TypingLoader from './TypingLoader.vue'

const config = useRuntimeConfig()
const { hydrate, getAuthHeaders } = useAuth()
const { messages, loading, language, sessionId, pushMessage, setMessages, ensureSession, lockLanguage, directionFromLanguage } = useChat()
const input = ref('')
const scrollContainer = ref<HTMLElement | null>(null)

const detectLanguage = (text: string): 'ar' | 'en' => (/\p{Script=Arabic}/u.test(text) ? 'ar' : 'en')

const direction = computed(() => {
  if (language.value) return directionFromLanguage(language.value)
  return detectLanguage(input.value || 'hello') === 'ar' ? 'rtl' : 'ltr'
})

const placeholder = computed(() => {
  return language.value === 'ar' ? 'اكتب رسالتك...' : 'Type your message...'
})

const scrollToBottom = async () => {
  await nextTick()
  if (scrollContainer.value) {
    scrollContainer.value.scrollTop = scrollContainer.value.scrollHeight
  }
}

const loadHistory = async () => {
  if (!sessionId.value) return
  try {
    const historyRes = await fetch(`${config.public.apiGatewayUrl}/chat/history/${sessionId.value}`, {
      headers: { ...getAuthHeaders() },
    })
    if (historyRes.ok) {
      const history = await historyRes.json() as Array<{ role: string; content: string; timestamp: string }>
      if (history.length) {
        const mapped = history
          .filter(item => item.role === 'user' || item.role === 'assistant')
          .map(item => ({
            role: item.role === 'assistant' ? 'bot' as const : 'user' as const,
            text: item.content,
            direction: detectLanguage(item.content) === 'ar' ? 'rtl' as const : 'ltr' as const,
            timestamp: item.timestamp || new Date().toISOString(),
          }))
        setMessages(mapped)
      } else {
        setMessages([])
      }
    }
  } catch {
    // Ignore history fetch failure and continue with empty chat state.
  }
}

watch(messages, scrollToBottom, { deep: true })
watch(sessionId, async () => {
  setMessages([])
  await loadHistory()
  if (!messages.value.length) {
    pushMessage({ role: 'bot', text: 'Hi! Tell me your goal and I will build your nutrition plan.', direction: 'ltr' })
  }
  await scrollToBottom()
})

onMounted(async () => {
  hydrate()
  ensureSession()
  await loadHistory()
  if (!messages.value.length) {
    pushMessage({ role: 'bot', text: 'Hi! Tell me your goal and I will build your nutrition plan.', direction: 'ltr' })
  }
  await scrollToBottom()
})

const send = async () => {
  const text = input.value.trim()
  if (!text || loading.value) return

  lockLanguage(text)
  const activeLang = language.value || detectLanguage(text)
  const dir = directionFromLanguage(activeLang)

  pushMessage({ role: 'user', text, direction: dir })
  input.value = ''
  loading.value = true

  try {
    const apiRes = await fetch(`${config.public.apiGatewayUrl}/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        ...getAuthHeaders(),
      },
      body: JSON.stringify({ message: text, session_id: sessionId.value }),
    })
    const response = await apiRes.json() as { reply: string; language: string; detail?: string }
    if (!apiRes.ok) {
      throw new Error(response.detail || 'Request failed')
    }

    await new Promise(resolve => setTimeout(resolve, 650))
    const botDir = response.language === 'ar' ? 'rtl' : 'ltr'
    pushMessage({ role: 'bot', text: response.reply, direction: botDir })
  } catch {
    const fallback = activeLang === 'ar' ? 'حصل خطأ، حاول مرة تانية.' : 'Something went wrong, try again.'
    pushMessage({ role: 'bot', text: fallback, direction: dir })
  } finally {
    loading.value = false
    await scrollToBottom()
  }
}
</script>
