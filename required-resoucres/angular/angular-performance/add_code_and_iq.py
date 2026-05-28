#!/usr/bin/env python3
"""Add hands-on code examples, interview questions, and code theory to every section."""

INPUT  = "angular-frontend-performance-guide.html"
OUTPUT = INPUT

with open(INPUT, "r", encoding="utf-8") as f:
    html = f.read()

import re

def insert_before_section_end(text, heading_fragment, content):
    """Insert content before the </section> that ends the section containing heading_fragment."""
    idx = text.find(heading_fragment)
    if idx == -1:
        print(f"WARNING: Could not find: {heading_fragment}")
        return text
    # Find the next </section> after this heading
    end = text.find("</section>", idx)
    if end == -1:
        print(f"WARNING: Could not find </section> after: {heading_fragment}")
        return text
    return text[:end] + content + "\n    " + text[end:]

# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 1: Performance Mindset
# ═══════════════════════════════════════════════════════════════════════════════

SEC1 = """
      <h3>Hands-on: Measuring the Performance Mindset in Practice</h3>
      <pre>// Step 1: Measure before optimizing — use the Performance API
performance.mark('page-ready-start');

// ... your app initialization code ...

performance.mark('page-ready-end');
performance.measure('page-ready-time', 'page-ready-start', 'page-ready-end');

const entries = performance.getEntriesByName('page-ready-time');
console.log('Page ready in:', entries[0].duration.toFixed(1), 'ms');</pre>
      <p><strong>Code theory:</strong> This code demonstrates the first rule of performance work — <strong>measure before you change anything</strong>. The Performance API lets you create named marks and measures that appear in Chrome DevTools traces. Without a baseline measurement, you cannot prove whether an optimization actually helped. The <code>performance.mark()</code> API is zero-overhead in production and works in all modern browsers.</p>

      <pre>// Step 2: Identify which layer is slow using a simple diagnostic
const navTiming = performance.getEntriesByType('navigation')[0] as PerformanceNavigationTiming;
console.table({
  'DNS':        navTiming.domainLookupEnd - navTiming.domainLookupStart,
  'TCP/TLS':    navTiming.connectEnd - navTiming.connectStart,
  'TTFB':       navTiming.responseStart - navTiming.requestStart,
  'Download':   navTiming.responseEnd - navTiming.responseStart,
  'DOM Parse':  navTiming.domInteractive - navTiming.responseEnd,
  'Load Event': navTiming.loadEventEnd - navTiming.loadEventStart
});
// This tells you immediately whether the delay is network, server, or browser</pre>
      <p><strong>Code theory:</strong> The Navigation Timing API breaks a page load into phases. By reading these timings, you can identify whether the bottleneck is DNS resolution, server processing (TTFB), download size, or browser parsing. This is the E2E diagnostic mindset — never guess which layer is slow when the browser already knows.</p>

      <h3>Interview Questions for Section 1</h3>
      <h4>Q: What is the correct order of performance work?</h4>
      <p><strong>A:</strong> Measure → identify bottleneck → optimize → verify. Never optimize blindly. Without measurement, you cannot prove a change helped, and without verification, you cannot catch regressions.</p>

      <h4>Q: What are the four fronts of frontend performance?</h4>
      <p><strong>A:</strong> Loading (how quickly content appears), interactivity (how quickly users can act), rendering smoothness (visual stability and jank-free UI), and resource efficiency (CPU, memory, bandwidth usage). A strong answer connects each front to a real metric: LCP for loading, INP for interactivity, CLS for smoothness, and memory/CPU profiles for efficiency.</p>

      <h4>Q: Why should you never optimize based on gut feeling?</h4>
      <p><strong>A:</strong> Because human perception of performance is unreliable, especially on developer machines which are faster than real user devices. Optimizing without data often means fixing the wrong layer. For example, you might optimize JavaScript when the real bottleneck is TTFB or image delivery. Measurement tells you exactly where time is spent.</p>

      <h4>Q: How do you distinguish a loading problem from an interaction problem?</h4>
      <p><strong>A:</strong> Loading problems show up in LCP, FCP, and TTFB — users wait too long before seeing content. Interaction problems show up in INP — users can see content but actions feel delayed. The diagnostic path is different: loading issues require inspecting network waterfall and resource priority, while interaction issues require inspecting main-thread traces and event handler cost.</p>
"""

# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 2: What Every Frontend Developer Should Know
# ═══════════════════════════════════════════════════════════════════════════════

SEC2 = """
      <h3>Hands-on: Diagnosing Which Layer Owns the Cost</h3>
      <pre>// Detect render-blocking resources programmatically
const resources = performance.getEntriesByType('resource') as PerformanceResourceTiming[];
const renderBlocking = resources.filter(r =&gt;
  r.renderBlockingStatus === 'blocking'
);
console.log('Render-blocking resources:', renderBlocking.map(r =&gt; r.name));</pre>
      <p><strong>Code theory:</strong> This uses the Resource Timing API to identify which resources the browser considers render-blocking. In interviews, this shows you understand the browser rendering pipeline — CSS and synchronous scripts can delay first paint because the browser needs them before it can safely render. Identifying blocking resources is the first step to fixing slow initial loads.</p>

      <pre>// Detect long tasks that block the main thread
const longTaskObserver = new PerformanceObserver((list) =&gt; {
  for (const entry of list.getEntries()) {
    console.warn('Long task detected:', {
      duration: entry.duration.toFixed(0) + 'ms',
      startTime: entry.startTime.toFixed(0) + 'ms',
      name: entry.name
    });
  }
});
longTaskObserver.observe({ type: 'longtask', buffered: true });</pre>
      <p><strong>Code theory:</strong> Long tasks (&gt;50ms) are the primary cause of poor interactivity. This observer runs in the background and logs whenever the main thread is blocked. In production, you would send these to your RUM pipeline. The <code>buffered: true</code> option captures long tasks that happened before the observer was created, ensuring you don't miss boot-time blocking.</p>

      <pre>// Quick memory health check
setInterval(() =&gt; {
  if ('memory' in performance) {
    const mem = (performance as any).memory;
    console.log('Heap:', (mem.usedJSHeapSize / 1048576).toFixed(1), 'MB',
                '/ Limit:', (mem.jsHeapSizeLimit / 1048576).toFixed(0), 'MB');
  }
}, 10000);</pre>
      <p><strong>Code theory:</strong> Memory growth over time is a silent performance killer. This simple interval logs heap usage every 10 seconds. If the number keeps climbing during repeated navigation, you have a memory leak. In interviews, mention that you would remove this in production and use heap snapshots for detailed investigation.</p>

      <h3>Interview Questions for Section 2</h3>
      <h4>Q: Name the stages of the browser rendering pipeline.</h4>
      <p><strong>A:</strong> HTML parsing → DOM construction → CSS parsing → CSSOM construction → style calculation → layout (geometry) → paint (pixels) → compositing (layers assembled on screen). Changes at earlier stages are more expensive because they invalidate later stages. For example, a layout change forces repaint and recomposite, while an opacity change can often be handled by compositing alone.</p>

      <h4>Q: What is the difference between a network bottleneck and a rendering bottleneck?</h4>
      <p><strong>A:</strong> A network bottleneck means resources arrive too slowly — you see high TTFB, slow downloads, or blocked requests in the waterfall. A rendering bottleneck means the browser has the resources but struggles to process them — you see long tasks, expensive style recalculations, frequent layout, or heavy paint in the performance trace. The tools are different: Network panel for network issues, Performance panel for rendering issues.</p>

      <h4>Q: Why are framework abstractions "not free"?</h4>
      <p><strong>A:</strong> Every framework adds execution paths. Angular's change detection walks component trees and evaluates bindings. React's reconciliation diffs virtual DOM. These operations consume CPU time. A simple <code>{{ user.name }}</code> binding costs almost nothing, but a method call in a template that filters an array is re-executed on every change detection cycle, potentially hundreds of times per second.</p>

      <h4>Q: How do you check if a performance problem is caused by JavaScript execution or by DOM/rendering work?</h4>
      <p><strong>A:</strong> Record a Chrome DevTools performance trace, then examine the main thread flame chart. Yellow blocks indicate JavaScript execution. Purple blocks indicate layout and style recalculation. Green blocks indicate paint. If yellow dominates, reduce JavaScript — smaller bundles, less work per interaction. If purple or green dominate, reduce DOM complexity, avoid layout thrashing, and optimize CSS.</p>
"""

# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 3: Metrics
# ═══════════════════════════════════════════════════════════════════════════════

