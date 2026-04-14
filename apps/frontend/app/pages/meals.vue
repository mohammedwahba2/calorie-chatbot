<template>
  <section class="space-y-4">
    <h2 class="text-lg font-semibold">Meal Tracker</h2>

    <div class="grid gap-2 sm:grid-cols-2">
      <select v-model="form.meal_type" class="field">
        <option value="breakfast">Breakfast</option>
        <option value="lunch">Lunch</option>
        <option value="dinner">Dinner</option>
        <option value="snack">Snack</option>
      </select>
      <input v-model="form.description" class="field" placeholder="Meal description" />
      <input v-model.number="form.calories" class="field" type="number" placeholder="Calories" />
      <button class="btn" @click="submitMeal">Log Meal</button>
    </div>

    <div class="space-y-2">
      <div v-for="meal in meals" :key="meal.id" class="rounded-lg border border-slate-800 bg-slate-900 p-3 text-sm">
        <p class="font-semibold capitalize">{{ meal.meal_type }} - {{ meal.calories || 0 }} kcal</p>
        <p class="text-slate-300">{{ meal.description }}</p>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
definePageMeta({ middleware: ['auth'] })

const config = useRuntimeConfig()
const { hydrate, getAuthHeaders } = useAuth()
const { sessionId, ensureSession } = useChat()

const meals = ref<any[]>([])
const form = ref({ meal_type: 'breakfast', description: '', calories: 0 })

const loadMeals = async () => {
  const res = await fetch(`${config.public.apiGatewayUrl}/meals/log`, { headers: getAuthHeaders() })
  meals.value = res.ok ? await res.json() : []
}

const submitMeal = async () => {
  await fetch(`${config.public.apiGatewayUrl}/meals/log`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', ...getAuthHeaders() },
    body: JSON.stringify({ ...form.value, session_id: sessionId.value }),
  })
  form.value.description = ''
  form.value.calories = 0
  await loadMeals()
}

onMounted(async () => {
  hydrate()
  ensureSession()
  await loadMeals()
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
