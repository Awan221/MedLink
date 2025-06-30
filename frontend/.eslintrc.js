// .eslintrc.js
module.exports = {
  root: true,
  env: {
    node: true,
  },
  parser: "vue-eslint-parser",
  parserOptions: {
    parser: "@babel/eslint-parser", // ou "espree" ou autre selon vos dépendances
    ecmaVersion: 2020,
    sourceType: "module",
  },
  extends: [
    "plugin:vue/vue3-recommended",
    "eslint:recommended",
  ],
  rules: {
    // Vos règles ici
  },
};