SEC3 = """
      <h3>Hands-on: Collecting and Logging Core Web Vitals</h3>
      <pre>// E2E metrics collection with web-vitals library
import { onLCP, onINP, onCLS, onFCP, onTTFB } from 'web-vitals';

interface MetricPayload {
  name: string;
  value: number;
  rating: string;  // 'good' | 'needs-improvement' | 'poor'
  path: string;
  deviceType: string;
}

function getDeviceType(): string {
  const ua = navigator.userAgent;
  if (/Mobi|Android/i.test(ua)) return 'mobile';
  if (/Tablet|iPad/i.test(ua)) return 'tablet';
  return 'desktop';
}

function reportMetric(metric: { name: string; value: number; rating: string }) {
  const payload: MetricPayload = {
    name: metric.name,
    value: Math.round(metric.value),
    rating: metric.rating,
    path: location.pathname,
    deviceType: getDeviceType()
  };
  // Use sendBeacon for reliable delivery even during page unload
  navigator.sendBeacon('/api/rum', JSON.stringify(payload));
}

onLCP(reportMetric);
onINP(reportMetric);
onCLS(reportMetric);
onFCP(reportMetric);
onTTFB(reportMetric);</pre>
      <p><strong>Code theory:</strong> This is a production-ready RUM (Real User Monitoring) setup. The <code>web-vitals</code> library captures lab-quality metrics from real users. <code>sendBeacon</code> ensures the data reaches your server even if the user navigates away mid-report. The device type and path enrichment let you segment performance by route and device — essential for finding which pages are slow and for whom.</p>

      <pre>// Observe CLS contributors — find which elements shift
const clsObserver = new PerformanceObserver((list) =&gt; {
  for (const entry of list.getEntries() as any[]) {
    if (entry.hadRecentInput) continue; // Ignore user-triggered shifts
    for (const source of entry.sources || []) {
      console.log('CLS source:', source.node, 'shifted by', entry.value.toFixed(4));
    }
  }
});
clsObserver.observe({ type: 'layout-shift', buffered: true });</pre>
      <p><strong>Code theory:</strong> CLS is often the hardest metric to debug because the shift can be caused by images, fonts, ads, or dynamic content injection. This observer identifies exactly which DOM node shifted and by how much. The <code>hadRecentInput</code> filter excludes shifts caused by user actions (which are expected). This is the kind of code that separates a diagnostic answer from a textbook answer in interviews.</p>

      <h3>Interview Questions for Section 3</h3>
      <h4>Q: What is the difference between LCP and FCP?</h4>
      <p><strong>A:</strong> FCP marks when <em>any</em> content first appears (could be a spinner or header). LCP marks when the <em>largest meaningful</em> content element is rendered — typically a hero image, main heading, or primary block. LCP better represents when users feel the page has "loaded" because it captures main content, not just first pixels.</p>

      <h4>Q: Why is INP replacing FID as a Core Web Vital?</h4>
      <p><strong>A:</strong> FID measured only the <em>first</em> interaction delay. INP measures responsiveness across the <em>entire page lifetime</em>, capturing the worst interaction. This is more realistic because users interact many times — a page with good first-click response but laggy scrolling or slow form interactions would score well on FID but poorly on INP, correctly reflecting the real user experience.</p>

      <h4>Q: What is the difference between lab and field metrics?</h4>
      <p><strong>A:</strong> Lab metrics are collected in controlled environments (Lighthouse, WebPageTest) — same device profile, same network, deterministic. Field metrics come from real users via RUM — variable devices, networks, geographies, and behaviors. Lab is for comparison and debugging. Field is for truth. A page can score perfectly in lab but poorly in the field because of device diversity, third-party scripts, or server-side variability.</p>

      <h4>Q: How would you debug a page with good LCP but poor CLS?</h4>
      <p><strong>A:</strong> Good LCP means main content loads fast, but poor CLS means layout shifts are happening. Common causes: images without explicit dimensions, fonts that swap and change text metrics, ads or banners injected after initial render, or dynamically loaded content pushing existing content down. I would use a PerformanceObserver for layout-shift entries to identify exactly which elements are shifting and when.</p>
"""

# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 4: General Frontend Performance
# ═══════════════════════════════════════════════════════════════════════════════

SEC4 = """
      <h3>Hands-on: E2E Frontend Optimization Code</h3>

      <h4>Example: Critical CSS inlining with deferred stylesheet</h4>
      <pre>&lt;head&gt;
  &lt;!-- Inline only critical above-the-fold CSS --&gt;
  &lt;style&gt;
    body { font-family: system-ui, sans-serif; margin: 0; }
    .hero { min-height: 400px; background: #1a1a2e; color: white; }
    .nav { height: 60px; display: flex; align-items: center; }
  &lt;/style&gt;

  &lt;!-- Defer non-critical CSS --&gt;
  &lt;link rel="preload" href="/styles/main.css" as="style"
        onload="this.onload=null;this.rel='stylesheet'" /&gt;
  &lt;noscript&gt;&lt;link rel="stylesheet" href="/styles/main.css" /&gt;&lt;/noscript&gt;
&lt;/head&gt;</pre>
      <p><strong>Code theory:</strong> CSS is render-blocking — the browser will not paint until CSSOM is complete. By inlining only the critical above-the-fold CSS and deferring the rest, you allow the browser to paint meaningful content faster. The <code>preload</code> with <code>onload</code> trick loads the full stylesheet asynchronously without blocking rendering. This directly improves LCP and FCP. The <code>noscript</code> fallback ensures the stylesheet still loads when JavaScript is disabled.</p>

      <h4>Example: Resource prioritization with fetchpriority</h4>
      <pre>&lt;!-- High priority for LCP image --&gt;
&lt;img src="/hero.avif" fetchpriority="high" width="1200" height="600" alt="Hero" /&gt;

&lt;!-- Low priority for below-fold images --&gt;
&lt;img src="/footer-bg.webp" fetchpriority="low" loading="lazy" width="800" height="200" alt="Footer" /&gt;

&lt;!-- Preconnect to API origin used on this page --&gt;
&lt;link rel="preconnect" href="https://api.myapp.com" /&gt;

&lt;!-- Preload critical font --&gt;
&lt;link rel="preload" href="/fonts/main.woff2" as="font" type="font/woff2" crossorigin /&gt;</pre>
      <p><strong>Code theory:</strong> Browsers prioritize resources using heuristics, but those heuristics do not always match your page's actual priorities. <code>fetchpriority="high"</code> tells the browser to prioritize the LCP image over other images. <code>fetchpriority="low"</code> prevents below-fold images from competing with critical resources. <code>preconnect</code> saves DNS+TCP+TLS time for origins you know will be needed. <code>preload</code> for fonts ensures the font is discovered early instead of waiting for CSS parsing to find the <code>@font-face</code> rule.</p>

      <h4>Example: Breaking long tasks with yield-to-main pattern</h4>
      <pre>// Process a large dataset without blocking the main thread
async function processInChunks&lt;T&gt;(
  items: T[],
  processFn: (item: T) =&gt; void,
  chunkSize = 50
): Promise&lt;void&gt; {
  for (let i = 0; i &lt; items.length; i += chunkSize) {
    const chunk = items.slice(i, i + chunkSize);
    chunk.forEach(processFn);

    // Yield to the main thread between chunks
    if (i + chunkSize &lt; items.length) {
      await new Promise(resolve =&gt; setTimeout(resolve, 0));
    }
  }
}

// Usage
await processInChunks(thousandsOfRecords, record =&gt; {
  updateDOMForRecord(record);
});</pre>
      <p><strong>Code theory:</strong> Long tasks (&gt;50ms) block the main thread and hurt INP. This pattern breaks large synchronous work into chunks and yields to the browser between chunks using <code>setTimeout(resolve, 0)</code>. This allows the browser to process user interactions, paint frames, and handle other events between chunks. The tradeoff is slightly slower total processing time, but much better responsiveness. Use this when you need to update the DOM for 100+ items without freezing the UI.</p>

      <h4>Example: Service Worker caching strategy</h4>
      <pre>// service-worker.ts — stale-while-revalidate for API data
self.addEventListener('fetch', (event: FetchEvent) =&gt; {
  if (event.request.url.includes('/api/products')) {
    event.respondWith(
      caches.open('api-cache').then(async (cache) =&gt; {
        const cached = await cache.match(event.request);
        const fetched = fetch(event.request).then((response) =&gt; {
          cache.put(event.request, response.clone());
          return response;
        });
        return cached || fetched;
      })
    );
  }
});</pre>
      <p><strong>Code theory:</strong> Stale-while-revalidate serves cached data immediately for instant perceived speed, while fetching fresh data in the background for next time. This is ideal for data that changes but is still useful when slightly stale (product lists, catalogs). The tradeoff: users may see old data briefly. For critical real-time data (cart, payments), use network-first strategies instead.</p>

      <h3>Interview Questions for Section 4</h3>
      <h4>Q: What is the critical rendering path and how do you optimize it?</h4>
      <p><strong>A:</strong> The critical rendering path is the sequence of steps from receiving HTML to painting the first meaningful pixel: HTML parsing → DOM → CSS parsing → CSSOM → render tree → layout → paint. To optimize it: inline critical CSS, defer non-critical CSS, use <code>async</code> or <code>defer</code> on scripts, reduce render-blocking resources, minimize critical resource count and size, and preconnect to important origins.</p>

      <h4>Q: Why is "ship less JavaScript" the most impactful advice?</h4>
      <p><strong>A:</strong> JavaScript has four costs: download, parse, compile, and execute. Even after caching eliminates download cost, parse and compile still run on every visit. On low-end mobile devices, parsing 300KB of JavaScript can block the main thread for several hundred milliseconds. Shipping less JS reduces all four costs simultaneously. Every other optimization (defer, split, tree shake) is a variation of this principle.</p>

      <h4>Q: How do you decide between preload, prefetch, and preconnect?</h4>
      <p><strong>A:</strong> <strong>Preconnect:</strong> use when you know you will need a specific origin soon (e.g., API server, font CDN) — saves DNS+TCP+TLS time. <strong>Preload:</strong> use for critical resources the browser discovers too late (e.g., fonts referenced in CSS, hero images loaded via CSS background). <strong>Prefetch:</strong> use for resources needed on likely next navigations, not the current page. Overusing preload starves critical resources; overusing prefetch wastes bandwidth.</p>

      <h4>Q: What is layout thrashing and how do you fix it?</h4>
      <p><strong>A:</strong> Layout thrashing happens when JavaScript repeatedly reads layout properties (offsetWidth, getBoundingClientRect) then writes to the DOM in a loop. Each read forces the browser to synchronously flush pending layout work. Fix: batch all reads first, then batch all writes. Or use <code>requestAnimationFrame</code> to schedule writes after reads. Modern practice: use CSS transforms instead of layout-triggering properties whenever possible.</p>

      <h4>Q: How do third-party scripts hurt performance?</h4>
      <p><strong>A:</strong> Third-party scripts compete for bandwidth, main-thread time, memory, and DOM space without following your architectural rules. They can add network requests, event listeners, timers, and forced layouts outside your control. Containment strategies: load them after critical rendering, use facades for heavy embeds, isolate via iframes, set separate performance budgets, and audit regularly.</p>
"""

# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 5: Angular Performance (already has lots of content, add IQ section)
# ═══════════════════════════════════════════════════════════════════════════════

