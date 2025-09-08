module.exports = {
  content: [
    "./templates/**/*.{html,js}",
    "./templates/*.{html,js}",
    "./static_files/**/*.{html,js}"
  ],
  safelist: [
    // Include commonly used DaisyUI classes
    'btn', 'btn-primary', 'card', 'card-body',
    // Or use regex patterns to include more classes:
    { pattern: /^(btn|navbar|dropdown|menu|card|badge|avatar|modal|input|hero)-/ }
  ],
  plugins: [
    require('daisyui'),
  ],
  daisyui: {
    themes: ["light", "dark"],
  },
}

