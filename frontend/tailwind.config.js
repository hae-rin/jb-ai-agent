/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      fontFamily: {
        sans: ['-apple-system', 'BlinkMacSystemFont', 'Segoe UI', 'Noto Sans KR', 'sans-serif'],
      },
      keyframes: {
        float: {
          '0%, 100%': { transform: 'translateY(0px)', animationTimingFunction: 'cubic-bezier(0.45, 0, 0.55, 1)' },
          '50%':       { transform: 'translateY(-12px)', animationTimingFunction: 'cubic-bezier(0.45, 0, 0.55, 1)' },
        },
        floatB: {
          '0%, 100%': { transform: 'translateY(0px)' },
          '50%':       { transform: 'translateY(-10px)' },
        },
        floatC: {
          '0%, 100%': { transform: 'translateY(0px) scale(1)', animationTimingFunction: 'cubic-bezier(0.45, 0, 0.55, 1)' },
          '50%':       { transform: 'translateY(-8px) scale(1.04)', animationTimingFunction: 'cubic-bezier(0.45, 0, 0.55, 1)' },
        },
        fadeInUp: {
          from: { opacity: '0', transform: 'translateY(28px)' },
          to:   { opacity: '1', transform: 'translateY(0)' },
        },
        fadeIn: {
          from: { opacity: '0' },
          to:   { opacity: '1' },
        },
        pulse_soft: {
          '0%, 100%': { opacity: '1' },
          '50%': { opacity: '0.7' },
        },
      },
      animation: {
        'float':         'float  3.8s ease-in-out infinite',
        'float-2':       'float  4.2s ease-in-out 0.5s infinite',
        'float-3':       'floatB 5.0s ease-in-out 1.1s infinite',
        'float-4':       'floatC 4.6s ease-in-out 1.8s infinite',
        'fade-in-up':    'fadeInUp 0.65s ease-out both',
        'fade-in-up-2':  'fadeInUp 0.65s ease-out 0.12s both',
        'fade-in-up-3':  'fadeInUp 0.65s ease-out 0.24s both',
        'fade-in-up-4':  'fadeInUp 0.65s ease-out 0.36s both',
        'fade-in':       'fadeIn 0.5s ease-out both',
        'pulse-soft':    'pulse_soft 2s ease-in-out infinite',
      },
    },
  },
  plugins: [],
}
