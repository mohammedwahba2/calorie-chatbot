<template>
  <section class="space-y-4">
    <h2 class="text-lg font-semibold">Progress</h2>

    <div class="grid gap-2 sm:grid-cols-3">
      <input v-model.number="weight" class="field" type="number" placeholder="Current weight" />
      <input v-model="note" class="field" placeholder="Optional note" />
      <button class="btn" @click="submitProgress">Log Weight</button>
    </div>

    <div class="rounded-xl border border-slate-800 bg-slate-900 p-4">
      <p class="text-sm text-slate-300">Average weight: {{ data.average_weight || '-' }} kg</p>
      <p class="mt-2 text-sm text-slate-300">AI insight: {{ data.insight || '-' }}</p>
      <p class="mt-2 text-xs text-slate-400">Reminder: {{ data.daily_reminder || '-' }}</p>
    </div>

    <div class="rounded-xl border border-slate-800 bg-slate-900 p-4">
      <p class="mb-2 text-sm">Weight trend</p>
      <div class="flex h-36 items-end gap-2">
        <div
          v-for="item in data.logs || []"
          :key="item.id"
          class="w-6 rounded-t bg-blue-500"
          :style="{ height: `${Math.min(item.weight, 140) * 2}px` }"
          :title="`${item.weight} kg`"
        />
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
definePageMeta({ middleware: ['auth'] })

const config = useRuntimeConfig()
const { hydrate, getAuthHeaders } = useAuth()

const weight = ref<number | null>(null)
const note = ref('')
const data = ref<any>({ logs: [] })

const loadProgress = async () => {
  const res = await fetch(`${config.public.apiGatewayUrl}/progress`, { headers: getAuthHeaders() })
  if (res.ok) data.value = await res.json()
}

const submitProgress = async () => {
  if (!weight.value) return
  await fetch(`${config.public.apiGatewayUrl}/progress`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', ...getAuthHeaders() },
    body: JSON.stringify({ weight: weight.value, note: note.value || null }),
  })
  note.value = ''
  await loadProgress()
}

onMounted(async () => {
  hydrate()
  await loadProgress()
})
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