SEC5 = """
      <h3>Hands-on: E2E Angular Performance Patterns</h3>

      <h4>Example: Signal-based derived state (replacing template methods)</h4>
      <pre>@Component({
  selector: 'app-user-list',
  changeDetection: ChangeDetectionStrategy.OnPush,
  template: `
    &lt;input #search (input)="searchTerm.set(search.value)" placeholder="Filter users" /&gt;
    &lt;p&gt;Showing {{ filteredUsers().length }} of {{ users().length }} users&lt;/p&gt;
    @for (user of filteredUsers(); track user.id) {
      &lt;div class="user-card"&gt;{{ user.name }} — {{ user.role }}&lt;/div&gt;
    }
  `
})
export class UserListComponent {
  users = signal&lt;User[]&gt;([]);
  searchTerm = signal('');

  // Derived state: only recomputes when users or searchTerm change
  filteredUsers = computed(() =&gt; {
    const term = this.searchTerm().toLowerCase();
    if (!term) return this.users();
    return this.users().filter(u =&gt; u.name.toLowerCase().includes(term));
  });

  constructor(private http: HttpClient) {
    this.http.get&lt;User[]&gt;('/api/users').subscribe(data =&gt; this.users.set(data));
  }
}</pre>
      <p><strong>Code theory:</strong> This is the modern Angular performance pattern. Instead of calling <code>filteredUsers()</code> as a method in the template (which re-executes on every change detection cycle), we use a <code>computed</code> signal. The signal dependency graph ensures filtering runs only when <code>users</code> or <code>searchTerm</code> actually change — not on unrelated Angular activity. Combined with <code>OnPush</code> and <code>@for...track</code>, this creates a component that does minimal work per update cycle.</p>

      <h4>Example: Zone pollution detection and fix</h4>
      <pre>// Detecting zone pollution: log every change detection run
@Component({ ... })
export class AppComponent {
  constructor(private ngZone: NgZone) {
    // DEBUG ONLY: log every CD cycle
    this.ngZone.onStable.subscribe(() =&gt; {
      console.count('Change detection cycle');
    });
  }
}

// Fix: run noisy third-party code outside Angular's zone
@Injectable({ providedIn: 'root' })
export class AnalyticsService {
  constructor(private ngZone: NgZone) {}

  init() {
    this.ngZone.runOutsideAngular(() =&gt; {
      // This timer no longer triggers change detection
      setInterval(() =&gt; this.sendAnalyticsPing(), 30000);
    });
  }

  trackEvent(name: string) {
    this.ngZone.runOutsideAngular(() =&gt; {
      navigator.sendBeacon('/analytics', JSON.stringify({ event: name }));
    });
  }
}</pre>
      <p><strong>Code theory:</strong> Zone.js patches all async APIs. An analytics timer firing every 30 seconds triggers change detection every 30 seconds — even when nothing in the UI changed. <code>runOutsideAngular()</code> executes code in a zone that Angular does not monitor, preventing unnecessary change detection cycles. The debug log in <code>onStable</code> reveals how often CD runs — if it runs hundreds of times when the UI is idle, zone pollution is the cause.</p>

      <h4>Example: Subscription cleanup with takeUntilDestroyed</h4>
      <pre>@Component({
  selector: 'app-dashboard',
  changeDetection: ChangeDetectionStrategy.OnPush,
  template: `
    &lt;div&gt;{{ statusMessage }}&lt;/div&gt;
    &lt;div&gt;{{ lastUpdate | date:'medium' }}&lt;/div&gt;
  `
})
export class DashboardComponent {
  statusMessage = '';
  lastUpdate = new Date();
  private destroyRef = inject(DestroyRef);

  constructor(private ws: WebSocketService, private cdr: ChangeDetectorRef) {
    this.ws.messages$.pipe(
      takeUntilDestroyed(this.destroyRef)
    ).subscribe(msg =&gt; {
      this.statusMessage = msg.text;
      this.lastUpdate = new Date();
      this.cdr.markForCheck();
    });
  }
}</pre>
      <p><strong>Code theory:</strong> Without <code>takeUntilDestroyed</code>, if the user navigates away and back 10 times, 10 subscriptions would stack up — each receiving messages and doing work. This is a classic memory leak. <code>takeUntilDestroyed</code> automatically unsubscribes when the component is destroyed. Combined with <code>OnPush</code> + <code>markForCheck()</code>, only the specific update triggers a CD cycle, not every unrelated event.</p>

      <h4>Example: Performance budget enforcement in angular.json</h4>
      <pre>// angular.json — complete budget configuration
{
  "projects": {
    "my-app": {
      "architect": {
        "build": {
          "configurations": {
            "production": {
              "budgets": [
                { "type": "initial", "maximumWarning": "250kb", "maximumError": "300kb" },
                { "type": "anyComponentStyle", "maximumWarning": "6kb", "maximumError": "10kb" },
                { "type": "anyScript", "maximumWarning": "80kb", "maximumError": "120kb" }
              ],
              "optimization": true,
              "sourceMap": false,
              "namedChunks": false
            }
          }
        }
      }
    }
  }
}</pre>
      <p><strong>Code theory:</strong> Build budgets act as automated performance guardrails. If a developer adds a large library, the build fails or warns before deployment. <code>"initial"</code> controls the main bundle that every user downloads. <code>"anyComponentStyle"</code> prevents bloated component CSS. <code>"anyScript"</code> catches individual lazy chunks that grow too large. This shifts performance from reactive debugging to proactive prevention.</p>

      <h3>Interview Questions for Section 5</h3>
      <h4>Q: Explain how Angular change detection works and when it runs.</h4>
      <p><strong>A:</strong> Angular walks the component tree top-down, evaluating bindings to check if the DOM needs updating. It runs after every async event that Zone.js patches — clicks, timers, HTTP responses, promise resolutions. With default strategy, Angular checks every component. With OnPush, Angular skips a subtree unless it has a new input reference, an internal event, or an explicit <code>markForCheck()</code>. The cost grows with tree size × bindings × frequency.</p>

      <h4>Q: When would you choose signals over RxJS in Angular?</h4>
      <p><strong>A:</strong> Signals for synchronous, local UI state and derived values — search terms, filters, counters, computed display values. RxJS for asynchronous streams — HTTP requests with cancellation, WebSocket messages, multi-event composition, retries, and debouncing. Often both are used together: RxJS manages the async flow, then writes results into signals that the template reads synchronously.</p>

      <h4>Q: What is zone pollution and how do you diagnose it?</h4>
      <p><strong>A:</strong> Zone pollution is when non-Angular async activity (third-party timers, analytics pings, chat widgets) triggers unnecessary change detection cycles. Diagnosis: subscribe to <code>NgZone.onStable</code> and count cycles, or use Angular DevTools profiler to see CD frequency. Fix: wrap noisy code in <code>NgZone.runOutsideAngular()</code>, or move to zoneless Angular with explicit reactivity.</p>

      <h4>Q: Why doesn't <code>@defer</code> remove performance cost — it only moves it?</h4>
      <p><strong>A:</strong> The deferred component's JavaScript still has to be downloaded, parsed, compiled, and executed — just at a later time. The win is that users get meaningful interaction sooner because the initial bundle is smaller. The cost is still paid when the trigger fires (viewport, interaction, idle). Watch for: cascaded defers creating request waterfalls, and placeholder components that are themselves expensive.</p>

      <h4>Q: How does OnPush break if misused?</h4>
      <p><strong>A:</strong> If you mutate an object property without creating a new reference, Angular with OnPush does not know the input changed. The view stays stale. Example: <code>this.user.name = 'new'</code> will not trigger an update because the object reference is unchanged. Fix: use immutable patterns like <code>this.user = { ...this.user, name: 'new' }</code> or use signals which track changes at the value level.</p>

      <h4>Q: What is the difference between trackBy and not using it in ngFor?</h4>
      <p><strong>A:</strong> Without trackBy, Angular uses object identity. If the array is replaced with a new one (even with the same items), Angular destroys and recreates all DOM nodes. With trackBy returning a stable ID, Angular can match existing DOM nodes to their corresponding items and only update what actually changed. For a 1000-item list, this can reduce DOM operations from 1000 destroys + 1000 creates to just a few updates.</p>
"""

# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 8: Performance Tooling (already has code, add more IQ)
# ═══════════════════════════════════════════════════════════════════════════════

