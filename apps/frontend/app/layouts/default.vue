<template>
  <div class="min-h-screen bg-slate-950 text-slate-100">
    <header class="border-b border-slate-800 bg-slate-900/70 backdrop-blur">
      <div class="mx-auto flex max-w-5xl items-center justify-between px-4 py-3">
        <h1 class="text-sm font-semibold tracking-wide">Calorie AI Assistant</h1>
        <button
          v-if="isAuthenticated"
          class="rounded-md bg-slate-800 px-3 py-1 text-xs hover:bg-slate-700"
          @click="logout"
        >
          Logout
        </button>
      </div>
    </header>

    <main class="mx-auto max-w-5xl px-4 py-6">
      <slot />
    </main>
  </div>
</template>

<script setup lang="ts">
const { isAuthenticated, logout } = useAuth()
</script>
