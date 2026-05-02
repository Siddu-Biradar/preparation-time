SECTIONS = r"""

<!-- ═══════════════════════════════════════════════════════════════════
     DOM & BROWSER APIs — 7 SUB-SECTIONS
     ═══════════════════════════════════════════════════════════════════ -->

<h2 id="dom-manipulation" class="section-break">13. DOM Manipulation</h2>
<p class="small"><strong>Checklist:</strong> getElementById · querySelector/All · createElement · appendChild · removeChild · insertBefore · insertAdjacentElement · cloneNode · innerHTML vs textContent vs innerText · classList · setAttribute/getAttribute · dataset · DocumentFragment</p>

<h3>13.1 Selecting Elements</h3>
<pre>// By ID — returns single element or null
const header = document.getElementById('header');

// CSS selector — returns first match or null
const card = document.querySelector('.product-card');
const activeTab = document.querySelector('[data-active="true"]');

// CSS selector — returns NodeList (static snapshot, NOT live)
const allCards = document.querySelectorAll('.product-card');
allCards.forEach(card => card.classList.add('loaded'));

// LIVE collections — update automatically when DOM changes
const divs = document.getElementsByTagName('div'); // HTMLCollection (live)
const items = document.getElementsByClassName('item'); // HTMLCollection (live)</pre>

<h3>13.2 Creating &amp; Modifying Elements</h3>
<pre>// Create and configure an element
const card = document.createElement('div');
card.className = 'product-card';
card.id = 'card-42';
card.dataset.productId = '42';        // sets data-product-id="42"
card.setAttribute('role', 'article');
card.textContent = 'Product Name';     // SAFE — no HTML injection
// card.innerHTML = '&lt;h3&gt;Title&lt;/h3&gt;'; // CAREFUL — can inject scripts!

// Append to DOM
document.getElementById('container').appendChild(card);

// Insert at specific positions
parent.insertBefore(newNode, referenceNode); // before reference
element.insertAdjacentElement('beforebegin', newEl); // before element
element.insertAdjacentElement('afterbegin', newEl);  // first child
element.insertAdjacentElement('beforeend', newEl);   // last child
element.insertAdjacentElement('afterend', newEl);    // after element

// Modern: append, prepend, before, after, replaceWith
parent.append(child1, child2, 'text'); // can append multiple + text
parent.prepend(child);                  // add as first child
node.before(newNode);                   // insert before
node.after(newNode);                    // insert after
node.replaceWith(newNode);              // replace
node.remove();                          // remove from DOM</pre>

<h3>13.3 innerHTML vs textContent vs innerText</h3>
<table>
<thead><tr><th>Property</th><th>Behavior</th><th>XSS Safe?</th><th>Performance</th></tr></thead>
<tbody>
<tr><td><code>textContent</code></td><td>Gets/sets raw text, ignores HTML</td><td>✅ Yes</td><td>Fast</td></tr>
<tr><td><code>innerText</code></td><td>Gets visible text only (respects CSS), triggers reflow</td><td>✅ Yes</td><td>Slow</td></tr>
<tr><td><code>innerHTML</code></td><td>Gets/sets HTML markup, parses as HTML</td><td>❌ Dangerous!</td><td>Medium</td></tr>
</tbody>
</table>

<h3>13.4 classList API</h3>
<pre>const el = document.querySelector('.btn');
el.classList.add('loading', 'disabled');    // add multiple
el.classList.remove('loading');              // remove
el.classList.toggle('active');               // add if absent, remove if present
el.classList.toggle('visible', condition);   // force add/remove based on boolean
el.classList.contains('active');             // check → true/false
el.classList.replace('old-class', 'new-class'); // swap</pre>

<h3>13.5 DocumentFragment — Batch DOM Updates</h3>
<pre>// BAD: 1000 individual DOM insertions → 1000 reflows
for (let i = 0; i &lt; 1000; i++) {
  const li = document.createElement('li');
  li.textContent = `Item ${i}`;
  list.appendChild(li); // triggers reflow each time!
}

// GOOD: DocumentFragment → single reflow
const fragment = document.createDocumentFragment();
for (let i = 0; i &lt; 1000; i++) {
  const li = document.createElement('li');
  li.textContent = `Item ${i}`;
  fragment.appendChild(li); // fragment is in memory, no reflow
}
list.appendChild(fragment); // ONE reflow for all 1000 items</pre>

<div class="interview-q">
<h4>🎯 Interview Questions — DOM Manipulation</h4>
<p><strong>Q: Why should you never use innerHTML with user input?</strong></p>
<p><strong>A:</strong> It creates an XSS vulnerability. If <code>userInput</code> contains <code>&lt;script&gt;alert('hacked')&lt;/script&gt;</code>, setting <code>element.innerHTML = userInput</code> executes the script. Always use <code>textContent</code> for user-provided data.</p>

<p><strong>Q: Why use DocumentFragment?</strong></p>
<p><strong>A:</strong> DOM operations trigger layout recalculations (reflows). Inserting 1000 elements one-by-one causes 1000 reflows. A DocumentFragment exists in memory — you build the entire tree in the fragment, then insert it once = 1 reflow.</p>
</div>

<!-- ─── Section 14: DOM Traversal ──────────────────────────────────── -->
<h2 id="dom-traversal" class="section-break">14. DOM Traversal</h2>
<p class="small"><strong>Checklist:</strong> parentNode/parentElement · childNodes/children · firstChild/lastChild · firstElementChild/lastElementChild · nextSibling/previousSibling · nextElementSibling/previousElementSibling · closest()</p>

<pre>// Node vs Element properties
// Node includes text nodes, comments, etc.
// Element only includes element nodes

const parent = document.querySelector('.list');
parent.childNodes;         // NodeList — includes text nodes, comments
parent.children;           // HTMLCollection — only element children
parent.firstChild;         // could be a text node (whitespace!)
parent.firstElementChild;  // first actual element

// Sibling navigation
const item = document.querySelector('.item');
item.nextSibling;              // might be text node (whitespace)
item.nextElementSibling;       // next element
item.previousElementSibling;   // previous element

// closest() — searches UP the DOM tree
const btn = document.querySelector('.delete-btn');
const card = btn.closest('.card');        // finds nearest ancestor with .card
const form = btn.closest('form');         // finds nearest ancestor form
const nothing = btn.closest('.nonexistent'); // null

// Walking the DOM tree
function walkDOM(node, callback) {
  callback(node);
  node = node.firstElementChild;
  while (node) {
    walkDOM(node, callback);
    node = node.nextElementSibling;
  }
}
walkDOM(document.body, el => console.log(el.tagName));</pre>

<div class="interview-q">
<h4>🎯 Interview Questions — DOM Traversal</h4>
<p><strong>Q: What's the difference between <code>childNodes</code> and <code>children</code>?</strong></p>
<p><strong>A:</strong> <code>childNodes</code> returns ALL child nodes including text nodes and comments (NodeList). <code>children</code> returns only element children (HTMLCollection). In practice, use <code>children</code> to avoid dealing with whitespace text nodes.</p>
</div>

<!-- ─── Section 15: Events ─────────────────────────────────────────── -->
<h2 id="dom-events" class="section-break">15. Events</h2>
<p class="small"><strong>Checklist:</strong> addEventListener/removeEventListener · event object (target, currentTarget, type) · bubbling · capturing · delegation · stopPropagation · preventDefault · keyboard/mouse/touch events · passive listeners · CustomEvent</p>

<h3>15.1 Event Flow: Capture → Target → Bubble</h3>
<pre>// Events flow in three phases:
// 1. CAPTURING: window → document → html → body → ... → target (top-down)
// 2. TARGET: event fires on the target element
// 3. BUBBLING: target → ... → body → html → document → window (bottom-up)

// By default, listeners fire during BUBBLING phase
element.addEventListener('click', handler);

// Listen during CAPTURE phase  
element.addEventListener('click', handler, { capture: true });
// or shorthand: element.addEventListener('click', handler, true);</pre>

<h3>15.2 target vs currentTarget</h3>
<pre>// target: the element that TRIGGERED the event (what was clicked)
// currentTarget: the element the LISTENER is attached to (where you're listening)

document.querySelector('.list').addEventListener('click', (e) => {
  console.log(e.target);        // the actual &lt;li&gt; or &lt;span&gt; clicked
  console.log(e.currentTarget); // always the .list element
});</pre>

<h3>15.3 Event Delegation</h3>
<pre>// Instead of 100 listeners on 100 items, use ONE on the parent
document.getElementById('todo-list').addEventListener('click', (e) => {
  // Check if a delete button was clicked  
  const deleteBtn = e.target.closest('[data-action="delete"]');
  if (deleteBtn) {
    const todoId = deleteBtn.closest('[data-todo-id]').dataset.todoId;
    deleteTodo(todoId);
    return;
  }
  
  // Check if a toggle was clicked
  const checkbox = e.target.closest('[data-action="toggle"]');
  if (checkbox) {
    toggleTodo(checkbox.closest('[data-todo-id]').dataset.todoId);
  }
});
// Benefits: works for dynamically added items, single listener, less memory</pre>

<h3>15.4 stopPropagation &amp; preventDefault</h3>
<pre>// preventDefault — stops the browser's default action
form.addEventListener('submit', (e) => {
  e.preventDefault(); // stops form from navigating
  // handle submission via fetch instead
});

link.addEventListener('click', (e) => {
  e.preventDefault(); // stops navigation
  router.navigate(link.href);
});

// stopPropagation — stops event from continuing to parent
child.addEventListener('click', (e) => {
  e.stopPropagation(); // parent's click handler won't fire
});

// stopImmediatePropagation — stops OTHER handlers on same element too
element.addEventListener('click', handler1); // this fires
element.addEventListener('click', (e) => {
  e.stopImmediatePropagation();
  // handler after this on same element won't fire
});</pre>

<h3>15.5 Custom Events</h3>
<pre>// Create and dispatch custom events
const cartEvent = new CustomEvent('cart:updated', {
  bubbles: true,     // event bubbles up through DOM
  composed: true,    // crosses shadow DOM boundaries
  detail: { items: 5, total: 2499 }
});
element.dispatchEvent(cartEvent);

// Listen for custom events
document.addEventListener('cart:updated', (e) => {
  updateCartBadge(e.detail.items);
});</pre>

<h3>15.6 Passive Event Listeners</h3>
<pre>// Passive listeners tell the browser "I won't call preventDefault()"
// This allows the browser to scroll smoothly without waiting for JS
document.addEventListener('touchstart', handleTouch, { passive: true });
document.addEventListener('wheel', handleWheel, { passive: true });

// Cleanup with AbortController
const controller = new AbortController();
element.addEventListener('click', handler, { signal: controller.signal });
element.addEventListener('keydown', handler2, { signal: controller.signal });
// Remove ALL listeners at once:
controller.abort();</pre>

<div class="interview-q">
<h4>🎯 Interview Questions — Events</h4>
<p><strong>Q: Explain event delegation. Why is it useful?</strong></p>
<p><strong>A:</strong> Event delegation attaches a single listener to a parent element instead of individual listeners on each child. It works because events bubble up. Benefits: (1) Works for dynamically added elements, (2) Less memory (1 listener vs N), (3) Less setup code. Use <code>e.target.closest(selector)</code> to identify which child was interacted with.</p>

<p><strong>Q: What's the difference between <code>stopPropagation</code> and <code>preventDefault</code>?</strong></p>
<p><strong>A:</strong> <code>preventDefault()</code> stops the browser's default behavior (navigation, form submission) but the event still propagates. <code>stopPropagation()</code> stops the event from bubbling to parent elements but the default action still occurs. They solve different problems.</p>
</div>

<!-- ─── Section 16: Browser Storage ────────────────────────────────── -->
<h2 id="dom-storage" class="section-break">16. Browser Storage</h2>
<p class="small"><strong>Checklist:</strong> localStorage · sessionStorage · storage events · cookies (document.cookie, attributes: expires, max-age, domain, path, secure, SameSite) · IndexedDB basics</p>

<table>
<thead><tr><th>Storage</th><th>Capacity</th><th>Lifetime</th><th>Scope</th><th>Sent with requests?</th></tr></thead>
<tbody>
<tr><td><code>localStorage</code></td><td>~5-10 MB</td><td>Until manually cleared</td><td>Same origin (protocol+host+port)</td><td>No</td></tr>
<tr><td><code>sessionStorage</code></td><td>~5-10 MB</td><td>Until tab closes</td><td>Same origin + same tab</td><td>No</td></tr>
<tr><td>Cookies</td><td>~4 KB per cookie</td><td>Expires or session</td><td>Origin + path</td><td>Yes — every HTTP request!</td></tr>
<tr><td>IndexedDB</td><td>50 MB+ (unlimited with permission)</td><td>Until cleared</td><td>Same origin</td><td>No</td></tr>
</tbody>
</table>

<pre>// localStorage — persists across browser restarts
localStorage.setItem('theme', JSON.stringify({ mode: 'dark', fontSize: 16 }));
const theme = JSON.parse(localStorage.getItem('theme'));
localStorage.removeItem('theme');
localStorage.clear(); // remove ALL items

// Cross-tab sync via storage event
window.addEventListener('storage', (e) => {
  if (e.key === 'user-session') {
    if (e.newValue === null) logoutCurrentTab(); // logged out in another tab
  }
});

// Cookies — set from JavaScript (NOT for HttpOnly cookies)
document.cookie = 'name=Sid; max-age=86400; path=/; SameSite=Lax; Secure';
// Reading cookies (messy — it's one big string)
const cookies = Object.fromEntries(
  document.cookie.split('; ').map(c => c.split('='))
);

// IndexedDB — async, structured data, large capacity
const request = indexedDB.open('MyDatabase', 1);
request.onupgradeneeded = (e) => {
  const db = e.target.result;
  const store = db.createObjectStore('products', { keyPath: 'id' });
  store.createIndex('category', 'category', { unique: false });
};</pre>

<div class="interview-q">
<h4>🎯 Interview Questions — Browser Storage</h4>
<p><strong>Q: Where should you store JWT tokens?</strong></p>
<p><strong>A:</strong> <strong>HttpOnly cookies</strong> are most secure — not accessible from JS (immune to XSS). localStorage is convenient but exposed to XSS attacks. Never store sensitive tokens in sessionStorage or non-HttpOnly cookies if XSS is a concern. Use <code>Secure; SameSite=Strict; HttpOnly</code> cookie attributes.</p>
</div>

<!-- ─── Section 17: Browser APIs ───────────────────────────────────── -->
<h2 id="dom-browser-apis" class="section-break">17. Browser APIs</h2>
<p class="small"><strong>Checklist:</strong> Fetch API · XMLHttpRequest · Geolocation · History API · Web Workers · Service Workers · IntersectionObserver · MutationObserver · ResizeObserver · Performance API · requestIdleCallback · Page Visibility · Clipboard · Notification · Drag &amp; Drop</p>

<h3>17.1 IntersectionObserver — Lazy Loading / Infinite Scroll</h3>
<pre>const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      const img = entry.target;
      img.src = img.dataset.src;    // load real image
      img.classList.add('loaded');
      observer.unobserve(img);       // stop watching
    }
  });
}, {
  root: null,            // viewport
  rootMargin: '200px',   // start loading 200px before visible
  threshold: 0.1         // trigger when 10% visible
});
document.querySelectorAll('img[data-src]').forEach(img => observer.observe(img));</pre>

<h3>17.2 MutationObserver — Watch DOM Changes</h3>
<pre>const observer = new MutationObserver((mutations) => {
  mutations.forEach(mutation => {
    if (mutation.type === 'childList') {
      console.log('Children changed:', mutation.addedNodes, mutation.removedNodes);
    }
    if (mutation.type === 'attributes') {
      console.log(`Attribute '${mutation.attributeName}' changed`);
    }
  });
});
observer.observe(targetElement, {
  childList: true,    // watch for added/removed children
  attributes: true,   // watch for attribute changes
  subtree: true       // watch entire subtree
});</pre>

<h3>17.3 ResizeObserver</h3>
<pre>const resizeObserver = new ResizeObserver(entries => {
  for (const entry of entries) {
    const { width, height } = entry.contentRect;
    entry.target.classList.toggle('compact', width < 400);
    entry.target.classList.toggle('wide', width >= 800);
  }
});
resizeObserver.observe(document.querySelector('.dashboard-widget'));</pre>

<h3>17.4 Page Visibility &amp; Clipboard</h3>
<pre>// Pause expensive work when tab is hidden
document.addEventListener('visibilitychange', () => {
  if (document.hidden) { pausePolling(); pauseAnimations(); }
  else { resumePolling(); }
});

// Clipboard API (async, requires HTTPS)
async function copyToClipboard(text) {
  try {
    await navigator.clipboard.writeText(text);
    showToast('Copied!');
  } catch (err) {
    // Fallback for older browsers
    const textarea = document.createElement('textarea');
    textarea.value = text;
    document.body.appendChild(textarea);
    textarea.select();
    document.execCommand('copy');
    textarea.remove();
  }
}

// Performance API — custom timings
performance.mark('api-start');
await fetch('/api/data');
performance.mark('api-end');
performance.measure('API Call', 'api-start', 'api-end');
const duration = performance.getEntriesByName('API Call')[0].duration;</pre>

<h3>17.5 History API</h3>
<pre>// SPA routing fundamentals
history.pushState({ page: 'products' }, '', '/products');    // add to history
history.replaceState({ page: 'home' }, '', '/');              // replace current
window.addEventListener('popstate', (e) => {
  console.log('Navigation:', e.state); // user clicked back/forward
  renderPage(e.state?.page);
});</pre>

<!-- ─── Section 18: Window & Document ──────────────────────────────── -->
<h2 id="dom-window-document" class="section-break">18. Window &amp; Document</h2>
<p class="small"><strong>Checklist:</strong> window.location · window.history · window.scrollTo/scrollBy · document.documentElement · document.readyState · DOMContentLoaded vs load · getBoundingClientRect · viewport dimensions</p>

<pre>// window.location — URL manipulation
window.location.href;       // full URL
window.location.pathname;   // '/products/42'
window.location.search;     // '?sort=price&amp;order=asc'
window.location.hash;       // '#reviews'
window.location.origin;     // 'https://example.com'
// Redirect:
window.location.href = '/new-page';   // adds to history
window.location.replace('/new-page'); // replaces in history (no back)

// Viewport dimensions
window.innerWidth;   // viewport width (includes scrollbar)
window.innerHeight;  // viewport height
document.documentElement.clientWidth;  // viewport width (excludes scrollbar)

// Scroll
window.scrollTo({ top: 0, behavior: 'smooth' });
window.scrollBy({ top: 100, behavior: 'smooth' });
element.scrollIntoView({ behavior: 'smooth', block: 'center' });

// DOMContentLoaded vs load
document.addEventListener('DOMContentLoaded', () => {
  // DOM is ready — HTML parsed, but images/CSS may still be loading
  initializeApp();
});
window.addEventListener('load', () => {
  // EVERYTHING is loaded — images, stylesheets, iframes, etc.
  hideLoadingScreen();
});
// document.readyState: 'loading' → 'interactive' (DOMContentLoaded) → 'complete' (load)

// getBoundingClientRect — element position relative to viewport
const rect = element.getBoundingClientRect();
// rect.top, rect.left, rect.right, rect.bottom, rect.width, rect.height
const isInViewport = rect.top >= 0 && rect.bottom <= window.innerHeight;</pre>

<!-- ─── Section 19: Forms ──────────────────────────────────────────── -->
<h2 id="dom-forms" class="section-break">19. Forms</h2>
<p class="small"><strong>Checklist:</strong> Form validation · Constraint Validation API · FormData API · input types &amp; attributes · form events (submit, reset, invalid)</p>

<pre>// FormData API — read form values without manual DOM queries
const form = document.querySelector('#checkout-form');
form.addEventListener('submit', async (e) => {
  e.preventDefault();
  const formData = new FormData(form);
  
  // Convert to object
  const data = Object.fromEntries(formData.entries());
  // { name: 'Sid', email: 'sid@test.com', ... }
  
  // Send as JSON
  await fetch('/api/checkout', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
  });
  
  // Or send as multipart (for file uploads)
  await fetch('/api/upload', { method: 'POST', body: formData });
});

// Constraint Validation API
const input = document.querySelector('#email');
input.validity.valid;         // is the input valid?
input.validity.typeMismatch;  // wrong type (e.g., invalid email)
input.validity.valueMissing;  // required field is empty
input.validity.tooShort;      // shorter than minlength
input.validity.patternMismatch; // doesn't match pattern attribute

// Custom validation message
input.addEventListener('invalid', () => {
  if (input.validity.typeMismatch) {
    input.setCustomValidity('Please enter a valid email address');
  }
});
input.addEventListener('input', () => input.setCustomValidity(''));

// Programmatic validation
if (!form.checkValidity()) {
  form.reportValidity(); // shows browser validation UI
}</pre>


<!-- ═══════════════════════════════════════════════════════════════════
     HTML — 5 SUB-SECTIONS
     ═══════════════════════════════════════════════════════════════════ -->

<h2 id="html-semantic" class="section-break">20. Semantic HTML</h2>
<p class="small"><strong>Checklist:</strong> header · nav · main · article · section · aside · footer · figure · figcaption · time · mark · progress · details · summary · benefits for SEO &amp; accessibility</p>

<pre>&lt;!-- Semantic page structure --&gt;
&lt;header&gt;
  &lt;nav aria-label="Main navigation"&gt;
    &lt;a href="#main" class="skip-link"&gt;Skip to content&lt;/a&gt;
    &lt;ul role="list"&gt;
      &lt;li&gt;&lt;a href="/"&gt;Home&lt;/a&gt;&lt;/li&gt;
      &lt;li&gt;&lt;a href="/products" aria-current="page"&gt;Products&lt;/a&gt;&lt;/li&gt;
    &lt;/ul&gt;
  &lt;/nav&gt;
&lt;/header&gt;

&lt;main id="main"&gt;
  &lt;article&gt;
    &lt;h1&gt;Product Review: MacBook Pro 2024&lt;/h1&gt;
    &lt;p&gt;Published &lt;time datetime="2024-03-15"&gt;March 15, 2024&lt;/time&gt;&lt;/p&gt;
    
    &lt;section&gt;
      &lt;h2&gt;Performance&lt;/h2&gt;
      &lt;p&gt;The M3 chip delivers &lt;mark&gt;40% faster&lt;/mark&gt; performance...&lt;/p&gt;
      &lt;figure&gt;
        &lt;img src="benchmark.png" alt="Benchmark scores: M3 vs M2 comparison"&gt;
        &lt;figcaption&gt;Figure 1: Benchmark results&lt;/figcaption&gt;
      &lt;/figure&gt;
    &lt;/section&gt;
    
    &lt;details&gt;
      &lt;summary&gt;Full Specifications&lt;/summary&gt;
      &lt;table&gt;...&lt;/table&gt;
    &lt;/details&gt;
  &lt;/article&gt;
  
  &lt;aside aria-label="Related articles"&gt;
    &lt;h2&gt;Related Reviews&lt;/h2&gt;
    &lt;ul&gt;...&lt;/ul&gt;
  &lt;/aside&gt;
&lt;/main&gt;

&lt;footer&gt;
  &lt;p&gt;&amp;copy; 2024 TechReview. All rights reserved.&lt;/p&gt;
&lt;/footer&gt;</pre>

<div class="callout">
<strong>Why Semantic HTML matters:</strong>  (1) <strong>Accessibility:</strong> Screen readers use landmarks (nav, main, article) for navigation. (2) <strong>SEO:</strong> Search engines understand content structure better. (3) <strong>Maintainability:</strong> Code is self-documenting. (4) <strong>Default behaviors:</strong> <code>&lt;button&gt;</code> is keyboard-accessible by default, <code>&lt;div&gt;</code> is not.
</div>

<!-- ─── HTML5 Features ──────────────────────────────────────────────── -->
<h2 id="html5-features" class="section-break">21. HTML5 Features</h2>
<p class="small"><strong>Checklist:</strong> Data attributes · contenteditable · draggable · hidden · input types · required/pattern/min/max · placeholder · autocomplete · output element</p>

<pre>&lt;!-- Data attributes — store custom data on elements --&gt;
&lt;div class="product-card"
     data-product-id="42"
     data-category="electronics"
     data-price="1299.99"&gt;
  ...
&lt;/div&gt;

&lt;script&gt;
const card = document.querySelector('.product-card');
card.dataset.productId;  // '42' (camelCase conversion)
card.dataset.price;      // '1299.99' (always a string)
card.dataset.inStock = 'true'; // sets data-in-stock="true"
&lt;/script&gt;

&lt;!-- HTML5 input types — built-in validation &amp; UI --&gt;
&lt;input type="email" required placeholder="user@example.com"&gt;
&lt;input type="tel" pattern="[0-9]{10}" title="10-digit phone number"&gt;
&lt;input type="url"&gt;
&lt;input type="date" min="2024-01-01" max="2025-12-31"&gt;
&lt;input type="number" min="0" max="100" step="5"&gt;
&lt;input type="range" min="0" max="100" value="50"&gt;
&lt;input type="color" value="#0f6b5f"&gt;
&lt;input type="search" list="suggestions"&gt;
&lt;datalist id="suggestions"&gt;
  &lt;option value="Angular"&gt;
  &lt;option value="React"&gt;
  &lt;option value="Vue"&gt;
&lt;/datalist&gt;

&lt;!-- contenteditable — inline editing --&gt;
&lt;div contenteditable="true"&gt;Click to edit this text&lt;/div&gt;

&lt;!-- output — for calculation results --&gt;
&lt;form oninput="result.value = a.valueAsNumber + b.valueAsNumber"&gt;
  &lt;input id="a" type="number"&gt; + &lt;input id="b" type="number"&gt;
  = &lt;output name="result" for="a b"&gt;0&lt;/output&gt;
&lt;/form&gt;</pre>

<!-- ─── Metadata & SEO ──────────────────────────────────────────────── -->
<h2 id="html-metadata-seo" class="section-break">22. Metadata &amp; SEO</h2>
<p class="small"><strong>Checklist:</strong> meta tags (description, viewport, keywords) · Open Graph · Twitter Cards · canonical URLs · structured data (JSON-LD, Schema.org)</p>

<pre>&lt;head&gt;
  &lt;!-- Essential meta tags --&gt;
  &lt;meta charset="UTF-8"&gt;
  &lt;meta name="viewport" content="width=device-width, initial-scale=1.0"&gt;
  &lt;meta name="description" content="Buy premium running shoes online. Free shipping on orders over ₹999."&gt;
  &lt;title&gt;Running Shoes | SportStore&lt;/title&gt;
  
  &lt;!-- Open Graph (Facebook, LinkedIn) --&gt;
  &lt;meta property="og:title" content="Premium Running Shoes"&gt;
  &lt;meta property="og:description" content="Top-rated running shoes for every terrain"&gt;
  &lt;meta property="og:image" content="https://example.com/shoes.jpg"&gt;
  &lt;meta property="og:url" content="https://example.com/running-shoes"&gt;
  &lt;meta property="og:type" content="product"&gt;
  
  &lt;!-- Twitter Cards --&gt;
  &lt;meta name="twitter:card" content="summary_large_image"&gt;
  &lt;meta name="twitter:title" content="Premium Running Shoes"&gt;
  
  &lt;!-- Canonical URL — prevent duplicate content --&gt;
  &lt;link rel="canonical" href="https://example.com/running-shoes"&gt;
  
  &lt;!-- Structured Data (JSON-LD) — rich search results --&gt;
  &lt;script type="application/ld+json"&gt;
  {
    "@context": "https://schema.org",
    "@type": "Product",
    "name": "Nike Air Max 2024",
    "image": "https://example.com/shoes.jpg",
    "description": "Premium running shoes",
    "offers": {
      "@type": "Offer",
      "price": "8999",
      "priceCurrency": "INR",
      "availability": "https://schema.org/InStock"
    },
    "aggregateRating": {
      "@type": "AggregateRating",
      "ratingValue": "4.5",
      "reviewCount": "128"
    }
  }
  &lt;/script&gt;
&lt;/head&gt;</pre>

<!-- ─── Media Elements ──────────────────────────────────────────────── -->
<h2 id="html-media" class="section-break">23. Media Elements</h2>
<p class="small"><strong>Checklist:</strong> video · audio · source · track (captions) · picture · srcset &amp; sizes</p>

<pre>&lt;!-- Responsive images with picture + srcset --&gt;
&lt;picture&gt;
  &lt;source media="(min-width: 1200px)" srcset="hero-1200.avif" type="image/avif"&gt;
  &lt;source media="(min-width: 1200px)" srcset="hero-1200.webp" type="image/webp"&gt;
  &lt;source media="(min-width: 600px)" srcset="hero-600.webp" type="image/webp"&gt;
  &lt;img src="hero-400.jpg" alt="Hero banner showing spring collection"
       loading="lazy" decoding="async" width="1200" height="600"&gt;
&lt;/picture&gt;

&lt;!-- Video with multiple sources + captions --&gt;
&lt;video controls preload="metadata" poster="thumb.jpg"
       width="640" height="360"&gt;
  &lt;source src="video.mp4" type="video/mp4"&gt;
  &lt;source src="video.webm" type="video/webm"&gt;
  &lt;track kind="subtitles" src="captions-en.vtt" srclang="en" label="English" default&gt;
  &lt;track kind="subtitles" src="captions-hi.vtt" srclang="hi" label="Hindi"&gt;
  Your browser does not support the video element.
&lt;/video&gt;

&lt;!-- srcset + sizes — let browser choose optimal image --&gt;
&lt;img srcset="photo-400.jpg 400w, photo-800.jpg 800w, photo-1200.jpg 1200w"
     sizes="(max-width: 600px) 400px, (max-width: 1000px) 800px, 1200px"
     src="photo-800.jpg"
     alt="Product photo"
     loading="lazy"&gt;</pre>

<!-- ─── Accessibility (HTML) ────────────────────────────────────────── -->
<h2 id="html-accessibility" class="section-break">24. HTML Accessibility</h2>
<p class="small"><strong>Checklist:</strong> ARIA roles · ARIA attributes (aria-label, labelledby, describedby) · aria-live regions · aria-hidden · landmark roles · alt text · label associations · tabindex · skip links</p>

<pre>&lt;!-- Skip link — lets keyboard users jump to main content --&gt;
&lt;a href="#main-content" class="skip-link"&gt;Skip to main content&lt;/a&gt;
&lt;style&gt;
.skip-link {
  position: absolute; left: -9999px;
  &amp;:focus { left: 10px; top: 10px; z-index: 10000; }
}
&lt;/style&gt;

&lt;!-- Accessible form --&gt;
&lt;form&gt;
  &lt;fieldset&gt;
    &lt;legend&gt;Shipping Address&lt;/legend&gt;
    
    &lt;label for="street"&gt;Street Address &lt;span aria-hidden="true"&gt;*&lt;/span&gt;&lt;/label&gt;
    &lt;input id="street" type="text" required aria-required="true"
           aria-describedby="street-help"&gt;
    &lt;small id="street-help"&gt;Include apartment/suite number&lt;/small&gt;
    
    &lt;label for="city"&gt;City&lt;/label&gt;
    &lt;input id="city" type="text" required aria-required="true"
           aria-invalid="false"&gt;
  &lt;/fieldset&gt;
&lt;/form&gt;

&lt;!-- aria-live — announces dynamic content to screen readers --&gt;
&lt;div aria-live="polite" aria-atomic="true" id="status"&gt;
  &lt;!-- When JS updates this content, screen reader announces it --&gt;
&lt;/div&gt;
&lt;script&gt;
document.getElementById('status').textContent = '3 results found';
// Screen reader: "3 results found"
&lt;/script&gt;

&lt;!-- Accessible custom button (prefer native &lt;button&gt;) --&gt;
&lt;div role="button" tabindex="0"
     aria-pressed="false"
     onkeydown="if(event.key==='Enter'||event.key===' ')this.click()"&gt;
  Toggle Dark Mode
&lt;/div&gt;

&lt;!-- aria-hidden — hide decorative elements from screen readers --&gt;
&lt;button&gt;
  &lt;span aria-hidden="true"&gt;🗑️&lt;/span&gt;
  &lt;span class="sr-only"&gt;Delete item&lt;/span&gt;
&lt;/button&gt;

&lt;!-- tabindex values --&gt;
&lt;!-- tabindex="0": adds to natural tab order --&gt;
&lt;!-- tabindex="-1": focusable via JS only, removed from tab order --&gt;
&lt;!-- tabindex="1+": AVOID — creates confusing tab order --&gt;</pre>

<div class="interview-q">
<h4>🎯 Interview Questions — HTML &amp; Accessibility</h4>
<p><strong>Q: What is the difference between <code>aria-label</code>, <code>aria-labelledby</code>, and <code>aria-describedby</code>?</strong></p>
<p><strong>A:</strong> <code>aria-label</code> provides an invisible label string directly. <code>aria-labelledby</code> references another element's ID whose text content becomes the label (for visible labels). <code>aria-describedby</code> adds supplementary description (help text, error messages) — read after the label. Priority: <code>aria-labelledby</code> > <code>aria-label</code> > native <code>&lt;label&gt;</code>.</p>

<p><strong>Q: Why is <code>&lt;div onclick&gt;</code> bad for accessibility?</strong></p>
<p><strong>A:</strong> It's not keyboard-accessible (no focus, no Enter/Space handling), has no ARIA role, and screen readers don't announce it as interactive. Use <code>&lt;button&gt;</code> instead — it gets focus, keyboard support, and semantics for free.</p>
</div>
"""
