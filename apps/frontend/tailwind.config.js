/** @type {import('tailwindcss').Config} */
export default {
  content: [
    './app/app.vue',
    './app/components/**/*.{js,ts,vue}',
    './app/composables/**/*.{js,ts}',
    './app/layouts/**/*.{js,ts,vue}',
    './app/pages/**/*.{js,ts,vue}',
    './app/middleware/**/*.{js,ts}',
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
