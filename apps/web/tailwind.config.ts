import type { Config } from 'tailwindcss';

const config: Config = {
  content: [
    './src/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        cockpit: {
          bg: '#0a0a0f',
          card: '#14141f',
          border: '#1e1e2e',
          accent: '#6366f1',
          'accent-light': '#818cf8',
          success: '#22c55e',
          warning: '#f59e0b',
          danger: '#ef4444',
          muted: '#a1a1aa',
          text: '#e4e4e7',
        },
      },
    },
  },
  plugins: [],
};

export default config;
