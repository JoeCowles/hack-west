import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        background: "var(--background)",
        foreground: "var(--foreground)",
      },
      backgroundSize: {
        '300%': '300%',
      },
      animation: {
        shimmer: 'shimmer 3s ease-in-out infinite',
      },
      keyframes: {
        shimmer: {
          '0%, 100%': { backgroundPosition: 'left center' },
          '50%': { backgroundPosition: 'right center' },
        },
      },
    },
  },
  plugins: [],
};
export default config;
