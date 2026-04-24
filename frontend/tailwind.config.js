/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        background: '#f9fafb', 
        panel: '#ffffff',
        primary: '#2563EB', 
        'primary-hover': '#1d4ed8', 
        border: '#e4e4e7', 
        text: '#18181b', 
        'text-muted': '#71717a', 
        success: '#22c55e',
        warning: '#eab308',
        error: '#ef4444'
      }
    },
  },
  plugins: [],
}
