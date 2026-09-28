/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        obsidian: {
          950: '#070B12',
          900: '#0B132B',
          850: '#0F172A',
          800: '#1E293B',
          750: '#283548',
          700: '#334155'
        },
        cyanAccent: {
          DEFAULT: '#00F2FE',
          dim: 'rgba(0, 242, 254, 0.15)',
          glow: 'rgba(0, 242, 254, 0.35)'
        }
      },
      fontFamily: {
        mono: ['"JetBrains Mono"', 'monospace']
      }
    },
  },
  plugins: [],
}