SEC8 = """
      <h3>Hands-on: E2E Tooling Code Examples</h3>

      <h4>Example: Automated Lighthouse CI in a pipeline</h4>
      <pre>// lighthouserc.js — Lighthouse CI configuration
module.exports = {
  ci: {
    collect: {
      url: ['http://localhost:4200/', 'http://localhost:4200/dashboard'],
      numberOfRuns: 3,
      settings: {
        preset: 'desktop',
        throttling: { cpuSlowdownMultiplier: 4 }
      }
    },
    assert: {
      assertions: {
        'categories:performance': ['error', { minScore: 0.85 }],
        'largest-contentful-paint': ['warn', { maxNumericValue: 2500 }],
        'interactive': ['error', { maxNumericValue: 5000 }],
        'total-byte-weight': ['warn', { maxNumericValue: 400000 }]
      }
    },
    upload: {
      target: 'temporary-public-storage'
    }
  }
};</pre>
      <p><strong>Code theory:</strong> This configuration runs Lighthouse 3 times per URL, averages the results, and fails the build if performance score drops below 0.85 or LCP exceeds 2.5s. Running it in CI means every pull request is automatically checked for performance regressions before merge. The <code>cpuSlowdownMultiplier: 4</code> simulates a mid-range phone, catching problems that developer laptops hide.</p>

      <h4>Example: Memory leak detection script</h4>
      <pre>// Run in Chrome DevTools console — navigate back and forth, then run this
async function detectLeaks() {
  const snapshots: number[] = [];

  for (let i = 0; i &lt; 5; i++) {
    // Trigger garbage collection (only works with --expose-gc flag)
    if (typeof gc === 'function') gc();

    const mem = (performance as any).memory;
    snapshots.push(mem.usedJSHeapSize);
    console.log(`Snapshot ${i + 1}: ${(mem.usedJSHeapSize / 1048576).toFixed(1)} MB`);

    // Wait 2 seconds between snapshots
    await new Promise(r =&gt; setTimeout(r, 2000));
  }

  const growth = snapshots[4] - snapshots[0];
  if (growth &gt; 5 * 1048576) {
    console.error('Possible memory leak: heap grew by',
                  (growth / 1048576).toFixed(1), 'MB over 5 snapshots');
  } else {
    console.log('Heap appears stable');
  }
}</pre>
      <p><strong>Code theory:</strong> This script takes periodic heap size measurements. If memory keeps growing after repeated navigation (go to a page, leave, return), it suggests leaked objects — detached DOM nodes, uncleaned subscriptions, retained closures, or growing caches. In real debugging, you would take heap snapshots in DevTools and compare retained sizes to find the exact leak source.</p>

      <h3>Interview Questions for Section 8</h3>
      <h4>Q: How do you use Chrome DevTools to diagnose a slow interaction?</h4>
      <p><strong>A:</strong> (1) Open Performance panel and enable CPU throttling. (2) Click Record, perform the slow interaction, then stop. (3) Find the interaction in the trace timeline. (4) Check the flame chart: is the delay in the event handler (yellow), in rendering (purple/green), or in queued work before the handler starts? (5) If handler is slow, inspect the call stack for expensive functions. If rendering is slow, check for layout thrashing or excessive DOM operations.</p>

      <h4>Q: What is the difference between Lighthouse score and real user performance?</h4>
      <p><strong>A:</strong> Lighthouse runs on one page, one device profile, one network condition, once. Real users have diverse devices, networks, geographies, and interaction patterns. A 95 Lighthouse score does not guarantee good field performance. Use Lighthouse for controlled comparisons and catching obvious regressions. Use RUM (CrUX, web-vitals) for actual user experience data. Always compare both.</p>

      <h4>Q: What does a heap snapshot "retainer path" tell you?</h4>
      <p><strong>A:</strong> The retainer path shows the chain of references keeping an object alive in memory. If a detached DOM node has a retainer path through an event listener → a component → a service → the root, you know the listener was never removed. The fix is to remove the listener when the component is destroyed. Retainer paths turn "there is a leak" into "here is exactly why and how to fix it."</p>

      <h4>Q: How do bundle budgets prevent performance regressions?</h4>
      <p><strong>A:</strong> Bundle budgets define maximum allowed sizes for initial bundles, lazy chunks, and component styles. When a developer adds a dependency that pushes a bundle past budget, the build fails before deployment. This catches regressions at the source — in the PR — instead of after users report slowness. Budgets should be per-route when possible, not just a single global target.</p>
"""

# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 9: Common Angular Performance Mistakes
# ═══════════════════════════════════════════════════════════════════════════════

SEC9 = """
      <h3>Hands-on: Mistake Examples with Before/After</h3>

      <h4>Mistake: Expensive method in template</h4>
      <pre>// BAD — re-runs on every change detection
@Component({
  template: `&lt;span&gt;Total: {{ calculateTotal() }}&lt;/span&gt;`
})
class OrderComponent {
  items: OrderItem[] = [];
  calculateTotal() {
    return this.items.reduce((sum, item) =&gt; sum + item.price * item.qty, 0);
  }
}

// FIXED — compute once, update only when data changes
@Component({
  changeDetection: ChangeDetectionStrategy.OnPush,
  template: `&lt;span&gt;Total: {{ total() }}&lt;/span&gt;`
})
class OrderComponent {
  items = signal&lt;OrderItem[]&gt;([]);
  total = computed(() =&gt;
    this.items().reduce((sum, item) =&gt; sum + item.price * item.qty, 0)
  );
}</pre>
      <p><strong>Code theory:</strong> In the bad version, <code>calculateTotal()</code> runs on every CD cycle — potentially 30+ times per second during scrolling or typing. The fixed version uses a computed signal that recalculates only when <code>items</code> changes. For a 100-item order, this could eliminate thousands of unnecessary array iterations per minute.</p>

      <h4>Mistake: Mutating objects under OnPush</h4>
      <pre>// BAD — OnPush does not detect the mutation
updateName(user: User) {
  user.name = 'Updated';  // Same reference, OnPush skips update
}

// FIXED — create a new reference
updateName(user: User): User {
  return { ...user, name: 'Updated' };  // New reference triggers OnPush
}</pre>
      <p><strong>Code theory:</strong> OnPush compares input references, not deep values. Mutating a property on an existing object does not change the reference, so Angular assumes nothing changed and skips the subtree. Creating a new object with the spread operator produces a new reference, which OnPush correctly detects as a change.</p>

      <h4>Mistake: Subscription leak</h4>
      <pre>// BAD — subscribes but never unsubscribes
ngOnInit() {
  this.dataService.stream$.subscribe(data =&gt; {
    this.data = data;
  });
  // If user navigates away and back 5 times, 5 subscriptions accumulate
}

// FIXED — auto-cleanup with takeUntilDestroyed
private destroyRef = inject(DestroyRef);
ngOnInit() {
  this.dataService.stream$.pipe(
    takeUntilDestroyed(this.destroyRef)
  ).subscribe(data =&gt; {
    this.data = data;
  });
}</pre>
      <p><strong>Code theory:</strong> Each unsubscribed subscription stays alive in memory, receiving data and executing callback code even after the component is destroyed. With repeated navigation, this creates memory growth and redundant processing. <code>takeUntilDestroyed</code> hooks into Angular's component lifecycle and automatically completes the subscription when the component is destroyed.</p>

      <h3>Interview Questions for Section 9</h3>
      <h4>Q: What are the top 3 Angular performance mistakes you have seen?</h4>
      <p><strong>A:</strong> (1) Template methods — functions in templates re-execute on every CD cycle. Fix: use computed signals or pure pipes. (2) Missing trackBy on lists — causes full DOM recreation on data refresh. Fix: provide stable identity function. (3) Subscription leaks — orphaned subscriptions waste memory and CPU. Fix: use <code>takeUntilDestroyed</code> or <code>async</code> pipe.</p>

      <h4>Q: How does mutating an object under OnPush cause bugs?</h4>
      <p><strong>A:</strong> OnPush checks input reference, not content. <code>user.name = 'new'</code> does not change the reference, so Angular skips the update. The UI shows stale data even though the underlying object changed. Users see "nothing happened" when they expected an update. Fix: always produce new references with spread operator or signal updates.</p>
"""

# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 10: Common General Frontend Mistakes
# ═══════════════════════════════════════════════════════════════════════════════

SEC10 = """
      <h3>Hands-on: Mistake Examples with Fixes</h3>

      <h4>Mistake: Images without dimensions causing CLS</h4>
      <pre>&lt;!-- BAD — no dimensions causes layout shift --&gt;
&lt;img src="/photo.jpg" alt="Photo" /&gt;

&lt;!-- FIXED — explicit dimensions + proper loading --&gt;
&lt;img src="/photo.webp" width="800" height="600" loading="lazy"
     decoding="async" alt="Photo" /&gt;</pre>
      <p><strong>Code theory:</strong> Without width and height, the browser allocates zero space for the image. When the image loads, content below it shifts down — this is a layout shift scored by CLS. Adding explicit dimensions lets the browser reserve the correct aspect ratio space before the image arrives.</p>

      <h4>Mistake: Loading full icon library</h4>
      <pre>// BAD — imports entire icon set (500KB+)
import '@fortawesome/fontawesome-free/css/all.css';

// FIXED — import only the icons you use
import { faSearch, faUser, faHome } from '@fortawesome/free-solid-svg-icons';
library.add(faSearch, faUser, faHome);</pre>
      <p><strong>Code theory:</strong> Full icon libraries can add 200-500KB of CSS/fonts/SVGs. Tree-shakeable icon imports ensure only the 5-10 icons you actually use are included in the bundle. This directly reduces download, parse, and rendering cost.</p>

      <h3>Interview Questions for Section 10</h3>
      <h4>Q: Why can Lighthouse score be 95 while users still complain about slowness?</h4>
      <p><strong>A:</strong> Lighthouse tests one synthetic load on a simulated device. Real users may have slower devices, weaker networks, third-party scripts that load only in production, dynamic content that shifts layout, and interaction-heavy flows that Lighthouse does not test. A high lab score does not guarantee good field performance (INP, real CLS) — you need RUM data to see what users actually experience.</p>

      <h4>Q: What causes CLS from font loading?</h4>
      <p><strong>A:</strong> When a web font loads and replaces the fallback system font, text metrics (width, height, spacing) can change, causing text to reflow and push neighboring elements. Fix: use <code>font-display: swap</code> with a well-matched system fallback, or use <code>size-adjust</code> CSS to match fallback metrics to the web font metrics.</p>
"""

# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 11: E2E Checklist
# ═══════════════════════════════════════════════════════════════════════════════

SEC11 = """
      <h3>Hands-on: Checklist as Executable Code</h3>
      <pre>// Automated pre-release performance audit script
async function preReleaseAudit() {
  const checks: { name: string; pass: boolean; detail: string }[] = [];

  // Check 1: Bundle size
  const stats = await fetch('/build-stats.json').then(r =&gt; r.json());
  const mainSize = stats.chunks.find((c: any) =&gt; c.initial)?.size || 0;
  checks.push({
    name: 'Initial bundle size',
    pass: mainSize &lt; 300 * 1024,
    detail: `${(mainSize / 1024).toFixed(0)}KB (budget: 300KB)`
  });

  // Check 2: LCP element has fetchpriority
  const lcpImg = document.querySelector('img[fetchpriority="high"]');
  checks.push({
    name: 'LCP image has fetchpriority=high',
    pass: !!lcpImg,
    detail: lcpImg ? lcpImg.getAttribute('src') || 'found' : 'NOT FOUND'
  });

  // Check 3: No render-blocking scripts without defer/async
  const blockingScripts = document.querySelectorAll(
    'script:not([defer]):not([async]):not([type="module"])'
  );
  checks.push({
    name: 'No blocking scripts',
    pass: blockingScripts.length === 0,
    detail: `${blockingScripts.length} blocking script(s)`
  });

  // Check 4: Images have dimensions
  const imagesWithoutDimensions = [...document.querySelectorAll('img')].filter(
    img =&gt; !img.width &amp;&amp; !img.getAttribute('width')
  );
  checks.push({
    name: 'All images have dimensions',
    pass: imagesWithoutDimensions.length === 0,
    detail: `${imagesWithoutDimensions.length} image(s) missing dimensions`
  });

  console.table(checks);
  return checks.every(c =&gt; c.pass);
}</pre>
      <p><strong>Code theory:</strong> This script automates the checklist as code — you can run it in CI or in a browser console before release. Each check maps to a real performance principle: bundle budget prevents bloat, fetchpriority ensures LCP images load fast, no blocking scripts prevents main-thread delay, and image dimensions prevent CLS. Making checklists executable means they cannot be forgotten.</p>

      <h3>Interview Questions for Section 11</h3>
      <h4>Q: Walk me through how you would introduce performance practices into a team that has never measured performance.</h4>
      <p><strong>A:</strong> (1) Start with a baseline: run Lighthouse on 3-5 key pages and record scores. (2) Add RUM to capture real user metrics (LCP, INP, CLS). (3) Set initial budgets that pass today and tighten them over sprints. (4) Add Lighthouse CI to block PRs that introduce regressions. (5) Create a monthly dashboard review for the team. (6) Build performance into DoD (definition-of-done) for features touching critical pages.</p>
"""

# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 12: Interview Readiness
# ═══════════════════════════════════════════════════════════════════════════════

SEC12 = """
      <h3>Hands-on: Practice Problem with Answer</h3>
      <pre>// Interview practice: explain what is wrong and fix it
@Component({
  template: `
    &lt;input (input)="onSearch($event)" /&gt;
    @for (item of getFilteredItems(); track item.id) {
      &lt;div&gt;{{ item.name }} — {{ formatPrice(item.price) }}&lt;/div&gt;
    }
  `
})
class SearchComponent {
  items: Item[] = [];
  term = '';

  onSearch(event: Event) {
    this.term = (event.target as HTMLInputElement).value;
  }

  getFilteredItems() {
    return this.items.filter(i =&gt; i.name.includes(this.term));
  }

  formatPrice(price: number) {
    return new Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR' }).format(price);
  }
}</pre>
      <p><strong>Correct interview answer:</strong></p>
      <ul>
        <li><strong>Problem 1:</strong> <code>getFilteredItems()</code> is a method call in the template — it re-executes on every CD cycle, filtering the array repeatedly.</li>
        <li><strong>Problem 2:</strong> <code>formatPrice()</code> creates a new <code>Intl.NumberFormat</code> on every call for every item on every CD cycle. For 100 items, that is hundreds of object allocations per cycle.</li>
        <li><strong>Problem 3:</strong> No debouncing on search — every keystroke triggers filtering.</li>
        <li><strong>Fix:</strong> Use signals for term and computed for filteredItems. Create a reusable pure pipe for price formatting. Add debounce if the list is large.</li>
      </ul>

      <h3>Interview Questions for Section 12</h3>
      <h4>Q: If an interviewer asks "tell me about your performance optimization experience," how should you structure your answer?</h4>
      <p><strong>A:</strong> Use this formula: (1) Describe the user symptom — "the checkout page took 6 seconds to load on mobile." (2) Name the metric — "LCP was 5.8 seconds." (3) Describe your diagnosis — "I traced it to a 400KB eager bundle including the chart library." (4) Describe the fix — "I moved the chart behind @defer and lazy-loaded the analytics route." (5) State the result — "LCP dropped to 2.1 seconds, verified in both lab and field metrics." (6) Mention the tradeoff — "chart loads 200ms later on first scroll, but the primary content is now interactive 3 seconds sooner."</p>
"""

# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 13: Study Roadmap
# ═══════════════════════════════════════════════════════════════════════════════

SEC13 = """
      <h3>Hands-on: Self-Assessment Code Exercises</h3>

      <h4>Level 1 exercise: Can you measure a page load?</h4>
      <pre>// Write this from memory to prove you understand Navigation Timing
const nav = performance.getEntriesByType('navigation')[0] as PerformanceNavigationTiming;
console.log('TTFB:', nav.responseStart - nav.requestStart, 'ms');
console.log('DOM ready:', nav.domContentLoadedEventEnd - nav.responseEnd, 'ms');
console.log('Full load:', nav.loadEventEnd - nav.navigationStart, 'ms');</pre>

      <h4>Level 2 exercise: Can you set up RUM?</h4>
      <pre>// Write a minimal web-vitals reporter from memory
import { onLCP, onINP, onCLS } from 'web-vitals';
const report = (m: { name: string; value: number }) =&gt;
  navigator.sendBeacon('/rum', JSON.stringify({ ...m, path: location.pathname }));
onLCP(report); onINP(report); onCLS(report);</pre>

      <h4>Level 3 exercise: Can you diagnose a performance trace?</h4>
      <pre>// Instrument a specific user interaction for profiling
performance.mark('search-filter-start');
this.filteredResults.set(
  this.allItems().filter(item =&gt; item.name.includes(this.searchTerm()))
);
performance.mark('search-filter-end');
performance.measure('search-filter-time', 'search-filter-start', 'search-filter-end');
// Open DevTools → Performance → record this interaction → inspect the measure</pre>

      <h3>Interview Questions for Section 13</h3>
      <h4>Q: How would you explain your performance learning journey in an interview?</h4>
      <p><strong>A:</strong> "I started by learning what LCP, INP, and CLS measure and why they matter. Then I learned to use Chrome DevTools to trace slow interactions. In Angular, I learned how change detection works and how OnPush and signals reduce unnecessary work. I practiced profiling real apps, setting budgets, and measuring before-and-after results. Now I approach any performance problem by identifying the bottleneck layer first, measuring it, fixing it, and verifying the improvement with data."</p>
"""

# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 17: E2E Architecture View
# ═══════════════════════════════════════════════════════════════════════════════

SEC17 = """
      <h3>Hands-on: Architecture Performance Diagnostic</h3>
      <pre>// E2E diagnostic: script to check all performance layers at once
async function fullStackDiagnostic() {
  const nav = performance.getEntriesByType('navigation')[0] as PerformanceNavigationTiming;
  const resources = performance.getEntriesByType('resource') as PerformanceResourceTiming[];

  console.group('Layer-by-layer diagnostic');

  // Network layer
  console.log('TTFB:', (nav.responseStart - nav.requestStart).toFixed(0), 'ms');
  console.log('Total resources:', resources.length);
  console.log('Total transfer:', resources.reduce((s, r) =&gt; s + r.transferSize, 0) / 1024, 'KB');

  // JavaScript layer
  const scripts = resources.filter(r =&gt; r.initiatorType === 'script');
  console.log('JS files:', scripts.length,
              'Total JS:', scripts.reduce((s, r) =&gt; s + r.transferSize, 0) / 1024, 'KB');

  // Render-blocking layer
  const blocking = resources.filter(r =&gt; (r as any).renderBlockingStatus === 'blocking');
  console.log('Render-blocking resources:', blocking.length, blocking.map(r =&gt; r.name));

  // DOM complexity
  console.log('DOM nodes:', document.querySelectorAll('*').length);
  console.log('DOM depth:', getMaxDOMDepth(document.body));

  console.groupEnd();
}

function getMaxDOMDepth(el: Element, depth = 0): number {
  let max = depth;
  for (const child of el.children) {
    max = Math.max(max, getMaxDOMDepth(child, depth + 1));
  }
  return max;
}</pre>
      <p><strong>Code theory:</strong> This script checks every layer from the E2E architecture table: network (TTFB, transfer sizes), JavaScript (script count and size), rendering (blocking resources, DOM complexity). Running this on any page gives you an instant performance overview. In an interview, describing this kind of systematic diagnostic shows you think in layers, not in isolated tricks.</p>

      <h3>Interview Questions for Section 17</h3>
      <h4>Q: Walk through the entire journey of a user clicking a link to seeing content on screen.</h4>
      <p><strong>A:</strong> (1) User clicks → browser fires navigation. (2) DNS resolution for the domain. (3) TCP connection + TLS handshake. (4) HTTP request sent to server/CDN. (5) Server processes request (or serves cached response). (6) HTML response begins streaming back. (7) Browser parses HTML, discovers CSS and JS resources. (8) CSS downloaded and parsed → CSSOM built. (9) JS downloaded, parsed, compiled, executed. (10) Angular bootstraps, creates component tree, runs initial change detection. (11) Style calculation → layout → paint → composite → pixels on screen. (12) Hydration (if SSR) attaches interactivity. Every step is a potential bottleneck.</p>

      <h4>Q: How do you explain to a non-technical stakeholder why performance matters?</h4>
      <p><strong>A:</strong> "Every second of delay reduces conversions by roughly 7%. Users who experience slow pages are 2-3x more likely to bounce. Google uses Core Web Vitals as a ranking signal. Performance is not a developer preference — it is directly tied to revenue, user satisfaction, and search visibility. The investment in performance work pays back in measurable business outcomes."</p>
"""

# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 18: Angular Internals
# ═══════════════════════════════════════════════════════════════════════════════

