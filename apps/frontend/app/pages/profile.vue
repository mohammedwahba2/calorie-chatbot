<template>
  <section class="space-y-4">
    <h2 class="text-lg font-semibold">Profile</h2>
    <div class="rounded-xl border border-slate-800 bg-slate-900 p-4 text-sm">
      <p class="text-slate-300">Email: {{ profile.email || '-' }}</p>
      <p class="text-slate-300">Goal: {{ profile.profile?.goal || '-' }}</p>
      <p class="text-slate-300">Weight: {{ profile.profile?.weight || '-' }} kg</p>
      <p class="text-slate-300">Height: {{ profile.profile?.height || '-' }} cm</p>
      <p class="text-slate-300">Age: {{ profile.profile?.age || '-' }}</p>
      <p class="text-slate-300">Activity: {{ profile.profile?.activity_level || '-' }}</p>
    </div>
  </section>
</template>

<script setup lang="ts">
definePageMeta({ middleware: ['auth'] })

const config = useRuntimeConfig()
const { hydrate, getAuthHeaders } = useAuth()
const profile = ref<any>({ profile: {} })

onMounted(async () => {
  hydrate()
  const res = await fetch(`${config.public.apiGatewayUrl}/me`, { headers: getAuthHeaders() })
  if (res.ok) profile.value = await res.json()
})
</script>
