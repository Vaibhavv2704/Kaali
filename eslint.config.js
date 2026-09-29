import tsParser from '@typescript-eslint/parser';
export default [
  {ignores:['node_modules/**','dist/**','.pnpm-store/**','artifacts/**']},
  {files:['**/*.{js,mjs,ts,tsx}'],languageOptions:{parser:tsParser,parserOptions:{ecmaVersion:'latest',sourceType:'module',ecmaFeatures:{jsx:true}}},rules:{'no-debugger':'error','no-dupe-args':'error','no-dupe-keys':'error','no-duplicate-case':'error','no-unreachable':'error','no-unsafe-finally':'error','valid-typeof':'error'}}
];
