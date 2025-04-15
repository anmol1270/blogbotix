/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      backgroundColor: {
        background: '#ffffff',
        foreground: '#213547',
        card: '#ffffff',
        'card-foreground': '#213547',
        popover: '#ffffff',
        'popover-foreground': '#213547',
        'primary-foreground': '#ffffff',
        secondary: '#f3f4f6',
        'secondary-foreground': '#213547',
        muted: '#f3f4f6',
        'muted-foreground': '#6b7280',
        accent: '#f3f4f6',
        'accent-foreground': '#213547',
        destructive: '#ef4444',
        'destructive-foreground': '#ffffff',
        border: '#e5e7eb',
        input: '#e5e7eb',
        ring: '#213547',
      },
      textColor: {
        background: '#ffffff',
        foreground: '#213547',
        card: '#ffffff',
        'card-foreground': '#213547',
        popover: '#ffffff',
        'popover-foreground': '#213547',
        'primary-foreground': '#ffffff',
        secondary: '#f3f4f6',
        'secondary-foreground': '#213547',
        muted: '#f3f4f6',
        'muted-foreground': '#6b7280',
        accent: '#f3f4f6',
        'accent-foreground': '#213547',
        destructive: '#ef4444',
        'destructive-foreground': '#ffffff',
        border: '#e5e7eb',
        input: '#e5e7eb',
        ring: '#213547',
      },
      colors: {
        primary: {
          50: '#f0f9ff',
          100: '#e0f2fe',
          200: '#bae6fd',
          300: '#7dd3fc',
          400: '#38bdf8',
          500: '#0ea5e9',
          600: '#0284c7',
          700: '#0369a1',
          800: '#075985',
          900: '#0c4a6e',
        },
      },
      borderRadius: {
        lg: "var(--radius)",
        md: "calc(var(--radius) - 2px)",
        sm: "calc(var(--radius) - 4px)",
      },
    },
  },
  plugins: [
    require('@tailwindcss/typography'),
  ],
}

