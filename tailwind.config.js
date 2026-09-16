/** Static Tailwind build — mirrors the design tokens previously in the CDN inline config */
module.exports = {
  content: ["./*.html"],
  theme: {
    extend: {
      colors: {
        surface: "#F5F2E9", "surface-low": "#EFEBDE", "surface-mid": "#E9E3D2",
        "surface-high": "#E1DAC5", cream: "#F5F2E9",
        forest: "#1C4A2A", "forest-deep": "#12351C", "forest-night": "#0D2416",
        gold: "#C6F84C", "gold-bright": "#D9FF70", "gold-soft": "#E4FCA6",
        bark: "#4A2E18", "bark-deep": "#39200b",
        ink: "#1b1c1a", "ink-soft": "#414942",
        outline: "#727971", "outline-soft": "#c1c8c0",
      },
      fontFamily: {
        display: ["'Bricolage Grotesque'", "sans-serif"],
        body: ["Manrope", "sans-serif"],
        label: ["Manrope", "sans-serif"],
        script: ["Caveat", "cursive"],
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
