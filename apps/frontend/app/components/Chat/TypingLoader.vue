<template>
  <div class="mr-auto flex items-center gap-1 rounded-full border border-slate-700 bg-slate-900 px-3 py-2">
    <span class="dot" />
    <span class="dot delay-1" />
    <span class="dot delay-2" />
  </div>
</template>

<style scoped>
.dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: #cbd5e1;
  animation: pulse 1.1s infinite ease-in-out;
}

.delay-1 {
  animation-delay: 0.15s;
}

.delay-2 {
  animation-delay: 0.3s;
}

@keyframes pulse {
  0%,
  80%,
  100% {
    transform: translateY(0);
    opacity: 0.5;
  }

  40% {
    transform: translateY(-4px);
    opacity: 1;
  }
}
</style>
