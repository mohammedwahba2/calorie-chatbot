interface ChatMessage {
  role: 'user' | 'bot'
  text: string
  direction?: 'rtl' | 'ltr'
  timestamp: string
}

const generateSessionId = () => {
  if (process.client && 'randomUUID' in crypto) {
    return crypto.randomUUID()
  }
  return `session-${Date.now()}-${Math.random().toString(16).slice(2)}`
}

export const useChat = () => {
  const messages = useState<ChatMessage[]>('chat-messages', () => [])
  const loading = useState<boolean>('chat-loading', () => false)
  const language = useState<'ar' | 'en' | null>('chat-language', () => null)
  const sessionId = useState<string | null>('chat-session-id', () => null)

  const detectLanguage = (text: string): 'ar' | 'en' => (/\p{Script=Arabic}/u.test(text) ? 'ar' : 'en')
  const directionFromLanguage = (lang: 'ar' | 'en') => (lang === 'ar' ? 'rtl' : 'ltr')

  const ensureSession = () => {
    if (!process.client) return
    if (!sessionId.value) {
      sessionId.value = localStorage.getItem('chat_session_id') || generateSessionId()
      localStorage.setItem('chat_session_id', sessionId.value)
    }
  }

  const getSessionMap = (): Record<string, string> => {
    if (!process.client) return {}
    try {
      const raw = localStorage.getItem('chat_session_map')
      return raw ? JSON.parse(raw) : {}
    } catch {
      return {}
    }
  }

  const saveSessionMap = (map: Record<string, string>) => {
    if (!process.client) return
    localStorage.setItem('chat_session_map', JSON.stringify(map))
  }

  const bindSessionToUser = (userKey: string, forceNew = false) => {
    if (!process.client) return
    const map = getSessionMap()
    const resolved = forceNew ? generateSessionId() : (map[userKey] || generateSessionId())
    map[userKey] = resolved
    saveSessionMap(map)
    sessionId.value = resolved
    localStorage.setItem('chat_session_id', resolved)
    messages.value = []
    language.value = null
    localStorage.setItem('chat_user_key', userKey)
  }

  const switchSessionForCurrentUser = (session: string) => {
    if (!process.client) return
    const userKey = localStorage.getItem('chat_user_key')
    if (!userKey) return
    const map = getSessionMap()
    map[userKey] = session
    saveSessionMap(map)
    sessionId.value = session
    localStorage.setItem('chat_session_id', session)
    messages.value = []
    language.value = null
  }

  const startNewChatForCurrentUser = (): string | null => {
    if (!process.client) return
    const userKey = localStorage.getItem('chat_user_key')
    if (!userKey) {
      reset()
      return sessionId.value
    }
    bindSessionToUser(userKey, true)
    return sessionId.value
  }

  const pushMessage = (message: Omit<ChatMessage, 'timestamp'> & { timestamp?: string }) => {
    messages.value.push({
      ...message,
      timestamp: message.timestamp || new Date().toISOString(),
    })
  }

  const setMessages = (items: ChatMessage[]) => {
    messages.value = items
  }

  const lockLanguage = (text: string) => {
    if (!language.value) {
      language.value = detectLanguage(text)
    }
  }

  const reset = () => {
    messages.value = []
    language.value = null
    sessionId.value = generateSessionId()
    if (process.client && sessionId.value) {
      localStorage.setItem('chat_session_id', sessionId.value)
    }
  }

  const clearRuntimeState = () => {
    messages.value = []
    language.value = null
  }

  return {
    messages,
    loading,
    language,
    sessionId,
    pushMessage,
    setMessages,
    ensureSession,
    bindSessionToUser,
    switchSessionForCurrentUser,
    startNewChatForCurrentUser,
    clearRuntimeState,
    lockLanguage,
    directionFromLanguage,
    reset,
  }
}
