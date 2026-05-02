SECTIONS = r"""

<!-- ═══════════════════════════════════════════════════════════════════
     TYPESCRIPT — 7 SUB-SECTIONS
     ═══════════════════════════════════════════════════════════════════ -->

<h2 id="ts-basics" class="section-break">40. TypeScript Basics</h2>
<p class="small"><strong>Checklist:</strong> Type annotations · inference · any/unknown/never/void · arrays/tuples · interfaces · type vs interface · optional/readonly</p>

<pre>// Type annotations vs inference
let name: string = 'Sid';    // explicit annotation
let age = 28;                 // inferred as number (no annotation needed)

// any vs unknown vs never
let risky: any = 42;          // disables type checking — avoid!
let safe: unknown = 42;       // must narrow before use
if (typeof safe === 'number') { safe.toFixed(2); } // OK after narrowing

function throwError(msg: string): never {
  throw new Error(msg);       // never returns — function always throws
}

// Tuples — fixed-length, typed arrays
type UserTuple = [string, number, boolean]; // [name, age, active]
const user: UserTuple = ['Sid', 28, true];
user[0].toUpperCase(); // TS knows index 0 is string

// Interface vs Type
interface User {
  readonly id: number;
  name: string;
  email?: string;      // optional
}
type UserOrAdmin = User | Admin; // unions only with type
interface AdminUser extends User { permissions: string[]; } // extends with interface
// Rule of thumb: use interface for object shapes, type for unions/intersections</pre>

<h2 id="ts-advanced-types" class="section-break">41. TypeScript Advanced Types</h2>
<p class="small"><strong>Checklist:</strong> Union/intersection · literal types · discriminated unions · type guards (typeof/instanceof/user-defined) · type assertions · type narrowing</p>

<pre>// Discriminated unions — type-safe state machines
type RequestState&lt;T&gt; =
  | { status: 'idle' }
  | { status: 'loading' }
  | { status: 'success'; data: T }
  | { status: 'error'; error: string };

function handleState&lt;T&gt;(state: RequestState&lt;T&gt;): string {
  switch (state.status) {
    case 'idle':    return 'Ready';
    case 'loading': return 'Loading...';
    case 'success': return `Got: ${JSON.stringify(state.data)}`; // TS knows .data exists
    case 'error':   return `Error: ${state.error}`;              // TS knows .error exists
  } // exhaustive — TS ensures all cases are handled
}

// User-defined type guard
interface Cat { meow(): void; }
interface Dog { bark(): void; }
function isCat(pet: Cat | Dog): pet is Cat {
  return 'meow' in pet; // narrows type within if block
}
const pet: Cat | Dog = getPet();
if (isCat(pet)) { pet.meow(); } // TS knows it's Cat
else { pet.bark(); }              // TS knows it's Dog

// Intersection types — combine types
type Timestamped = { createdAt: Date; updatedAt: Date };
type SoftDeletable = { deletedAt: Date | null };
type AuditableUser = User & Timestamped & SoftDeletable;

// Literal types
type Direction = 'up' | 'down' | 'left' | 'right';
type HttpStatus = 200 | 201 | 400 | 401 | 403 | 404 | 500;

// Template literal types
type HttpMethod = 'GET' | 'POST' | 'PUT' | 'DELETE';
type ApiRoute = `/${string}`;
type Endpoint = `${HttpMethod} ${ApiRoute}`;
// Valid: 'GET /users', 'POST /orders'</pre>

<h2 id="ts-generics" class="section-break">42. TypeScript Generics</h2>
<p class="small"><strong>Checklist:</strong> Generic functions · interfaces · classes · constraints · default parameters · utility types</p>

<pre>// Generic function — works with any type while maintaining type safety
function first&lt;T&gt;(arr: T[]): T | undefined {
  return arr[0];
}
first([1, 2, 3]);         // returns number
first(['a', 'b']);         // returns string
// TS infers the type from the argument!

// Generic with constraint
function getProperty&lt;T, K extends keyof T&gt;(obj: T, key: K): T[K] {
  return obj[key];
}
const user = { name: 'Sid', age: 28 };
getProperty(user, 'name');  // string
// getProperty(user, 'invalid'); // ❌ Compile error!

// Generic interface
interface ApiResponse&lt;T&gt; {
  data: T;
  status: number;
  message: string;
  timestamp: Date;
}
type UserResponse = ApiResponse&lt;User&gt;;
type OrderListResponse = ApiResponse&lt;Order[]&gt;;

// Generic class
class TypedStorage&lt;T&gt; {
  private items = new Map&lt;string, T&gt;();
  set(key: string, value: T): void { this.items.set(key, value); }
  get(key: string): T | undefined { return this.items.get(key); }
}
const userStore = new TypedStorage&lt;User&gt;();
userStore.set('u1', { id: 1, name: 'Sid' });
const u = userStore.get('u1'); // User | undefined

// Default generic parameter
interface PaginatedResponse&lt;T, M = Record&lt;string, unknown&gt;&gt; {
  data: T[];
  meta: M;
  total: number;
  page: number;
}</pre>

<h2 id="ts-utility-types" class="section-break">43. TypeScript Utility Types</h2>
<p class="small"><strong>Checklist:</strong> Partial/Required/Readonly · Pick/Omit · Record · Exclude/Extract · NonNullable · ReturnType/Parameters · Awaited · mapped types · conditional types</p>

<pre>interface User {
  id: number;
  name: string;
  email: string;
  password: string;
  role: 'admin' | 'user';
}

// Built-in utility types — CRITICAL for interviews
type CreateUser = Omit&lt;User, 'id'&gt;;                        // no id for creation
type UpdateUser = Partial&lt;Omit&lt;User, 'id'&gt;&gt;;                // all fields optional
type PublicUser = Pick&lt;User, 'id' | 'name' | 'email'&gt;;      // no password
type ReadonlyUser = Readonly&lt;User&gt;;                          // all readonly
type RequiredUser = Required&lt;User&gt;;                          // all required
type UserRecord = Record&lt;string, User&gt;;                      // dictionary

// Exclude/Extract — filter union types
type StringOrNumber = string | number | boolean;
type OnlyStrNum = Exclude&lt;StringOrNumber, boolean&gt;;  // string | number
type OnlyBool = Extract&lt;StringOrNumber, boolean&gt;;    // boolean

// ReturnType & Parameters
function createUser(name: string, email: string): User { /* ... */ }
type CreateReturn = ReturnType&lt;typeof createUser&gt;;    // User
type CreateParams = Parameters&lt;typeof createUser&gt;;    // [string, string]

// Awaited — unwrap Promise type
type UserPromise = Promise&lt;User&gt;;
type ResolvedUser = Awaited&lt;UserPromise&gt;; // User

// Custom mapped type — make all properties nullable
type Nullable&lt;T&gt; = { [K in keyof T]: T[K] | null };
type NullableUser = Nullable&lt;User&gt;; // { id: number | null; name: string | null; ... }

// Conditional type
type IsArray&lt;T&gt; = T extends Array&lt;any&gt; ? true : false;
type Test1 = IsArray&lt;string[]&gt;;  // true
type Test2 = IsArray&lt;string&gt;;    // false

// Deep Partial — recursive
type DeepPartial&lt;T&gt; = {
  [K in keyof T]?: T[K] extends object ? DeepPartial&lt;T[K]&gt; : T[K];
};</pre>

<h2 id="ts-functions" class="section-break">44. TypeScript Functions</h2>
<p class="small"><strong>Checklist:</strong> Function type expressions · call signatures · overload signatures · rest params with types · optional params · return types</p>

<pre>// Function type expression
type MathFn = (a: number, b: number) => number;
const add: MathFn = (a, b) => a + b;

// Call signatures (in interfaces)
interface Formatter {
  (input: string): string;
  locale: string; // function with properties
}

// Overload signatures — different return types based on input
function parse(input: string): string[];
function parse(input: string, limit: number): string[];
function parse(input: number): number;
function parse(input: string | number, limit?: number): string[] | number {
  if (typeof input === 'string') return input.split(',', limit);
  return input;
}
const result = parse('a,b,c'); // TS infers string[]
const result2 = parse(42);     // TS infers number

// Rest parameters
function merge&lt;T&gt;(...objects: Partial&lt;T&gt;[]): T {
  return Object.assign({}, ...objects) as T;
}</pre>

<h2 id="ts-enums" class="section-break">45. TypeScript Enums</h2>
<p class="small"><strong>Checklist:</strong> Numeric enums · string enums · const enums · heterogeneous enums</p>

<pre>// String enum — most recommended
enum OrderStatus {
  Pending = 'PENDING',
  Processing = 'PROCESSING',
  Shipped = 'SHIPPED',
  Delivered = 'DELIVERED',
  Cancelled = 'CANCELLED'
}
function getStatusColor(status: OrderStatus): string {
  switch (status) {
    case OrderStatus.Pending: return 'yellow';
    case OrderStatus.Shipped: return 'blue';
    case OrderStatus.Delivered: return 'green';
    case OrderStatus.Cancelled: return 'red';
    default: return 'gray';
  }
}

// const enum — inlined at compile time (no runtime object!)
const enum Direction { Up = 0, Down = 1, Left = 2, Right = 3 }
const move = Direction.Up; // compiled to: const move = 0;
// No Direction object exists at runtime = smaller bundle

// Modern alternative: union of literals (recommended over enum)
type Status = 'pending' | 'active' | 'closed';
// Advantages over enum: no runtime code, simpler, tree-shakeable</pre>

<h2 id="ts-modules" class="section-break">46. TypeScript Modules &amp; Configuration</h2>
<p class="small"><strong>Checklist:</strong> ES6 module syntax · declaration files (.d.ts) · ambient declarations · triple-slash directives · tsconfig.json · strict mode · target/lib · module resolution · path mapping</p>

<pre>// Declaration files — type definitions for JS libraries
// types.d.ts
declare module 'legacy-library' {
  export function doSomething(input: string): number;
  export interface Config { timeout: number; }
}

// Ambient declarations — global types
declare global {
  interface Window {
    analytics: { track: (event: string, data: object) => void };
  }
}

// tsconfig.json — key options explained
{
  "compilerOptions": {
    "target": "ES2022",           // output JS version
    "lib": ["ES2022", "DOM"],     // available APIs
    "module": "ESNext",           // module system
    "moduleResolution": "bundler", // how imports are resolved
    "strict": true,               // enables ALL strict checks:
    // strictNullChecks, strictFunctionTypes, strictBindCallApply,
    // strictPropertyInitialization, noImplicitAny, noImplicitThis
    "esModuleInterop": true,      // import default from CommonJS
    "skipLibCheck": true,         // skip checking .d.ts files (faster)
    "paths": {                    // path aliases
      "@shared/*": ["src/shared/*"],
      "@models/*": ["src/models/*"]
    },
    "baseUrl": "./",
    "declaration": true,          // generate .d.ts files
    "sourceMap": true             // generate source maps
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist"]
}</pre>

<div class="interview-q">
<h4>🎯 Interview Questions — TypeScript</h4>
<p><strong>Q: What's the difference between <code>any</code> and <code>unknown</code>?</strong></p>
<p><strong>A:</strong> <code>any</code> disables type checking entirely — you can do anything with it (unsafe). <code>unknown</code> is the type-safe version — you must narrow the type before using it (with <code>typeof</code>, <code>instanceof</code>, or type guards). Use <code>unknown</code> for values of uncertain type (e.g., API responses, user input).</p>

<p><strong>Q: When would you use <code>type</code> vs <code>interface</code>?</strong></p>
<p><strong>A:</strong> <strong>interface</strong>: object shapes, class contracts, declaration merging (extensions). <strong>type</strong>: unions, intersections, mapped types, conditional types, primitives. If it's an object shape that might be extended, use interface. If it involves unions or complex type manipulation, use type.</p>

<p><strong>Q: Implement a type that makes certain keys required and the rest optional.</strong></p>
<pre>type RequireKeys&lt;T, K extends keyof T&gt; = Required&lt;Pick&lt;T, K&gt;&gt; & Partial&lt;Omit&lt;T, K&gt;&gt;;
type CreateOrder = RequireKeys&lt;Order, 'productId' | 'quantity'&gt;;
// productId and quantity are required, everything else is optional</pre>
</div>

<!-- ═══════════════════════════════════════════════════════════════════
     PERFORMANCE — 8 SUB-SECTIONS
     ═══════════════════════════════════════════════════════════════════ -->

<h2 id="perf-loading" class="section-break">47. Loading Performance</h2>
<p class="small"><strong>Checklist:</strong> Code splitting · dynamic imports · tree shaking · bundle analysis · minification/compression · lazy loading images · preload/prefetch/preconnect · resource hints · HTTP/2-3 · CDN</p>

<pre>&lt;!-- Resource hints — tell the browser what's coming --&gt;
&lt;link rel="preconnect" href="https://api.example.com"&gt;       &lt;!-- establish connection early --&gt;
&lt;link rel="dns-prefetch" href="https://cdn.example.com"&gt;     &lt;!-- resolve DNS early --&gt;
&lt;link rel="preload" href="/fonts/inter.woff2" as="font" type="font/woff2" crossorigin&gt; &lt;!-- load critical resource --&gt;
&lt;link rel="prefetch" href="/js/checkout.chunk.js"&gt;            &lt;!-- speculative next page --&gt;
&lt;link rel="modulepreload" href="/js/utils.mjs"&gt;               &lt;!-- preload ES module --&gt;

// Code splitting with dynamic imports
const AdminModule = lazy(() => import('./admin/admin.module'));
// Angular: loadChildren in routes
{ path: 'admin', loadChildren: () => import('./admin/admin.routes') }

// Tree shaking — works with ES modules (static imports)
import { formatDate } from './utils'; // only formatDate is bundled
// ❌ import * as Utils from './utils'; // may prevent tree shaking

// Bundle analysis commands
// Angular: ng build --stats-json → webpack-bundle-analyzer
// Vite: npx vite-bundle-visualizer</pre>

<h2 id="perf-runtime" class="section-break">48. Runtime Performance</h2>
<p class="small"><strong>Checklist:</strong> Debounce/throttle · requestAnimationFrame · avoiding layout thrashing · read-write batching · virtual scrolling · infinite scroll optimization · memoization · Web Workers · OffscreenCanvas</p>

<pre>// Layout thrashing — BAD: read-write-read-write forces multiple reflows
elements.forEach(el => {
  const height = el.offsetHeight;        // READ → forces layout
  el.style.height = height * 2 + 'px';  // WRITE → invalidates layout
  // Next iteration: READ forces layout AGAIN!
});

// GOOD: Batch all reads, THEN all writes
const heights = elements.map(el => el.offsetHeight); // batch READ
elements.forEach((el, i) => {
  el.style.height = heights[i] * 2 + 'px'; // batch WRITE
});

// Virtual scrolling — only render visible items
// For a list of 100,000 items, only render ~20-30 visible in viewport
// Angular CDK VirtualScroll:
// &lt;cdk-virtual-scroll-viewport itemSize="48"&gt;
//   &lt;div *cdkVirtualFor="let item of items"&gt;{{item.name}}&lt;/div&gt;
// &lt;/cdk-virtual-scroll-viewport&gt;

// Web Worker — offload heavy computation to background thread
// worker.ts
self.addEventListener('message', (e) => {
  const sorted = e.data.sort((a, b) => a.price - b.price); // heavy work
  self.postMessage(sorted);
});
// main.ts
const worker = new Worker(new URL('./worker', import.meta.url));
worker.postMessage(hugeDataSet);
worker.onmessage = ({ data }) => renderTable(data);
// Main thread stays responsive!</pre>

<h2 id="perf-rendering" class="section-break">49. Rendering Performance</h2>
<p class="small"><strong>Checklist:</strong> Critical rendering path · reflow vs repaint · composite layers · will-change · transform/opacity for animations · reducing DOM size · CSS containment</p>

<pre>// Critical rendering path
// 1. HTML → DOM tree
// 2. CSS → CSSOM tree
// 3. DOM + CSSOM → Render tree (skip display:none)
// 4. Layout — calculate positions and sizes
// 5. Paint — fill in pixels
// 6. Compositing — combine layers, render to screen

// Cheap properties (compositor only — no layout/paint):
// transform, opacity, filter, will-change

// Medium properties (paint only — no layout):
// color, background, box-shadow, visibility

// Expensive properties (trigger layout + paint):
// width, height, padding, margin, top, left, font-size, display

// Reduce DOM size
// ✅ Virtual scrolling for long lists
// ✅ Remove hidden elements (not just visibility:hidden)
// ✅ Use CSS for decorative elements (::before, ::after)
// ✅ Flatten deeply nested structures
// Target: under 1500 DOM nodes for good performance</pre>

<h2 id="perf-caching" class="section-break">50. Caching Strategies</h2>
<p class="small"><strong>Checklist:</strong> Browser caching headers · Service Worker caching · Cache-Control · ETag · stale-while-revalidate · application cache · memoization</p>

<pre>// HTTP Cache headers
Cache-Control: public, max-age=31536000, immutable  // static assets with hash
Cache-Control: no-cache                              // always revalidate
Cache-Control: no-store                              // never cache (sensitive data)
Cache-Control: public, max-age=0, must-revalidate    // use ETag

// ETag — content-based validation
// Server sends: ETag: "abc123"
// Browser sends: If-None-Match: "abc123"
// Server returns 304 Not Modified (no body) if unchanged

// stale-while-revalidate — serve stale, update in background
Cache-Control: max-age=3600, stale-while-revalidate=86400
// Serve cached for 1hr, then serve stale for 24hrs while revalidating

// Service Worker caching strategies
// 1. Cache First: check cache → fallback to network (static assets)
// 2. Network First: check network → fallback to cache (API data)
// 3. Stale While Revalidate: serve cache → update from network
// 4. Cache Only: only from cache (offline resources)
// 5. Network Only: never cache (real-time data)

// Application-level memoization
const apiCache = new Map();
async function cachedFetch(url, ttl = 60000) {
  const cached = apiCache.get(url);
  if (cached && Date.now() - cached.timestamp < ttl) return cached.data;
  const data = await fetch(url).then(r => r.json());
  apiCache.set(url, { data, timestamp: Date.now() });
  return data;
}</pre>

<h2 id="perf-web-vitals" class="section-break">51. Core Web Vitals</h2>
<p class="small"><strong>Checklist:</strong> LCP · FID/INP · CLS · FCP · TTI · TBT</p>

<table>
<thead><tr><th>Metric</th><th>What</th><th>Good</th><th>Poor</th><th>How to fix</th></tr></thead>
<tbody>
<tr><td><strong>LCP</strong></td><td>Largest Contentful Paint — when biggest element renders</td><td>&lt; 2.5s</td><td>&gt; 4.0s</td><td>Optimize hero image, preload fonts, SSR</td></tr>
<tr><td><strong>INP</strong></td><td>Interaction to Next Paint — responsiveness to ALL interactions</td><td>&lt; 200ms</td><td>&gt; 500ms</td><td>Break long tasks, yield to main thread, Web Workers</td></tr>
<tr><td><strong>CLS</strong></td><td>Cumulative Layout Shift — visual stability</td><td>&lt; 0.1</td><td>&gt; 0.25</td><td>Set image dimensions, avoid dynamic content insertion</td></tr>
<tr><td><strong>FCP</strong></td><td>First Contentful Paint — first pixel</td><td>&lt; 1.8s</td><td>&gt; 3.0s</td><td>Inline critical CSS, eliminate render-blocking resources</td></tr>
<tr><td><strong>TBT</strong></td><td>Total Blocking Time — sum of long task blocking time</td><td>&lt; 200ms</td><td>&gt; 600ms</td><td>Code split, defer non-critical JS, requestIdleCallback</td></tr>
</tbody>
</table>

<pre>// Measure in your app
import { onLCP, onINP, onCLS } from 'web-vitals';
onLCP(metric => sendToAnalytics('LCP', metric));
onINP(metric => sendToAnalytics('INP', metric));
onCLS(metric => sendToAnalytics('CLS', metric));

// Yield to main thread — prevent long tasks
async function processLargeArray(items) {
  for (let i = 0; i < items.length; i++) {
    processItem(items[i]);
    if (i % 100 === 0) {
      // Yield every 100 items so browser can handle user interactions
      await new Promise(resolve => setTimeout(resolve, 0));
    }
  }
}</pre>

<h2 id="perf-images" class="section-break">52. Images &amp; Media Performance</h2>
<p class="small"><strong>Checklist:</strong> Responsive images (srcset/sizes) · modern formats (WebP/AVIF) · compression · lazy loading · image sprites · SVG optimization · video optimization</p>

<pre>&lt;!-- Responsive images with modern formats --&gt;
&lt;picture&gt;
  &lt;source srcset="hero-400.avif 400w, hero-800.avif 800w, hero-1200.avif 1200w"
          sizes="(max-width:600px) 400px, (max-width:1000px) 800px, 1200px"
          type="image/avif"&gt;
  &lt;source srcset="hero-400.webp 400w, hero-800.webp 800w"
          type="image/webp"&gt;
  &lt;img src="hero-800.jpg" alt="..." loading="lazy" decoding="async"
       width="1200" height="600"
       fetchpriority="high"&gt; &lt;!-- high priority for LCP image --&gt;
&lt;/picture&gt;

&lt;!-- Always set width &amp; height to prevent CLS --&gt;
&lt;img src="photo.jpg" width="400" height="300" alt="..."
     style="width: 100%; height: auto;"&gt;

// SVG optimization checklist:
// 1. Remove metadata, comments (SVGO tool)
// 2. Use viewBox instead of width/height for responsiveness
// 3. Inline small SVGs (saves HTTP request)
// 4. Use &lt;symbol&gt; + &lt;use&gt; for repeated icons (sprite sheet)</pre>

<h2 id="perf-fonts" class="section-break">53. Font Performance</h2>
<p class="small"><strong>Checklist:</strong> Font loading strategies · font-display · FOUT/FOIT/FOFT · subsetting · system font fallbacks</p>

<pre>/* Font loading behavior:
   FOUT (Flash of Unstyled Text): text shows in fallback font, then swaps
   FOIT (Flash of Invisible Text): text is invisible until font loads
   FOFT (Flash of Faux Text): show faux bold/italic, then swap */

@font-face {
  font-family: 'Inter';
  src: url('/fonts/inter-var.woff2') format('woff2');
  font-display: swap;          /* FOUT — best for body text */
  font-weight: 100 900;        /* variable font */
  unicode-range: U+0000-00FF;  /* only Latin characters = smaller file */
}

/* font-display values:
   swap:     show fallback immediately, swap when loaded (recommended)
   optional: browser may skip loading if connection is slow
   fallback: tiny invisible period (100ms), then fallback
   block:    invisible for up to 3s, then fallback */

/* Preload your critical font */
&lt;link rel="preload" href="/fonts/inter-var.woff2" as="font"
      type="font/woff2" crossorigin&gt;

/* System font stack — zero download time */
body {
  font-family: system-ui, -apple-system, BlinkMacSystemFont,
               'Segoe UI', Roboto, sans-serif;
}</pre>

<h2 id="perf-measuring" class="section-break">54. Measuring Performance</h2>
<p class="small"><strong>Checklist:</strong> Performance API · Navigation Timing · Resource Timing · User Timing marks/measures · Lighthouse · WebPageTest · Chrome DevTools Performance panel</p>

<pre>// Performance API — custom timing
performance.mark('component-render-start');
renderComponent();
performance.mark('component-render-end');
performance.measure('Component Render', 'component-render-start', 'component-render-end');

const entry = performance.getEntriesByName('Component Render')[0];
console.log(`Render took: ${entry.duration.toFixed(2)}ms`);

// Navigation Timing — page load breakdown
const nav = performance.getEntriesByType('navigation')[0];
console.log({
  dns: nav.domainLookupEnd - nav.domainLookupStart,
  tcp: nav.connectEnd - nav.connectStart,
  ttfb: nav.responseStart - nav.requestStart,
  download: nav.responseEnd - nav.responseStart,
  domParsing: nav.domInteractive - nav.responseEnd,
  domComplete: nav.domComplete - nav.domInteractive,
  total: nav.loadEventEnd - nav.startTime
});

// Resource Timing — individual resource metrics
const resources = performance.getEntriesByType('resource');
resources.forEach(r => {
  if (r.duration > 500) {
    console.warn(`Slow resource: ${r.name} took ${r.duration}ms`);
  }
});

// PerformanceObserver — watch for long tasks
const observer = new PerformanceObserver((list) => {
  list.getEntries().forEach(entry => {
    console.warn(`Long task detected: ${entry.duration}ms`);
    sendToMonitoring({ type: 'long-task', duration: entry.duration });
  });
});
observer.observe({ type: 'longtask', buffered: true });</pre>

<div class="interview-q">
<h4>🎯 Interview Questions — Performance</h4>
<p><strong>Q: A page has an LCP of 5 seconds. How do you diagnose and fix it?</strong></p>
<p><strong>A:</strong> (1) Identify the LCP element (DevTools → Performance → LCP marker). (2) If it's an image: preload it, use modern formats (AVIF/WebP), set <code>fetchpriority="high"</code>, ensure no lazy-loading on LCP image. (3) If it's text: inline critical CSS, preload fonts, use <code>font-display: swap</code>. (4) Check server TTFB — implement SSR, CDN, caching. (5) Remove render-blocking resources.</p>

<p><strong>Q: How do you prevent layout shifts (CLS)?</strong></p>
<p><strong>A:</strong> (1) Always set <code>width</code> and <code>height</code> on images/videos. (2) Use <code>aspect-ratio</code> CSS for dynamic containers. (3) Reserve space for ads/embeds. (4) Avoid inserting content above existing content. (5) Use CSS <code>contain</code> for dynamic widgets. (6) Use <code>font-display: optional</code> to prevent font-swap shifts.</p>
</div>
"""
