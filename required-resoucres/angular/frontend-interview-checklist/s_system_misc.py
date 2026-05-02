SECTIONS = r"""

<!-- ═══════════════════════════════════════════════════════════════════
     SYSTEM DESIGN — 5 SUB-SECTIONS
     ═══════════════════════════════════════════════════════════════════ -->

<h2 id="sd-component" class="section-break">87. Component Design</h2>
<p class="small"><strong>Checklist:</strong> Reusable components · props/inputs design · composition vs inheritance · compound components · render props / content projection · single responsibility</p>

<pre>// Designing a reusable DataTable component
@Component({
  selector: 'app-data-table',
  template: `
    &lt;table&gt;
      &lt;thead&gt;
        &lt;tr&gt;
          &lt;th *ngFor="let col of columns"
              (click)="sortBy(col.key)"
              [class.sorted]="sortColumn === col.key"&gt;
            {{ col.label }}
            &lt;span *ngIf="sortColumn === col.key"&gt;
              {{ sortDirection === 'asc' ? '▲' : '▼' }}
            &lt;/span&gt;
          &lt;/th&gt;
        &lt;/tr&gt;
      &lt;/thead&gt;
      &lt;tbody&gt;
        &lt;tr *ngFor="let row of paginatedData; trackBy: trackByFn"&gt;
          &lt;td *ngFor="let col of columns"&gt;
            &lt;ng-container *ngIf="col.template; else defaultCell"&gt;
              &lt;ng-container *ngTemplateOutlet="col.template; context: { $implicit: row }"&gt;
              &lt;/ng-container&gt;
            &lt;/ng-container&gt;
            &lt;ng-template #defaultCell&gt;{{ row[col.key] }}&lt;/ng-template&gt;
          &lt;/td&gt;
        &lt;/tr&gt;
      &lt;/tbody&gt;
    &lt;/table&gt;
    &lt;app-pagination [total]="data.length" [pageSize]="pageSize"
                    (pageChange)="currentPage = $event"&gt;
    &lt;/app-pagination&gt;
  `
})
export class DataTableComponent {
  @Input() columns: Column[] = [];
  @Input() data: any[] = [];
  @Input() pageSize = 10;
  @Input() trackByFn = (i: number, item: any) => item.id;

  sortColumn = '';
  sortDirection: 'asc' | 'desc' = 'asc';
  currentPage = 1;

  get paginatedData() {
    const sorted = this.sortedData;
    const start = (this.currentPage - 1) * this.pageSize;
    return sorted.slice(start, start + this.pageSize);
  }
}

// Design principles for reusable components:
// 1. Single Responsibility — one component, one concern
// 2. Open/Closed — extensible (ng-template, content projection) without modifying source
// 3. Configurability — reasonable defaults, override-able via inputs
// 4. Type safety — strong typing for inputs/outputs
// 5. Accessibility — ARIA attributes, keyboard support built-in</pre>

<h2 id="sd-architecture" class="section-break">88. Application Architecture</h2>
<p class="small"><strong>Checklist:</strong> Folder structure · feature modules · core/shared modules · lazy loading · state management placement · service layer · API layer</p>

<pre>// Scalable Angular project structure
src/
  app/
    core/                    // singleton services, global guards, interceptors
      auth/
        auth.service.ts
        auth.guard.ts
        auth.interceptor.ts
      http/
        api.service.ts       // base API service
        error.interceptor.ts
      core.module.ts         // imported ONCE in AppModule

    shared/                  // reusable components, pipes, directives
      components/
        data-table/
        modal/
        pagination/
        loading-spinner/
      pipes/
        date-format.pipe.ts
        currency.pipe.ts
      directives/
        click-outside.directive.ts
        tooltip.directive.ts
      shared.module.ts       // imported by feature modules

    features/                // lazy-loaded feature modules
      dashboard/
        components/
          dashboard-chart.component.ts
          dashboard-stats.component.ts
        pages/
          dashboard.component.ts
        services/
          dashboard.service.ts
        dashboard-routing.module.ts
        dashboard.module.ts

      orders/
        components/
        pages/
        models/
          order.model.ts
        services/
          order.service.ts
          order.resolver.ts
        store/               // feature-level state (if using NgRx)
          order.actions.ts
          order.reducer.ts
          order.effects.ts
          order.selectors.ts
        orders-routing.module.ts
        orders.module.ts

    app-routing.module.ts    // lazy-load routes
    app.module.ts
    app.component.ts

// Lazy loading routes
const routes: Routes = [
  { path: '', redirectTo: 'dashboard', pathMatch: 'full' },
  { path: 'dashboard', loadChildren: () =>
    import('./features/dashboard/dashboard.module').then(m => m.DashboardModule) },
  { path: 'orders', loadChildren: () =>
    import('./features/orders/orders.module').then(m => m.OrdersModule) }
];</pre>

<h2 id="sd-components" class="section-break">89. Common Components to Design</h2>
<p class="small"><strong>Checklist:</strong> Autocomplete · infinite scroll list · modal system · toast notifications · form builder · file uploader · drag &amp; drop</p>

<pre>// AUTOCOMPLETE — typeahead search
class AutocompleteController {
  private searchSubject = new Subject&lt;string&gt;();
  results$: Observable&lt;SearchResult[]&gt;;

  constructor(private api: SearchService) {
    this.results$ = this.searchSubject.pipe(
      debounceTime(300),        // wait 300ms after typing stops
      distinctUntilChanged(),   // skip if same query
      filter(q => q.length >= 2), // min 2 chars
      switchMap(query =>        // cancel previous request
        this.api.search(query).pipe(
          catchError(() => of([])) // graceful error handling
        )
      )
    );
  }

  onInput(query: string) { this.searchSubject.next(query); }
}

// INFINITE SCROLL — with IntersectionObserver
class InfiniteScrollList {
  private page = 1;
  private loading = false;
  private hasMore = true;

  constructor(private sentinel: HTMLElement) {
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting &amp;&amp; !this.loading &amp;&amp; this.hasMore) {
          this.loadMore();
        }
      },
      { rootMargin: '200px' }  // trigger 200px before sentinel is visible
    );
    observer.observe(this.sentinel);
  }

  async loadMore() {
    this.loading = true;
    const items = await api.getItems({ page: this.page, limit: 20 });
    this.renderItems(items);
    this.hasMore = items.length === 20;
    this.page++;
    this.loading = false;
  }
}

// TOAST NOTIFICATION SYSTEM
interface Toast {
  id: string;
  type: 'success' | 'error' | 'warning' | 'info';
  message: string;
  duration?: number;
}

@Injectable({ providedIn: 'root' })
class ToastService {
  private toasts = new BehaviorSubject&lt;Toast[]&gt;([]);
  toasts$ = this.toasts.asObservable();

  show(type: Toast['type'], message: string, duration = 5000) {
    const toast: Toast = { id: crypto.randomUUID(), type, message, duration };
    this.toasts.next([...this.toasts.value, toast]);
    if (duration > 0) {
      setTimeout(() => this.dismiss(toast.id), duration);
    }
  }

  dismiss(id: string) {
    this.toasts.next(this.toasts.value.filter(t => t.id !== id));
  }
}</pre>

<h2 id="sd-full-apps" class="section-break">90. Full Application Designs</h2>
<p class="small"><strong>Checklist:</strong> E-commerce · chat application · social media feed · dashboard with real-time data · collaborative editor</p>

<pre>// E-COMMERCE ARCHITECTURE

// High-level architecture:
// CDN → Load Balancer → Web Servers → API Gateway → Microservices
//                                                    ├── Auth Service
//                                                    ├── Product Service (catalog + search)
//                                                    ├── Cart Service (Redis for speed)
//                                                    ├── Order Service (with saga pattern)
//                                                    ├── Payment Service (Stripe/Razorpay)
//                                                    ├── Notification Service (email/SMS/push)
//                                                    └── Inventory Service

// Frontend considerations:
// 1. Product listing: virtual scrolling, lazy image loading, skeleton screens
// 2. Search: debounced input, faceted filters, URL state for shareability
// 3. Cart: persist in localStorage + sync with server, optimistic updates
// 4. Checkout: multi-step form with validation, address autocomplete
// 5. Payment: PCI compliance (never handle raw card data, use Stripe Elements)
// 6. Real-time: stock alerts via WebSocket, price updates

// CHAT APPLICATION ARCHITECTURE
// WebSocket connection for real-time messaging
// Message states: sending → sent → delivered → read
// Offline support: queue messages in IndexedDB, sync on reconnect
// Typing indicators: debounced WebSocket events
// Message pagination: cursor-based (load more on scroll up)

// Features to design:
// - Message types: text, image, file, reply, forward
// - Group chat: member management, admin controls
// - Read receipts: track per-user read position
// - Search: full-text search across conversations
// - Push notifications: Service Worker + Push API
// - Encryption: end-to-end (Signal protocol)</pre>

<h2 id="sd-scalability" class="section-break">91. Scalability Topics</h2>
<p class="small"><strong>Checklist:</strong> CDN · load balancing · caching layers · database sharding · message queues · micro-frontends · SSR/SSG</p>

<pre>// Frontend scalability strategies

// 1. CDN — serve static assets from edge locations
// Put HTML, CSS, JS, images on CDN (CloudFront, Cloudflare)
// Cache-Control: public, max-age=31536000, immutable (for hashed files)
// Cache-Control: no-cache (for index.html — always revalidate)

// 2. Code splitting — load only what's needed
const routes = [
  { path: 'admin', loadChildren: () => import('./admin/admin.module') },
  // Admin module (50KB) only loaded for admin users
];

// 3. SSR (Server-Side Rendering) with Angular Universal
// Benefits: faster FCP, better SEO, works without JS
// Use for: marketing pages, product pages, blog posts
// Trade-offs: server cost, TTFB latency, hydration complexity

// 4. SSG (Static Site Generation) for content pages
// Pre-render at build time → deploy as static files
// Best for: docs, blogs, landing pages, product catalogs

// 5. Service Worker caching
// Cache critical resources for offline use
// Strategies: cache-first (assets), network-first (API), stale-while-revalidate

// 6. Micro-frontends — independently deployable frontend modules
// Module Federation (Webpack 5)
// Each team owns a feature, builds/deploys independently
// Shell app loads feature modules at runtime
new ModuleFederationPlugin({
  name: 'shell',
  remotes: {
    products: 'products@https://products.example.com/remoteEntry.js',
    checkout: 'checkout@https://checkout.example.com/remoteEntry.js'
  }
});

// 7. Performance budgets
// Set limits: main bundle &lt; 200KB, page load &lt; 3s
// Enforce in CI: fail build if budget exceeded
// angular.json budgets:
"budgets": [
  { "type": "initial", "maximumWarning": "500kb", "maximumError": "1mb" },
  { "type": "anyComponentStyle", "maximumWarning": "4kb" }
]</pre>

<!-- ═══════════════════════════════════════════════════════════════════
     VERSION CONTROL — 3 SUB-SECTIONS
     ═══════════════════════════════════════════════════════════════════ -->

<h2 id="git-basics" class="section-break">92. Git Basics</h2>
<p class="small"><strong>Checklist:</strong> add / commit / push / pull · branching · merging · stashing · .gitignore · commit messages</p>

<pre>// Essential Git commands
git init                           // initialize repo
git clone &lt;url&gt;                    // clone remote repo
git add .                          // stage all changes
git commit -m "feat: add login"    // commit with message
git push origin main               // push to remote
git pull origin main               // fetch + merge

// Branching
git branch feature/login           // create branch
git checkout feature/login         // switch to branch
git checkout -b feature/login      // create + switch (shortcut)
git branch -d feature/login        // delete merged branch
git branch -D feature/login        // force delete unmerged branch

// Merging
git merge feature/login            // merge branch into current
git merge --no-ff feature/login    // create merge commit even if fast-forward

// Stashing
git stash                          // save uncommitted changes
git stash list                     // list stashes
git stash pop                      // apply + delete latest stash
git stash apply stash@{1}          // apply specific stash (keep it)

// Conventional commit messages
// type(scope): description
// feat:     new feature
// fix:      bug fix
// docs:     documentation
// style:    formatting (no code change)
// refactor: restructuring (no feature/fix)
// perf:     performance improvement
// test:     adding/fixing tests
// chore:    tooling, dependencies, CI

git commit -m "feat(auth): add OAuth 2.0 login"
git commit -m "fix(cart): prevent duplicate items"
git commit -m "perf(images): lazy-load below-fold images"</pre>

<h2 id="git-workflows" class="section-break">93. Git Workflows</h2>
<p class="small"><strong>Checklist:</strong> Git Flow · GitHub Flow · trunk-based development · feature branches · release branches</p>

<pre>// GITHUB FLOW (simple, recommended for most teams)
// 1. Create feature branch from main
// 2. Make commits
// 3. Open Pull Request
// 4. Code review + CI checks
// 5. Merge to main
// 6. Deploy from main

// GIT FLOW (for versioned releases)
// main — production code, tagged releases
// develop — integration branch
// feature/* — new features (branch from develop)
// release/* — release prep (branch from develop)
// hotfix/* — urgent fixes (branch from main)

// TRUNK-BASED DEVELOPMENT (for CI/CD teams)
// Everyone commits to main (or short-lived branches < 1 day)
// Feature flags control incomplete features in production
// Key: small, frequent commits, excellent CI pipeline

// Pull Request best practices:
// - Small PRs (< 400 lines changed)
// - Clear title following conventional commits
// - Description with context, screenshots, testing steps
// - Link to issue/ticket
// - Self-review before requesting review
// - Address all comments before merging</pre>

<h2 id="git-advanced" class="section-break">94. Advanced Git</h2>
<p class="small"><strong>Checklist:</strong> Rebase vs merge · interactive rebase · cherry-pick · bisect · reflog · hooks</p>

<pre>// Rebase — rewrite history for clean linear history
git checkout feature/login
git rebase main                    // replay feature commits on top of main
// ⚠️ Never rebase public/shared branches!

// Interactive rebase — clean up commits before PR
git rebase -i HEAD~3               // edit last 3 commits
// pick   abc1234 feat: add login form
// squash def5678 fix: typo in login   → combine into previous
// reword ghi9012 add validation       → rename commit

// Cherry-pick — apply specific commit to another branch
git cherry-pick abc1234            // apply commit abc1234 to current branch

// Bisect — find which commit introduced a bug
git bisect start
git bisect bad                     // current commit is bad
git bisect good v1.0.0             // last known good commit
// Git checks out middle commit, you test, mark good/bad
// Repeats binary search until the bad commit is found

// Reflog — recover "lost" commits
git reflog                         // shows ALL recent HEAD movements
git checkout abc1234               // go back to a "lost" commit
git branch recovered abc1234       // create branch from lost commit

// Git hooks (with Husky)
// pre-commit: lint, format, run tests
// commit-msg: validate commit message format
// pre-push: run full test suite</pre>

<!-- ═══════════════════════════════════════════════════════════════════
     WEB FUNDAMENTALS — 4 SUB-SECTIONS
     ═══════════════════════════════════════════════════════════════════ -->

<h2 id="web-rendering" class="section-break">95. Browser Rendering Pipeline</h2>
<p class="small"><strong>Checklist:</strong> DOM construction · CSSOM · render tree · layout · paint · compositing · critical rendering path</p>

<pre>// Browser rendering pipeline:
// 1. Parse HTML → DOM tree
// 2. Parse CSS → CSSOM tree
// 3. Combine DOM + CSSOM → Render tree (visible elements only)
// 4. Layout (Reflow) — calculate position and size of each element
// 5. Paint — fill pixels (colors, borders, shadows, text)
// 6. Composite — combine painted layers, handle transforms, opacity

// What triggers each stage:
// Layout (most expensive):
//   width, height, padding, margin, top/left, font-size, display, position
// Paint:
//   color, background, border-radius, box-shadow, visibility
// Composite only (cheapest — GPU accelerated):
//   transform, opacity, will-change, filter

// Optimization strategies:
// 1. Minimize DOM depth and size (&lt;1500 nodes ideal)
// 2. Use CSS containment: contain: layout style paint;
// 3. Batch DOM reads/writes (avoid layout thrashing)
// 4. Use transform instead of top/left for animations
// 5. Use content-visibility: auto for off-screen content
// 6. Use requestAnimationFrame for visual updates

// Layout thrashing example:
// ❌ BAD — reads and writes interleaved
for (const el of elements) {
  const width = el.offsetWidth;     // FORCE LAYOUT (read)
  el.style.width = width * 2 + 'px'; // write
  // next iteration forces layout again!
}

// ✅ GOOD — batch reads, then batch writes
const widths = elements.map(el => el.offsetWidth);  // all reads
elements.forEach((el, i) => {
  el.style.width = widths[i] * 2 + 'px';            // all writes
});</pre>

<h2 id="web-browsers" class="section-break">96. How Browsers Work</h2>
<p class="small"><strong>Checklist:</strong> URL to pixels · DNS resolution · TCP/TLS · HTTP request · parsing · rendering · JavaScript execution</p>

<pre>// What happens when you type a URL and press Enter:

// 1. URL PARSING
//    Browser parses URL: protocol + domain + path + query + fragment

// 2. DNS RESOLUTION
//    Browser cache → OS cache → Router cache → ISP DNS → Root DNS
//    → TLD server (.com) → Authoritative DNS → IP address

// 3. TCP CONNECTION
//    Three-way handshake: SYN → SYN-ACK → ACK
//    If HTTPS: TLS handshake (certificate exchange, key agreement)

// 4. HTTP REQUEST
//    GET /index.html HTTP/2
//    Host: example.com
//    Accept: text/html
//    Cookie: session=abc123

// 5. SERVER RESPONSE
//    HTTP/2 200 OK
//    Content-Type: text/html
//    Set-Cookie: session=abc123

// 6. HTML PARSING
//    Parser builds DOM tree token by token
//    When it hits &lt;link rel="stylesheet"&gt; → parallel CSS download + CSSOM build
//    When it hits &lt;script&gt; → BLOCKS parsing (unless async/defer)

// 7. SCRIPT LOADING
//    &lt;script&gt;              → blocks parsing, download + execute immediately
//    &lt;script async&gt;        → download in parallel, execute ASAP (blocks parsing)
//    &lt;script defer&gt;        → download in parallel, execute AFTER HTML parsing
//    &lt;script type="module"&gt; → deferred by default

// 8. RENDERING
//    DOM + CSSOM → Render Tree → Layout → Paint → Composite → Pixels on screen

// 9. HYDRATION (for SSR apps)
//    Attach event listeners to server-rendered HTML
//    Make the page interactive</pre>

<h2 id="web-progressive" class="section-break">97. Progressive Enhancement</h2>
<p class="small"><strong>Checklist:</strong> Core functionality without JS · feature detection · graceful degradation · polyfills</p>

<pre>// Progressive enhancement: build from baseline up
// 1. HTML — semantic, works without CSS/JS
// 2. CSS — enhanced layout and visuals
// 3. JavaScript — enhanced interactivity

// Feature detection (prefer over browser sniffing)
if ('IntersectionObserver' in window) {
  // use IntersectionObserver for lazy loading
} else {
  // fallback: load all images immediately
}

if ('serviceWorker' in navigator) {
  navigator.serviceWorker.register('/sw.js');
}

if (CSS.supports('display', 'grid')) {
  // use CSS Grid layout
}

// @supports in CSS
@supports (display: grid) {
  .container { display: grid; }
}
@supports not (display: grid) {
  .container { display: flex; flex-wrap: wrap; }
}

// Modern progressive enhancement
// - &lt;noscript&gt; message for JS-disabled users
// - Server-side rendering as baseline
// - Client-side hydration for interactivity
// - Feature flags for browser capabilities</pre>

<h2 id="web-standards" class="section-break">98. Web Standards</h2>
<p class="small"><strong>Checklist:</strong> W3C · WHATWG · TC39 · ECMAScript proposal stages · Web APIs · browser compatibility</p>

<pre>// TC39 ECMAScript Proposal Stages
// Stage 0: Strawperson — idea proposed
// Stage 1: Proposal — problem described, solution outlined
// Stage 2: Draft — formal spec language, experimental implementations
// Stage 3: Candidate — complete spec, needs real-world feedback
// Stage 4: Finished — ready for inclusion in ECMAScript standard

// Recent notable proposals:
// ✅ Stage 4: Array.prototype.findLast(), Object.groupBy()
// ✅ Stage 4: Promise.withResolvers()
// 🔄 Stage 3: Temporal (date/time replacement for Date)
// 🔄 Stage 3: Decorators
// 🔄 Stage 2: Pattern Matching

// Checking browser support:
// - caniuse.com — browser support tables
// - MDN — compatibility tables per API
// - @babel/preset-env — auto-polyfill based on browserslist target
// - core-js — polyfill library for ES features</pre>

<!-- ═══════════════════════════════════════════════════════════════════
     MOBILE & PWA + CSS ARCHITECTURE + MODERN JS + REMAINING
     ═══════════════════════════════════════════════════════════════════ -->

<h2 id="mobile-responsive" class="section-break">99. Mobile &amp; Progressive Web Apps</h2>
<p class="small"><strong>Checklist:</strong> Responsive techniques · mobile-specific concerns · touch events · viewport · PWA: manifest · service worker · push notifications · offline support · install prompt</p>

<pre>// PWA — Progressive Web App essentials

// 1. Web App Manifest
// manifest.json
{
  "name": "My Interview App",
  "short_name": "Interview",
  "start_url": "/",
  "display": "standalone",      // fullscreen, standalone, minimal-ui, browser
  "theme_color": "#1a5c2e",
  "background_color": "#ffffff",
  "icons": [
    { "src": "/icon-192.png", "sizes": "192x192", "type": "image/png" },
    { "src": "/icon-512.png", "sizes": "512x512", "type": "image/png" }
  ]
}

// 2. Service Worker — offline support
// sw.js
const CACHE_NAME = 'v1';
const ASSETS = ['/', '/index.html', '/styles.css', '/app.js'];

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => cache.addAll(ASSETS))
  );
});

self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request).then(cached => {
      return cached || fetch(event.request).then(response => {
        const clone = response.clone();
        caches.open(CACHE_NAME).then(cache => cache.put(event.request, clone));
        return response;
      });
    })
  );
});

// 3. Install prompt
let deferredPrompt;
window.addEventListener('beforeinstallprompt', (e) => {
  e.preventDefault();
  deferredPrompt = e;
  showInstallButton();
});
installBtn.addEventListener('click', () => {
  deferredPrompt.prompt();
});

// Mobile touch events
element.addEventListener('touchstart', handler, { passive: true }); // passive improves scroll perf
// Touch gestures: touchstart → touchmove → touchend
// Pointer events (modern): pointerdown → pointermove → pointerup (unified mouse+touch+pen)

// Viewport meta tag (required for mobile)
&lt;meta name="viewport" content="width=device-width, initial-scale=1"&gt;</pre>

<h2 id="css-architecture" class="section-break">100. CSS Architecture</h2>
<p class="small"><strong>Checklist:</strong> Specificity management · cascade &amp; inheritance · CSS organization · naming conventions · utility-first · component-scoped</p>

<pre>// Specificity scoring: (inline, ID, class, element)
// *              → 0,0,0,0
// div            → 0,0,0,1
// .class         → 0,0,1,0
// #id            → 0,1,0,0
// style=""       → 1,0,0,0
// !important     → overrides everything (avoid!)

// div.active     → 0,0,1,1  (element + class)
// #nav .item a   → 0,1,1,1  (id + class + element)
// :is(.a, #b)    → uses HIGHEST specificity of arguments (0,1,0,0)
// :where(.a, #b) → ALWAYS 0 specificity (great for defaults)

// Cascade layers (CSS @layer) — control specificity at scale
@layer reset, base, components, utilities;

@layer reset {
  * { margin: 0; padding: 0; box-sizing: border-box; }
}
@layer base {
  body { font-family: system-ui; line-height: 1.6; }
}
@layer components {
  .card { padding: 1rem; border: 1px solid #ddd; }
}
@layer utilities {
  .mt-4 { margin-top: 1rem; }  // always wins over components
}

// Angular ViewEncapsulation
// Emulated (default): scopes CSS to component via attribute selectors
// None: styles are global
// ShadowDom: uses native Shadow DOM (true isolation)

// CSS organization for large projects
styles/
  _variables.scss      // design tokens
  _mixins.scss         // reusable patterns
  _reset.scss          // normalize/reset
  _typography.scss     // base type styles
  _utilities.scss      // utility classes
  components/          // component-specific styles
  pages/               // page-specific styles
  main.scss            // imports everything</pre>

<h2 id="modern-js" class="section-break">101. Modern JavaScript Features</h2>
<p class="small"><strong>Checklist:</strong> ES modules · dynamic import · top-level await · decorators · structuredClone · AbortController · Temporal (upcoming)</p>

<pre>// Dynamic imports — code splitting at runtime
const module = await import('./heavy-chart-lib.js');
const chart = new module.ChartRenderer(data);

// Top-level await (ES2022)
const config = await fetch('/config.json').then(r => r.json());
export { config };

// structuredClone — deep clone (ES2022)
const original = { a: 1, b: { c: 2 }, d: new Date() };
const clone = structuredClone(original);
// ✅ Handles: nested objects, arrays, dates, maps, sets, RegExp, ArrayBuffer
// ❌ Cannot clone: functions, DOM nodes, Error objects, symbols

// Iterator helpers (Stage 3/4)
const iter = [1, 2, 3, 4, 5].values();
const result = iter.filter(x => x % 2).map(x => x * 10).toArray();
// [10, 30, 50] — lazy evaluation, no intermediate arrays

// Set methods (ES2025)
const setA = new Set([1, 2, 3, 4]);
const setB = new Set([3, 4, 5, 6]);
setA.intersection(setB);  // Set {3, 4}
setA.union(setB);          // Set {1, 2, 3, 4, 5, 6}
setA.difference(setB);     // Set {1, 2}
setA.symmetricDifference(setB); // Set {1, 2, 5, 6}

// Promise.withResolvers() (ES2024)
const { promise, resolve, reject } = Promise.withResolvers();
// Useful when you need to resolve/reject from outside the constructor

// Object.groupBy() (ES2024)
const people = [
  { name: 'Alice', department: 'eng' },
  { name: 'Bob', department: 'sales' },
  { name: 'Carol', department: 'eng' }
];
const byDept = Object.groupBy(people, p => p.department);
// { eng: [Alice, Carol], sales: [Bob] }</pre>

<h2 id="framework-comparisons" class="section-break">102. Framework Comparisons</h2>
<p class="small"><strong>Checklist:</strong> Angular vs React vs Vue · change detection strategies · state management · when to use what</p>

<table>
<thead><tr><th>Feature</th><th>Angular</th><th>React</th><th>Vue</th></tr></thead>
<tbody>
<tr><td>Type</td><td>Full framework</td><td>UI library</td><td>Progressive framework</td></tr>
<tr><td>Language</td><td>TypeScript</td><td>JavaScript/TypeScript</td><td>JavaScript/TypeScript</td></tr>
<tr><td>Change Detection</td><td>Zone.js / Signals</td><td>Virtual DOM diffing</td><td>Reactive proxies</td></tr>
<tr><td>State Mgmt</td><td>NgRx / Signals / Services</td><td>Redux / Zustand / Context</td><td>Pinia / Vuex</td></tr>
<tr><td>Routing</td><td>Built-in (@angular/router)</td><td>React Router (3rd party)</td><td>Vue Router (official)</td></tr>
<tr><td>Forms</td><td>Built-in (template/reactive)</td><td>Controlled/uncontrolled (+ libs)</td><td>v-model (built-in)</td></tr>
<tr><td>Learning Curve</td><td>Steep</td><td>Moderate</td><td>Gentle</td></tr>
<tr><td>Best For</td><td>Enterprise, large teams</td><td>Flexible, ecosystem</td><td>Quick setup, simplicity</td></tr>
<tr><td>Bundle Size</td><td>~50KB gzipped (core)</td><td>~40KB gzipped</td><td>~30KB gzipped</td></tr>
</tbody>
</table>

<pre>// Change detection comparison:
// Angular: Zone.js patches async APIs, triggers change detection on ANY async event
//   → Angular 16+ Signals: fine-grained reactivity, no Zone.js overhead
// React: setState/useState triggers re-render, Virtual DOM diffing
//   → React 18 concurrent features: transitions, suspense
// Vue: Reactive proxies track dependencies, only re-render what changed
//   → Most precise reactivity out of the box

// When to choose:
// Angular: large enterprise teams, need full batteries-included framework,
//          strict patterns, long-term maintainability
// React: flexible team, want ecosystem choice, need React Native for mobile
// Vue: smaller team, quick prototyping, gradual adoption</pre>

<h2 id="soft-skills" class="section-break">103. Soft Skills &amp; Interview Process</h2>
<p class="small"><strong>Checklist:</strong> Code review skills · communication · problem-solving approach · project discussion</p>

<pre>// Problem-solving framework for interview coding questions:
// 1. UNDERSTAND — repeat the problem, clarify inputs/outputs/edge cases
// 2. PLAN — discuss approach BEFORE coding, talk about trade-offs
// 3. CODE — write clean code, explain as you go
// 4. TEST — walk through with examples, check edge cases
// 5. OPTIMIZE — discuss time/space complexity, can we do better?

// Talking about past projects (STAR method):
// Situation: Context and challenge
// Task: Your specific responsibility
// Action: What YOU did (technical decisions, leadership)
// Result: Measurable outcome (performance improvement, team velocity)

// Code review checklist:
// ✅ Does it solve the stated problem?
// ✅ Are edge cases handled?
// ✅ Is the code readable and maintainable?
// ✅ Are there performance concerns?
// ✅ Is it secure? (XSS, injection, auth)
// ✅ Are there tests? Do they cover important cases?
// ✅ Is it consistent with existing codebase patterns?
// ✅ Are error messages helpful for debugging?

// Communication tips:
// - Think out loud — interviewers want to see your thought process
// - Ask clarifying questions before diving in
// - Discuss trade-offs (time vs space, simplicity vs performance)
// - Don't panic if stuck — explain what you're thinking
// - If you don't know something, say so and discuss how you'd find out</pre>

<!-- ═══════════════════════════════════════════════════════════════════
     REAL-WORLD IMPLEMENTATION PATTERNS — 8 implementations
     ═══════════════════════════════════════════════════════════════════ -->

<h2 id="impl-patterns" class="section-break">104. Real-World Implementation Patterns</h2>
<p class="small"><strong>Checklist:</strong> Debounce · Throttle · Deep Clone · Event Emitter · Flatten Array · Promise implementation · Curry · Memoize</p>

<h3>104.1 Debounce</h3>
<pre>function debounce(fn, delay) {
  let timer;
  return function(...args) {
    clearTimeout(timer);
    timer = setTimeout(() => fn.apply(this, args), delay);
  };
}
// With leading edge and cancel
function debounceAdvanced(fn, delay, { leading = false } = {}) {
  let timer;
  let isLeading = true;
  function debounced(...args) {
    if (leading &amp;&amp; isLeading) {
      fn.apply(this, args);
      isLeading = false;
    }
    clearTimeout(timer);
    timer = setTimeout(() => {
      if (!leading) fn.apply(this, args);
      isLeading = true;
    }, delay);
  }
  debounced.cancel = () => { clearTimeout(timer); isLeading = true; };
  return debounced;
}</pre>

<h3>104.2 Throttle</h3>
<pre>function throttle(fn, limit) {
  let inThrottle = false;
  return function(...args) {
    if (!inThrottle) {
      fn.apply(this, args);
      inThrottle = true;
      setTimeout(() => (inThrottle = false), limit);
    }
  };
}
// Throttle with trailing call
function throttleTrailing(fn, limit) {
  let lastArgs, timer, lastTime = 0;
  return function(...args) {
    const now = Date.now();
    const remaining = limit - (now - lastTime);
    if (remaining &lt;= 0) {
      fn.apply(this, args);
      lastTime = now;
    } else {
      lastArgs = args;
      clearTimeout(timer);
      timer = setTimeout(() => {
        fn.apply(this, lastArgs);
        lastTime = Date.now();
      }, remaining);
    }
  };
}</pre>

<h3>104.3 Deep Clone</h3>
<pre>function deepClone(obj, seen = new WeakMap()) {
  if (obj === null || typeof obj !== 'object') return obj;
  if (obj instanceof Date) return new Date(obj);
  if (obj instanceof RegExp) return new RegExp(obj.source, obj.flags);
  if (obj instanceof Map) {
    const map = new Map();
    seen.set(obj, map);
    obj.forEach((v, k) => map.set(deepClone(k, seen), deepClone(v, seen)));
    return map;
  }
  if (obj instanceof Set) {
    const set = new Set();
    seen.set(obj, set);
    obj.forEach(v => set.add(deepClone(v, seen)));
    return set;
  }
  if (seen.has(obj)) return seen.get(obj);  // handle circular references

  const clone = Array.isArray(obj) ? [] : Object.create(Object.getPrototypeOf(obj));
  seen.set(obj, clone);
  for (const key of Reflect.ownKeys(obj)) {
    clone[key] = deepClone(obj[key], seen);
  }
  return clone;
}
// In production, use: structuredClone(obj) or lodash.cloneDeep(obj)</pre>

<h3>104.4 Event Emitter</h3>
<pre>class EventEmitter {
  #listeners = new Map();

  on(event, callback) {
    if (!this.#listeners.has(event)) this.#listeners.set(event, new Set());
    this.#listeners.get(event).add(callback);
    return () => this.off(event, callback);  // return unsubscribe
  }

  once(event, callback) {
    const wrapper = (...args) => {
      callback(...args);
      this.off(event, wrapper);
    };
    return this.on(event, wrapper);
  }

  off(event, callback) {
    this.#listeners.get(event)?.delete(callback);
  }

  emit(event, ...args) {
    this.#listeners.get(event)?.forEach(cb => cb(...args));
  }
}</pre>

<h3>104.5 Flatten Array</h3>
<pre>// Recursive
function flatten(arr, depth = Infinity) {
  return depth > 0
    ? arr.reduce((acc, val) =>
        acc.concat(Array.isArray(val) ? flatten(val, depth - 1) : val), [])
    : arr.slice();
}

// Iterative (no recursion)
function flattenIterative(arr) {
  const stack = [...arr];
  const result = [];
  while (stack.length) {
    const item = stack.pop();
    Array.isArray(item) ? stack.push(...item) : result.push(item);
  }
  return result.reverse();
}

// Built-in: arr.flat(Infinity)</pre>

<h3>104.6 Promise Implementation</h3>
<pre>class MyPromise {
  #state = 'pending'; // pending | fulfilled | rejected
  #value;
  #handlers = [];

  constructor(executor) {
    const resolve = (value) => {
      if (this.#state !== 'pending') return;
      this.#state = 'fulfilled';
      this.#value = value;
      this.#handlers.forEach(h => h.onFulfilled(value));
    };
    const reject = (reason) => {
      if (this.#state !== 'pending') return;
      this.#state = 'rejected';
      this.#value = reason;
      this.#handlers.forEach(h => h.onRejected(reason));
    };
    try { executor(resolve, reject); }
    catch (e) { reject(e); }
  }

  then(onFulfilled, onRejected) {
    return new MyPromise((resolve, reject) => {
      const handle = (fn, fallback) => (value) => {
        try {
          const result = (fn || fallback)(value);
          result instanceof MyPromise ? result.then(resolve, reject) : resolve(result);
        } catch (e) { reject(e); }
      };
      const handler = {
        onFulfilled: handle(onFulfilled, v => v),
        onRejected: handle(onRejected, e => { throw e; })
      };
      if (this.#state === 'pending') this.#handlers.push(handler);
      else if (this.#state === 'fulfilled') queueMicrotask(() => handler.onFulfilled(this.#value));
      else queueMicrotask(() => handler.onRejected(this.#value));
    });
  }

  catch(onRejected) { return this.then(null, onRejected); }

  static resolve(value) { return new MyPromise(r => r(value)); }
  static reject(reason) { return new MyPromise((_, r) => r(reason)); }
}</pre>

<h3>104.7 Curry Function</h3>
<pre>function curry(fn) {
  return function curried(...args) {
    if (args.length >= fn.length) {
      return fn.apply(this, args);
    }
    return function(...moreArgs) {
      return curried.apply(this, args.concat(moreArgs));
    };
  };
}

const add = curry((a, b, c) => a + b + c);
add(1)(2)(3);     // 6
add(1, 2)(3);     // 6
add(1)(2, 3);     // 6
add(1, 2, 3);     // 6</pre>

<h3>104.8 Memoize</h3>
<pre>function memoize(fn) {
  const cache = new Map();
  return function(...args) {
    const key = JSON.stringify(args);
    if (cache.has(key)) return cache.get(key);
    const result = fn.apply(this, args);
    cache.set(key, result);
    return result;
  };
}

// LRU Memoize (bounded cache size)
function memoizeLRU(fn, maxSize = 100) {
  const cache = new Map();
  return function(...args) {
    const key = JSON.stringify(args);
    if (cache.has(key)) {
      const value = cache.get(key);
      cache.delete(key);        // move to end (most recently used)
      cache.set(key, value);
      return value;
    }
    const result = fn.apply(this, args);
    cache.set(key, result);
    if (cache.size > maxSize) {
      const oldest = cache.keys().next().value;
      cache.delete(oldest);     // evict least recently used
    }
    return result;
  };
}</pre>

<!-- ═══════════════════════════════════════════════════════════════════
     ADDITIONAL INTERVIEW TOPICS — 8 topics
     ═══════════════════════════════════════════════════════════════════ -->

<h2 id="additional-topics" class="section-break">105. Additional Interview Topics</h2>
<p class="small"><strong>Checklist:</strong> Web Components · Internationalization (i18n) · Error Tracking · SEO for SPAs · Micro-frontends · Monorepos · CI/CD</p>

<h3>105.1 Web Components</h3>
<pre>// Custom Elements + Shadow DOM + HTML Templates
class MyCard extends HTMLElement {
  constructor() {
    super();
    const shadow = this.attachShadow({ mode: 'open' });
    shadow.innerHTML = `
      &lt;style&gt;
        :host { display: block; border: 1px solid #ddd; border-radius: 8px; padding: 16px; }
        :host([variant="primary"]) { border-color: #1a5c2e; }
        ::slotted(h3) { margin-top: 0; }
      &lt;/style&gt;
      &lt;slot name="header"&gt;&lt;/slot&gt;
      &lt;slot&gt;&lt;/slot&gt;
    `;
  }

  static get observedAttributes() { return ['variant']; }
  attributeChangedCallback(name, oldVal, newVal) { /* react to changes */ }
  connectedCallback() { /* element added to DOM */ }
  disconnectedCallback() { /* element removed from DOM */ }
}
customElements.define('my-card', MyCard);
// Usage: &lt;my-card variant="primary"&gt;&lt;h3 slot="header"&gt;Title&lt;/h3&gt;Content&lt;/my-card&gt;</pre>

<h3>105.2 Internationalization (i18n)</h3>
<pre>// Angular i18n (built-in)
&lt;h1 i18n="@@welcomeTitle"&gt;Welcome to our app&lt;/h1&gt;
&lt;p i18n&gt;You have {{ count }} items in your cart.&lt;/p&gt;

// JavaScript Intl API
new Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR' }).format(1234567.89);
// "₹12,34,567.89"

new Intl.DateTimeFormat('en-GB', { dateStyle: 'long' }).format(new Date());
// "15 March 2025"

new Intl.RelativeTimeFormat('en', { numeric: 'auto' }).format(-1, 'day');
// "yesterday"

new Intl.PluralRules('en').select(1);  // "one"
new Intl.PluralRules('en').select(5);  // "other"

// RTL (Right-to-Left) support
&lt;html dir="auto" lang="ar"&gt;
// Use CSS logical properties: margin-inline-start instead of margin-left</pre>

<h3>105.3 Error Tracking &amp; Monitoring</h3>
<pre>// Global error handlers
window.addEventListener('error', (event) => {
  reportError({ message: event.message, stack: event.error?.stack,
    filename: event.filename, line: event.lineno, col: event.colno });
});

window.addEventListener('unhandledrejection', (event) => {
  reportError({ message: event.reason?.message || 'Unhandled promise rejection',
    stack: event.reason?.stack });
});

// Angular global error handler
@Injectable()
class GlobalErrorHandler implements ErrorHandler {
  constructor(private logger: LoggingService) {}
  handleError(error: any) {
    this.logger.logError(error);
    // Send to Sentry, DataDog, etc.
  }
}
// providers: [{ provide: ErrorHandler, useClass: GlobalErrorHandler }]

// Source maps in production
// Upload source maps to error tracking service (Sentry, DataDog)
// NEVER serve source maps to users (security risk)</pre>

<h3>105.4 SEO for SPAs</h3>
<pre>// SPA SEO challenges:
// - Search engines may not execute JavaScript
// - Dynamic content not in initial HTML
// - No unique meta tags per page

// Solutions:
// 1. SSR (Angular Universal) — render on server, send full HTML
// 2. Pre-rendering — generate static HTML at build time
// 3. Dynamic meta tags
@Component({})
class ProductPage {
  constructor(private meta: Meta, private title: Title) {}

  ngOnInit() {
    this.title.setTitle('Product Name | My Store');
    this.meta.updateTag({ name: 'description', content: 'Product description...' });
    this.meta.updateTag({ property: 'og:title', content: 'Product Name' });
    this.meta.updateTag({ property: 'og:image', content: '/images/product.jpg' });
  }
}

// 4. Structured data (JSON-LD)
&lt;script type="application/ld+json"&gt;{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": "Product Name",
  "offers": { "@type": "Offer", "price": "29.99", "priceCurrency": "USD" }
}&lt;/script&gt;</pre>

<h3>105.5 Micro-frontends</h3>
<pre>// Approaches:
// 1. Module Federation (Webpack 5) — runtime module sharing
// 2. Single-SPA — framework-agnostic orchestrator
// 3. iframes — simple isolation, limited interaction
// 4. Web Components — framework-agnostic, Shadow DOM isolation

// Module Federation example
// Remote app (team-products)
new ModuleFederationPlugin({
  name: 'products',
  filename: 'remoteEntry.js',
  exposes: {
    './ProductList': './src/app/product-list/product-list.module.ts'
  },
  shared: { '@angular/core': { singleton: true }, rxjs: { singleton: true } }
});

// Shell app
new ModuleFederationPlugin({
  name: 'shell',
  remotes: {
    products: 'products@http://localhost:4201/remoteEntry.js'
  },
  shared: { '@angular/core': { singleton: true }, rxjs: { singleton: true } }
});

// Challenges: shared dependencies, routing, styling conflicts, communication</pre>

<h3>105.6 Monorepos</h3>
<pre>// Tools: Nx, Turborepo, Lerna, pnpm workspaces
// Benefits: shared code, atomic changes, unified CI, consistent tooling

// Nx workspace structure
my-workspace/
  apps/
    web-app/
    admin-app/
    api/
  libs/
    shared/
      ui/            // shared UI components
      utils/         // shared utilities
      models/        // shared TypeScript interfaces
    feature/
      auth/          // auth feature library
      products/      // products feature library

// nx.json — define task dependencies
{
  "targetDefaults": {
    "build": { "dependsOn": ["^build"] },  // build deps first
    "test": { "dependsOn": ["build"] }
  }
}

// npx nx affected --target=test  → only test what changed</pre>

<h3>105.7 CI/CD Pipeline</h3>
<pre>// GitHub Actions example
name: CI/CD Pipeline
on:
  push: { branches: [main] }
  pull_request: { branches: [main] }

jobs:
  build-and-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: 20, cache: 'npm' }
      - run: npm ci                    # install exact versions from lockfile
      - run: npm run lint              # lint check
      - run: npm run test -- --ci      # unit tests
      - run: npm run build -- --prod   # production build
      - run: npm run e2e               # E2E tests

  deploy:
    needs: build-and-test
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm ci &amp;&amp; npm run build
      - uses: actions/upload-artifact@v4
        with: { name: dist, path: dist/ }
      # Deploy to hosting (Vercel, AWS, Azure, etc.)</pre>

<div class="interview-q">
<h4>🎯 Interview Questions — System Design &amp; Architecture</h4>
<p><strong>Q: How would you design a real-time collaborative editor?</strong></p>
<p><strong>A:</strong> Use <strong>Operational Transformation (OT)</strong> or <strong>CRDTs</strong> for conflict resolution. WebSocket for real-time sync. Each user's cursor position broadcast to others. Operations: insert, delete at position. Server maintains canonical document state. Offline support: queue operations, apply on reconnect. Libraries: Yjs (CRDT), ShareDB (OT). Cursor presence using ephemeral WebSocket messages.</p>

<p><strong>Q: How do you decide between SSR, SSG, and CSR?</strong></p>
<p><strong>A:</strong> <strong>SSR</strong> (Server-Side Rendering): dynamic content, SEO-critical, personalized pages (e.g., product pages, dashboards). <strong>SSG</strong> (Static Site Generation): content doesn't change often, public pages (e.g., blog, docs, landing pages). <strong>CSR</strong> (Client-Side Rendering): behind auth, interactive apps, real-time features (e.g., admin panels, chat). Many apps use a mix: SSG for marketing, SSR for product pages, CSR for authenticated areas.</p>
</div>
"""
