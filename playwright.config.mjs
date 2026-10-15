import {defineConfig} from '@playwright/test';
export default defineConfig({
  testDir: './tests', testMatch: '**/*.spec.mjs', timeout: 20000, use: {baseURL: 'http://127.0.0.1:4179'},
  webServer: {command: 'python3 -m http.server 4179 --bind 127.0.0.1 --directory dist', url: 'http://127.0.0.1:4179', reuseExistingServer: false, stdout: 'ignore', stderr: 'ignore'},
  projects: [{name: 'chromium', use: {browserName: 'chromium'}}],
});