SEC18 = """
      <h3>Hands-on: Exploring Angular Internals in Code</h3>

      <h4>Example: Visualizing change detection frequency</h4>
      <pre>// Debug component that shows CD cycle count — useful for identifying waste
@Component({
  selector: 'app-cd-counter',
  template: `&lt;small style="color:red"&gt;CD: {{ cdCount }}&lt;/small&gt;`,
  changeDetection: ChangeDetectionStrategy.Default
})
export class CdCounterComponent {
  cdCount = 0;

  ngDoCheck() {
    this.cdCount++;
  }
}
// Drop this component into any page during debugging.
// If the count climbs rapidly while the UI is idle, you have zone pollution.</pre>
      <p><strong>Code theory:</strong> <code>ngDoCheck</code> runs on every change detection cycle for this component. By counting its invocations, you can see exactly how many CD cycles Angular runs. On a well-optimized idle page, this should barely increment. If it climbs by dozens per second, something is triggering unnecessary cycles — usually noisy async activity (timers, WebSockets, third-party scripts).</p>

      <h4>Example: OnPush with manual change detection</h4>
      <pre>@Component({
  selector: 'app-live-ticker',
  changeDetection: ChangeDetectionStrategy.OnPush,
  template: `&lt;span&gt;{{ price | currency }}&lt;/span&gt;`
})
export class LiveTickerComponent implements OnDestroy {
  price = 0;
  private ws = new WebSocket('wss://prices.example.com');
  private ngZone = inject(NgZone);
  private cdr = inject(ChangeDetectorRef);

  constructor() {
    // Receive price updates outside Angular zone — no CD pollution
    this.ngZone.runOutsideAngular(() =&gt; {
      this.ws.onmessage = (event) =&gt; {
        const newPrice = JSON.parse(event.data).price;
        if (Math.abs(newPrice - this.price) &gt; 0.01) {
          this.price = newPrice;
          this.cdr.markForCheck(); // Only trigger CD when price meaningfully changed
        }
      };
    });
  }

  ngOnDestroy() { this.ws.close(); }
}</pre>
      <p><strong>Code theory:</strong> This is an advanced pattern for high-frequency data streams. The WebSocket runs outside Angular's zone so rapid messages (possibly 100+/sec) do not trigger 100 CD cycles. We manually call <code>markForCheck()</code> only when the price change is meaningful (greater than 0.01). This gives precise control: the UI updates when needed, not when the zone says so.</p>

      <h3>Interview Questions for Section 18</h3>
      <h4>Q: Explain how OnPush change detection decides whether to check a component.</h4>
      <p><strong>A:</strong> OnPush checks the component only when: (1) an @Input reference changes (new object, not mutation), (2) an event fires inside the component or its children, (3) <code>markForCheck()</code> is called explicitly, or (4) an async pipe emits a new value. In all other cases, Angular skips the subtree entirely, saving the cost of evaluating all bindings in that branch.</p>

      <h4>Q: What happens when you call markForCheck() vs detectChanges()?</h4>
      <p><strong>A:</strong> <code>markForCheck()</code> marks the component and all ancestors as dirty, then waits for Angular's next scheduled CD cycle to check them — it is safe and batched. <code>detectChanges()</code> immediately runs CD on that component and its children synchronously — it can cause double-checking and should be used sparingly. Prefer <code>markForCheck()</code> in most cases.</p>

      <h4>Q: How do signals differ from Zone.js-based change detection?</h4>
      <p><strong>A:</strong> Zone.js-based CD is event-driven and broad — any async event triggers a tree-wide check. Signals are data-driven and precise — only computations that actually depend on a changed signal re-evaluate. Signals build a dependency graph at runtime. Zone.js patches async APIs. The result: signals can achieve the same UI consistency with far fewer unnecessary computations.</p>
"""

# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 19: Network Deep Dive
# ═══════════════════════════════════════════════════════════════════════════════

SEC19 = """
      <h3>Hands-on: Network Performance Code</h3>

      <h4>Example: Measuring API response times</h4>
      <pre>// Angular HTTP interceptor for performance tracking
@Injectable()
export class PerfInterceptor implements HttpInterceptor {
  intercept(req: HttpRequest&lt;any&gt;, next: HttpHandler): Observable&lt;HttpEvent&lt;any&gt;&gt; {
    const startTime = performance.now();
    return next.handle(req).pipe(
      tap({
        next: (event) =&gt; {
          if (event instanceof HttpResponse) {
            const duration = performance.now() - startTime;
            if (duration &gt; 1000) {
              console.warn(`Slow API: ${req.method} ${req.url} took ${duration.toFixed(0)}ms`);
            }
            // Send to RUM in production
            performance.measure(`api:${req.url}`, { start: startTime, duration });
          }
        }
      })
    );
  }
}</pre>
      <p><strong>Code theory:</strong> This interceptor wraps every HTTP call with performance measurement. Requests taking more than 1 second are flagged. In production, you would send these timings to your RUM pipeline. This helps you distinguish frontend slowness from backend slowness — if the API response takes 3 seconds, no amount of Angular optimization will make the page feel fast.</p>

      <h4>Example: Smart preloading strategy for Angular routes</h4>
      <pre>// Custom preloading strategy: only preload routes the user is likely to visit
@Injectable({ providedIn: 'root' })
export class SmartPreloadStrategy implements PreloadingStrategy {
  preload(route: Route, load: () =&gt; Observable&lt;any&gt;): Observable&lt;any&gt; {
    // Only preload routes marked with data.preload: true
    if (route.data?.['preload']) {
      return load();
    }
    return of(null); // Skip preloading for non-priority routes
  }
}

// In routes config:
{ path: 'dashboard', loadComponent: () =&gt; import('./dashboard/...'),
  data: { preload: true } },
{ path: 'admin', loadComponent: () =&gt; import('./admin/...') }
// admin is NOT preloaded — only downloaded when user navigates there</pre>
      <p><strong>Code theory:</strong> Angular's built-in <code>PreloadAllModules</code> downloads every lazy route immediately, wasting bandwidth on routes most users never visit. A selective strategy preloads only high-priority routes (dashboard, cart) while leaving admin and settings truly lazy. This saves bandwidth on mobile and reduces network contention during critical loading.</p>

      <h3>Interview Questions for Section 19</h3>
      <h4>Q: What is the difference between HTTP/2 and HTTP/3 for performance?</h4>
      <p><strong>A:</strong> HTTP/2 multiplexes requests over a single TCP connection, eliminating head-of-line blocking at the HTTP level. However, TCP-level head-of-line blocking remains — one lost packet delays all streams. HTTP/3 uses QUIC over UDP, fixing this: each stream is independent, so packet loss on one stream does not block others. HTTP/3 also has faster connection setup (0-RTT). For high-latency mobile networks, HTTP/3 can significantly improve resource delivery.</p>

      <h4>Q: Why can over-preloading hurt performance?</h4>
      <p><strong>A:</strong> Every preloaded resource competes for bandwidth with truly critical resources. If you preload 5 images and a font, the hero image that determines LCP may load slower because bandwidth is shared. Preload should be reserved for resources that are critical but discovered late by the browser. Overuse turns preload from a priority hint into a bandwidth drain.</p>
"""

# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 20: Rendering Deep Dive
# ═══════════════════════════════════════════════════════════════════════════════

SEC20 = """
      <h3>Hands-on: Rendering Performance Code</h3>

      <h4>Example: requestAnimationFrame for smooth animations</h4>
      <pre>// Smooth progress bar animation without layout thrashing
function animateProgress(element: HTMLElement, targetPercent: number) {
  let current = 0;

  function step() {
    current += (targetPercent - current) * 0.1;
    // Use transform instead of width — stays on compositor thread
    element.style.transform = `scaleX(${current / 100})`;
    element.style.transformOrigin = 'left';

    if (Math.abs(current - targetPercent) &gt; 0.5) {
      requestAnimationFrame(step);
    }
  }
  requestAnimationFrame(step);
}
// Using transform instead of width avoids triggering layout and paint on every frame</pre>
      <p><strong>Code theory:</strong> Animating <code>width</code> triggers layout → paint → composite on every frame. Animating <code>transform: scaleX()</code> only triggers composite, which is much cheaper. <code>requestAnimationFrame</code> synchronizes updates with the browser's refresh cycle (usually 60fps). This pattern keeps animations smooth even on slower devices.</p>

      <h4>Example: Intersection Observer for lazy rendering</h4>
      <pre>// Only render expensive widgets when they scroll into view
@Directive({ selector: '[appLazyRender]' })
export class LazyRenderDirective implements OnInit, OnDestroy {
  @Input() appLazyRender!: TemplateRef&lt;any&gt;;
  private observer?: IntersectionObserver;

  constructor(
    private viewContainer: ViewContainerRef,
    private element: ElementRef
  ) {}

  ngOnInit() {
    this.observer = new IntersectionObserver(([entry]) =&gt; {
      if (entry.isIntersecting) {
        this.viewContainer.createEmbeddedView(this.appLazyRender);
        this.observer?.disconnect(); // Only render once
      }
    }, { rootMargin: '200px' }); // Start 200px before viewport

    this.observer.observe(this.element.nativeElement);
  }

  ngOnDestroy() { this.observer?.disconnect(); }
}</pre>
      <p><strong>Code theory:</strong> Instead of rendering all widgets on page load (which creates DOM nodes and runs change detection for off-screen content), this directive defers rendering until the element is near the viewport. The 200px rootMargin ensures content appears before the user scrolls to it, avoiding visible loading delays. This is the manual equivalent of <code>@defer (on viewport)</code> for cases where you need custom behavior.</p>

      <h3>Interview Questions for Section 20</h3>
      <h4>Q: Why are transform and opacity preferred for animations?</h4>
      <p><strong>A:</strong> Transform and opacity changes can be handled entirely by the compositor thread, without triggering layout or paint on the main thread. Properties like width, height, top, left trigger layout recalculation (the browser must recompute geometry for the element and its neighbors). This means transform animations stay smooth at 60fps even when the main thread is busy, while layout-triggering animations will jank if the main thread is blocked.</p>

      <h4>Q: What is the difference between paint and composite in the rendering pipeline?</h4>
      <p><strong>A:</strong> Paint converts render tree nodes into pixel data for each layer. Composite assembles those pre-painted layers into the final screen image. Paint is expensive because it processes visual details (colors, shadows, text, images). Compositing is cheaper because it only moves, rotates, scales, or blends pre-existing layers. Elements on their own compositor layer (via <code>will-change</code> or <code>transform</code>) can be animated via composite alone, skipping paint entirely.</p>
"""

# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 21: Debugging Playbook
# ═══════════════════════════════════════════════════════════════════════════════

