import { defineConfig } from 'vite';

export default defineConfig(({ mode }) => {
  if (mode === 'plugin') {
    return {
      build: {
        outDir: 'dist',
        emptyOutDir: false,
        lib: {
          entry: 'src/plugin.js',
          formats: ['es'],
          fileName: () => 'mcp-tools.js',
        },
        rollupOptions: {
          external: ['react', 'react-dom'],
        },
      },
    };
  }
  return {
    build: {
      outDir: 'dist',
      emptyOutDir: false,
    },
  };
});
