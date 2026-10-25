/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,jsx}'],
  darkMode: 'class',
  theme: {
    extend: {
      fontFamily: {
        sans: ['Inter', 'ui-sans-serif', 'system-ui', 'sans-serif'],
        mono: ['"JetBrains Mono"', 'ui-monospace', 'monospace'],
      },
      colors: {
        phonetic: '#3b82f6',
        semantic: '#8b5cf6',
        visual: '#22c55e',
        goods: '#f97316',
      },
    },
  },
  plugins: [],
}