SEC21 = """
      <h3>Hands-on: Debugging Scripts</h3>

      <h4>Example: Automated INP diagnostics</h4>
      <pre>// Log every slow interaction with details
const interactionObserver = new PerformanceObserver((list) =&gt; {
  for (const entry of list.getEntries() as any[]) {
    if (entry.duration &gt; 200) {
      console.warn('Slow interaction:', {
        type: entry.name,
        duration: entry.duration.toFixed(0) + 'ms',
        target: entry.target?.tagName,
        startTime: entry.startTime.toFixed(0)
      });
    }
  }
});
interactionObserver.observe({ type: 'event', buffered: true, durationThreshold: 100 });</pre>
      <p><strong>Code theory:</strong> This observer monitors all user interactions (clicks, key presses, taps) and logs any that exceed 200ms — the "poor" INP threshold. It captures the target element and interaction type, so you know exactly which button or input field is problematic. In interviews, this kind of automated diagnostics shows you do not rely on manual testing alone.</p>

      <h4>Example: Quick waterfall diagnostic</h4>
      <pre>// Identify biggest resource bottlenecks
const resources = performance.getEntriesByType('resource') as PerformanceResourceTiming[];
const sorted = [...resources]
  .sort((a, b) =&gt; b.duration - a.duration)
  .slice(0, 10);

console.log('Top 10 slowest resources:');
sorted.forEach((r, i) =&gt;
  console.log(`${i + 1}. ${r.initiatorType.padEnd(8)} ${r.duration.toFixed(0).padStart(6)}ms  ${r.name.split('/').pop()}`)
);</pre>
      <p><strong>Code theory:</strong> Instead of manually scanning the Network panel, this script programmatically sorts resources by duration and surfaces the worst offenders. This is useful in production (sent to RUM) or in CI pipelines. Long-duration resources often point to CDN issues, uncompressed assets, or oversized dependencies.</p>

      <h3>Interview Questions for Section 21</h3>
      <h4>Q: A user reports "the app feels slow after using it for 30 minutes." How do you investigate?</h4>
      <p><strong>A:</strong> This is a memory leak symptom. Steps: (1) Open the page and navigate through the main flows. (2) Take a heap snapshot. (3) Repeat the same navigation 5 times. (4) Take another heap snapshot. (5) Compare the two snapshots — look for growing object counts, detached DOM trees, and retained listeners. (6) Check the retainer path to find which code is holding references. Common causes: uncleaned subscriptions, setInterval/setTimeout without cleanup, event listeners added but never removed, growing caches in services.</p>

      <h4>Q: If LCP is good but INP is poor after SSR, what is the most likely cause?</h4>
      <p><strong>A:</strong> SSR delivered fast HTML (good LCP), but hydration is heavy — the client has to download, parse, and execute JavaScript to make the page interactive. If the hydration bundle is large or many components hydrate immediately, the main thread is blocked during that process, making interactions unresponsive. Fix: reduce the client bundle, use incremental hydration, or defer non-critical widget hydration.</p>
"""

# ═══════════════════════════════════════════════════════════════════════════════
# SECTIONS 22-28: Add IQ blocks (these already have rich content)
# ═══════════════════════════════════════════════════════════════════════════════

SEC22 = """
      <h3>Hands-on: Building a Scenario Answer</h3>
      <pre>// Scenario: "Dashboard loads too slowly"
// Step 1: Measure
performance.mark('dashboard-start');
await bootstrapDashboard();
performance.mark('dashboard-end');
performance.measure('dashboard-load', 'dashboard-start', 'dashboard-end');
// Result: 4200ms

// Step 2: Diagnose — check what loads eagerly
const jsFiles = performance.getEntriesByType('resource')
  .filter((r: any) =&gt; r.initiatorType === 'script');
console.log('JS loaded:', jsFiles.length, 'files,',
  jsFiles.reduce((s: number, r: any) =&gt; s + r.transferSize, 0) / 1024, 'KB');
// Found: chart-lib.js (180KB) loaded eagerly

// Step 3: Fix — move chart behind @defer
// @defer (on viewport; prefetch on idle) { &lt;app-chart /&gt; }

// Step 4: Verify
// Re-measure: dashboard-load dropped from 4200ms to 1800ms
// LCP: 2.1s → 1.3s, INP: 380ms → 120ms</pre>
      <p><strong>Code theory:</strong> This demonstrates the complete performance improvement lifecycle in code — measure the problem, diagnose the cause with data, apply a targeted fix, and verify the improvement with the same measurement. In interviews, walking through this process with actual numbers is far more convincing than listing random optimization tips.</p>

      <h3>Interview Questions for Section 22</h3>
      <h4>Q: How would you optimize an Angular app where scrolling through a data table with 10,000 rows causes jank?</h4>
      <p><strong>A:</strong> (1) First, measure: record a DevTools performance trace during scroll and check for long tasks. (2) The most likely cause is 10,000 DOM nodes being rendered and updated. (3) Primary fix: use CDK virtual scroll to render only visible rows (~20-30). (4) Secondary fix: add <code>trackBy</code> to prevent unnecessary DOM recreation. (5) If rows have complex components, simplify the row template or defer secondary details. (6) Verify: DOM node count should drop from 10,000+ to ~50, and scroll jank should disappear in the performance trace.</p>
"""

SEC23 = """
      <h3>Hands-on: Quick-Fire Q&A Practice Code</h3>
      <pre>// Q: Show code for the simplest possible OnPush+signal component
@Component({
  selector: 'app-counter',
  changeDetection: ChangeDetectionStrategy.OnPush,
  template: `
    &lt;button (click)="count.set(count() + 1)"&gt;Count: {{ count() }}&lt;/button&gt;
    &lt;p&gt;Double: {{ double() }}&lt;/p&gt;
  `
})
export class CounterComponent {
  count = signal(0);
  double = computed(() =&gt; this.count() * 2);
  // Theory: count is the source signal. double is derived. OnPush +
  // signals mean Angular only checks this component when the signal
  // actually changes. No Zone.js noise, no broad CD cycles.
}</pre>

      <pre>// Q: Show code for cancelling stale HTTP requests
searchResults$ = this.searchInput.valueChanges.pipe(
  debounceTime(300),            // Wait for typing to pause
  distinctUntilChanged(),       // Skip if term hasn't changed
  switchMap(term =&gt;             // Cancel previous request
    term.length &gt; 2
      ? this.http.get&lt;Result[]&gt;('/api/search?q=' + encodeURIComponent(term))
      : of([])
  )
);
// Theory: switchMap unsubscribes from the previous inner observable
// when a new one starts. This means if the user types "ang" → "angu",
// the request for "ang" is cancelled before the response arrives.</pre>

      <h3>Interview Questions for Section 23</h3>
      <h4>Q: What exactly happens when Zone.js is removed from an Angular app?</h4>
      <p><strong>A:</strong> Without Zone.js, Angular no longer auto-detects async events. Change detection does not run automatically after timers, HTTP responses, or promises resolve. The developer must explicitly trigger updates via signals, <code>markForCheck()</code>, or manual change detection. The benefit: zero unnecessary CD cycles from third-party noise. The cost: more explicit state management required. Signals make this practical because they automatically notify Angular about data changes.</p>
"""

SEC24 = """
      <h3>Hands-on: Decision Table as Algorithm</h3>
      <pre>// Decision function: which optimization strategy to apply?
function recommendOptimization(problem: {
  type: 'slow-load' | 'slow-interaction' | 'memory-growth' | 'layout-shift';
  context: 'angular' | 'vanilla' | 'both';
}): string[] {
  const recommendations: string[] = [];

  switch (problem.type) {
    case 'slow-load':
      recommendations.push('Analyze bundle size and lazy-load secondary features');
      recommendations.push('Check LCP element and resource priority');
      recommendations.push('Audit render-blocking resources');
      if (problem.context === 'angular') {
        recommendations.push('Use @defer for below-fold widgets');
        recommendations.push('Check if SSR would help this page type');
      }
      break;
    case 'slow-interaction':
      recommendations.push('Profile main-thread trace around the interaction');
      recommendations.push('Check for long tasks blocking the event handler');
      if (problem.context === 'angular') {
        recommendations.push('Check change detection frequency with Angular DevTools');
        recommendations.push('Look for template methods and zone pollution');
      }
      break;
    case 'memory-growth':
      recommendations.push('Take heap snapshots before and after repeated navigation');
      if (problem.context === 'angular') {
        recommendations.push('Check for unsubscribed observables and listeners');
      }
      break;
    case 'layout-shift':
      recommendations.push('Reserve dimensions for images and embeds');
      recommendations.push('Check font loading strategy');
      recommendations.push('Inspect late DOM insertion above the fold');
      break;
  }
  return recommendations;
}</pre>
      <p><strong>Code theory:</strong> This function encodes the decision tables from this guide into executable logic. In a real team, similar logic could drive an internal performance audit tool or PR review automation. The structure shows that performance diagnosis is systematic, not random — the problem type determines the investigation path.</p>

      <h3>Interview Questions for Section 24</h3>
      <h4>Q: When would you choose SSR over CSR for an Angular app?</h4>
      <p><strong>A:</strong> SSR when: public-facing content pages need fast initial render and SEO (marketing, product pages, blog). CSR when: internal admin tools where SEO does not matter and operational simplicity is preferred. Hybrid when: apps with both public content and logged-in interactive sections. The tradeoff: SSR adds server infrastructure complexity and hydration cost, but delivers faster perceived loading for content-first pages.</p>

      <h4>Q: When would debouncing hurt user experience?</h4>
      <p><strong>A:</strong> When users expect immediate feedback: toggle switches, checkboxes, button clicks, navigation. Debouncing a button click by 300ms makes the UI feel broken. Debouncing is appropriate for continuous input like search typing, resize events, or scroll tracking — where the user is still in the middle of an action and only the final value matters.</p>
"""

SEC25 = """
      <h3>Interview Questions for Section 25</h3>
      <h4>Q: Walk through your mental checklist when preparing for a performance interview.</h4>
      <p><strong>A:</strong> (1) Can I explain Core Web Vitals in user terms, not just definitions? (2) Can I draw the browser rendering pipeline? (3) Can I diagnose whether a problem is network, JS, rendering, or Angular-specific? (4) Can I explain change detection, OnPush, signals with code? (5) Can I walk through a real optimization with before-after metrics? (6) Can I explain lazy loading, @defer, SSR tradeoffs? (7) Can I discuss memory leaks with heap snapshot reasoning? (8) Can I set up RUM and budgets? If yes to all, I am ready.</p>
"""

