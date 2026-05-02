SECTIONS = r"""

<!-- ═══════════════════════════════════════════════════════════════════
     BUILD TOOLS & DEV ENVIRONMENT — 6 SUB-SECTIONS
     ═══════════════════════════════════════════════════════════════════ -->

<h2 id="build-webpack" class="section-break">68. Webpack</h2>
<p class="small"><strong>Checklist:</strong> Entry/output · loaders · plugins · code splitting · tree shaking · dev server · HMR · Module Federation</p>

<pre>// webpack.config.js
const path = require('path');
const HtmlWebpackPlugin = require('html-webpack-plugin');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const { BundleAnalyzerPlugin } = require('webpack-bundle-analyzer');

module.exports = (env, argv) => ({
  mode: argv.mode || 'development',

  // Entry — where Webpack starts building the dependency graph
  entry: {
    main: './src/index.ts',
    vendor: './src/vendor.ts'    // separate bundle for 3rd-party code
  },

  // Output — where bundles go
  output: {
    path: path.resolve(__dirname, 'dist'),
    filename: '[name].[contenthash:8].js',   // cache-busting
    chunkFilename: '[name].[contenthash:8].chunk.js',
    clean: true                               // clear dist/ on build
  },

  // Loaders — transform files before bundling
  module: {
    rules: [
      { test: /\.tsx?$/, use: 'ts-loader', exclude: /node_modules/ },
      {
        test: /\.scss$/,
        use: [
          MiniCssExtractPlugin.loader,  // extract CSS to separate file
          'css-loader',                  // resolve @import, url()
          'postcss-loader',              // autoprefixer, etc.
          'sass-loader'                  // compile SCSS → CSS
        ]
      },
      {
        test: /\.(png|jpg|gif|svg)$/,
        type: 'asset',                  // Webpack 5: auto inline/file based on size
        parser: { dataUrlCondition: { maxSize: 8 * 1024 } } // inline &lt; 8KB
      }
    ]
  },

  // Plugins — extend Webpack functionality
  plugins: [
    new HtmlWebpackPlugin({ template: './src/index.html' }),
    new MiniCssExtractPlugin({ filename: '[name].[contenthash:8].css' }),
    new BundleAnalyzerPlugin({ analyzerMode: 'static', openAnalyzer: false })
  ],

  // Code splitting
  optimization: {
    splitChunks: {
      chunks: 'all',
      cacheGroups: {
        vendor: {
          test: /[\\/]node_modules[\\/]/,
          name: 'vendors',
          chunks: 'all'
        }
      }
    },
    runtimeChunk: 'single'  // separate Webpack runtime
  },

  devServer: {
    port: 3000,
    hot: true,          // Hot Module Replacement
    proxy: { '/api': 'http://localhost:8080' }
  },

  resolve: {
    extensions: ['.ts', '.tsx', '.js'],
    alias: { '@': path.resolve(__dirname, 'src') }
  }
});</pre>

<h2 id="build-vite" class="section-break">69. Vite</h2>
<p class="small"><strong>Checklist:</strong> ES modules in dev · Rollup for production · config · plugins · CSS handling · env variables · SSR</p>

<pre>// vite.config.ts
import { defineConfig } from 'vite';

export default defineConfig({
  root: 'src',
  build: {
    outDir: '../dist',
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ['lodash-es', 'date-fns'],  // separate vendor chunk
          charts: ['chart.js']
        }
      }
    },
    target: 'es2020',
    sourcemap: true,
    minify: 'terser'
  },
  server: {
    port: 3000,
    proxy: {
      '/api': { target: 'http://localhost:8080', changeOrigin: true }
    }
  },
  css: {
    preprocessorOptions: {
      scss: { additionalData: '@use "src/styles/vars" as *;' }
    },
    modules: { localsConvention: 'camelCase' }
  },
  resolve: {
    alias: { '@': '/src' }
  }
});

// Why Vite is faster than Webpack in development:
// 1. Uses native ES modules — no bundling in dev!
//    Browser requests modules → Vite serves them directly
// 2. Pre-bundles dependencies with esbuild (100x faster than JS-based tools)
// 3. HMR only updates the changed module (not full rebuild)
// 4. Production uses Rollup — optimized, tree-shaken bundles</pre>

<h2 id="build-babel" class="section-break">70. Babel &amp; Transpilation</h2>
<p class="small"><strong>Checklist:</strong> Presets · plugins · polyfills · browserslist · source maps · babel.config.json vs .babelrc</p>

<pre>// babel.config.json
{
  "presets": [
    ["@babel/preset-env", {
      "targets": "> 0.5%, last 2 versions, not dead",
      "useBuiltIns": "usage",     // auto-import polyfills only when used
      "corejs": 3,                 // polyfill library version
      "modules": false             // keep ES modules for tree-shaking
    }],
    "@babel/preset-typescript"
  ],
  "plugins": [
    ["@babel/plugin-proposal-decorators", { "version": "2023-11" }],
    "@babel/plugin-transform-runtime"  // reuse Babel helpers
  ]
}

// .browserslistrc — shared target for Babel, PostCSS, etc.
> 0.5%
last 2 versions
not dead
not ie 11

// What Babel transforms:
// ES2015+ → ES5 (arrow functions, classes, async/await, optional chaining)
// TypeScript → JavaScript (strips types, no type checking)
// JSX → createElement calls
// Decorators → wrapper functions

// What Babel does NOT do:
// ❌ Type checking (use tsc for that)
// ❌ Bundling (that's Webpack/Rollup/Vite)
// ❌ Minification (that's Terser/esbuild)</pre>

<h2 id="build-package-managers" class="section-break">71. Package Managers</h2>
<p class="small"><strong>Checklist:</strong> npm vs yarn vs pnpm · lockfiles · semantic versioning · peer dependencies · workspaces · publishing</p>

<table>
<thead><tr><th>Feature</th><th>npm</th><th>yarn</th><th>pnpm</th></tr></thead>
<tbody>
<tr><td>Speed</td><td>Moderate</td><td>Fast</td><td>Fastest</td></tr>
<tr><td>Disk usage</td><td>Duplicates</td><td>Duplicates</td><td>Content-addressable store (shared)</td></tr>
<tr><td>Lock file</td><td>package-lock.json</td><td>yarn.lock</td><td>pnpm-lock.yaml</td></tr>
<tr><td>Workspaces</td><td>Yes (npm 7+)</td><td>Yes</td><td>Yes</td></tr>
<tr><td>Strictness</td><td>Hoists all</td><td>Hoists all</td><td>Strict (symlinks, no phantom deps)</td></tr>
</tbody>
</table>

<pre>// Semantic Versioning: MAJOR.MINOR.PATCH
// ^1.2.3 → >=1.2.3 &lt;2.0.0  (caret: compatible with minor updates)
// ~1.2.3 → >=1.2.3 &lt;1.3.0  (tilde: compatible with patch updates)
// 1.2.3  → exactly 1.2.3

// Peer dependencies — "I expect the consumer to have this"
// Used by libraries to avoid bundling framework they extend
{
  "peerDependencies": {
    "@angular/core": ">=16.0.0"    // consumer must install Angular 16+
  },
  "peerDependenciesMeta": {
    "@angular/core": { "optional": false }
  }
}

// Monorepo workspaces (pnpm)
// pnpm-workspace.yaml
packages:
  - 'packages/*'
  - 'apps/*'
// Shared node_modules, symlinked packages, faster installs</pre>

<h2 id="build-linting" class="section-break">72. Linting &amp; Formatting</h2>
<p class="small"><strong>Checklist:</strong> ESLint configuration · custom rules · Prettier · Stylelint · pre-commit hooks (husky + lint-staged) · EditorConfig</p>

<pre>// .eslintrc.json
{
  "root": true,
  "extends": [
    "eslint:recommended",
    "plugin:@typescript-eslint/recommended",
    "plugin:@angular-eslint/recommended",
    "prettier"                    // disables formatting rules (Prettier handles those)
  ],
  "rules": {
    "no-console": "warn",
    "@typescript-eslint/no-explicit-any": "error",
    "@typescript-eslint/no-unused-vars": ["error", { "argsIgnorePattern": "^_" }]
  },
  "overrides": [{
    "files": ["*.spec.ts"],
    "rules": { "@typescript-eslint/no-explicit-any": "off" }
  }]
}

// .prettierrc
{
  "semi": true,
  "singleQuote": true,
  "printWidth": 100,
  "trailingComma": "all",
  "arrowParens": "always",
  "bracketSpacing": true
}

// Pre-commit hooks with Husky + lint-staged
// package.json
{
  "lint-staged": {
    "*.{ts,js}": ["eslint --fix", "prettier --write"],
    "*.{css,scss}": ["stylelint --fix", "prettier --write"],
    "*.html": ["prettier --write"]
  }
}

// .husky/pre-commit
#!/bin/sh
npx lint-staged</pre>

<h2 id="build-env-vars" class="section-break">73. Environment Variables</h2>
<p class="small"><strong>Checklist:</strong> .env files · dotenv · environment-specific configs · never commit secrets</p>

<pre>// Angular environment files
// src/environments/environment.ts (dev)
export const environment = {
  production: false,
  apiUrl: 'http://localhost:3000/api',
  featureFlags: { darkMode: true, newCheckout: true }
};

// src/environments/environment.prod.ts (prod)
export const environment = {
  production: true,
  apiUrl: 'https://api.example.com',
  featureFlags: { darkMode: true, newCheckout: false }
};

// Vite — .env files
// .env              → loaded in all cases
// .env.local        → loaded in all cases, ignored by git
// .env.development  → loaded in dev mode
// .env.production   → loaded in production build

// .env
VITE_API_URL=http://localhost:3000
VITE_APP_TITLE=My App

// Access in code (only VITE_ prefixed vars are exposed!)
const apiUrl = import.meta.env.VITE_API_URL;

// Security rules:
// ❌ NEVER put secrets in frontend .env files (they're in the bundle!)
// ❌ NEVER commit .env.local or files with real credentials
// ✅ Use backend environment variables for secrets
// ✅ Use CI/CD environment variables for build-time config
// ✅ Add .env*.local to .gitignore</pre>

<div class="interview-q">
<h4>🎯 Interview Questions — Build Tools</h4>
<p><strong>Q: Why is Vite faster than Webpack in development?</strong></p>
<p><strong>A:</strong> Vite uses native ES modules in development — the browser loads modules individually, so there's no bundling step. Dependencies are pre-bundled with esbuild (written in Go, 100x faster than JS-based bundlers). HMR only replaces the changed module, not rebuilds. In production, Vite uses Rollup for optimized output. Webpack bundles everything even in dev.</p>

<p><strong>Q: What is tree shaking and how does it work?</strong></p>
<p><strong>A:</strong> Tree shaking eliminates dead code (unused exports) from the final bundle. It works by analyzing ES module static imports at build time. Requirements: (1) Use ES modules (import/export, not require). (2) Set <code>"sideEffects": false</code> in package.json. (3) Avoid side effects at module top level. (4) Use named imports, not <code>import *</code>. Webpack, Rollup, and esbuild all support it.</p>
</div>

"""
