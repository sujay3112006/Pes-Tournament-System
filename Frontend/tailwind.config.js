/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        dark: {
          50: '#f8fafc',
          100: '#f1f5f9',
          200: '#e2e8f0',
          300: '#cbd5e1',
          400: '#94a3b8',
          500: '#64748b',
          600: '#475569',
          700: '#334155',
          800: '#1e293b',
          900: '#0b0f1a',
          950: '#050812',
        },
        neon: {
          blue: '#00f0ff',
          cyan: '#00d9ff',
          purple: '#7a00ff',
          pink: '#ec4899',
          green: '#10b981',
          red: '#ef4444',
          orange: '#f97316',
        },
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', '-apple-system', 'sans-serif'],
        display: ['Poppins', 'system-ui', '-apple-system', 'sans-serif'],
        mono: ['JetBrains Mono', 'Fira Code', 'monospace'],
      },
      boxShadow: {
        glow: '0 0 15px rgba(0, 240, 255, 0.3), 0 0 30px rgba(0, 240, 255, 0.15)',
        'glow-md': '0 0 20px rgba(0, 240, 255, 0.4), 0 0 40px rgba(0, 240, 255, 0.2)',
        'glow-lg': '0 0 30px rgba(0, 240, 255, 0.5), 0 0 60px rgba(0, 240, 255, 0.25)',
        'glow-purple': '0 0 15px rgba(122, 0, 255, 0.4), 0 0 30px rgba(122, 0, 255, 0.2)',
        'glow-pink': '0 0 15px rgba(236, 72, 153, 0.4), 0 0 30px rgba(236, 72, 153, 0.2)',
        'inner-glow': 'inset 0 0 20px rgba(0, 240, 255, 0.1)',
        'gaming': '0 0 20px rgba(0, 240, 255, 0.3), inset 0 0 10px rgba(0, 240, 255, 0.1)',
      },
      animation: {
        pulse: 'pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'glow': 'glow 2s ease-in-out infinite',
        'pulse-urgent': 'pulse-urgent 1s infinite',
        'pulse-urgent-fast': 'pulse-urgent-fast 0.6s infinite',
        'shine': 'shine 3s ease-in-out infinite',
        'flash': 'flash 0.5s ease-in-out',
        'shake': 'shake 0.5s ease-in-out',
        'slide-up': 'slide-up 0.5s ease-out',
        'slide-down': 'slide-down 0.5s ease-out',
      },
      keyframes: {
        glow: {
          '0%, 100%': { boxShadow: '0 0 15px rgba(0, 240, 255, 0.3)' },
          '50%': { boxShadow: '0 0 30px rgba(0, 240, 255, 0.6)' },
        },
        'pulse-urgent': {
          '0%, 100%': { boxShadow: '0 0 0 0 rgba(0, 240, 255, 0.7)' },
          '50%': { boxShadow: '0 0 0 10px rgba(0, 240, 255, 0)' },
        },
        'pulse-urgent-fast': {
          '0%, 100%': { boxShadow: '0 0 0 0 rgba(236, 72, 153, 0.7)' },
          '50%': { boxShadow: '0 0 0 8px rgba(236, 72, 153, 0)' },
        },
        shine: {
          '0%, 100%': { boxShadow: 'inset -1000px 0 0 -1000px rgba(255, 255, 255, 0), 0 0 20px rgba(0, 240, 255, 0.3)' },
          '50%': { boxShadow: 'inset 0 0 20px rgba(255, 255, 255, 0.1), 0 0 30px rgba(0, 240, 255, 0.5)' },
        },
        flash: {
          '0%, 100%': { opacity: '1' },
          '50%': { opacity: '0.3' },
        },
        shake: {
          '0%, 100%': { transform: 'translateX(0)' },
          '25%': { transform: 'translateX(-5px)' },
          '75%': { transform: 'translateX(5px)' },
        },
        'slide-up': {
          from: { opacity: '0', transform: 'translateY(20px)' },
          to: { opacity: '1', transform: 'translateY(0)' },
        },
        'slide-down': {
          from: { opacity: '0', transform: 'translateY(-20px)' },
          to: { opacity: '1', transform: 'translateY(0)' },
        },
      },
      backdropBlur: {
        xs: '2px',
        sm: '4px',
        md: '12px',
        lg: '16px',
        xl: '24px',
        '2xl': '40px',
      },
    },
  },
  plugins: [],
}
