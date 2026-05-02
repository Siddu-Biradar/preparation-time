SECTIONS = r"""

<!-- ═══════════════════════════════════════════════════════════════════
     TRICKY JS OUTPUT QUESTIONS — EVERY tough interview has these
     ═══════════════════════════════════════════════════════════════════ -->

<h2 id="tricky-output" class="section-break">121. Tricky JavaScript Output Questions</h2>
<p class="small"><strong>Checklist:</strong> Hoisting traps · closure traps · this binding puzzles · async execution order · type coercion · scope chains · event loop micro/macro tasks</p>

<h3>121.1 Hoisting &amp; TDZ Traps</h3>
<pre>// Q1: What's the output?
console.log(a);     // undefined (var is hoisted, initialized as undefined)
console.log(b);     // ReferenceError: Cannot access 'b' before initialization (TDZ!)
var a = 1;
let b = 2;

// Q2: What's the output?
var x = 1;
function foo() {
  console.log(x);   // undefined — NOT 1! var x below is hoisted inside foo
  var x = 2;
  console.log(x);   // 2
}
foo();

// Q3: What's the output?
function foo() { return 1; }
var foo;
console.log(typeof foo);  // "function"
// Function declarations are hoisted ABOVE var declarations
// var foo doesn't overwrite because it has no assignment

// Q4: What's the output?
var foo = function() { return 1; };
function foo() { return 2; }
console.log(foo());  // 1
// function foo(){} is hoisted to top, then var foo = function(){} overwrites it</pre>

<h3>121.2 Closure Traps — The Classic Loop Problem</h3>
<pre>// Q5: What's the output?
for (var i = 0; i &lt; 3; i++) {
  setTimeout(() => console.log(i), 100);
}
// Output: 3, 3, 3  (NOT 0, 1, 2!)
// Reason: var i is function-scoped, all closures share same i.
// By the time setTimeout fires, loop is done, i === 3.

// Fix 1: use let (block-scoped, each iteration gets its own i)
for (let i = 0; i &lt; 3; i++) {
  setTimeout(() => console.log(i), 100);
}
// Output: 0, 1, 2 ✅

// Fix 2: IIFE (creates new scope per iteration)
for (var i = 0; i &lt; 3; i++) {
  (function(j) {
    setTimeout(() => console.log(j), 100);
  })(i);
}
// Output: 0, 1, 2 ✅

// Q6: What's the output?
function createCounter() {
  let count = 0;
  return {
    increment: () => ++count,
    getCount: () => count
  };
}
const counter = createCounter();
counter.increment();
counter.increment();
console.log(counter.getCount()); // 2
// Both methods close over the SAME count variable</pre>

<h3>121.3 this Binding Puzzles</h3>
<pre>// Q7: What's the output?
const obj = {
  name: 'Sid',
  greet: function() { console.log(this.name); },
  greetArrow: () => { console.log(this.name); }
};
obj.greet();         // "Sid" — this = obj (implicit binding)
obj.greetArrow();    // undefined — arrow inherits this from outer scope (window/module)

// Q8: What's the output?
const obj2 = {
  name: 'Sid',
  greet() {
    console.log(this.name);
  }
};
const fn = obj2.greet;
fn();                // undefined (or error in strict mode)
// When you extract a method, `this` binding is lost!
// Fix: const fn = obj2.greet.bind(obj2);

// Q9: What's the output?
function Person(name) {
  this.name = name;
  this.sayHi = function() {
    console.log(this.name);
  };
  this.sayHiArrow = () => {
    console.log(this.name);
  };
}
const p = new Person('Sid');
const sayHi = p.sayHi;
const sayHiArrow = p.sayHiArrow;
sayHi();            // undefined (lost this)
sayHiArrow();       // "Sid" ✅ (arrow captures this from constructor scope!)

// Q10: What's the output?
const obj3 = {
  x: 42,
  getX: function() { return this.x; }
};
const unboundGetX = obj3.getX;
console.log(unboundGetX());         // undefined
const boundGetX = unboundGetX.bind(obj3);
console.log(boundGetX());           // 42
console.log(obj3.getX.call({ x: 99 })); // 99 (explicit binding)</pre>

<h3>121.4 Event Loop &amp; Async Execution Order</h3>
<pre>// Q11: What's the output ORDER?
console.log('1');

setTimeout(() => console.log('2'), 0);

Promise.resolve().then(() => console.log('3'));

console.log('4');

// Output: 1, 4, 3, 2
// Explanation:
// 1. Synchronous: log '1'
// 2. setTimeout → macrotask queue
// 3. Promise.then → microtask queue
// 4. Synchronous: log '4'
// 5. Microtasks run first → log '3'
// 6. Macrotasks → log '2'

// Q12: What's the output ORDER?
async function foo() {
  console.log('A');
  await Promise.resolve();
  console.log('B');
}

console.log('C');
foo();
console.log('D');

// Output: C, A, D, B
// C: synchronous
// foo() starts: A is synchronous
// await pauses foo, schedules B as microtask
// D: synchronous
// B: microtask runs

// Q13: What's the output ORDER?
setTimeout(() => console.log('timeout'), 0);
Promise.resolve()
  .then(() => console.log('promise 1'))
  .then(() => console.log('promise 2'));
queueMicrotask(() => console.log('microtask'));
console.log('sync');

// Output: sync, promise 1, microtask, promise 2, timeout
// sync → microtasks (promise 1, microtask) → promise 2 (chained) → timeout

// Q14: What's the output?
for (var i = 0; i &lt; 3; i++) {
  setTimeout(() => console.log(i), 0);
}
Promise.resolve().then(() => console.log('promise'));
// Output: promise, 3, 3, 3
// Promise (microtask) runs before setTimeout (macrotask)</pre>

<h3>121.5 Type Coercion Gotchas</h3>
<pre>// Q15: What are these?
console.log([] + []);            // "" (both convert to "", then string concat)
console.log([] + {});            // "[object Object]"
console.log({} + []);            // 0 (in some contexts) or "[object Object]" (depends)
console.log(true + true);       // 2
console.log(true + false);      // 1
console.log('5' - 3);           // 2 (- converts string to number)
console.log('5' + 3);           // "53" (+ prefers string concat)
console.log(null + 1);          // 1 (null → 0)
console.log(undefined + 1);     // NaN (undefined → NaN)
console.log('2' > '12');        // true! (string comparison: '2' > '1')
console.log(NaN === NaN);       // false (NaN is not equal to anything)
console.log(0.1 + 0.2 === 0.3); // false (floating point: 0.30000000000000004)

// Q16: What's the output?
console.log(typeof null);        // "object" (historical bug, never fixed)
console.log(typeof undefined);   // "undefined"
console.log(typeof NaN);         // "number" (NaN is a number!)
console.log(typeof []);          // "object"
console.log(typeof function(){}); // "function"

// Q17: Equality weirdness
console.log(null == undefined);   // true (loose equality special case)
console.log(null === undefined);  // false
console.log('' == false);         // true (both coerce to 0)
console.log('' === false);        // false (different types)
console.log([] == false);         // true ([] → '' → 0, false → 0)
console.log([1] == 1);            // true ([1] → '1' → 1)</pre>

<div class="interview-q">
<h4>🎯 Master Rule for Output Questions</h4>
<p><strong>Step-by-step approach:</strong> (1) Identify ALL synchronous code — runs first. (2) Identify microtasks (Promise.then, queueMicrotask, MutationObserver) — runs after sync. (3) Identify macrotasks (setTimeout, setInterval, I/O) — runs last. (4) For closures — ask "what is the variable's value AT THE TIME the function executes, not when it's defined?" (5) For <code>this</code> — ask "how is the function CALLED?" (method call → object, standalone → undefined/window, arrow → lexical, new → new object, bind/call/apply → explicit).</p>
</div>

<!-- ═══════════════════════════════════════════════════════════════════
     CODING CHALLENGES — Implement from scratch
     ═══════════════════════════════════════════════════════════════════ -->

<h2 id="challenge-polyfills" class="section-break">122. Implement JS Built-ins (Polyfills)</h2>
<p class="small"><strong>Checklist:</strong> Promise.all · Promise.race · Promise.any · Array.map · Array.filter · Array.reduce · Array.flat · Function.bind · call/apply · Object.assign · Object.create · Array.from</p>

<pre>// IMPLEMENT Promise.all
function promiseAll(promises) {
  return new Promise((resolve, reject) => {
    const results = [];
    let completed = 0;
    const total = promises.length;

    if (total === 0) return resolve([]);

    promises.forEach((promise, index) => {
      Promise.resolve(promise)  // handle non-promise values
        .then(value => {
          results[index] = value;  // maintain order!
          completed++;
          if (completed === total) resolve(results);
        })
        .catch(reject);  // first rejection rejects the whole thing
    });
  });
}

// IMPLEMENT Promise.race
function promiseRace(promises) {
  return new Promise((resolve, reject) => {
    promises.forEach(promise => {
      Promise.resolve(promise).then(resolve, reject);
      // First to settle (resolve or reject) wins
    });
  });
}

// IMPLEMENT Promise.any
function promiseAny(promises) {
  return new Promise((resolve, reject) => {
    const errors = [];
    let rejectedCount = 0;
    promises.forEach((promise, index) => {
      Promise.resolve(promise).then(resolve, error => {
        errors[index] = error;
        rejectedCount++;
        if (rejectedCount === promises.length) {
          reject(new AggregateError(errors, 'All promises rejected'));
        }
      });
    });
  });
}

// IMPLEMENT Array.prototype.map
Array.prototype.myMap = function(callback, thisArg) {
  const result = [];
  for (let i = 0; i &lt; this.length; i++) {
    if (i in this) {  // handle sparse arrays
      result.push(callback.call(thisArg, this[i], i, this));
    }
  }
  return result;
};

// IMPLEMENT Array.prototype.filter
Array.prototype.myFilter = function(callback, thisArg) {
  const result = [];
  for (let i = 0; i &lt; this.length; i++) {
    if (i in this &amp;&amp; callback.call(thisArg, this[i], i, this)) {
      result.push(this[i]);
    }
  }
  return result;
};

// IMPLEMENT Array.prototype.reduce
Array.prototype.myReduce = function(callback, initialValue) {
  let accumulator;
  let startIndex;

  if (arguments.length >= 2) {
    accumulator = initialValue;
    startIndex = 0;
  } else {
    if (this.length === 0) throw new TypeError('Reduce of empty array with no initial value');
    accumulator = this[0];
    startIndex = 1;
  }

  for (let i = startIndex; i &lt; this.length; i++) {
    if (i in this) {
      accumulator = callback(accumulator, this[i], i, this);
    }
  }
  return accumulator;
};

// IMPLEMENT Function.prototype.bind
Function.prototype.myBind = function(context, ...args) {
  const fn = this;
  return function(...moreArgs) {
    return fn.apply(context, [...args, ...moreArgs]);
  };
};

// IMPLEMENT Function.prototype.call
Function.prototype.myCall = function(context, ...args) {
  context = context ?? globalThis;
  const sym = Symbol('fn');
  context[sym] = this;
  const result = context[sym](...args);
  delete context[sym];
  return result;
};

// IMPLEMENT Object.create
function objectCreate(proto, propertiesObject) {
  function F() {}
  F.prototype = proto;
  const obj = new F();
  if (propertiesObject) {
    Object.defineProperties(obj, propertiesObject);
  }
  return obj;
}

// IMPLEMENT new keyword
function myNew(Constructor, ...args) {
  const obj = Object.create(Constructor.prototype);
  const result = Constructor.apply(obj, args);
  return result instanceof Object ? result : obj;
}</pre>

<h2 id="challenge-machine" class="section-break">123. Machine Coding — Common UI Components</h2>
<p class="small"><strong>Checklist:</strong> Star rating · Accordion · Countdown timer · Infinite scroll · Type-ahead / Autocomplete · Modal · Tabs · Carousel · Drag &amp; Drop sortable list · Tic-tac-toe</p>

<h3>123.1 Star Rating Component</h3>
<pre>// Pure JavaScript — no framework
class StarRating {
  constructor(container, { maxStars = 5, rating = 0, onChange } = {}) {
    this.container = container;
    this.maxStars = maxStars;
    this.rating = rating;
    this.onChange = onChange;
    this.render();
  }

  render() {
    this.container.innerHTML = '';
    this.container.style.cssText = 'display:inline-flex;gap:4px;cursor:pointer;font-size:28px;';

    for (let i = 1; i &lt;= this.maxStars; i++) {
      const star = document.createElement('span');
      star.textContent = i &lt;= this.rating ? '★' : '☆';
      star.style.color = i &lt;= this.rating ? '#f59e0b' : '#d1d5db';
      star.style.transition = 'transform 0.15s, color 0.15s';

      star.addEventListener('click', () => {
        this.rating = this.rating === i ? 0 : i; // click same star to clear
        this.onChange?.(this.rating);
        this.render();
      });

      star.addEventListener('mouseenter', () => {
        this.highlight(i);
      });

      this.container.appendChild(star);
    }

    this.container.addEventListener('mouseleave', () => this.render());
  }

  highlight(upTo) {
    const stars = this.container.children;
    for (let i = 0; i &lt; stars.length; i++) {
      stars[i].textContent = i &lt; upTo ? '★' : '☆';
      stars[i].style.color = i &lt; upTo ? '#f59e0b' : '#d1d5db';
      if (i &lt; upTo) stars[i].style.transform = 'scale(1.15)';
    }
  }
}
// Usage: new StarRating(document.getElementById('stars'), { rating: 3, onChange: r => console.log(r) });</pre>

<h3>123.2 Countdown Timer</h3>
<pre>class CountdownTimer {
  constructor(container, targetDate) {
    this.container = container;
    this.targetDate = new Date(targetDate).getTime();
    this.interval = null;
    this.start();
  }

  start() {
    this.update(); // immediate first render
    this.interval = setInterval(() => this.update(), 1000);
  }

  update() {
    const now = Date.now();
    const diff = this.targetDate - now;

    if (diff &lt;= 0) {
      clearInterval(this.interval);
      this.container.textContent = '🎉 Time is up!';
      return;
    }

    const days = Math.floor(diff / (1000 * 60 * 60 * 24));
    const hours = Math.floor((diff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
    const mins = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
    const secs = Math.floor((diff % (1000 * 60)) / 1000);

    this.container.innerHTML = [
      this.box(days, 'Days'), this.box(hours, 'Hours'),
      this.box(mins, 'Minutes'), this.box(secs, 'Seconds')
    ].join('');
  }

  box(val, label) {
    return `&lt;div style="display:inline-block;text-align:center;margin:0 10px"&gt;
      &lt;div style="font-size:2.5rem;font-weight:bold"&gt;${String(val).padStart(2, '0')}&lt;/div&gt;
      &lt;div style="font-size:0.8rem;color:#666"&gt;${label}&lt;/div&gt;
    &lt;/div&gt;`;
  }

  destroy() { clearInterval(this.interval); }
}</pre>

<h3>123.3 LRU Cache — Most Common Data Structure Question</h3>
<pre>class LRUCache {
  constructor(capacity) {
    this.capacity = capacity;
    this.cache = new Map(); // Map preserves insertion order
  }

  get(key) {
    if (!this.cache.has(key)) return -1;
    // Move to end (most recently used)
    const value = this.cache.get(key);
    this.cache.delete(key);
    this.cache.set(key, value);
    return value;
  }

  put(key, value) {
    if (this.cache.has(key)) {
      this.cache.delete(key); // remove old position
    } else if (this.cache.size >= this.capacity) {
      // Evict least recently used (first item in Map)
      const oldestKey = this.cache.keys().next().value;
      this.cache.delete(oldestKey);
    }
    this.cache.set(key, value); // add at end (most recent)
  }
}

// Test:
const cache = new LRUCache(2);
cache.put(1, 'a');
cache.put(2, 'b');
cache.get(1);       // 'a' — moves 1 to most recent
cache.put(3, 'c');  // evicts key 2 (least recently used)
cache.get(2);       // -1 (evicted!)
cache.get(3);       // 'c'</pre>

<h2 id="challenge-advanced-coding" class="section-break">124. Advanced Coding Challenges</h2>
<p class="small"><strong>Checklist:</strong> Implement setInterval using setTimeout · Implement pipe/compose · Implement JSON.stringify · Implement instanceof · Implement Object.assign · Implement Array.from · Implement flat with depth · Intersection of arrays</p>

<pre>// IMPLEMENT setInterval using setTimeout (frequently asked!)
function mySetInterval(callback, delay) {
  let id = { cancelled: false };

  function tick() {
    if (!id.cancelled) {
      callback();
      setTimeout(tick, delay);
    }
  }

  setTimeout(tick, delay);
  return id;
}
function myClearInterval(id) { id.cancelled = true; }

// IMPLEMENT pipe (left-to-right function composition)
function pipe(...fns) {
  return (input) => fns.reduce((acc, fn) => fn(acc), input);
}
const transform = pipe(
  x => x * 2,
  x => x + 10,
  x => `Result: ${x}`
);
transform(5); // "Result: 20"

// IMPLEMENT compose (right-to-left function composition)
function compose(...fns) {
  return (input) => fns.reduceRight((acc, fn) => fn(acc), input);
}

// IMPLEMENT instanceof
function myInstanceOf(obj, Constructor) {
  if (obj === null || typeof obj !== 'object') return false;
  let proto = Object.getPrototypeOf(obj);
  while (proto !== null) {
    if (proto === Constructor.prototype) return true;
    proto = Object.getPrototypeOf(proto);
  }
  return false;
}

// IMPLEMENT JSON.stringify (simplified but covers main cases)
function myStringify(value) {
  if (value === null) return 'null';
  if (value === undefined) return undefined;
  if (typeof value === 'boolean') return String(value);
  if (typeof value === 'number') {
    if (!isFinite(value)) return 'null';
    return String(value);
  }
  if (typeof value === 'string') return `"${value}"`;
  if (Array.isArray(value)) {
    const items = value.map(v => myStringify(v) ?? 'null');
    return `[${items.join(',')}]`;
  }
  if (typeof value === 'object') {
    const entries = Object.entries(value)
      .filter(([, v]) => v !== undefined &amp;&amp; typeof v !== 'function')
      .map(([k, v]) => `"${k}":${myStringify(v)}`);
    return `{${entries.join(',')}}`;
  }
}

// IMPLEMENT Array.prototype.flat with depth
function flatDeep(arr, depth = 1) {
  if (depth &lt;= 0) return arr.slice();
  return arr.reduce((acc, val) =>
    acc.concat(Array.isArray(val) ? flatDeep(val, depth - 1) : val), []);
}
flatDeep([1, [2, [3, [4]]]], 2); // [1, 2, 3, [4]]
flatDeep([1, [2, [3, [4]]]], Infinity); // [1, 2, 3, 4]

// IMPLEMENT debounce with leading + trailing + cancel + flush
function debounce(fn, delay, { leading = false, trailing = true } = {}) {
  let timer = null;
  let lastArgs = null;

  function debounced(...args) {
    lastArgs = args;
    const callNow = leading &amp;&amp; !timer;

    clearTimeout(timer);
    timer = setTimeout(() => {
      timer = null;
      if (trailing &amp;&amp; lastArgs) fn.apply(this, lastArgs);
      lastArgs = null;
    }, delay);

    if (callNow) fn.apply(this, args);
  }

  debounced.cancel = () => { clearTimeout(timer); timer = null; lastArgs = null; };
  debounced.flush = () => {
    if (timer) { clearTimeout(timer); timer = null; fn.apply(this, lastArgs); lastArgs = null; }
  };

  return debounced;
}</pre>

<!-- ═══════════════════════════════════════════════════════════════════
     ADVANCED TYPESCRIPT & SYSTEM DESIGN ADDITIONS
     ═══════════════════════════════════════════════════════════════════ -->

<h2 id="ts-advanced-patterns" class="section-break">125. Advanced TypeScript Patterns</h2>
<p class="small"><strong>Checklist:</strong> Conditional types with infer · template literal types · branded types · module augmentation · recursive types · discriminated union exhaustiveness · const assertions</p>

<pre>// CONDITIONAL TYPES with infer — extract types
type ReturnOf&lt;T&gt; = T extends (...args: any[]) => infer R ? R : never;
type T1 = ReturnOf&lt;() => string&gt;;    // string
type T2 = ReturnOf&lt;(x: number) => boolean&gt;; // boolean

// Extract Promise value
type Unwrap&lt;T&gt; = T extends Promise&lt;infer U&gt; ? Unwrap&lt;U&gt; : T;
type T3 = Unwrap&lt;Promise&lt;Promise&lt;string&gt;&gt;&gt;; // string (recursive unwrap!)

// Extract array element type
type ElementOf&lt;T&gt; = T extends (infer E)[] ? E : never;
type T4 = ElementOf&lt;string[]&gt;; // string

// BRANDED TYPES — prevent accidental type mixups
type UserId = string &amp; { readonly __brand: 'UserId' };
type OrderId = string &amp; { readonly __brand: 'OrderId' };

function createUserId(id: string): UserId { return id as UserId; }
function createOrderId(id: string): OrderId { return id as OrderId; }

function getUser(id: UserId) { /* ... */ }
function getOrder(id: OrderId) { /* ... */ }

const userId = createUserId('user-123');
const orderId = createOrderId('order-456');
getUser(userId);    // ✅
getUser(orderId);   // ❌ Compile error! OrderId is not assignable to UserId

// TEMPLATE LITERAL TYPES
type HTTPMethod = 'GET' | 'POST' | 'PUT' | 'DELETE';
type ApiRoute = '/users' | '/products' | '/orders';
type Endpoint = `${HTTPMethod} ${ApiRoute}`;
// 'GET /users' | 'GET /products' | 'GET /orders' | 'POST /users' | ...

// Event handler type
type EventName = 'click' | 'focus' | 'blur';
type Handler = `on${Capitalize&lt;EventName&gt;}`; // 'onClick' | 'onFocus' | 'onBlur'

// EXHAUSTIVE SWITCH — compile error if case is missing
type Shape = { kind: 'circle'; r: number } | { kind: 'square'; s: number };

function area(shape: Shape): number {
  switch (shape.kind) {
    case 'circle': return Math.PI * shape.r ** 2;
    case 'square': return shape.s ** 2;
    default: {
      const _exhaustive: never = shape; // ← ERROR if case is missing!
      return _exhaustive;
    }
  }
}

// const ASSERTION — narrowest possible type
const config = {
  endpoint: '/api',
  retries: 3,
  methods: ['GET', 'POST']
} as const;
// type: { readonly endpoint: "/api"; readonly retries: 3; readonly methods: readonly ["GET", "POST"] }
// Without as const: { endpoint: string; retries: number; methods: string[] }

// RECURSIVE TYPES
type DeepReadonly&lt;T&gt; = {
  readonly [K in keyof T]: T[K] extends object ? DeepReadonly&lt;T[K]&gt; : T[K];
};

type DeepPartial&lt;T&gt; = {
  [K in keyof T]?: T[K] extends object ? DeepPartial&lt;T[K]&gt; : T[K];
};

type JSONValue =
  | string | number | boolean | null
  | JSONValue[]
  | { [key: string]: JSONValue };

// BUILDER PATTERN with TypeScript (type-safe)
class QueryBuilder&lt;Selected extends string = never&gt; {
  select&lt;F extends string&gt;(field: F): QueryBuilder&lt;Selected | F&gt; {
    return this as any;
  }
  execute(): Record&lt;Selected, unknown&gt; {
    return {} as any;
  }
}
const result = new QueryBuilder()
  .select('name')
  .select('email')
  .execute();
// type: { name: unknown; email: unknown }  ← only selected fields!</pre>

<h2 id="sd-frontend-lld" class="section-break">126. Frontend Low-Level Design (LLD)</h2>
<p class="small"><strong>Checklist:</strong> Design a real-time notification system · Design a form builder · Design a drag-and-drop kanban · Design an image gallery with zoom · Design a rich text editor · Design a rate limiter</p>

<pre>// LLD: Real-Time Notification System

// Requirements:
// - Multiple notification types (info, warning, error, success)
// - Auto-dismiss with configurable timeout
// - Stack with max visible (newest replaces oldest)
// - Persistent notifications (don't auto-dismiss)
// - Action buttons (undo, retry, view)
// - Sound/vibration for urgent notifications
// - Queue system: if max visible, queue up the rest

interface Notification {
  id: string;
  type: 'info' | 'warning' | 'error' | 'success';
  title: string;
  message: string;
  duration?: number;        // ms, 0 = persistent
  actions?: NotificationAction[];
  persistent?: boolean;
  priority?: 'low' | 'normal' | 'high';
  timestamp: number;
}

interface NotificationAction {
  label: string;
  handler: () => void;
  style?: 'primary' | 'secondary' | 'danger';
}

class NotificationService {
  private visible: Notification[] = [];
  private queue: Notification[] = [];
  private maxVisible = 5;
  private timers = new Map&lt;string, number&gt;();
  private subscribers = new Set&lt;(notifications: Notification[]) => void&gt;();

  show(options: Omit&lt;Notification, 'id' | 'timestamp'&gt;): string {
    const notification: Notification = {
      ...options,
      id: crypto.randomUUID(),
      timestamp: Date.now(),
      duration: options.duration ?? 5000
    };

    if (this.visible.length >= this.maxVisible) {
      // Remove lowest priority non-persistent notification
      const removable = this.visible.find(n => !n.persistent);
      if (removable) this.dismiss(removable.id);
      else { this.queue.push(notification); return notification.id; }
    }

    this.visible.push(notification);
    this.notify();

    if (notification.duration > 0 &amp;&amp; !notification.persistent) {
      const timer = window.setTimeout(
        () => this.dismiss(notification.id),
        notification.duration
      );
      this.timers.set(notification.id, timer);
    }

    return notification.id;
  }

  dismiss(id: string) {
    clearTimeout(this.timers.get(id));
    this.timers.delete(id);
    this.visible = this.visible.filter(n => n.id !== id);

    // Show queued notification
    if (this.queue.length > 0) {
      const next = this.queue.shift()!;
      this.visible.push(next);
    }
    this.notify();
  }

  subscribe(fn: (notifications: Notification[]) => void) {
    this.subscribers.add(fn);
    return () => this.subscribers.delete(fn);
  }

  private notify() {
    this.subscribers.forEach(fn => fn([...this.visible]));
  }
}

// LLD: Token Bucket Rate Limiter (client-side)
class RateLimiter {
  private tokens: number;
  private lastRefill: number;

  constructor(
    private maxTokens: number,     // max burst
    private refillRate: number     // tokens per second
  ) {
    this.tokens = maxTokens;
    this.lastRefill = Date.now();
  }

  tryAcquire(): boolean {
    this.refill();
    if (this.tokens &lt; 1) return false;
    this.tokens -= 1;
    return true;
  }

  private refill() {
    const now = Date.now();
    const elapsed = (now - this.lastRefill) / 1000;
    this.tokens = Math.min(this.maxTokens, this.tokens + elapsed * this.refillRate);
    this.lastRefill = now;
  }
}

// Usage: const limiter = new RateLimiter(10, 2); // 10 burst, 2/sec refill
// if (limiter.tryAcquire()) { makeApiCall(); }
// else { showRateLimitMessage(); }</pre>

<h2 id="challenge-system-design" class="section-break">127. Frontend System Design Interview Patterns</h2>
<p class="small"><strong>Checklist:</strong> Design approach framework · component hierarchy · data flow · API design · state management · error handling · performance · accessibility · edge cases</p>

<pre>// FRAMEWORK FOR ANY FRONTEND SYSTEM DESIGN QUESTION

// Step 1: REQUIREMENTS CLARIFICATION (5 min)
// - Functional requirements: What features?
// - Non-functional: Performance, accessibility, offline support?
// - Scale: How many users? How much data?
// - Platform: Desktop? Mobile? Both?
// - Browser support?

// Step 2: HIGH-LEVEL ARCHITECTURE (5 min)
// Draw: Component tree, data flow, API endpoints
// Identify: Pages, shared components, services, stores

// Step 3: DATA MODEL & API (5 min)
// Define: TypeScript interfaces for all entities
// API endpoints: REST or GraphQL schema
// State shape: What goes in global store vs local state vs URL?

// Step 4: COMPONENT DESIGN (10 min)
// Smart vs Dumb components
// Content projection / composition patterns
// Reusability considerations

// Step 5: KEY INTERACTIONS (10 min)
// Walk through critical user flows
// Error states, loading states, empty states
// Optimistic updates, retry logic

// Step 6: OPTIMIZATIONS (5 min)
// Performance: lazy loading, virtual scroll, memoization
// Caching strategy
// Bundle size considerations

// EXAMPLE: Design a Twitter-like Feed

// Data model:
interface Tweet {
  id: string;
  author: User;
  content: string;
  media?: Media[];
  likes: number;
  retweets: number;
  replies: number;
  isLiked: boolean;
  isRetweeted: boolean;
  createdAt: string;
}

// Component hierarchy:
// FeedPage (smart)
//   ├── ComposeBox (smart — handles post creation)
//   ├── FeedList (dumb — receives tweets)
//   │   ├── TweetCard (dumb — single tweet)
//   │   │   ├── UserAvatar
//   │   │   ├── TweetContent (handles text, links, media)
//   │   │   ├── TweetActions (like, retweet, reply buttons)
//   │   │   └── TweetThread (if it's a thread)
//   │   └── InfiniteScrollSentinel
//   ├── TrendingSidebar
//   └── SuggestedFollows

// State management:
// - Feed items → SignalStore (paginated, cursor-based)
// - Current user → global store (auth)
// - New tweet form → local state (component)
// - Filters/tab → URL state (router)
// - Like/retweet counts → optimistic update pattern

// Performance:
// - Virtual scrolling (1000s of tweets, only render ~20 DOM nodes)
// - Image lazy loading (IntersectionObserver)
// - Optimistic updates for likes (instant UI, background API)
// - Debounced search
// - WebSocket for real-time new tweet count badge

// Edge cases:
// - Network failure during post → retry with saved draft
// - Duplicate rapid likes → exhaustMap prevents double-request
// - Content longer than limit → show "Read more" truncation
// - Deleted tweets → handle 404 gracefully
// - Rate limiting → show message, queue requests</pre>

<h2 id="common-scenarios" class="section-break">128. Web Performance Case Studies</h2>
<p class="small"><strong>Checklist:</strong> Diagnosing slow FCP · fixing layout shifts · optimizing bundle size · handling slow APIs · memory leak detection</p>

<pre>// CASE STUDY 1: Slow First Contentful Paint (FCP > 4s)
// Diagnosis steps:
// 1. Run Lighthouse → see what's blocking
// 2. Check Network waterfall → large blocking resources?
// 3. Check Coverage tab → unused CSS/JS %

// Common fixes:
// - Inline critical CSS, defer non-critical
// - Preconnect to API: &lt;link rel="preconnect" href="https://api.example.com"&gt;
// - Preload key resources: &lt;link rel="preload" href="/fonts/main.woff2" as="font"&gt;
// - Remove render-blocking scripts (add defer/async)
// - Server-side render the above-the-fold content
// - Compress assets (Brotli > gzip, 20-30% smaller)

// CASE STUDY 2: Layout Shift (CLS > 0.25)
// Diagnosis: DevTools Performance tab → Layout Shift rows
// Common causes + fixes:
// 1. Images without dimensions → add width/height or aspect-ratio
// 2. Web fonts causing FOUT → font-display: swap + preload
// 3. Dynamic content inserted above → reserve space with min-height
// 4. Ads/embeds without size → use &lt;iframe width="..." height="..."&gt;

// CASE STUDY 3: Memory Leak
// Diagnosis: DevTools → Memory → Heap Snapshot → Compare snapshots
function detectLeak() {
  // Take snapshot 1
  // Perform action (open/close modal 10 times)
  // Take snapshot 2
  // Compare: if detached DOM nodes keep growing → LEAK!
}

// Common frontend memory leaks:
// 1. Unsubscribed observables / event listeners
// 2. Closures holding references to detached DOM
// 3. Global arrays/maps that grow without bounds
// 4. setInterval without clearInterval
// 5. Detached DOM trees (element removed but JS still references it)

// Fix pattern:
class Widget {
  private abortController = new AbortController();

  init() {
    window.addEventListener('resize', this.onResize, {
      signal: this.abortController.signal // auto-cleanup!
    });
  }

  destroy() {
    this.abortController.abort(); // removes ALL listeners at once
  }
}</pre>

<h2 id="behavioral-questions" class="section-break">129. Behavioral &amp; Situational Questions</h2>
<p class="small"><strong>Checklist:</strong> Conflict resolution · technical debt decisions · mentoring · handling tight deadlines · production incidents · architectural decisions</p>

<pre>// SITUATIONAL QUESTIONS — prepare stories using STAR method

// Q: "Tell me about a time you disagreed with a technical decision."
// Framework:
// Situation: What was the context and the disagreement?
// Task: What was your role?
// Action: How did you handle it? (data-driven arguments, POC, compromise?)
// Result: What happened? What did you learn?

// Q: "How do you handle technical debt?"
// Good answer framework:
// 1. Document it: maintain a tech debt register with impact scores
// 2. Prioritize: security debt > performance debt > code quality debt
// 3. Budget time: 20% of sprint for tech debt (negotiate with PM)
// 4. Prevent: enforce coding standards, PR reviews, automated linting
// 5. Track: measure code coverage, bundle size, Lighthouse scores over time

// Q: "A critical production bug is reported. Walk me through your approach."
// 1. ASSESS: Severity? Users affected? Data loss? Revenue impact?
// 2. COMMUNICATE: Inform stakeholders, set incident channel
// 3. MITIGATE: Can we feature-flag or rollback? Reduce blast radius
// 4. DIAGNOSE: Check error tracking (Sentry), logs, recent deployments
// 5. FIX: Minimal fix for production (hotfix), thorough fix for next release
// 6. POSTMORTEM: Root cause, timeline, what we'll do to prevent recurrence

// Q: "How do you mentor junior developers?"
// - Pair programming sessions on complex features
// - Code review as a teaching tool (explain WHY, not just WHAT)
// - Set up knowledge sharing sessions (tech talks, demos)
// - Create clear documentation and coding guidelines
// - Give increasing ownership: start small, build confidence
// - Regular 1:1s to understand their goals and blockers

// Q: "How do you make architectural decisions?"
// 1. Define the problem and constraints clearly
// 2. Research options (at least 2-3 alternatives)
// 3. Create a comparison matrix: pros, cons, effort, risk
// 4. Build a lightweight POC for risky choices
// 5. Write an Architecture Decision Record (ADR)
// 6. Get team buy-in through RFC process
// 7. Decide with data, document with ADRs</pre>

<h2 id="frontend-security-advanced" class="section-break">130. Advanced Frontend Security</h2>
<p class="small"><strong>Checklist:</strong> Prototype pollution · supply chain attacks · DOM clobbering · ReDoS · dependency auditing · subresource integrity · permissions policy</p>

<pre>// PROTOTYPE POLLUTION — manipulate Object.prototype
// Attack: JSON.parse('{"__proto__": {"isAdmin": true}}')
// After pollution: ({}).isAdmin === true  // DANGER!

// Prevention:
// 1. Use Object.create(null) for dictionaries (no prototype)
const safeMap = Object.create(null);

// 2. Freeze the prototype
Object.freeze(Object.prototype);

// 3. Validate input keys
function safeAssign(target, source) {
  for (const key of Object.keys(source)) {
    if (key === '__proto__' || key === 'constructor' || key === 'prototype') {
      continue; // skip dangerous keys
    }
    target[key] = source[key];
  }
  return target;
}

// SUPPLY CHAIN ATTACKS — compromised npm packages
// Prevention:
// 1. npm audit / pnpm audit (check for known vulnerabilities)
// 2. Lock file (package-lock.json) — pin exact versions
// 3. Use npm ci in CI (installs from lock file only)
// 4. Subresource Integrity for CDN scripts
// 5. Renovate/Dependabot for automated security updates
// 6. Review dependency tree: npm ls --all
// 7. Use Socket.dev or Snyk for supply chain scanning

// PERMISSIONS POLICY — control browser features
Permissions-Policy:
  camera=(),                    // disable camera
  microphone=(),                // disable microphone
  geolocation=(self),           // only our origin
  payment=(self "https://pay.example.com")

// DOM CLOBBERING — HTML elements override global properties
// Attack: &lt;img name="location" /&gt; → window.location is now the img!
// Prevention: always use explicit references, CSP, sanitize HTML inputs

// DEPENDENCY AUDIT CHECKLIST for production:
// □ npm audit --production (zero critical/high vulnerabilities)
// □ Check bundle for eval(), Function(), innerHTML usage
// □ Review postinstall scripts in dependencies
// □ Pin dependency versions in lock file
// □ Enable 2FA on npm account (if publishing)
// □ Monitor with Snyk/Socket.dev/GitHub Dependabot</pre>

<div class="interview-q">
<h4>🎯 Final Interview Power Tips</h4>
<p><strong>Before the interview:</strong></p>
<p>• Review your past projects — be ready to explain architecture, challenges, and trade-offs for ANY project on your resume.</p>
<p>• Practice explaining concepts out loud — interviewers evaluate communication as much as knowledge.</p>
<p>• Know your numbers: "I reduced bundle size from 2.4MB to 800KB" beats "I optimized the build."</p>
<p>• Prepare 2-3 stories for behavioral questions (conflict, mentoring, production incident, technical decision).</p>

<p><strong>During the interview:</strong></p>
<p>• Think out loud — silence is worse than a wrong direction (they can redirect you).</p>
<p>• Ask clarifying questions before coding — shows maturity.</p>
<p>• Start with brute force, then optimize — shows systematic thinking.</p>
<p>• For system design: draw the component tree first, then dive into details.</p>
<p>• If stuck: "I'd approach this by..." (describe the concept even if you can't code it perfectly).</p>
<p>• Always discuss trade-offs: "We could use X, but Y might be better here because..."</p>
</div>
"""
