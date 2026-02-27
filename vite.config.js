import { defineConfig } from 'vite'

export default defineConfig({
  base: '/matt-beer-tasting/',
  build: {
    rollupOptions: {
      input: {
        main: 'index.html',
        rating: 'rating-sheet.html',
      },
    },
  },
})
