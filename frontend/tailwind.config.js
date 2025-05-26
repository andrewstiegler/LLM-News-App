/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {},
  },
  plugins: [
    require('@tailwindcss/line-clamp'),
],
}

theme: {
  extend: {
    colors: {
      primary: '#2563EB',
      accent: '#FACC15',
      dark: '#111827',
      light: '#F3F4F6',
    },
  },
},