SEC26 = """
      <h3>Hands-on: Practice Exercise Templates</h3>
      <pre>// Exercise 1: Intentionally slow component — can you fix all issues?
@Component({
  template: `
    &lt;input (keyup)="onSearch($event)" /&gt;
    &lt;div *ngFor="let item of filterItems()"&gt;
      {{ item.name }} - {{ computeDiscount(item) }}%
    &lt;/div&gt;
  `
})
class SlowSearchComponent {
  items: Product[] = HUGE_LIST; // 5000 items
  searchTerm = '';

  onSearch(e: KeyboardEvent) { this.searchTerm = (e.target as HTMLInputElement).value; }
  filterItems() { return this.items.filter(i =&gt; i.name.includes(this.searchTerm)); }
  computeDiscount(item: Product) { return Math.round(item.originalPrice / item.salePrice * 100 - 100); }
}

// Issues to fix:
// 1. filterItems() is a template method — re-runs every CD cycle
// 2. computeDiscount() is a template method — runs for every item every CD cycle
// 3. No debouncing — every keystroke triggers filtering
// 4. No trackBy — list re-creates DOM on every filter
// 5. No virtual scroll — 5000 DOM nodes
// 6. Default change detection — every event checks this component

// Challenge: rewrite with signals, computed, OnPush, trackBy, debounce, virtual scroll</pre>

      <h3>Interview Questions for Section 26</h3>
      <h4>Q: How would you fix the SlowSearchComponent above? Walk through each issue.</h4>
      <p><strong>A:</strong> (1) Replace <code>filterItems()</code> with a <code>computed</code> signal that depends on <code>searchTerm</code> signal. (2) Replace <code>computeDiscount()</code> with a pure pipe or precompute discounts when data loads. (3) Debounce the input using RxJS <code>debounceTime(300)</code> or a signal-based debounce. (4) Add <code>track item.id</code> to the <code>@for</code> loop. (5) Use CDK virtual scroll for 5000 items. (6) Switch to <code>ChangeDetectionStrategy.OnPush</code>. This would reduce DOM nodes from 5000 to ~30, eliminate template method re-execution, and debounce search-triggered reflows.</p>
"""

SEC27 = """
      <h3>Hands-on: Senior-Level Proof Patterns</h3>
      <pre>// Pattern: A/B performance measurement for proving optimization impact
class PerformanceExperiment {
  private baseline: number[] = [];
  private optimized: number[] = [];

  async runBaseline(action: () =&gt; Promise&lt;void&gt;, iterations = 10) {
    for (let i = 0; i &lt; iterations; i++) {
      const start = performance.now();
      await action();
      this.baseline.push(performance.now() - start);
    }
  }

  async runOptimized(action: () =&gt; Promise&lt;void&gt;, iterations = 10) {
    for (let i = 0; i &lt; iterations; i++) {
      const start = performance.now();
      await action();
      this.optimized.push(performance.now() - start);
    }
  }

  report() {
    const avg = (arr: number[]) =&gt; arr.reduce((a, b) =&gt; a + b, 0) / arr.length;
    const p95 = (arr: number[]) =&gt; arr.sort((a, b) =&gt; a - b)[Math.floor(arr.length * 0.95)];

    console.table({
      'Baseline avg': avg(this.baseline).toFixed(1) + 'ms',
      'Optimized avg': avg(this.optimized).toFixed(1) + 'ms',
      'Improvement': ((1 - avg(this.optimized) / avg(this.baseline)) * 100).toFixed(1) + '%',
      'Baseline p95': p95(this.baseline).toFixed(1) + 'ms',
      'Optimized p95': p95(this.optimized).toFixed(1) + 'ms'
    });
  }
}</pre>
      <p><strong>Code theory:</strong> Senior interviews want to hear numbers, not feelings. This measurement pattern lets you quantify improvement by running the same action multiple times before and after optimization. Using median and p95 instead of single measurements removes noise and provides confidence that the improvement is real. This structure directly translates to how you should describe optimization results in interviews: baseline → change → measured improvement.</p>

      <h3>Interview Questions for Section 27</h3>
      <h4>Q: How do you prove to a stakeholder that a performance optimization was worth the engineering investment?</h4>
      <p><strong>A:</strong> (1) Show before-after metrics with the same measurement conditions. (2) Segment by user impact — "p75 LCP improved from 4.2s to 1.8s, affecting 75% of users." (3) Tie to business metrics if available — "bounce rate on product pages dropped 15% after the optimization." (4) Show the regression risk was controlled — "we added a budget to prevent future regressions." (5) Be honest about tradeoffs — "the page now loads a chart 200ms later on demand, but primary content is interactive 2.4 seconds sooner."</p>
"""

SEC28 = """
      <h3>Hands-on: Production Monitoring Code</h3>
      <pre>// Complete production RUM setup with error boundary
import { onLCP, onINP, onCLS, onFCP, onTTFB } from 'web-vitals';

interface RumEvent {
  metric: string;
  value: number;
  rating: string;
  route: string;
  release: string;
  device: 'mobile' | 'tablet' | 'desktop';
  connection: string;
  timestamp: number;
}

const RELEASE = document.querySelector('meta[name="release"]')?.getAttribute('content') || 'unknown';

function getConnection(): string {
  const conn = (navigator as any).connection;
  return conn?.effectiveType || 'unknown';
}

function getDevice(): 'mobile' | 'tablet' | 'desktop' {
  if (window.innerWidth &lt; 768) return 'mobile';
  if (window.innerWidth &lt; 1024) return 'tablet';
  return 'desktop';
}

function sendRum(event: RumEvent) {
  // Use sendBeacon for reliability during page unload
  navigator.sendBeacon('/api/rum', JSON.stringify(event));
}

function initRum() {
  const handler = (metric: { name: string; value: number; rating: string }) =&gt; {
    sendRum({
      metric: metric.name,
      value: Math.round(metric.value),
      rating: metric.rating,
      route: location.pathname,
      release: RELEASE,
      device: getDevice(),
      connection: getConnection(),
      timestamp: Date.now()
    });
  };

  onLCP(handler);
  onINP(handler);
  onCLS(handler);
  onFCP(handler);
  onTTFB(handler);
}

// Sample at 10% in production to control volume
if (Math.random() &lt; 0.1) {
  initRum();
}</pre>
      <p><strong>Code theory:</strong> This is a production-grade RUM implementation. Key decisions: (1) <code>sendBeacon</code> for reliable delivery. (2) Release version for regression detection after deployments. (3) Device and connection type for user segmentation. (4) 10% sampling to control telemetry volume while maintaining statistical significance. (5) Route-level granularity so you can compare /dashboard vs /checkout performance separately. In an interview, walking through each design decision shows production-level thinking.</p>

      <h3>Interview Questions for Section 28</h3>
      <h4>Q: How do you set up performance alerting for a production Angular app?</h4>
      <p><strong>A:</strong> (1) Collect RUM data segmented by route and release version. (2) Compute rolling p75 for LCP, INP, and CLS per critical route. (3) Set alert thresholds: e.g., if p75 INP for /checkout exceeds 200ms or increases by more than 20% compared to previous release. (4) Alert channels: team Slack for warnings, PagerDuty for critical regressions on revenue-impacting routes. (5) Include release version in alerts so you can immediately correlate the regression to a specific deployment.</p>

      <h4>Q: What is the difference between shallow size and retained size in heap snapshots?</h4>
      <p><strong>A:</strong> Shallow size is the memory directly occupied by an object's own fields. Retained size is the total memory that would be freed if the object were garbage collected — including all objects it exclusively references. A 100-byte service with a reference to a 10MB DOM tree has 100 bytes shallow but 10MB retained. Retained size reveals the true leak impact. When debugging leaks, sort by retained size to find the biggest problems first.</p>
"""

# ═══════════════════════════════════════════════════════════════════════════════
# Apply all insertions
# ═══════════════════════════════════════════════════════════════════════════════

html = insert_before_section_end(html, "<h2>1. Performance Mindset</h2>", SEC1)
html = insert_before_section_end(html, "<h2>2. What Every Frontend Developer Should Know</h2>", SEC2)
html = insert_before_section_end(html, "<h2>3. Important Metrics From Basic to Advanced</h2>", SEC3)
html = insert_before_section_end(html, "<h2>4. General Frontend Performance Optimization Techniques</h2>", SEC4)
html = insert_before_section_end(html, "<h2>5. Angular Performance Optimization From Basic to Advanced</h2>", SEC5)
html = insert_before_section_end(html, "<h2>8. Performance Tooling You Should Know</h2>", SEC8)
html = insert_before_section_end(html, "<h2>9. Common Angular Performance Mistakes</h2>", SEC9)
html = insert_before_section_end(html, "<h2>10. Common General Frontend Performance Mistakes</h2>", SEC10)
html = insert_before_section_end(html, "<h2>11. End-to-End Performance Checklist</h2>", SEC11)
html = insert_before_section_end(html, "<h2>12. Interview and Career Readiness</h2>", SEC12)
html = insert_before_section_end(html, "<h2>13. Study Roadmap", SEC13)
html = insert_before_section_end(html, "<h2>17. End-to-End Performance Architecture View</h2>", SEC17)
html = insert_before_section_end(html, "<h2>18. Angular Internals You Should Understand</h2>", SEC18)
html = insert_before_section_end(html, "<h2>19. Network, Caching, and Delivery Deep Dive</h2>", SEC19)
html = insert_before_section_end(html, "<h2>20. Rendering and Main Thread Deep Dive</h2>", SEC20)
html = insert_before_section_end(html, "<h2>21. End-to-End Debugging Playbook</h2>", SEC21)
html = insert_before_section_end(html, "<h2>22. Real-World Scenario Questions", SEC22)
html = insert_before_section_end(html, "<h2>23. Tough Interview Questions", SEC23)
html = insert_before_section_end(html, "<h2>24. Advanced Decision Tables", SEC24)
html = insert_before_section_end(html, "<h2>25. End-to-End Revision Checklist", SEC25)
html = insert_before_section_end(html, "<h2>26. Practice Exercises", SEC26)
html = insert_before_section_end(html, "<h2>27. What Senior Interviewers", SEC27)
html = insert_before_section_end(html, "<h2>28. Production and Measurement Depth</h2>", SEC28)

with open(OUTPUT, "w", encoding="utf-8") as f:
    f.write(html)

print(f"Done. File size: {len(html)} characters, ~{len(html.splitlines())} lines")
