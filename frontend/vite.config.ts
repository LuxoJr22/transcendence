import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';

export default defineConfig({
    plugins: [sveltekit()],
    server: {
        proxy: {
            '/api': 'http://backend:8000',
            '/ws': 'ws://backend:8000',
            '/media': 'http://backend:8000',
        }
    }
});
