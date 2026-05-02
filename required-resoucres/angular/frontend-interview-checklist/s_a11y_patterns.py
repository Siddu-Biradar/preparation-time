SECTIONS = r"""

<!-- ═══════════════════════════════════════════════════════════════════
     ACCESSIBILITY (A11Y) — 6 SUB-SECTIONS
     ═══════════════════════════════════════════════════════════════════ -->

<h2 id="a11y-wcag" class="section-break">74. WCAG Guidelines</h2>
<p class="small"><strong>Checklist:</strong> WCAG 2.1 / 2.2 levels (A, AA, AAA) · POUR principles · conformance requirements · common violations</p>

<h3>Four Principles — POUR</h3>
<table>
<thead><tr><th>Principle</th><th>Meaning</th><th>Key Guidelines</th></tr></thead>
<tbody>
<tr><td><strong>Perceivable</strong></td><td>Users can perceive content</td><td>Alt text, captions, color contrast, resizable text</td></tr>
<tr><td><strong>Operable</strong></td><td>UI can be operated</td><td>Keyboard accessible, enough time, no seizures, navigable</td></tr>
<tr><td><strong>Understandable</strong></td><td>Content is understandable</td><td>Readable, predictable, input assistance</td></tr>
<tr><td><strong>Robust</strong></td><td>Works with assistive tech</td><td>Valid HTML, ARIA used correctly, status messages</td></tr>
</tbody>
</table>

<pre>// Common WCAG violations and fixes
// 1. Missing alt text
&lt;img src="hero.jpg"&gt;                          // ❌ No alt
&lt;img src="hero.jpg" alt=""&gt;                    // ✅ Decorative (intentionally empty)
&lt;img src="chart.png" alt="Q3 revenue: $2.4M"&gt; // ✅ Informative

// 2. Insufficient color contrast
// AA requires: 4.5:1 for normal text, 3:1 for large text (18px+ or 14px+ bold)
// AAA requires: 7:1 for normal text, 4.5:1 for large text
// Use: chrome DevTools → Inspect element → Color picker shows contrast ratio

// 3. Missing form labels
&lt;input type="email"&gt;                          // ❌ No label
&lt;label for="email"&gt;Email&lt;/label&gt;
&lt;input id="email" type="email"&gt;                // ✅ Explicit label
&lt;label&gt;Email &lt;input type="email"&gt;&lt;/label&gt;     // ✅ Implicit label

// 4. Missing page language
&lt;html&gt;                                         // ❌
&lt;html lang="en"&gt;                               // ✅

// 5. Missing skip navigation
&lt;a href="#main-content" class="skip-link"&gt;Skip to main content&lt;/a&gt;
&lt;main id="main-content"&gt;...&lt;/main&gt;</pre>

<h2 id="a11y-keyboard" class="section-break">75. Keyboard Navigation</h2>
<p class="small"><strong>Checklist:</strong> Focus management · tab order · focus trapping (modals) · skip links · visible focus indicators · roving tabindex</p>

<pre>// Focus management for SPA route changes
router.events.subscribe(event => {
  if (event instanceof NavigationEnd) {
    const heading = document.querySelector('h1');
    heading?.focus();  // move focus to new page heading
  }
});

// Focus trap for modals
class FocusTrap {
  private focusableElements: HTMLElement[];
  private firstFocusable: HTMLElement;
  private lastFocusable: HTMLElement;

  constructor(private container: HTMLElement) {
    this.focusableElements = Array.from(
      container.querySelectorAll(
        'a[href], button:not([disabled]), input:not([disabled]), ' +
        'select:not([disabled]), textarea:not([disabled]), [tabindex]:not([tabindex="-1"])'
      )
    );
    this.firstFocusable = this.focusableElements[0];
    this.lastFocusable = this.focusableElements[this.focusableElements.length - 1];
    this.handleKeyDown = this.handleKeyDown.bind(this);
    container.addEventListener('keydown', this.handleKeyDown);
    this.firstFocusable.focus();
  }

  private handleKeyDown(e: KeyboardEvent) {
    if (e.key !== 'Tab') return;
    if (e.shiftKey &amp;&amp; document.activeElement === this.firstFocusable) {
      e.preventDefault();
      this.lastFocusable.focus();
    } else if (!e.shiftKey &amp;&amp; document.activeElement === this.lastFocusable) {
      e.preventDefault();
      this.firstFocusable.focus();
    }
  }

  destroy() { this.container.removeEventListener('keydown', this.handleKeyDown); }
}

// Roving tabindex — arrow key navigation for widget groups (tabs, toolbars)
&lt;div role="tablist"&gt;
  &lt;button role="tab" tabindex="0" aria-selected="true"&gt;Tab 1&lt;/button&gt;
  &lt;button role="tab" tabindex="-1" aria-selected="false"&gt;Tab 2&lt;/button&gt;
  &lt;button role="tab" tabindex="-1" aria-selected="false"&gt;Tab 3&lt;/button&gt;
&lt;/div&gt;
// Only active tab has tabindex="0", others have tabindex="-1"
// Arrow keys move focus between tabs, Tab key moves out of the group</pre>

<h2 id="a11y-screen-readers" class="section-break">76. Screen Readers</h2>
<p class="small"><strong>Checklist:</strong> How screen readers parse DOM · landmark regions · heading hierarchy · hidden content · live regions</p>

<pre>// Landmark regions — screen readers can jump between these
&lt;header&gt;...&lt;/header&gt;              // banner
&lt;nav&gt;...&lt;/nav&gt;                    // navigation
&lt;main&gt;...&lt;/main&gt;                  // main content
&lt;aside&gt;...&lt;/aside&gt;               // complementary
&lt;footer&gt;...&lt;/footer&gt;             // contentinfo

// Heading hierarchy — must be sequential, no skipping
&lt;h1&gt;Page Title&lt;/h1&gt;              // one per page
  &lt;h2&gt;Section&lt;/h2&gt;
    &lt;h3&gt;Subsection&lt;/h3&gt;
  &lt;h2&gt;Another Section&lt;/h2&gt;       // ✅ back to h2 is okay
    &lt;h4&gt;Subsection&lt;/h4&gt;          // ❌ skipped h3!

// Visually hidden but accessible to screen readers
.sr-only {
  position: absolute;
  width: 1px; height: 1px;
  padding: 0; margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border: 0;
}
// display:none and visibility:hidden hide from screen readers too — don't use for a11y text

// Hiding from screen readers (decorative only)
&lt;span aria-hidden="true"&gt;🔒&lt;/span&gt;
&lt;img src="decoration.svg" alt="" role="presentation"&gt;</pre>

<h2 id="a11y-aria" class="section-break">77. ARIA Attributes</h2>
<p class="small"><strong>Checklist:</strong> Roles · states · properties · live regions · aria-label vs aria-labelledby · aria-describedby · aria-expanded · aria-hidden</p>

<pre>// Rule #1: Don't use ARIA if native HTML works!
&lt;div role="button" tabindex="0"&gt;Click&lt;/div&gt;  // ❌ Fake button
&lt;button&gt;Click&lt;/button&gt;                        // ✅ Real button

// ARIA labels
&lt;button aria-label="Close dialog"&gt;✕&lt;/button&gt;
&lt;input aria-labelledby="name-label" /&gt;
&lt;h2 id="name-label"&gt;Full Name&lt;/h2&gt;

// ARIA states
&lt;button aria-expanded="false" aria-controls="menu"&gt;Menu&lt;/button&gt;
&lt;ul id="menu" hidden&gt;...&lt;/ul&gt;

// Live regions — announce dynamic content changes
&lt;div aria-live="polite"&gt;                // announce when convenient
  {{ statusMessage }}
&lt;/div&gt;
&lt;div aria-live="assertive"&gt;             // announce immediately
  {{ errorMessage }}
&lt;/div&gt;
&lt;div role="alert"&gt;                      // equivalent to aria-live="assertive"
  Form submission failed!
&lt;/div&gt;
&lt;div role="status"&gt;                     // equivalent to aria-live="polite"
  3 results found
&lt;/div&gt;

// ARIA for custom widgets
&lt;div role="progressbar" aria-valuenow="60" aria-valuemin="0" aria-valuemax="100"
     aria-label="Upload progress"&gt;
  60%
&lt;/div&gt;

// Common ARIA mistakes
// ❌ aria-label on a &lt;div&gt; (non-interactive elements)
// ❌ role="button" without keyboard support
// ❌ aria-hidden="true" on focusable elements
// ❌ Redundant: &lt;button role="button"&gt; (button already has that role)</pre>

<h2 id="a11y-color" class="section-break">78. Color &amp; Contrast</h2>
<p class="small"><strong>Checklist:</strong> Contrast ratios (AA/AAA) · color-blind friendly design · not relying on color alone · dark mode accessibility</p>

<pre>// Contrast requirements (WCAG 2.1)
// AA  → 4.5:1  normal text,  3:1  large text,  3:1  UI components
// AAA → 7:1    normal text,  4.5:1 large text

// Never use color alone to convey information
// ❌ Red text for errors (color-blind users can't see it)
&lt;span style="color: red"&gt;Error&lt;/span&gt;

// ✅ Color + icon + text
&lt;span class="error"&gt;
  &lt;svg aria-hidden="true"&gt;...&lt;/svg&gt;  &lt;!-- error icon --&gt;
  Error: Email is required
&lt;/span&gt;

// ✅ Color + pattern for charts
// Use different patterns (dots, stripes, crosshatch) in addition to colors

// Dark mode — maintain contrast
:root {
  --text-primary: #1a1a1a;        // dark text on light bg
  --bg-primary: #ffffff;
}
@media (prefers-color-scheme: dark) {
  :root {
    --text-primary: #e0e0e0;      // light text on dark bg
    --bg-primary: #121212;
  }
}

// Test tools: Chrome DevTools → Rendering → Emulate vision deficiencies</pre>

<h2 id="a11y-forms" class="section-break">79. Form Accessibility</h2>
<p class="small"><strong>Checklist:</strong> Labels · error messages · field descriptions · required fields · autocomplete · input types</p>

<pre>// Accessible form pattern
&lt;form novalidate (ngSubmit)="onSubmit()"&gt;
  &lt;div class="form-group"&gt;
    &lt;label for="email"&gt;
      Email address
      &lt;span class="required" aria-hidden="true"&gt;*&lt;/span&gt;
    &lt;/label&gt;
    &lt;input
      id="email"
      type="email"
      autocomplete="email"
      required
      aria-required="true"
      [attr.aria-invalid]="emailInvalid"
      [attr.aria-describedby]="emailInvalid ? 'email-error' : 'email-hint'"
    &gt;
    &lt;span id="email-hint" class="hint"&gt;We'll never share your email.&lt;/span&gt;
    &lt;span id="email-error" class="error" *ngIf="emailInvalid" role="alert"&gt;
      Please enter a valid email address.
    &lt;/span&gt;
  &lt;/div&gt;

  &lt;fieldset&gt;
    &lt;legend&gt;Notification preferences&lt;/legend&gt;
    &lt;label&gt;&lt;input type="checkbox" name="email-notif"&gt; Email&lt;/label&gt;
    &lt;label&gt;&lt;input type="checkbox" name="sms-notif"&gt; SMS&lt;/label&gt;
  &lt;/fieldset&gt;

  &lt;button type="submit"&gt;Submit&lt;/button&gt;
&lt;/form&gt;

// Key patterns:
// 1. Every input has a &lt;label&gt; with matching for/id
// 2. Required fields use aria-required + visual indicator
// 3. Errors use role="alert" or aria-live to announce
// 4. aria-describedby links input to hint/error text
// 5. aria-invalid indicates validation state
// 6. Use &lt;fieldset&gt; + &lt;legend&gt; for related inputs
// 7. autocomplete attribute helps autofill</pre>

<div class="interview-q">
<h4>🎯 Interview Questions — Accessibility</h4>
<p><strong>Q: How do you make a custom dropdown accessible?</strong></p>
<p><strong>A:</strong> Use ARIA: <code>role="listbox"</code> on container, <code>role="option"</code> on items. Add <code>aria-expanded</code>, <code>aria-activedescendant</code> (points to focused option), <code>aria-labelledby</code>. Support keyboard: Enter/Space to open, Arrow keys to navigate, Escape to close. Focus trap while open. Announce selection changes with <code>aria-live</code>. Better approach: use native <code>&lt;select&gt;</code> when possible.</p>

<p><strong>Q: What is the difference between aria-label, aria-labelledby, and aria-describedby?</strong></p>
<p><strong>A:</strong> <code>aria-label</code>: inline text label (no visible element). <code>aria-labelledby</code>: points to element ID whose text IS the label (overrides aria-label + native label). <code>aria-describedby</code>: points to element providing EXTRA description (read after the label). Priority: aria-labelledby &gt; aria-label &gt; &lt;label&gt; &gt; title.</p>
</div>

<!-- ═══════════════════════════════════════════════════════════════════
     DESIGN PATTERNS — 4 SUB-SECTIONS
     ═══════════════════════════════════════════════════════════════════ -->

<h2 id="patterns-creational" class="section-break">80. Creational Patterns</h2>
<p class="small"><strong>Checklist:</strong> Singleton · Factory · Abstract Factory · Builder · Prototype</p>

<pre>// SINGLETON — one instance for the entire application
class Logger {
  private static instance: Logger;
  private logs: string[] = [];

  private constructor() {} // prevent external instantiation

  static getInstance(): Logger {
    if (!Logger.instance) {
      Logger.instance = new Logger();
    }
    return Logger.instance;
  }

  log(message: string) {
    this.logs.push(`[${new Date().toISOString()}] ${message}`);
    console.log(message);
  }
}

// Angular services are singletons by default (providedIn: 'root')
@Injectable({ providedIn: 'root' })
export class LoggerService {
  log(msg: string) { console.log(msg); }
}

// FACTORY — create objects without specifying exact class
interface Notification { send(to: string, message: string): void; }

class EmailNotification implements Notification {
  send(to: string, message: string) { /* send email */ }
}
class SmsNotification implements Notification {
  send(to: string, message: string) { /* send SMS */ }
}
class PushNotification implements Notification {
  send(to: string, message: string) { /* send push */ }
}

function createNotification(type: 'email' | 'sms' | 'push'): Notification {
  const map = {
    email: EmailNotification,
    sms: SmsNotification,
    push: PushNotification
  };
  return new map[type]();
}

// BUILDER — construct complex objects step by step
class QueryBuilder {
  private table = '';
  private conditions: string[] = [];
  private orderByField = '';
  private limitCount = 0;

  from(table: string)      { this.table = table; return this; }
  where(condition: string)  { this.conditions.push(condition); return this; }
  orderBy(field: string)    { this.orderByField = field; return this; }
  limit(n: number)          { this.limitCount = n; return this; }

  build(): string {
    let query = `SELECT * FROM ${this.table}`;
    if (this.conditions.length) query += ` WHERE ${this.conditions.join(' AND ')}`;
    if (this.orderByField) query += ` ORDER BY ${this.orderByField}`;
    if (this.limitCount) query += ` LIMIT ${this.limitCount}`;
    return query;
  }
}

const query = new QueryBuilder()
  .from('users')
  .where('age > 18')
  .where('active = true')
  .orderBy('name')
  .limit(10)
  .build();</pre>

<h2 id="patterns-structural" class="section-break">81. Structural Patterns</h2>
<p class="small"><strong>Checklist:</strong> Adapter · Decorator · Facade · Proxy · Composite</p>

<pre>// ADAPTER — make incompatible interfaces work together
// Old analytics library
class OldAnalytics {
  track(eventName: string, data: object) { /* old API */ }
}
// New analytics library
class NewAnalytics {
  send(event: { name: string; properties: object; timestamp: number }) { /* new API */ }
}
// Adapter
class AnalyticsAdapter {
  constructor(private newAnalytics: NewAnalytics) {}
  track(eventName: string, data: object) {
    this.newAnalytics.send({
      name: eventName,
      properties: data,
      timestamp: Date.now()
    });
  }
}

// DECORATOR — add behavior without modifying original
function withLogging&lt;T extends (...args: any[]) => any&gt;(fn: T): T {
  return function(...args: any[]) {
    console.log(`Calling ${fn.name} with`, args);
    const result = fn.apply(this, args);
    console.log(`Result:`, result);
    return result;
  } as T;
}
const add = (a: number, b: number) => a + b;
const loggedAdd = withLogging(add);
loggedAdd(2, 3); // logs: Calling add with [2, 3] → Result: 5

// FACADE — simple interface for complex subsystem
class OrderFacade {
  constructor(
    private inventory: InventoryService,
    private payment: PaymentService,
    private shipping: ShippingService,
    private notification: NotificationService
  ) {}

  async placeOrder(order: Order): Promise&lt;OrderResult&gt; {
    await this.inventory.reserve(order.items);
    const payment = await this.payment.charge(order.total, order.paymentMethod);
    const tracking = await this.shipping.createLabel(order.address, order.items);
    await this.notification.sendConfirmation(order.email, tracking);
    return { orderId: order.id, tracking, payment };
  }
}

// PROXY — control access to an object
class CachedApiProxy {
  private cache = new Map&lt;string, { data: any; expires: number }&gt;();

  constructor(private api: ApiService, private ttl = 60000) {}

  async get(url: string) {
    const cached = this.cache.get(url);
    if (cached &amp;&amp; cached.expires > Date.now()) return cached.data;
    const data = await this.api.get(url);
    this.cache.set(url, { data, expires: Date.now() + this.ttl });
    return data;
  }
}</pre>

<h2 id="patterns-behavioral" class="section-break">82. Behavioral Patterns</h2>
<p class="small"><strong>Checklist:</strong> Observer · Strategy · Command · Mediator · Iterator</p>

<pre>// OBSERVER — event-driven communication
class EventEmitter {
  private listeners = new Map&lt;string, Set&lt;Function&gt;&gt;();

  on(event: string, callback: Function) {
    if (!this.listeners.has(event)) this.listeners.set(event, new Set());
    this.listeners.get(event)!.add(callback);
    return () => this.listeners.get(event)!.delete(callback); // unsubscribe
  }

  emit(event: string, ...args: any[]) {
    this.listeners.get(event)?.forEach(cb => cb(...args));
  }
}

// Angular: RxJS Subjects ARE the Observer pattern
const subject = new Subject&lt;string&gt;();
const sub = subject.subscribe(value => console.log(value));
subject.next('Hello');
sub.unsubscribe();

// STRATEGY — swap algorithms at runtime
interface SortStrategy&lt;T&gt; {
  sort(data: T[]): T[];
}
class QuickSort&lt;T&gt; implements SortStrategy&lt;T&gt; { sort(data: T[]) { /* ... */ } }
class MergeSort&lt;T&gt; implements SortStrategy&lt;T&gt; { sort(data: T[]) { /* ... */ } }

class DataProcessor&lt;T&gt; {
  constructor(private strategy: SortStrategy&lt;T&gt;) {}
  setStrategy(s: SortStrategy&lt;T&gt;) { this.strategy = s; }
  process(data: T[]) { return this.strategy.sort(data); }
}

// COMMAND — encapsulate actions for undo/redo
interface Command {
  execute(): void;
  undo(): void;
}
class AddTextCommand implements Command {
  constructor(private editor: Editor, private text: string, private position: number) {}
  execute() { this.editor.insert(this.text, this.position); }
  undo() { this.editor.delete(this.position, this.text.length); }
}
class CommandHistory {
  private history: Command[] = [];
  private pointer = -1;
  execute(cmd: Command) { cmd.execute(); this.history[++this.pointer] = cmd; }
  undo() { if (this.pointer >= 0) this.history[this.pointer--].undo(); }
  redo() { if (this.pointer < this.history.length - 1) this.history[++this.pointer].execute(); }
}</pre>

<h2 id="patterns-architectural" class="section-break">83. Architectural Patterns</h2>
<p class="small"><strong>Checklist:</strong> MVC · MVVM · MVP · Flux/Redux · Clean Architecture · Hexagonal Architecture</p>

<pre>// MVC (Model-View-Controller)
// Model: data + business logic
// View: UI rendering
// Controller: handles user input, updates model → view
// Used in: classic web frameworks (Express, Ruby on Rails)

// MVVM (Model-View-ViewModel) — Angular's pattern
// Model: data/entities
// View: template (HTML)
// ViewModel: component class (data binding, event handling)
@Component({
  template: `
    &lt;input [ngModel]="name" (ngModelChange)="name = $event"&gt;
    &lt;p&gt;Hello, {{ name }}&lt;/p&gt;
  `
})
class GreetComponent {
  name = 'World'; // ViewModel — two-way binding to view
}

// Flux/Redux — unidirectional data flow
// View → Action → Dispatcher → Store → View
// Benefits: predictable state, time-travel debugging, easy testing

// Clean Architecture layers (inside → outside)
// 1. Entities: business rules, domain objects
// 2. Use Cases: application-specific logic
// 3. Interface Adapters: controllers, presenters, gateways
// 4. Frameworks: Angular, database, HTTP
// Rule: dependencies point INWARD only

// Frontend Clean Architecture
src/
  domain/          // entities, value objects (no framework imports!)
    user.model.ts
    order.model.ts
  application/     // use cases, ports (interfaces)
    create-order.usecase.ts
    order.repository.ts  // interface
  infrastructure/  // adapters (implementations)
    http-order.repository.ts  // implements order.repository.ts
    local-storage.adapter.ts
  presentation/    // Angular components, pages
    order-list.component.ts
    order-detail.component.ts</pre>

<div class="interview-q">
<h4>🎯 Interview Questions — Design Patterns</h4>
<p><strong>Q: Which patterns do you use most in frontend development?</strong></p>
<p><strong>A:</strong> <strong>Observer</strong> (RxJS, event emitters, pub/sub for component communication). <strong>Strategy</strong> (swappable validators, sort algorithms, rendering strategies). <strong>Facade</strong> (service layer abstracting complex API calls). <strong>Singleton</strong> (Angular services with providedIn: root). <strong>Decorator</strong> (Angular decorators, function wrappers for logging/caching). <strong>Factory</strong> (dynamic component creation, object creation based on config).</p>
</div>

<!-- ═══════════════════════════════════════════════════════════════════
     DATA STRUCTURES & ALGORITHMS — 3 SUB-SECTIONS
     ═══════════════════════════════════════════════════════════════════ -->

<h2 id="dsa-structures" class="section-break">84. Data Structures</h2>
<p class="small"><strong>Checklist:</strong> Arrays · Linked Lists · Stacks · Queues · Hash Tables · Trees · Graphs · Heaps · Tries</p>

<pre>// STACK — LIFO (Last In, First Out)
class Stack&lt;T&gt; {
  private items: T[] = [];
  push(item: T) { this.items.push(item); }
  pop(): T | undefined { return this.items.pop(); }
  peek(): T | undefined { return this.items[this.items.length - 1]; }
  get size() { return this.items.length; }
  get isEmpty() { return this.items.length === 0; }
}
// Use cases: undo/redo, browser history, balanced parentheses, call stack

// QUEUE — FIFO (First In, First Out)
class Queue&lt;T&gt; {
  private items: T[] = [];
  enqueue(item: T) { this.items.push(item); }
  dequeue(): T | undefined { return this.items.shift(); }
  peek(): T | undefined { return this.items[0]; }
}
// Use cases: task scheduling, BFS, print queue, message queues

// LINKED LIST
class ListNode&lt;T&gt; {
  constructor(public value: T, public next: ListNode&lt;T&gt; | null = null) {}
}
class LinkedList&lt;T&gt; {
  head: ListNode&lt;T&gt; | null = null;

  prepend(value: T) {
    this.head = new ListNode(value, this.head);
  }

  append(value: T) {
    if (!this.head) { this.head = new ListNode(value); return; }
    let current = this.head;
    while (current.next) current = current.next;
    current.next = new ListNode(value);
  }

  delete(value: T) {
    if (!this.head) return;
    if (this.head.value === value) { this.head = this.head.next; return; }
    let current = this.head;
    while (current.next &amp;&amp; current.next.value !== value) current = current.next;
    if (current.next) current.next = current.next.next;
  }
}

// HASH MAP — O(1) average lookup, insert, delete
const map = new Map&lt;string, number&gt;();
map.set('apple', 3);
map.get('apple'); // 3
map.has('apple'); // true
// Collision resolution: chaining (linked lists) or open addressing (linear probing)

// BINARY SEARCH TREE
class BSTNode {
  constructor(
    public value: number,
    public left: BSTNode | null = null,
    public right: BSTNode | null = null
  ) {}
}
class BST {
  root: BSTNode | null = null;

  insert(value: number) {
    if (!this.root) { this.root = new BSTNode(value); return; }
    let current = this.root;
    while (true) {
      if (value &lt; current.value) {
        if (!current.left) { current.left = new BSTNode(value); return; }
        current = current.left;
      } else {
        if (!current.right) { current.right = new BSTNode(value); return; }
        current = current.right;
      }
    }
  }

  // In-order traversal → sorted output
  inOrder(node = this.root, result: number[] = []): number[] {
    if (node) {
      this.inOrder(node.left, result);
      result.push(node.value);
      this.inOrder(node.right, result);
    }
    return result;
  }
}

// TRIE — prefix tree for autocomplete, spell-check
class TrieNode {
  children = new Map&lt;string, TrieNode&gt;();
  isEnd = false;
}
class Trie {
  root = new TrieNode();

  insert(word: string) {
    let node = this.root;
    for (const char of word) {
      if (!node.children.has(char)) node.children.set(char, new TrieNode());
      node = node.children.get(char)!;
    }
    node.isEnd = true;
  }

  search(word: string): boolean {
    let node = this.root;
    for (const char of word) {
      if (!node.children.has(char)) return false;
      node = node.children.get(char)!;
    }
    return node.isEnd;
  }

  startsWith(prefix: string): string[] {
    let node = this.root;
    for (const char of prefix) {
      if (!node.children.has(char)) return [];
      node = node.children.get(char)!;
    }
    return this.collectWords(node, prefix);
  }

  private collectWords(node: TrieNode, prefix: string): string[] {
    const results: string[] = [];
    if (node.isEnd) results.push(prefix);
    for (const [char, child] of node.children) {
      results.push(...this.collectWords(child, prefix + char));
    }
    return results;
  }
}</pre>

<h2 id="dsa-algorithms" class="section-break">85. Common Algorithms</h2>
<p class="small"><strong>Checklist:</strong> Sorting (bubble, merge, quick) · Binary search · BFS · DFS · Two pointers · Sliding window · Dynamic programming basics</p>

<pre>// BINARY SEARCH — O(log n)
function binarySearch(arr: number[], target: number): number {
  let left = 0, right = arr.length - 1;
  while (left &lt;= right) {
    const mid = Math.floor((left + right) / 2);
    if (arr[mid] === target) return mid;
    if (arr[mid] &lt; target) left = mid + 1;
    else right = mid - 1;
  }
  return -1; // not found
}

// MERGE SORT — O(n log n), stable
function mergeSort(arr: number[]): number[] {
  if (arr.length &lt;= 1) return arr;
  const mid = Math.floor(arr.length / 2);
  const left = mergeSort(arr.slice(0, mid));
  const right = mergeSort(arr.slice(mid));
  return merge(left, right);
}
function merge(a: number[], b: number[]): number[] {
  const result: number[] = [];
  let i = 0, j = 0;
  while (i &lt; a.length &amp;&amp; j &lt; b.length) {
    result.push(a[i] &lt;= b[j] ? a[i++] : b[j++]);
  }
  return result.concat(a.slice(i), b.slice(j));
}

// BFS — level-order traversal, shortest path (unweighted)
function bfs(root: TreeNode): number[][] {
  const levels: number[][] = [];
  const queue: TreeNode[] = [root];
  while (queue.length) {
    const level: number[] = [];
    const size = queue.length;
    for (let i = 0; i &lt; size; i++) {
      const node = queue.shift()!;
      level.push(node.value);
      if (node.left) queue.push(node.left);
      if (node.right) queue.push(node.right);
    }
    levels.push(level);
  }
  return levels;
}

// DFS — three traversals
function dfsPreOrder(node: TreeNode | null): number[] {
  if (!node) return [];
  return [node.value, ...dfsPreOrder(node.left), ...dfsPreOrder(node.right)];
}
function dfsInOrder(node: TreeNode | null): number[] {
  if (!node) return [];
  return [...dfsInOrder(node.left), node.value, ...dfsInOrder(node.right)];
}
function dfsPostOrder(node: TreeNode | null): number[] {
  if (!node) return [];
  return [...dfsPostOrder(node.left), ...dfsPostOrder(node.right), node.value];
}

// TWO POINTERS — find pair with target sum in sorted array
function twoSum(arr: number[], target: number): [number, number] | null {
  let left = 0, right = arr.length - 1;
  while (left &lt; right) {
    const sum = arr[left] + arr[right];
    if (sum === target) return [left, right];
    if (sum &lt; target) left++;
    else right--;
  }
  return null;
}

// SLIDING WINDOW — max sum subarray of size k
function maxSumSubarray(arr: number[], k: number): number {
  let windowSum = arr.slice(0, k).reduce((a, b) => a + b, 0);
  let maxSum = windowSum;
  for (let i = k; i &lt; arr.length; i++) {
    windowSum += arr[i] - arr[i - k]; // slide: add right, remove left
    maxSum = Math.max(maxSum, windowSum);
  }
  return maxSum;
}

// DYNAMIC PROGRAMMING — Fibonacci (bottom-up)
function fibonacci(n: number): number {
  if (n &lt;= 1) return n;
  let prev2 = 0, prev1 = 1;
  for (let i = 2; i &lt;= n; i++) {
    [prev2, prev1] = [prev1, prev2 + prev1];
  }
  return prev1;
}</pre>

<h2 id="dsa-complexity" class="section-break">86. Complexity Analysis</h2>
<p class="small"><strong>Checklist:</strong> Big O notation · time vs space · common complexities · amortized analysis</p>

<table>
<thead><tr><th>Big O</th><th>Name</th><th>Example</th></tr></thead>
<tbody>
<tr><td>O(1)</td><td>Constant</td><td>Array access, hash map get/set</td></tr>
<tr><td>O(log n)</td><td>Logarithmic</td><td>Binary search, balanced BST operations</td></tr>
<tr><td>O(n)</td><td>Linear</td><td>Array iteration, linear search</td></tr>
<tr><td>O(n log n)</td><td>Linearithmic</td><td>Merge sort, quick sort (average), heap sort</td></tr>
<tr><td>O(n²)</td><td>Quadratic</td><td>Bubble sort, nested loops, selection sort</td></tr>
<tr><td>O(2ⁿ)</td><td>Exponential</td><td>Recursive Fibonacci (naive), power set</td></tr>
<tr><td>O(n!)</td><td>Factorial</td><td>Permutations, traveling salesman (brute force)</td></tr>
</tbody>
</table>

<pre>// JavaScript built-in complexities
// Array:
//   push/pop: O(1) amortized
//   shift/unshift: O(n)   ← moves all elements!
//   splice: O(n)
//   indexOf/includes: O(n)
//   sort: O(n log n)
//   map/filter/reduce: O(n)

// Map/Set:
//   get/set/has/delete: O(1) average
//   forEach: O(n)

// Object:
//   property access: O(1)
//   Object.keys(): O(n)

// Space complexity examples:
// O(1) — in-place sorting, fixed variables
// O(n) — creating a copy of array, hash map of n items
// O(n²) — 2D matrix of size n×n
// O(log n) — recursive binary search (call stack depth)</pre>

<div class="interview-q">
<h4>🎯 Interview Questions — DSA</h4>
<p><strong>Q: What's the time complexity of searching in a hash map vs a sorted array?</strong></p>
<p><strong>A:</strong> Hash map: O(1) average, O(n) worst case (hash collisions). Sorted array: O(log n) with binary search. Hash map is faster for single lookups. Sorted array is better when you need range queries or sorted output.</p>

<p><strong>Q: When would you choose a linked list over an array?</strong></p>
<p><strong>A:</strong> When you need frequent insertions/deletions at arbitrary positions (O(1) for linked list vs O(n) for array shifting). In practice, arrays are almost always faster due to cache locality (contiguous memory). Linked lists are rarely used directly in frontend — but the concept is used in LRU caches, undo history, and task queues.</p>
</div>
"""
