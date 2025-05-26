module.exports = {
  content: [
    "./templates/**/*.{html,js}",
    "./**/templates/**/*.{html,js}", // pega templates dentro dos apps
    "./static/**/*.{js,css}"
  ],
  theme: {
    extend: {
      colors: {
        primary: { 500: "#6366f1", 600: "#4f46e5" },
      },
      borderRadius: { "2xl": "1.5rem" },
    },
  },
  plugins: [],
}