import { defineConfig } from 'vite'
import { resolve } from 'path'

export default defineConfig({
  root: 'site',
  base: '/matt-beer-tasting/',
  build: {
    outDir: '../dist',
    emptyOutDir: true,
    rollupOptions: {
      input: {
        main: resolve(__dirname, 'site/index.html'),
        rating: resolve(__dirname, 'site/rating-sheet.html'),
        tastingNotes: resolve(__dirname, 'site/tasting-notes.html'),
      },
    },
  },
})
