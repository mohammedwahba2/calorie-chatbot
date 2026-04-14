<template>
  <div :class="['flex w-full items-end gap-2', role === 'user' ? 'justify-end' : 'justify-start']">
    <div
      v-if="role === 'bot'"
      class="flex h-8 w-8 items-center justify-center rounded-full bg-slate-700 text-xs font-semibold text-slate-200"
    >
      AI
    </div>

    <div
      :dir="direction"
      :class="[
        'max-w-[85%] rounded-2xl px-4 py-3 text-sm leading-6 shadow',
        role === 'user'
          ? 'rounded-br-md bg-blue-500 text-white'
          : 'rounded-bl-md border border-slate-700 bg-slate-800 text-slate-100'
      ]"
    >
      <slot />
      <p class="mt-1 text-[11px] opacity-70">{{ formattedTime }}</p>
    </div>
  </div>
</template>

<script setup lang="ts">
const props = defineProps<{ role: 'user' | 'bot'; direction?: 'rtl' | 'ltr'; timestamp: string }>()
const formattedTime = computed(() => new Date(props.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }))
</script>
