/** Static Tailwind build — mirrors the design tokens previously in the CDN inline config */
module.exports = {
  content: ["./*.html"],
  theme: {
    extend: {
      colors: {
        surface: "#fbf9f6", "surface-low": "#f5f3f0", "surface-mid": "#efeeeb",
        "surface-high": "#eae8e5", cream: "#FAF8F5",
        forest: "#1A4329", "forest-deep": "#012d15", "forest-night": "#0E2616",
        gold: "#D4AF37", "gold-bright": "#fed65b", "gold-soft": "#ffe088",
        bark: "#4A2E18", "bark-deep": "#39200b",
        ink: "#1b1c1a", "ink-soft": "#414942",
        outline: "#727971", "outline-soft": "#c1c8c0",
      },
      fontFamily: {
        display: ["Syne", "sans-serif"],
        body: ["'DM Sans'", "sans-serif"],
        label: ["'Space Grotesk'", "sans-serif"],
      },
      boxShadow: {
        card: "0 8px 24px -4px rgba(26, 65, 41, 0.08)",
        pop: "0 16px 32px -6px rgba(74, 46, 24, 0.12)",
        modal: "0 20px 40px -8px rgba(26, 65, 41, 0.22)",
      },
      maxWidth: { shell: "1360px" },
    },
  },
  plugins: [require("@tailwindcss/forms")],
};
