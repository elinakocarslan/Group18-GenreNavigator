import { defineConfig } from 'vite';
import { sveltekit } from '@sveltejs/kit/vite';
import svelte from '@sveltejs/vite-plugin-svelte';

export default defineConfig({
	plugins: [sveltekit()],
	server: {
	  proxy: {
		'/start_game': 'http://127.0.0.1:5000',
		'/guess': 'http://127.0.0.1:5000',
	  },
	},
  });

