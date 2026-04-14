<template>
  <section class="space-y-5">
    <div class="flex flex-wrap gap-2 text-xs">
      <NuxtLink to="/chat" class="rounded-lg border border-slate-700 px-3 py-2 hover:bg-slate-800">Chat</NuxtLink>
      <NuxtLink to="/profile" class="rounded-lg border border-slate-700 px-3 py-2 hover:bg-slate-800">Profile</NuxtLink>
      <NuxtLink to="/meals" class="rounded-lg border border-slate-700 px-3 py-2 hover:bg-slate-800">Meals</NuxtLink>
      <NuxtLink to="/progress" class="rounded-lg border border-slate-700 px-3 py-2 hover:bg-slate-800">Progress</NuxtLink>
    </div>

    <h2 class="text-lg font-semibold">Coach Dashboard</h2>

    <div class="grid gap-3 sm:grid-cols-3">
      <div class="rounded-xl border border-slate-800 bg-slate-900 p-4">
        <p class="text-xs text-slate-400">Calories Logged Today</p>
        <p class="text-2xl font-semibold">{{ stats.totalCalories }}</p>
      </div>
      <div class="rounded-xl border border-slate-800 bg-slate-900 p-4">
        <p class="text-xs text-slate-400">Protein</p>
        <p class="text-2xl font-semibold">{{ stats.protein }} g</p>
      </div>
      <div class="rounded-xl border border-slate-800 bg-slate-900 p-4">
        <p class="text-xs text-slate-400">Carbs</p>
        <p class="text-2xl font-semibold">{{ stats.carbs }} g</p>
      </div>
    </div>

    <div class="rounded-xl border border-slate-800 bg-slate-900 p-4">
      <p class="mb-2 text-sm text-slate-300">Macro split</p>
      <div class="h-3 overflow-hidden rounded bg-slate-700">
        <div class="h-full bg-blue-500" :style="{ width: macroSplit.protein + '%' }"></div>
      </div>
      <div class="mt-2 h-3 overflow-hidden rounded bg-slate-700">
        <div class="h-full bg-emerald-500" :style="{ width: macroSplit.carbs + '%' }"></div>
      </div>
      <div class="mt-2 h-3 overflow-hidden rounded bg-slate-700">
        <div class="h-full bg-amber-500" :style="{ width: macroSplit.fat + '%' }"></div>
      </div>
      <p class="mt-2 text-xs text-slate-400">Protein / Carbs / Fat</p>
    </div>
  </section>
</template>

<script setup lang="ts">
definePageMeta({ middleware: ['auth'] })

const config = useRuntimeConfig()
const { hydrate, getAuthHeaders } = useAuth()

const meals = ref<any[]>([])

const fetchMeals = async () => {
  hydrate()
  const res = await fetch(`${config.public.apiGatewayUrl}/meals/log`, { headers: getAuthHeaders() })
  meals.value = res.ok ? await res.json() : []
}

const stats = computed(() => {
  const totalCalories = Math.round(meals.value.reduce((acc, m) => acc + (m.calories || 0), 0))
  const protein = Math.round(meals.value.reduce((acc, m) => acc + (m.protein_g || 0), 0))
  const carbs = Math.round(meals.value.reduce((acc, m) => acc + (m.carbs_g || 0), 0))
  const fat = Math.round(meals.value.reduce((acc, m) => acc + (m.fat_g || 0), 0))
  return { totalCalories, protein, carbs, fat }
})

const macroSplit = computed(() => {
  const total = stats.value.protein + stats.value.carbs + stats.value.fat
  if (!total) return { protein: 0, carbs: 0, fat: 0 }
  return {
    protein: Math.round((stats.value.protein / total) * 100),
    carbs: Math.round((stats.value.carbs / total) * 100),
    fat: Math.round((stats.value.fat / total) * 100),
  }
})

onMounted(fetchMeals)
</script>
