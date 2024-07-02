/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './templates/**/*.html',
    './static/css/**/*.css',
  ],
    theme: {
      extend: {
        colors: {
         'custom-disco':'#d7e334',
         'custom-disco2':'#B459B0'
         ,
        },
      },
  },
  plugins: [],
}

