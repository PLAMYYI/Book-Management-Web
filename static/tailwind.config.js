module.exports = {
  content: [
    "../templates/**/*.html"
  ],
  theme: {
    extend: {},
  },
  plugins: [require("daisyui")],
  daisyui: {
    themes: ["silk"], // 👈 ใช้ silk
  },
}