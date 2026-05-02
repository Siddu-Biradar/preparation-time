"""
Build the complete Frontend Interview Checklist HTML guide.
Creates the file in sections to avoid token limits.
"""
from pathlib import Path

OUT = Path(__file__).parent / "frontend-interview-checklist-guide.html"

HEAD = r"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Frontend Interview Concepts — Complete Checklist Guide</title>
  <style>
    @page{size:A4;margin:18mm 16mm}
    :root{--bg:#f4f1ea;--paper:#fffdf8;--ink:#1d1d1b;--muted:#5c584f;--line:#d8d0c3;--accent:#0f6b5f;--accent-soft:#d9efe8;--warning:#7a3a12;--warning-soft:#f7e7dd;--code:#f3efe7;--blue:#0b5e8a;--blue-soft:#e1f0fa}
    *{box-sizing:border-box}
    html{scroll-behavior:smooth;scroll-padding-top:20px}
    body{margin:0;font-family:"Georgia","Times New Roman",serif;color:var(--ink);background:var(--bg);line-height:1.5;font-size:11.4pt}
    main{max-width:920px;margin:0 auto;background:var(--paper);padding:28px 34px 44px}
    h1,h2,h3,h4{font-family:"Avenir Next","Helvetica Neue",Helvetica,Arial,sans-serif;line-height:1.2;margin:0 0 10px;color:#152923}
    h1{font-size:28pt;letter-spacing:-0.03em;margin-bottom:8px}
    h2{font-size:19pt;margin-top:28px;padding-top:8px;border-top:1px solid var(--line)}
    h3{font-size:14.5pt;margin-top:18px}
    h4{font-size:12pt;margin-top:14px}
    p{margin:0 0 10px}
    ul,ol{margin:6px 0 12px 22px;padding:0}
    li{margin:0 0 6px}
    code,pre{font-family:"SFMono-Regular",Menlo,Monaco,Consolas,"Liberation Mono",monospace}
    pre{background:var(--code);border:1px solid var(--line);border-radius:8px;padding:12px 14px;overflow-x:auto;white-space:pre-wrap;word-break:break-word;font-size:9.8pt;line-height:1.45;margin:10px 0 14px}
    table{width:100%;border-collapse:collapse;margin:10px 0 16px;font-size:10.4pt}
    th,td{border:1px solid var(--line);padding:8px 10px;vertical-align:top;text-align:left}
    th{background:#f1ece2;font-family:"Avenir Next","Helvetica Neue",Helvetica,Arial,sans-serif;font-weight:700}
    a{color:#0b5e8a;text-decoration:none;word-break:break-word}
    .hero{padding:18px 18px 14px;border:1px solid var(--line);background:linear-gradient(135deg,#f9f6f0 0%,#edf7f2 100%);border-radius:14px;margin-bottom:22px}
    .subtitle{font-family:"Avenir Next","Helvetica Neue",Helvetica,Arial,sans-serif;color:var(--muted);font-size:11.2pt;margin-bottom:12px}
    .pill-row{display:flex;flex-wrap:wrap;gap:8px;margin-top:10px}
    .pill{display:inline-block;padding:6px 10px;border-radius:999px;background:var(--accent-soft);color:#13443d;font-family:"Avenir Next","Helvetica Neue",Helvetica,Arial,sans-serif;font-size:9.4pt;border:1px solid #bfded5}
    .callout{border-left:4px solid var(--accent);background:#f4fbf8;padding:10px 12px;margin:12px 0 16px}
    .warning{border-left-color:var(--warning);background:var(--warning-soft)}
    .small{font-size:9.8pt;color:var(--muted)}
    .section-break{page-break-before:always}
    .avoid-break{page-break-inside:avoid}
    .sidebar-nav{position:fixed;top:0;left:0;width:270px;height:100vh;background:#1e2a26;color:#c8d6d0;overflow-y:auto;padding:16px 0 24px;z-index:1000;font-family:"Avenir Next","Helvetica Neue",Helvetica,Arial,sans-serif;scrollbar-width:thin;scrollbar-color:#3a4f47 #1e2a26}
    .sidebar-nav::-webkit-scrollbar{width:6px}
    .sidebar-nav::-webkit-scrollbar-track{background:#1e2a26}
    .sidebar-nav::-webkit-scrollbar-thumb{background:#3a4f47;border-radius:3px}
    .sidebar-nav .nav-title{font-size:13px;font-weight:700;color:#8bf0cc;padding:0 18px 12px;margin:0 0 6px;border-bottom:1px solid #2e3e38;letter-spacing:0.02em}
    .sidebar-nav .nav-group-label{font-size:9.5px;font-weight:700;text-transform:uppercase;letter-spacing:0.08em;color:#5a7a6e;padding:14px 18px 4px;margin:0}
    .sidebar-nav a{display:block;padding:5px 18px;font-size:11.5px;color:#a3bdb3;text-decoration:none;line-height:1.35;border-left:3px solid transparent;transition:all 0.15s ease}
    .sidebar-nav a:hover{background:#263832;color:#d4f5e6;border-left-color:#5cccaa}
    .sidebar-nav a.active{background:#263832;color:#8bf0cc;border-left-color:#8bf0cc;font-weight:600}
    body{margin-left:270px}
    .nav-toggle{display:none;position:fixed;top:12px;left:12px;z-index:1001;background:#1e2a26;color:#8bf0cc;border:none;border-radius:6px;width:38px;height:38px;font-size:20px;cursor:pointer;align-items:center;justify-content:center}
    @media(max-width:1100px){.sidebar-nav{transform:translateX(-100%);transition:transform 0.25s ease}.sidebar-nav.open{transform:translateX(0);box-shadow:4px 0 20px rgba(0,0,0,0.3)}body{margin-left:0}.nav-toggle{display:flex}}
    @media print{.sidebar-nav,.nav-toggle{display:none!important}body{margin-left:0;background:#fff}main{max-width:none;padding:0}}
  </style>
</head>
<body>
<button class="nav-toggle" onclick="document.querySelector('.sidebar-nav').classList.toggle('open')" aria-label="Toggle navigation">&#9776;</button>
<nav class="sidebar-nav" id="sidebarNav">
  <div class="nav-title">&#128203; Checklist Guide</div>
  <p class="nav-group-label">JavaScript</p>
  <a href="#s1">1. JS Fundamentals</a>
  <a href="#s2">2. Scope &amp; Closures</a>
  <a href="#s3">3. this Keyword</a>
  <a href="#s4">4. Prototypes &amp; Inheritance</a>
  <a href="#s5">5. Async JavaScript</a>
  <a href="#s6">6. ES6+ Features</a>
  <a href="#s7">7. Advanced JS Concepts</a>
  <a href="#s8">8. Array &amp; Object Methods</a>
  <a href="#s9">9. Error Handling &amp; Modules</a>
  <a href="#s10">10. Regular Expressions</a>
  <p class="nav-group-label">DOM &amp; Browser</p>
  <a href="#s11">11. DOM Manipulation &amp; Traversal</a>
  <a href="#s12">12. Events</a>
  <a href="#s13">13. Browser Storage</a>
  <a href="#s14">14. Browser APIs</a>
  <a href="#s15">15. Forms</a>
  <p class="nav-group-label">HTML &amp; CSS</p>
  <a href="#s16">16. Semantic HTML &amp; Accessibility</a>
  <a href="#s17">17. CSS Selectors &amp; Box Model</a>
  <a href="#s18">18. CSS Layout (Flex &amp; Grid)</a>
  <a href="#s19">19. Responsive Design &amp; Typography</a>
  <a href="#s20">20. CSS Animations &amp; Modern CSS</a>
  <a href="#s21">21. CSS Architecture &amp; Methodologies</a>
  <p class="nav-group-label">TypeScript</p>
  <a href="#s22">22. TypeScript Complete</a>
  <p class="nav-group-label">Performance</p>
  <a href="#s23">23. Loading &amp; Runtime Performance</a>
  <a href="#s24">24. Core Web Vitals &amp; Measurement</a>
  <p class="nav-group-label">Security &amp; Networking</p>
  <a href="#s25">25. Security</a>
  <a href="#s26">26. Networking &amp; APIs</a>
  <p class="nav-group-label">Testing &amp; Build</p>
  <a href="#s27">27. Testing</a>
  <a href="#s28">28. Build Tools &amp; Dev Environment</a>
  <p class="nav-group-label">Design &amp; Architecture</p>
  <a href="#s29">29. Design Patterns</a>
  <a href="#s30">30. System Design</a>
  <a href="#s31">31. DSA for Frontend</a>
  <p class="nav-group-label">Misc</p>
  <a href="#s32">32. Version Control (Git)</a>
  <a href="#s33">33. Web Fundamentals</a>
  <a href="#s34">34. Mobile &amp; PWA</a>
  <a href="#s35">35. Implementation Patterns</a>
  <a href="#s36">36. Additional Topics</a>
  <a href="#s37">37. Soft Skills</a>
</nav>
<main>

<section class="hero avoid-break">
  <h1>Frontend Interview Concepts — Complete Checklist</h1>
  <div class="subtitle">Every concept from Babek Naghiyev's Medium checklist — expanded with theory, real-time use cases, and hands-on code. React sections excluded (Angular-focused coverage in companion guide).</div>
  <p><strong>Source:</strong> <a href="https://nagibaba.medium.com/frontend-interview-concepts-complete-checklist-c928c45b9aa2">Frontend Interview Concepts — Complete Checklist (Medium)</a></p>
  <div class="pill-row">
    <span class="pill">JavaScript Core</span><span class="pill">DOM &amp; Browser</span><span class="pill">HTML</span><span class="pill">CSS</span><span class="pill">TypeScript</span><span class="pill">Performance</span><span class="pill">Security</span><span class="pill">Networking</span><span class="pill">Testing</span><span class="pill">Build Tools</span><span class="pill">Design Patterns</span><span class="pill">System Design</span><span class="pill">DSA</span><span class="pill">Git</span><span class="pill">PWA</span>
  </div>
</section>
"""

# ─── SECTION 1: JS Fundamentals ───────────────────────────────────────
S1 = r"""
<section class="section-break">
<h2 id="s1">1. JavaScript Fundamentals</h2>
<p><strong>Checklist items:</strong> Primitive types, type coercion, strict equality, truthy/falsy, var/let/const, TDZ, hoisting, function declarations vs expressions, arrow functions, IIFE.</p>

<h3>Theory &amp; Concept</h3>
<h4>1.1 Primitive types</h4>
<p>JavaScript has 7 primitives: <code>string</code>, <code>number</code>, <code>boolean</code>, <code>null</code>, <code>undefined</code>, <code>symbol</code>, <code>bigint</code>. Primitives are immutable and compared by value. Everything else is an object (including arrays, functions, dates).</p>

<h4>1.2 Type coercion &amp; strict equality</h4>
<p><code>==</code> performs type coercion before comparison: <code>0 == ''</code> is <code>true</code>. <code>===</code> checks type AND value: <code>0 === ''</code> is <code>false</code>. Always use <code>===</code> unless you have a deliberate reason not to.</p>

<h4>1.3 Truthy &amp; falsy values</h4>
<p>Falsy values: <code>false</code>, <code>0</code>, <code>-0</code>, <code>0n</code>, <code>""</code>, <code>null</code>, <code>undefined</code>, <code>NaN</code>. Everything else is truthy — including <code>[]</code>, <code>{}</code>, <code>"0"</code>, <code>"false"</code>.</p>

<h4>1.4 var, let, const &amp; TDZ</h4>
<table>
<thead><tr><th>Feature</th><th>var</th><th>let</th><th>const</th></tr></thead>
<tbody>
<tr><td>Scope</td><td>Function</td><td>Block</td><td>Block</td></tr>
<tr><td>Hoisting</td><td>Yes (as undefined)</td><td>Yes (in TDZ)</td><td>Yes (in TDZ)</td></tr>
<tr><td>Redeclaration</td><td>Allowed</td><td>Not allowed</td><td>Not allowed</td></tr>
<tr><td>Reassignment</td><td>Allowed</td><td>Allowed</td><td>Not allowed (binding)</td></tr>
</tbody>
</table>
<p><strong>Temporal Dead Zone (TDZ):</strong> The period between entering a block scope and the <code>let</code>/<code>const</code> declaration line. Accessing the variable during TDZ throws <code>ReferenceError</code>.</p>

<h4>1.5 Hoisting</h4>
<p>JavaScript moves declarations to the top of their scope during compilation. <code>var</code> declarations are hoisted and initialized as <code>undefined</code>. <code>function</code> declarations are fully hoisted (you can call them before the declaration). <code>let</code>/<code>const</code> are hoisted but not initialized — they sit in TDZ.</p>

<h4>1.6 Function declarations vs expressions vs arrow functions</h4>
<table>
<thead><tr><th>Type</th><th>Hoisted?</th><th>Has own this?</th><th>Can be constructor?</th></tr></thead>
<tbody>
<tr><td>Declaration: <code>function foo() {}</code></td><td>Yes (fully)</td><td>Yes</td><td>Yes</td></tr>
<tr><td>Expression: <code>const foo = function() {}</code></td><td>No</td><td>Yes</td><td>Yes</td></tr>
<tr><td>Arrow: <code>const foo = () => {}</code></td><td>No</td><td>No (lexical)</td><td>No</td></tr>
</tbody>
</table>

<h4>1.7 IIFE</h4>
<p>Immediately Invoked Function Expression — a function that runs the moment it's defined. Used to create a private scope (before modules existed).</p>

<h3>Real-time Use Cases</h3>
<ul>
<li><strong>const for API configs:</strong> <code>const API_URL = '/api/v1';</code> — prevents accidental reassignment in services.</li>
<li><strong>TDZ in Angular:</strong> Using <code>inject()</code> before the class field initializer runs throws a TDZ-like error because the injection context isn't ready.</li>
<li><strong>Arrow functions in callbacks:</strong> Event handlers and <code>.subscribe()</code> callbacks use arrow functions to preserve <code>this</code> from the enclosing component.</li>
<li><strong>Truthy checks in templates:</strong> Angular's <code>@if (user())</code> relies on truthy evaluation — an empty string or 0 would be falsy.</li>
</ul>

<h3>Hands-on Code</h3>
<pre>// TDZ in action
console.log(x); // undefined (var is hoisted)
// console.log(y); // ReferenceError: Cannot access 'y' before initialization
var x = 1;
let y = 2;

// Type coercion traps
console.log([] == false);    // true  — [] → '' → 0, false → 0
console.log([] === false);   // false — different types
console.log(null == undefined); // true  — special coercion rule
console.log(null === undefined); // false

// IIFE — creating a private counter
const counter = (() => {
  let count = 0;
  return {
    increment: () => ++count,
    getCount: () => count
  };
})();
counter.increment(); // 1
counter.increment(); // 2
counter.getCount();  // 2

// Arrow vs regular function — 'this' difference
class UserService {
  name = 'Angular';

  // Arrow: 'this' is the class instance
  greetArrow = () => console.log(`Hello from ${this.name}`);

  // Regular: 'this' depends on how it's called
  greetRegular() { console.log(`Hello from ${this.name}`); }
}
const svc = new UserService();
const arrowRef = svc.greetArrow;
const regularRef = svc.greetRegular;
arrowRef();   // "Hello from Angular"
regularRef(); // "Hello from undefined" — 'this' is lost!</pre>
</section>
"""

S2 = r"""
<section class="section-break">
<h2 id="s2">2. Scope &amp; Closures</h2>
<p><strong>Checklist items:</strong> Global/function/block scope, lexical scoping, closure creation &amp; use cases, module pattern, private variables through closures, memory implications.</p>

<h3>Theory &amp; Concept</h3>
<p><strong>Scope</strong> determines where variables are accessible. JavaScript has three scope levels: global, function, and block (let/const). <strong>Lexical scoping</strong> means a function's scope is determined by where it is written, not where it is called.</p>
<p><strong>Closure:</strong> When a function retains access to its outer scope's variables even after the outer function has returned. Every function in JavaScript creates a closure.</p>

<h3>Real-time Use Cases</h3>
<ul>
<li><strong>Angular services:</strong> Singleton services are closures — injected deps and private state are enclosed in the service's scope.</li>
<li><strong>Event handlers:</strong> <code>addEventListener</code> callbacks close over component variables.</li>
<li><strong>Factory functions:</strong> Creating multiple instances of a pattern (route guards, validators) where each instance has its own enclosed state.</li>
<li><strong>Debounce/throttle:</strong> Timer IDs are stored in closures to persist between calls.</li>
</ul>

<h3>Hands-on Code</h3>
<pre>// Closure — private state
function createBankAccount(initial) {
  let balance = initial; // private via closure
  return {
    deposit(amount)  { balance += amount; return balance; },
    withdraw(amount) { if (amount > balance) throw Error('Insufficient'); balance -= amount; return balance; },
    getBalance()     { return balance; }
  };
}
const acct = createBankAccount(1000);
acct.deposit(500);    // 1500
acct.withdraw(200);   // 1300
// acct.balance → undefined (private!)

// Closure memory trap — loop with var
for (var i = 0; i < 3; i++) {
  setTimeout(() => console.log(i), 100); // 3, 3, 3 — all share same 'i'
}
// Fix with let (block scope):
for (let i = 0; i < 3; i++) {
  setTimeout(() => console.log(i), 100); // 0, 1, 2

}

// Module pattern — used before ES modules
const Logger = (() => {
  const logs = []; // private
  return {
    log(msg)  { logs.push({ msg, ts: Date.now() }); console.log(msg); },
    history() { return [...logs]; } // return copy, not reference
  };
})();</pre>
</section>
"""

S3 = r"""
<section class="section-break">
<h2 id="s3">3. The <code>this</code> Keyword</h2>
<p><strong>Checklist items:</strong> Implicit binding, explicit binding (call/apply/bind), new binding, arrow function binding, default binding, precedence rules.</p>

<h3>Theory &amp; Concept</h3>
<table>
<thead><tr><th>Rule</th><th>this equals</th><th>Example</th></tr></thead>
<tbody>
<tr><td>Default binding</td><td><code>window</code> (or <code>undefined</code> in strict mode)</td><td><code>foo()</code></td></tr>
<tr><td>Implicit binding</td><td>The object calling the method</td><td><code>obj.foo()</code> → <code>this === obj</code></td></tr>
<tr><td>Explicit binding</td><td>Whatever you pass to call/apply/bind</td><td><code>foo.call(myObj)</code></td></tr>
<tr><td>new binding</td><td>The newly created object</td><td><code>new Foo()</code></td></tr>
<tr><td>Arrow function</td><td>Lexical — inherits from enclosing scope</td><td><code>() => this</code></td></tr>
</tbody>
</table>
<p><strong>Precedence:</strong> new &gt; explicit (call/apply/bind) &gt; implicit (obj.method) &gt; default.</p>

<h3>Real-time Use Cases</h3>
<ul>
<li><strong>Angular component methods:</strong> Template event handlers (<code>(click)="onClick()"</code>) are called as implicit binding — <code>this</code> is the component instance.</li>
<li><strong>Callbacks losing this:</strong> Passing <code>this.handleClick</code> as a callback loses the binding. Arrow functions or <code>.bind(this)</code> fix it.</li>
<li><strong>RxJS tap/subscribe:</strong> Arrow functions in <code>.pipe(tap(() => this.data.set(...)))</code> preserve component <code>this</code>.</li>
</ul>

<h3>Hands-on Code</h3>
<pre>// All four bindings
const person = {
  name: 'Sid',
  greet() { console.log(`Hi, I'm ${this.name}`); }
};

person.greet();             // Implicit: "Hi, I'm Sid"
person.greet.call({ name: 'Raj' }); // Explicit: "Hi, I'm Raj"

function Person(name) { this.name = name; }
const p = new Person('Dev'); // new binding: p.name === 'Dev'

const fn = person.greet;
fn();                       // Default: "Hi, I'm undefined" (strict mode)

// bind — creating a permanently bound function
const boundGreet = person.greet.bind({ name: 'Bound' });
boundGreet(); // "Hi, I'm Bound" — even if called as a standalone function

// call vs apply
function sum(a, b) { return a + b; }
sum.call(null, 1, 2);    // 3 — args passed individually
sum.apply(null, [1, 2]); // 3 — args passed as array</pre>
</section>
"""

S4 = r"""
<section class="section-break">
<h2 id="s4">4. Prototypes &amp; Inheritance</h2>
<p><strong>Checklist items:</strong> Prototype chain, __proto__ vs prototype, Object.create(), constructor functions, class syntax, prototypal inheritance, hasOwnProperty(), Object.getPrototypeOf().</p>

<h3>Theory &amp; Concept</h3>
<p>JavaScript uses prototypal inheritance — objects inherit from other objects via the prototype chain. When you access a property, JS looks on the object first, then walks up <code>__proto__</code> links until it reaches <code>null</code>.</p>
<p><code>class</code> is syntactic sugar over prototype-based inheritance. Angular components, services, and directives use <code>class</code> syntax, but under the hood it's all prototypes.</p>

<h3>Hands-on Code</h3>
<pre>// Prototype chain in action
function Animal(name) { this.name = name; }
Animal.prototype.speak = function() { return `${this.name} makes a sound`; };

function Dog(name, breed) {
  Animal.call(this, name); // call parent constructor
  this.breed = breed;
}
Dog.prototype = Object.create(Animal.prototype); // inherit methods
Dog.prototype.constructor = Dog;
Dog.prototype.bark = function() { return `${this.name} barks!`; };

const d = new Dog('Rex', 'Labrador');
d.speak(); // "Rex makes a sound" — inherited from Animal
d.bark();  // "Rex barks!" — own method
d.hasOwnProperty('name');  // true
d.hasOwnProperty('speak'); // false — it's on the prototype

// Same thing with class syntax (Angular style)
class Vehicle {
  constructor(public make: string) {}
  describe() { return `Vehicle: ${this.make}`; }
}
class Car extends Vehicle {
  constructor(make: string, public model: string) { super(make); }
  describe() { return `${this.make} ${this.model}`; }
}
// Object.getPrototypeOf(new Car('Toyota','Camry')) === Car.prototype</pre>
</section>
"""

S5 = r"""
<section class="section-break">
<h2 id="s5">5. Asynchronous JavaScript</h2>
<p><strong>Checklist items:</strong> Callbacks, callback hell, Promises (states, methods), Promise.all/race/allSettled/any, async/await, try/catch, microtasks vs macrotasks, event loop phases, call stack, task queue, setTimeout/setInterval, requestAnimationFrame.</p>

<h3>Theory &amp; Concept</h3>
<p>JavaScript is single-threaded with an event loop. The <strong>call stack</strong> executes synchronous code. When async operations complete, their callbacks go to either the <strong>microtask queue</strong> (Promises, queueMicrotask, MutationObserver) or the <strong>macrotask queue</strong> (setTimeout, setInterval, I/O, UI events). The event loop processes all microtasks before any macrotask.</p>

<h4>Promise states</h4>
<table>
<thead><tr><th>State</th><th>Description</th><th>Transitions to</th></tr></thead>
<tbody>
<tr><td>pending</td><td>Initial state, operation in progress</td><td>fulfilled or rejected</td></tr>
<tr><td>fulfilled</td><td>Operation completed successfully</td><td>Final — cannot change</td></tr>
<tr><td>rejected</td><td>Operation failed</td><td>Final — cannot change</td></tr>
</tbody>
</table>

<h4>Promise static methods</h4>
<table>
<thead><tr><th>Method</th><th>Behavior</th><th>Use case</th></tr></thead>
<tbody>
<tr><td>Promise.all</td><td>Resolves when ALL resolve; rejects on first rejection</td><td>Parallel API calls where all are needed</td></tr>
<tr><td>Promise.race</td><td>Resolves/rejects with the FIRST settled promise</td><td>Timeout pattern</td></tr>
<tr><td>Promise.allSettled</td><td>Waits for ALL to settle (fulfilled or rejected)</td><td>Batch operations where partial success is OK</td></tr>
<tr><td>Promise.any</td><td>Resolves with first FULFILLED; rejects only if ALL reject</td><td>Fastest CDN, fallback APIs</td></tr>
</tbody>
</table>

<h3>Real-time Use Cases</h3>
<ul>
<li><strong>forkJoin in Angular:</strong> Like Promise.all — waits for all HTTP calls on a dashboard page.</li>
<li><strong>Race condition in search:</strong> switchMap cancels previous requests — similar to Promise.race logic.</li>
<li><strong>requestAnimationFrame:</strong> Smooth animations outside Angular zone, canvas rendering.</li>
</ul>

<h3>Hands-on Code</h3>
<pre>// Event loop — predict the output
console.log('1');
setTimeout(() => console.log('2'), 0);
Promise.resolve().then(() => console.log('3'));
queueMicrotask(() => console.log('4'));
console.log('5');
// Output: 1, 5, 3, 4, 2
// Sync first (1, 5), then microtasks (3, 4), then macrotask (2)

// Promise.allSettled — batch API calls
const results = await Promise.allSettled([
  fetch('/api/users'),
  fetch('/api/orders'),
  fetch('/api/broken-endpoint')
]);
results.forEach((result, i) => {
  if (result.status === 'fulfilled') {
    console.log(`API ${i}: Success`);
  } else {
    console.log(`API ${i}: Failed — ${result.reason}`);
  }
});

// Async/await with error handling
async function fetchUserData(id) {
  try {
    const response = await fetch(`/api/users/${id}`);
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    return await response.json();
  } catch (error) {
    console.error('Failed to fetch user:', error.message);
    return null; // graceful fallback
  }
}

// requestAnimationFrame — smooth scroll progress
function updateProgressBar() {
  const scrollTop = document.documentElement.scrollTop;
  const scrollHeight = document.documentElement.scrollHeight - window.innerHeight;
  const progress = (scrollTop / scrollHeight) * 100;
  document.getElementById('progress').style.width = `${progress}%`;
  requestAnimationFrame(updateProgressBar);
}
requestAnimationFrame(updateProgressBar);</pre>
</section>
"""

S6 = r"""
<section class="section-break">
<h2 id="s6">6. ES6+ Features</h2>
<p><strong>Checklist items:</strong> Destructuring, spread/rest, template literals, default params, enhanced object literals, computed property names, for...of, iterators &amp; generators, Symbol, Map/Set, WeakMap/WeakSet, optional chaining, nullish coalescing, logical assignment operators.</p>

<h3>Hands-on Code</h3>
<pre>// Destructuring — nested + rename + defaults
const { name: userName, address: { city = 'Unknown' } = {} } = user;

// Spread — immutable updates (critical for Angular signals)
const updated = { ...state, items: [...state.items, newItem] };

// Optional chaining + nullish coalescing
const street = user?.address?.street ?? 'No street provided';

// Map — when keys are not strings
const permissions = new Map&lt;string, Set&lt;string&gt;&gt;();
permissions.set('admin', new Set(['read', 'write', 'delete']));
permissions.set('viewer', new Set(['read']));
permissions.get('admin')?.has('write'); // true

// WeakMap — private data without memory leaks
const privateData = new WeakMap();
class MyComponent {
  constructor() { privateData.set(this, { secret: 42 }); }
  getSecret() { return privateData.get(this)?.secret; }
}
// When MyComponent instance is GC'd, WeakMap entry is also removed

// Generator — lazy sequence
function* fibonacci() {
  let [a, b] = [0, 1];
  while (true) { yield a; [a, b] = [b, a + b]; }
}
const fib = fibonacci();
fib.next().value; // 0
fib.next().value; // 1
fib.next().value; // 1
fib.next().value; // 2

// Logical assignment
let config = { timeout: 0, retries: null };
config.timeout ||= 3000;  // stays 0 (||= checks falsy, 0 is falsy!) 
config.timeout ??= 3000;  // stays 0 (??= checks null/undefined only)
config.retries ??= 3;     // becomes 3 (null is nullish)</pre>

<h3>Real-time Use Cases</h3>
<ul>
<li><strong>Destructuring in Angular:</strong> <code>const { data, error } = result;</code> — extracting HTTP response parts.</li>
<li><strong>Spread for immutable signal updates:</strong> <code>items.update(list => [...list, newItem])</code>.</li>
<li><strong>Optional chaining in templates:</strong> <code>user()?.address?.city</code> prevents null reference errors.</li>
<li><strong>Map for caching:</strong> RxJS <code>shareReplay</code> internally uses Map-like structures.</li>
</ul>
</section>
"""

S7 = r"""
<section class="section-break">
<h2 id="s7">7. Advanced JavaScript Concepts</h2>
<p><strong>Checklist items:</strong> Higher-order functions, pure functions, function composition, currying, partial application, memoization, recursion, debouncing, throttling, Proxy &amp; Reflect, property descriptors, Object.defineProperty, getters/setters, immutability.</p>

<h3>Hands-on Code</h3>

<h4>Currying</h4>
<pre>// Currying — transforms f(a, b, c) into f(a)(b)(c)
const multiply = (a) => (b) => a * b;
const double = multiply(2);
const triple = multiply(3);
double(5); // 10
triple(5); // 15

// Real use: creating reusable validators
const minLength = (min) => (value) => value.length >= min;
const isValidPassword = minLength(8);
isValidPassword('abc');       // false
isValidPassword('securePass'); // true</pre>

<h4>Debounce &amp; Throttle</h4>
<pre>// Debounce — delays execution until pause in calls
function debounce(fn, delay) {
  let timer;
  return function(...args) {
    clearTimeout(timer);
    timer = setTimeout(() => fn.apply(this, args), delay);
  };
}
// Use case: search input — API call only after user stops typing
const debouncedSearch = debounce((term) => fetchResults(term), 300);

// Throttle — max one execution per interval
function throttle(fn, limit) {
  let lastCall = 0;
  return function(...args) {
    const now = Date.now();
    if (now - lastCall >= limit) {
      lastCall = now;
      fn.apply(this, args);
    }
  };
}
// Use case: scroll handler — fire at most once per 100ms
window.addEventListener('scroll', throttle(handleScroll, 100));</pre>

<h4>Memoization</h4>
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
const expensiveCalc = memoize((n) => {
  console.log('Computing...');
  return n * n;
});
expensiveCalc(5); // "Computing..." → 25
expensiveCalc(5); // 25 (cached, no log)</pre>

<h4>Proxy</h4>
<pre>// Proxy — intercept object operations
const validated = new Proxy({}, {
  set(target, prop, value) {
    if (prop === 'age' && (typeof value !== 'number' || value < 0)) {
      throw new TypeError('Age must be a positive number');
    }
    target[prop] = value;
    return true;
  }
});
validated.age = 25;  // OK
// validated.age = -5; // TypeError!

// Real use: Angular signals internally use Proxy-like patterns
// to track reads and notify consumers of changes.</pre>
</section>
"""

S8 = r"""
<section class="section-break">
<h2 id="s8">8. Array &amp; Object Methods</h2>
<p><strong>Checklist items:</strong> map, filter, reduce, forEach, some, every, find, findIndex, slice, splice, concat, join, split, sort, flat, flatMap, Array.from/of, includes, indexOf. Object.keys/values/entries, Object.assign, Object.freeze/seal, Object.is, shallow vs deep cloning.</p>

<h3>Hands-on Code</h3>
<pre>// Real-world data pipeline — Angular service processing API data
const orders = [
  { id: 1, status: 'completed', total: 150, items: [{ name: 'A' }, { name: 'B' }] },
  { id: 2, status: 'pending', total: 80, items: [{ name: 'C' }] },
  { id: 3, status: 'completed', total: 220, items: [{ name: 'D' }, { name: 'E' }, { name: 'F' }] }
];

// Total revenue from completed orders
const revenue = orders
  .filter(o => o.status === 'completed')
  .reduce((sum, o) => sum + o.total, 0); // 370

// All item names from all orders (flatMap)
const allItems = orders.flatMap(o => o.items.map(i => i.name)); // ['A','B','C','D','E','F']

// sort — custom comparator (by total, descending)
const sorted = [...orders].sort((a, b) => b.total - a.total);

// Shallow vs deep clone
const original = { a: 1, nested: { b: 2 } };
const shallow = { ...original };
shallow.nested.b = 99;
console.log(original.nested.b); // 99 — shared reference!

const deep = structuredClone(original); // Deep clone (modern)
deep.nested.b = 100;
console.log(original.nested.b); // 99 — independent

// Object.freeze — immutable config
const CONFIG = Object.freeze({
  API_URL: '/api/v1',
  TIMEOUT: 5000
});
// CONFIG.API_URL = '/api/v2'; // silently fails (throws in strict mode)

// Object.entries → Map
const userMap = new Map(Object.entries({ alice: 1, bob: 2, charlie: 3 }));</pre>
</section>
"""

S9 = r"""
<section class="section-break">
<h2 id="s9">9. Error Handling &amp; Modules</h2>
<p><strong>Checklist items:</strong> try/catch/finally, error types, custom error classes, error propagation, async error handling, ES6 modules, named/default exports, dynamic imports, CommonJS, module bundling.</p>

<h3>Hands-on Code</h3>
<pre>// Custom error class
class ApiError extends Error {
  constructor(public statusCode: number, message: string, public endpoint: string) {
    super(message);
    this.name = 'ApiError';
  }
}

// Usage with async/await
async function fetchData(url) {
  try {
    const res = await fetch(url);
    if (!res.ok) throw new ApiError(res.status, res.statusText, url);
    return await res.json();
  } catch (error) {
    if (error instanceof ApiError) {
      console.error(`API ${error.statusCode} at ${error.endpoint}: ${error.message}`);
    } else if (error instanceof TypeError) {
      console.error('Network error — are you offline?');
    } else {
      throw error; // re-throw unknown errors
    }
  } finally {
    hideLoadingSpinner(); // always runs
  }
}

// Dynamic import — lazy loading a heavy library
async function renderChart(data) {
  const { Chart } = await import('chart.js'); // loaded on demand
  new Chart(canvas, { type: 'bar', data });
}

// Named vs default exports
// utils.ts
export function formatDate(d) { /* ... */ }  // named
export function formatCurrency(n) { /* ... */ } // named
export default class ApiService { /* ... */ }   // default

// Importing
import ApiService from './utils';                    // default
import { formatDate, formatCurrency } from './utils'; // named
import * as Utils from './utils';                     // namespace</pre>
</section>
"""

S10 = r"""
<section>
<h2 id="s10">10. Regular Expressions</h2>
<p><strong>Checklist items:</strong> Pattern matching, flags (g, i, m, s, u, y), character classes, quantifiers, groups &amp; capturing, lookahead/lookbehind, string methods (match, search, replace, split).</p>

<h3>Hands-on Code</h3>
<pre>// Email validation
const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
emailRegex.test('user@example.com'); // true

// Phone number formatting
const phone = '1234567890';
phone.replace(/(\d{3})(\d{3})(\d{4})/, '($1) $2-$3'); // "(123) 456-7890"

// Named groups
const dateStr = '2024-03-15';
const { groups: { year, month, day } } =
  dateStr.match(/(?&lt;year&gt;\d{4})-(?&lt;month&gt;\d{2})-(?&lt;day&gt;\d{2})/);
// year='2024', month='03', day='15'

// Lookahead — password validation
// At least 8 chars, 1 uppercase, 1 lowercase, 1 digit, 1 special char
const strongPassword = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/;
strongPassword.test('Str0ng@Pass'); // true

// replace with function
const template = 'Hello {{name}}, welcome to {{city}}!';
const data = { name: 'Sid', city: 'Bengaluru' };
const result = template.replace(/\{\{(\w+)\}\}/g, (_, key) => data[key] || '');
// "Hello Sid, welcome to Bengaluru!"</pre>

<h3>Real-time Use Cases</h3>
<ul>
<li><strong>Form validation:</strong> Custom Angular validators use regex for email, phone, password patterns.</li>
<li><strong>Search highlighting:</strong> Replace matched text with <code>&lt;mark&gt;</code> tags for search results.</li>
<li><strong>URL parsing:</strong> Extract route params, query strings from URLs.</li>
<li><strong>Template engines:</strong> Angular's template compiler uses regex-like parsing for interpolation.</li>
</ul>
</section>
"""

# DOM & BROWSER
S11 = r"""
<section class="section-break">
<h2 id="s11">11. DOM Manipulation &amp; Traversal</h2>
<p><strong>Checklist items:</strong> getElementById, querySelector, querySelectorAll, createElement, appendChild, removeChild, insertBefore, cloneNode, innerHTML vs textContent vs innerText, classList, setAttribute, dataset, DocumentFragment. Traversal: parentNode, children, firstElementChild, siblings, closest().</p>

<h3>Hands-on Code</h3>
<pre>// Efficient batch DOM updates with DocumentFragment
const fragment = document.createDocumentFragment();
for (let i = 0; i < 1000; i++) {
  const li = document.createElement('li');
  li.textContent = `Item ${i}`;
  li.dataset.index = i; // data-index attribute
  fragment.appendChild(li);
}
document.getElementById('list').appendChild(fragment);
// Only ONE reflow instead of 1000!

// DOM traversal
const card = document.querySelector('.product-card');
const title = card.querySelector('h3');        // child search
const container = card.closest('.grid');         // ancestor search
const nextCard = card.nextElementSibling;        // sibling
const allCards = card.parentElement.children;     // all siblings

// innerHTML vs textContent (XSS risk!)
element.textContent = userInput;   // SAFE — escapes HTML
element.innerHTML = userInput;     // DANGEROUS — executes HTML/scripts!

// classList for toggling states
const btn = document.querySelector('.btn');
btn.classList.add('loading');
btn.classList.remove('loading');
btn.classList.toggle('active');
btn.classList.contains('active'); // true/false</pre>

<h3>Real-time Use Cases</h3>
<ul>
<li><strong>Angular Renderer2:</strong> Angular wraps DOM manipulation via <code>Renderer2</code> for SSR compatibility — never use <code>document.querySelector</code> directly in Angular components.</li>
<li><strong>DocumentFragment:</strong> Angular's compiler creates fragments for structural directives like <code>@for</code>.</li>
<li><strong>closest():</strong> Event delegation — clicking any child of a list, use <code>event.target.closest('li')</code> to find the list item.</li>
</ul>
</section>
"""

S12 = r"""
<section class="section-break">
<h2 id="s12">12. Events</h2>
<p><strong>Checklist items:</strong> addEventListener/removeEventListener, event object (target, currentTarget, type), bubbling, capturing, event delegation, stopPropagation, preventDefault, keyboard/mouse/touch events, passive listeners, CustomEvent &amp; dispatchEvent.</p>

<h3>Theory &amp; Concept</h3>
<p>Events flow in three phases: <strong>Capturing</strong> (window → target), <strong>Target</strong> (event fires on target), <strong>Bubbling</strong> (target → window). By default, listeners fire during bubbling. Use <code>{ capture: true }</code> for the capture phase.</p>
<p><strong>Event delegation:</strong> Instead of adding listeners to 100 list items, add one listener to the parent and check <code>event.target</code>. This is more efficient and works for dynamically added elements.</p>

<h3>Hands-on Code</h3>
<pre>// Event delegation — one listener for many items
document.getElementById('product-list').addEventListener('click', (e) => {
  const card = e.target.closest('[data-product-id]');
  if (!card) return;
  const productId = card.dataset.productId;
  navigateToProduct(productId);
});

// Custom events — cross-component communication (vanilla JS)
// In micro-frontend or Web Component architecture
const cartEvent = new CustomEvent('cart:updated', {
  bubbles: true,
  detail: { itemCount: 5, total: 2499 }
});
document.dispatchEvent(cartEvent);

// Listen anywhere in the app
document.addEventListener('cart:updated', (e) => {
  console.log('Cart count:', e.detail.itemCount);
});

// Passive listener — improves scroll performance
document.addEventListener('scroll', handleScroll, { passive: true });
// Tells the browser: "I won't call preventDefault() — you can optimize scrolling"

// Cleanup — preventing memory leaks
const controller = new AbortController();
element.addEventListener('click', handler, { signal: controller.signal });
// Later: controller.abort() removes ALL listeners registered with this signal</pre>
</section>
"""

S13 = r"""
<section class="section-break">
<h2 id="s13">13. Browser Storage</h2>
<p><strong>Checklist items:</strong> localStorage, sessionStorage, storage events, cookies (attributes: expires, max-age, domain, path, secure, SameSite), IndexedDB basics.</p>

<h3>Theory &amp; Concept</h3>
<table>
<thead><tr><th>Storage</th><th>Capacity</th><th>Lifetime</th><th>Accessible from</th><th>Sent with requests?</th></tr></thead>
<tbody>
<tr><td>localStorage</td><td>~5-10MB</td><td>Until cleared</td><td>Same origin</td><td>No</td></tr>
<tr><td>sessionStorage</td><td>~5-10MB</td><td>Until tab closes</td><td>Same tab + origin</td><td>No</td></tr>
<tr><td>Cookies</td><td>~4KB</td><td>Configurable (expires)</td><td>Same origin + path</td><td>Yes (every request!)</td></tr>
<tr><td>IndexedDB</td><td>50MB+</td><td>Until cleared</td><td>Same origin</td><td>No</td></tr>
</tbody>
</table>

<h3>Hands-on Code</h3>
<pre>// localStorage — persisting user preferences
const prefs = { theme: 'dark', lang: 'en', fontSize: 14 };
localStorage.setItem('user-prefs', JSON.stringify(prefs));
const saved = JSON.parse(localStorage.getItem('user-prefs') ?? '{}');

// Cookie with security attributes
document.cookie = `token=abc123; Secure; SameSite=Strict; HttpOnly; max-age=3600; path=/`;
// Note: HttpOnly cookies cannot be set via JS — they must be set by the server
// The above is for illustration. In practice, set HttpOnly cookies server-side.

// Storage event — cross-tab sync
window.addEventListener('storage', (e) => {
  if (e.key === 'user-prefs') {
    applyPreferences(JSON.parse(e.newValue));
  }
});</pre>

<h3>Real-time Use Cases</h3>
<ul>
<li><strong>Angular theme service:</strong> Save dark/light mode preference in localStorage, sync across tabs via storage event.</li>
<li><strong>JWT storage:</strong> HttpOnly cookies (secure) vs localStorage (convenient but XSS-vulnerable). Use cookies for auth tokens.</li>
<li><strong>IndexedDB:</strong> Offline-first apps store large datasets (product catalogs, cached API responses) in IndexedDB.</li>
</ul>
</section>
"""

S14 = r"""
<section class="section-break">
<h2 id="s14">14. Browser APIs</h2>
<p><strong>Checklist items:</strong> Fetch API, XMLHttpRequest, Geolocation, History API, Web Workers, Service Workers, IntersectionObserver, MutationObserver, ResizeObserver, Performance API, requestIdleCallback, Page Visibility, Clipboard API, Notification API, Drag &amp; Drop, window/document properties, DOMContentLoaded vs load, getBoundingClientRect.</p>

<h3>Hands-on Code</h3>
<pre>// IntersectionObserver — lazy load images
const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      const img = entry.target;
      img.src = img.dataset.src; // load real image
      observer.unobserve(img);   // stop observing
    }
  });
}, { rootMargin: '200px' }); // start loading 200px before visible

document.querySelectorAll('img[data-src]').forEach(img => observer.observe(img));

// ResizeObserver — responsive component without media queries
const resizeObserver = new ResizeObserver(entries => {
  for (const entry of entries) {
    const width = entry.contentRect.width;
    entry.target.classList.toggle('compact', width < 400);
  }
});
resizeObserver.observe(document.querySelector('.dashboard-widget'));

// Page Visibility — pause expensive operations when tab is hidden
document.addEventListener('visibilitychange', () => {
  if (document.hidden) {
    pausePolling();   // stop API polling when user switches tab
  } else {
    resumePolling();  // resume when they come back
  }
});

// Clipboard API
async function copyToClipboard(text) {
  await navigator.clipboard.writeText(text);
  showToast('Copied!');
}

// Performance API — measure custom timings
performance.mark('api-start');
await fetch('/api/data');
performance.mark('api-end');
performance.measure('api-call', 'api-start', 'api-end');
const duration = performance.getEntriesByName('api-call')[0].duration;
console.log(`API call took ${duration.toFixed(2)}ms`);</pre>
</section>
"""

S15 = r"""
<section>
<h2 id="s15">15. Forms</h2>
<p><strong>Checklist items:</strong> Form validation, Constraint Validation API, FormData API, input types &amp; attributes, form events (submit, reset, invalid).</p>

<h3>Hands-on Code</h3>
<pre>// FormData — reading form values without manual DOM queries
const form = document.querySelector('form');
form.addEventListener('submit', (e) => {
  e.preventDefault();
  const data = new FormData(form);
  const payload = Object.fromEntries(data.entries());
  // { name: 'Sid', email: 'sid@example.com', ... }
  fetch('/api/submit', { method: 'POST', body: JSON.stringify(payload) });
});

// Constraint Validation API — custom validation messages
const emailInput = document.querySelector('#email');
emailInput.addEventListener('invalid', (e) => {
  if (emailInput.validity.typeMismatch) {
    emailInput.setCustomValidity('Please enter a valid email address');
  }
});
emailInput.addEventListener('input', () => {
  emailInput.setCustomValidity(''); // clear on input
});

// Custom validation with reportValidity()
function validateAge(input) {
  const age = parseInt(input.value);
  if (age < 18) {
    input.setCustomValidity('Must be 18 or older');
    input.reportValidity();
    return false;
  }
  input.setCustomValidity('');
  return true;
}</pre>
</section>
"""

# HTML & CSS
S16 = r"""
<section class="section-break">
<h2 id="s16">16. Semantic HTML &amp; Accessibility</h2>
<p><strong>Checklist items:</strong> Semantic elements (header, nav, main, article, section, aside, footer, figure, details/summary), HTML5 features (data attributes, contenteditable, input types), metadata &amp; SEO (meta tags, Open Graph, JSON-LD), media elements (video, audio, picture, srcset), ARIA (roles, attributes, live regions, landmarks), label associations, tabindex, skip links.</p>

<h3>Hands-on Code</h3>
<pre>&lt;!-- Semantic page structure --&gt;
&lt;header&gt;
  &lt;nav aria-label="Main navigation"&gt;
    &lt;a href="#main-content" class="skip-link"&gt;Skip to content&lt;/a&gt;
    &lt;ul role="list"&gt;
      &lt;li&gt;&lt;a href="/dashboard"&gt;Dashboard&lt;/a&gt;&lt;/li&gt;
      &lt;li&gt;&lt;a href="/products"&gt;Products&lt;/a&gt;&lt;/li&gt;
    &lt;/ul&gt;
  &lt;/nav&gt;
&lt;/header&gt;

&lt;main id="main-content"&gt;
  &lt;article&gt;
    &lt;h1&gt;Product Details&lt;/h1&gt;
    &lt;figure&gt;
      &lt;picture&gt;
        &lt;source srcset="product.avif" type="image/avif"&gt;
        &lt;source srcset="product.webp" type="image/webp"&gt;
        &lt;img src="product.jpg" alt="Red running shoes, side view"
             loading="lazy" width="600" height="400"&gt;
      &lt;/picture&gt;
      &lt;figcaption&gt;Nike Air Max 2024&lt;/figcaption&gt;
    &lt;/figure&gt;
    &lt;details&gt;
      &lt;summary&gt;Shipping Information&lt;/summary&gt;
      &lt;p&gt;Free shipping on orders over ₹999.&lt;/p&gt;
    &lt;/details&gt;
  &lt;/article&gt;
&lt;/main&gt;

&lt;!-- Accessible form --&gt;
&lt;form&gt;
  &lt;fieldset&gt;
    &lt;legend&gt;Contact Information&lt;/legend&gt;
    &lt;label for="name"&gt;Name &lt;span aria-hidden="true"&gt;*&lt;/span&gt;&lt;/label&gt;
    &lt;input id="name" type="text" required aria-required="true"&gt;
    &lt;label for="email"&gt;Email&lt;/label&gt;
    &lt;input id="email" type="email" aria-describedby="email-help"&gt;
    &lt;small id="email-help"&gt;We'll never share your email.&lt;/small&gt;
  &lt;/fieldset&gt;
&lt;/form&gt;

&lt;!-- SEO meta tags --&gt;
&lt;head&gt;
  &lt;meta name="description" content="Buy running shoes online"&gt;
  &lt;meta property="og:title" content="Nike Air Max 2024"&gt;
  &lt;meta property="og:image" content="https://example.com/product.jpg"&gt;
  &lt;link rel="canonical" href="https://example.com/products/air-max-2024"&gt;
  &lt;script type="application/ld+json"&gt;
  { "@context": "https://schema.org", "@type": "Product",
    "name": "Nike Air Max 2024", "offers": { "@type": "Offer", "price": "8999" }}
  &lt;/script&gt;
&lt;/head&gt;</pre>
</section>
"""

S17 = r"""
<section class="section-break">
<h2 id="s17">17. CSS Selectors &amp; Box Model</h2>
<p><strong>Checklist items:</strong> Type/class/ID/attribute selectors, pseudo-classes (:hover, :focus, :nth-child, :is, :where, :has, :not), pseudo-elements (::before, ::after), combinators, specificity. Box model (content, padding, border, margin), box-sizing, margin collapse, negative margins.</p>

<h3>Theory &amp; Concept</h3>
<h4>Specificity calculation</h4>
<table>
<thead><tr><th>Selector type</th><th>Weight</th><th>Example</th></tr></thead>
<tbody>
<tr><td>Inline styles</td><td>1000</td><td><code>style="color:red"</code></td></tr>
<tr><td>ID</td><td>100</td><td><code>#header</code></td></tr>
<tr><td>Class, attribute, pseudo-class</td><td>10</td><td><code>.card</code>, <code>[type="text"]</code>, <code>:hover</code></td></tr>
<tr><td>Element, pseudo-element</td><td>1</td><td><code>div</code>, <code>::before</code></td></tr>
<tr><td><code>:where()</code></td><td>0</td><td>Always 0 specificity — great for defaults</td></tr>
<tr><td><code>:is()</code></td><td>Highest within</td><td>Takes specificity of most specific argument</td></tr>
</tbody>
</table>

<h4>Margin collapse</h4>
<p>Vertical margins of adjacent block elements collapse — the larger margin wins. Horizontal margins never collapse. Margin collapse does NOT happen with: flexbox items, grid items, floated elements, absolute/fixed positioned elements, or elements with <code>overflow</code> other than <code>visible</code>.</p>

<h3>Hands-on Code</h3>
<pre>/* :has() — parent selector (modern CSS) */
/* Style a card differently when it contains an image */
.card:has(img) {
  grid-template-rows: 200px auto;
}

/* :is() — grouping selectors without specificity issues */
:is(h1, h2, h3, h4) {
  font-family: 'Avenir Next', sans-serif;
  color: #152923;
}

/* :where() — zero specificity base styles (easily overridable) */
:where(.btn) {
  padding: 8px 16px;
  border-radius: 6px;
}

/* Box model */
.card {
  box-sizing: border-box; /* width includes padding + border */
  width: 300px;
  padding: 16px;
  border: 1px solid #ccc;
  /* Actual content width = 300 - 32 - 2 = 266px */
}

/* Negative margin — overlapping elements */
.badge {
  margin-top: -12px; /* pulls element up, overlapping previous */
  margin-left: -8px;
}</pre>
</section>
"""

S18 = r"""
<section class="section-break">
<h2 id="s18">18. CSS Layout — Flexbox &amp; Grid</h2>
<p><strong>Checklist items:</strong> Flexbox (direction, wrap, justify-content, align-items, flex-grow/shrink/basis, align-self, order, gap). Grid (template-columns/rows, template-areas, fr, repeat, minmax, auto-fill/fit, placement, implicit grid, named lines, place-items).</p>

<h3>Hands-on Code</h3>
<pre>/* Flexbox — responsive navbar */
.navbar {
  display: flex;
  justify-content: space-between; /* logo left, nav right */
  align-items: center;
  gap: 16px;
  flex-wrap: wrap; /* wraps on small screens */
}

.nav-links {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
}

/* Flexbox — card with footer pushed to bottom */
.card {
  display: flex;
  flex-direction: column;
  height: 100%;
}
.card-body { flex: 1; } /* takes remaining space */
.card-footer { margin-top: auto; } /* pushed to bottom */

/* Grid — responsive product grid (no media queries!) */
.product-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 24px;
}

/* Grid — dashboard layout with named areas */
.dashboard {
  display: grid;
  grid-template-areas:
    "header  header"
    "sidebar main"
    "sidebar footer";
  grid-template-columns: 250px 1fr;
  grid-template-rows: 60px 1fr 40px;
  min-height: 100vh;
}
.header  { grid-area: header; }
.sidebar { grid-area: sidebar; }
.main    { grid-area: main; }
.footer  { grid-area: footer; }

/* auto-fill vs auto-fit */
/* auto-fill: creates empty tracks when space is available */
/* auto-fit:  collapses empty tracks, stretching existing items */
.auto-fill { grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); }
.auto-fit  { grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); }</pre>
</section>
"""

S19 = r"""
<section class="section-break">
<h2 id="s19">19. Responsive Design &amp; Typography</h2>
<p><strong>Checklist items:</strong> Media queries, mobile-first, breakpoints, fluid typography, container queries, clamp()/min()/max(), aspect-ratio. Typography: font-family, line-height, @font-face, font-display, WOFF2, system font stacks, variable fonts. Colors &amp; backgrounds: hex/rgb/hsl, currentColor, gradients, opacity.</p>

<h3>Hands-on Code</h3>
<pre>/* Fluid typography with clamp — no media queries needed */
h1 { font-size: clamp(1.5rem, 4vw + 0.5rem, 3rem); }
p  { font-size: clamp(0.9rem, 1.5vw + 0.5rem, 1.1rem); }

/* Container queries — responsive to parent, not viewport */
.card-container { container-type: inline-size; }

@container (min-width: 400px) {
  .card { display: flex; gap: 16px; }
}
@container (max-width: 399px) {
  .card { display: block; }
  .card img { width: 100%; }
}

/* Font loading strategy */
@font-face {
  font-family: 'Inter';
  src: url('/fonts/inter.woff2') format('woff2');
  font-display: swap;     /* show fallback immediately, swap when loaded */
  font-weight: 100 900;   /* variable font range */
  unicode-range: U+0000-00FF; /* subset: latin only */
}

/* System font stack — fastest possible (no download) */
body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto,
               'Helvetica Neue', Arial, sans-serif;
}

/* Modern gradient background */
.hero {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

/* Aspect ratio — responsive video/images */
.video-wrapper {
  aspect-ratio: 16 / 9;
  width: 100%;
}
.avatar {
  aspect-ratio: 1 / 1;    /* perfect square */
  border-radius: 50%;
  object-fit: cover;
}</pre>
</section>
"""

S20 = r"""
<section class="section-break">
<h2 id="s20">20. CSS Animations &amp; Modern CSS</h2>
<p><strong>Checklist items:</strong> Transforms (translate, rotate, scale, skew), 3D transforms, transitions, @keyframes, will-change, GPU acceleration. CSS variables (custom properties, var(), scope, JS manipulation). Modern CSS: subgrid, logical properties, scroll-snap, backdrop-filter, mix-blend-mode, filter, clip-path, shape-outside.</p>

<h3>Hands-on Code</h3>
<pre>/* Performant animation — only transform + opacity (GPU layer) */
.card {
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.card:hover {
  transform: translateY(-4px) scale(1.02);
  box-shadow: 0 12px 24px rgba(0,0,0,0.1);
}

/* Keyframe animation — loading spinner */
@keyframes spin {
  from { transform: rotate(0deg); }
  to   { transform: rotate(360deg); }
}
.spinner {
  width: 24px; height: 24px;
  border: 3px solid #e0e0e0;
  border-top-color: #0f6b5f;
  border-radius: 50%;
  animation: spin 0.6s linear infinite;
}

/* CSS variables — theming */
:root {
  --color-primary: #0f6b5f;
  --color-bg: #fffdf8;
  --radius: 8px;
}
[data-theme="dark"] {
  --color-primary: #8bf0cc;
  --color-bg: #1a1a2e;
}
.btn {
  background: var(--color-primary);
  border-radius: var(--radius);
}

/* Toggle theme with JS */
document.documentElement.dataset.theme =
  document.documentElement.dataset.theme === 'dark' ? 'light' : 'dark';

/* Scroll snap — carousel without JS */
.carousel {
  display: flex;
  overflow-x: auto;
  scroll-snap-type: x mandatory;
  gap: 16px;
}
.carousel-item {
  scroll-snap-align: start;
  flex: 0 0 80%;
}

/* backdrop-filter — frosted glass */
.modal-overlay {
  backdrop-filter: blur(8px);
  background: rgba(0, 0, 0, 0.3);
}

/* clip-path — diagonal section */
.hero {
  clip-path: polygon(0 0, 100% 0, 100% 85%, 0 100%);
}</pre>
</section>
"""

S21 = r"""
<section class="section-break">
<h2 id="s21">21. CSS Architecture &amp; Methodologies</h2>
<p><strong>Checklist items:</strong> BEM, SMACSS, OOCSS, Atomic CSS, CSS Modules, utility-first CSS. CSS-in-JS (styled-components, emotion). Preprocessors (SASS/SCSS, PostCSS). CSS performance (critical CSS, containment, content-visibility, reflows/repaints). Specificity deep dive, cascade &amp; inheritance, ITCSS.</p>

<h3>Theory &amp; Concept</h3>
<table>
<thead><tr><th>Methodology</th><th>Core idea</th><th>When to use</th></tr></thead>
<tbody>
<tr><td><strong>BEM</strong></td><td><code>.block__element--modifier</code></td><td>Component-based projects, Angular with global styles</td></tr>
<tr><td><strong>Utility-first (Tailwind)</strong></td><td>Small single-purpose classes</td><td>Rapid prototyping, design-system-backed projects</td></tr>
<tr><td><strong>CSS Modules</strong></td><td>Locally scoped class names (auto-generated)</td><td>Component isolation without Angular view encapsulation</td></tr>
<tr><td><strong>ITCSS</strong></td><td>Inverted triangle — settings → tools → generic → elements → objects → components → utilities</td><td>Large projects needing structured CSS architecture</td></tr>
</tbody>
</table>

<h3>Hands-on Code</h3>
<pre>/* BEM naming */
.product-card {}                    /* Block */
.product-card__title {}             /* Element */
.product-card__title--highlighted {} /* Modifier */
.product-card--featured {}          /* Block modifier */

/* SCSS with BEM */
.product-card {
  border: 1px solid #ddd;

  &__title {
    font-size: 18px;
    &--highlighted { color: red; }
  }

  &__price { font-weight: bold; }
  &--featured { border-color: gold; }
}

/* Critical CSS — inline above-fold styles */
&lt;style&gt;
  /* Only styles needed for the first viewport */
  .header, .hero, .nav { ... }
&lt;/style&gt;
&lt;link rel="stylesheet" href="full.css" media="print" onload="this.media='all'"&gt;

/* CSS containment — optimize rendering */
.widget {
  contain: layout style paint;  /* isolate from rest of page */
  content-visibility: auto;     /* skip rendering when off-screen */
  contain-intrinsic-size: 0 300px; /* placeholder size */
}</pre>
</section>
"""

# TypeScript
S22 = r"""
<section class="section-break">
<h2 id="s22">22. TypeScript Complete</h2>
<p><strong>Checklist items:</strong> Type annotations, inference, any/unknown/never/void, arrays/tuples, interfaces, type vs interface, optional/readonly. Union/intersection types, literal types, discriminated unions, type guards, narrowing, assertions. Generics (functions, interfaces, classes, constraints, defaults, utility types). Utility types: Partial, Required, Pick, Omit, Record, Exclude, Extract, ReturnType, Parameters, Awaited, mapped types, conditional types. Enums (numeric, string, const). Modules, declaration files, tsconfig.</p>

<h3>Hands-on Code</h3>
<pre>// Discriminated union — type-safe state management
type RequestState&lt;T&gt; =
  | { status: 'idle' }
  | { status: 'loading' }
  | { status: 'success'; data: T }
  | { status: 'error'; error: string };

function renderState&lt;T&gt;(state: RequestState&lt;T&gt;) {
  switch (state.status) {
    case 'idle':    return 'Ready';
    case 'loading': return 'Loading...';
    case 'success': return `Data: ${JSON.stringify(state.data)}`; // TS knows data exists
    case 'error':   return `Error: ${state.error}`; // TS knows error exists
  }
}

// Mapped types — make all properties optional and nullable
type Nullable&lt;T&gt; = { [K in keyof T]: T[K] | null };
type FormFields = Nullable&lt;User&gt;; // { name: string | null; email: string | null; ... }

// Conditional types
type IsString&lt;T&gt; = T extends string ? 'yes' : 'no';
type A = IsString&lt;string&gt;;  // 'yes'
type B = IsString&lt;number&gt;;  // 'no'

// Template literal types
type HttpMethod = 'GET' | 'POST' | 'PUT' | 'DELETE';
type ApiEndpoint = `/api/${string}`;
type Route = `${HttpMethod} ${ApiEndpoint}`;
// Valid: 'GET /api/users', 'POST /api/orders'

// Generic constraint
function getProperty&lt;T, K extends keyof T&gt;(obj: T, key: K): T[K] {
  return obj[key];
}
const user = { name: 'Sid', age: 28 };
getProperty(user, 'name'); // string
// getProperty(user, 'invalid'); // Compile error!

// Utility types in practice
interface User { id: number; name: string; email: string; password: string; }
type CreateUser = Omit&lt;User, 'id'&gt;;                    // No id for creation
type UpdateUser = Partial&lt;Omit&lt;User, 'id'&gt;&gt;;            // All fields optional
type PublicUser = Pick&lt;User, 'id' | 'name' | 'email'&gt;;  // No password exposed
type UserRecord = Record&lt;string, User&gt;;                  // Dictionary of users

// const enum — inlined at compile time (no runtime object)
const enum Direction { Up, Down, Left, Right }
const move = Direction.Up; // compiled to: const move = 0;</pre>
</section>
"""

# Performance
S23 = r"""
<section class="section-break">
<h2 id="s23">23. Loading &amp; Runtime Performance</h2>
<p><strong>Checklist items:</strong> Code splitting, dynamic imports, tree shaking, bundle analysis, minification, lazy loading images, preload/prefetch/preconnect, HTTP/2-3, CDN. Runtime: debounce/throttle, rAF, layout thrashing, read-write batching, virtual scroll, Web Workers. Rendering: critical rendering path, reflow vs repaint, composite layers, will-change, CSS containment. Caching: browser headers, service worker, Cache-Control, ETag, stale-while-revalidate.</p>

<h3>Hands-on Code</h3>
<pre>// Resource hints — load critical resources faster
&lt;link rel="preconnect" href="https://api.example.com"&gt;
&lt;link rel="dns-prefetch" href="https://cdn.example.com"&gt;
&lt;link rel="preload" href="/fonts/inter.woff2" as="font" type="font/woff2" crossorigin&gt;
&lt;link rel="prefetch" href="/js/checkout.chunk.js"&gt; &lt;!-- speculative next-page --&gt;

// Avoiding layout thrashing — batch reads then writes
// BAD — read/write/read/write forces multiple reflows
elements.forEach(el =&gt; {
  const height = el.offsetHeight;     // READ (forces layout)
  el.style.height = height * 2 + 'px'; // WRITE (invalidates layout)
});

// GOOD — batch all reads, then all writes
const heights = elements.map(el =&gt; el.offsetHeight); // all reads
elements.forEach((el, i) =&gt; {
  el.style.height = heights[i] * 2 + 'px'; // all writes
});

// Virtual scroll concept — only render visible items
function getVisibleItems(scrollTop, viewportHeight, itemHeight, totalItems) {
  const start = Math.floor(scrollTop / itemHeight);
  const visible = Math.ceil(viewportHeight / itemHeight);
  const end = Math.min(start + visible + 2, totalItems); // +2 buffer
  return { startIndex: start, endIndex: end };
}

// Web Worker for heavy computation
const worker = new Worker(new URL('./sort.worker', import.meta.url));
worker.postMessage({ data: hugeArray, sortField: 'price' });
worker.onmessage = ({ data }) =&gt; renderTable(data.sorted);</pre>
</section>
"""

S24 = r"""
<section class="section-break">
<h2 id="s24">24. Core Web Vitals &amp; Performance Measurement</h2>
<p><strong>Checklist items:</strong> LCP, FID/INP, CLS, FCP, TTI, TBT. Images: responsive images, WebP/AVIF, compression, lazy loading, sprites, SVG. Fonts: font-display, FOUT/FOIT/FOFT, subsetting. Measuring: Performance API, Navigation/Resource/User Timing, Lighthouse, WebPageTest, DevTools.</p>

<h3>Theory &amp; Concept</h3>
<table>
<thead><tr><th>Metric</th><th>What it measures</th><th>Good</th><th>How to improve</th></tr></thead>
<tbody>
<tr><td><strong>LCP</strong></td><td>Largest visible content element</td><td>&lt; 2.5s</td><td>Optimize hero image, preload fonts, SSR</td></tr>
<tr><td><strong>INP</strong></td><td>Responsiveness to all interactions</td><td>&lt; 200ms</td><td>Break long tasks, yield to main thread, use Web Workers</td></tr>
<tr><td><strong>CLS</strong></td><td>Visual stability (layout shifts)</td><td>&lt; 0.1</td><td>Set dimensions on images/ads, avoid dynamic content injection above fold</td></tr>
<tr><td><strong>FCP</strong></td><td>First pixel painted</td><td>&lt; 1.8s</td><td>Inline critical CSS, eliminate render-blocking resources</td></tr>
<tr><td><strong>TBT</strong></td><td>Time main thread is blocked (&gt;50ms tasks)</td><td>&lt; 200ms</td><td>Code split, defer non-critical JS, use requestIdleCallback</td></tr>
</tbody>
</table>

<h3>Hands-on Code</h3>
<pre>// Measure Core Web Vitals in your app
import { onLCP, onINP, onCLS } from 'web-vitals';

onLCP(metric =&gt; sendToAnalytics('LCP', metric));
onINP(metric =&gt; sendToAnalytics('INP', metric));
onCLS(metric =&gt; sendToAnalytics('CLS', metric));

function sendToAnalytics(name, { value, rating }) {
  navigator.sendBeacon('/api/vitals', JSON.stringify({
    name, value: Math.round(value), rating, url: location.href
  }));
}

// Responsive images with modern formats
&lt;picture&gt;
  &lt;source srcset="hero-400.avif 400w, hero-800.avif 800w" type="image/avif"&gt;
  &lt;source srcset="hero-400.webp 400w, hero-800.webp 800w" type="image/webp"&gt;
  &lt;img src="hero-800.jpg" alt="..." loading="lazy"
       sizes="(max-width:600px) 400px, 800px" width="800" height="500"&gt;
&lt;/picture&gt;

// Font subsetting — only include characters you need
@font-face {
  font-family: 'Inter';
  src: url('inter-latin.woff2') format('woff2');
  font-display: swap;
  unicode-range: U+0000-00FF, U+0131, U+0152-0153;
}</pre>
</section>
"""

# Security & Networking
S25 = r"""
<section class="section-break">
<h2 id="s25">25. Security</h2>
<p><strong>Checklist items:</strong> XSS (reflected, stored, DOM-based), CSRF, clickjacking, MITM. Prevention: input sanitization, output encoding, CSP, HTTPS, secure cookies (HttpOnly, Secure, SameSite), CORS, SRI, X-Frame-Options, X-Content-Type-Options. Auth: JWT, OAuth 2.0, token storage, refresh rotation, session management, MFA.</p>

<h3>Hands-on Code</h3>
<pre>// XSS prevention — always escape user input
// BAD:
element.innerHTML = userInput; // Executes &lt;script&gt; tags!

// GOOD:
element.textContent = userInput; // Safe — treats as plain text

// Content Security Policy header
Content-Security-Policy:
  default-src 'self';
  script-src 'self' 'nonce-abc123';
  style-src 'self' 'unsafe-inline';
  img-src 'self' data: https://cdn.example.com;
  connect-src 'self' https://api.example.com;
  frame-ancestors 'none'; // prevents clickjacking

// Subresource Integrity — verify CDN files haven't been tampered
&lt;script src="https://cdn.example.com/lib.js"
        integrity="sha384-oqVuAfXRKap7fdgcCY5uykM6+R9GqQ8K/uxnGz..."
        crossorigin="anonymous"&gt;&lt;/script&gt;

// JWT token refresh pattern
async function fetchWithAuth(url) {
  let token = getAccessToken();
  let response = await fetch(url, {
    headers: { 'Authorization': `Bearer ${token}` }
  });
  if (response.status === 401) {
    token = await refreshToken(); // get new access token
    response = await fetch(url, {
      headers: { 'Authorization': `Bearer ${token}` }
    });
  }
  return response;
}

// CORS — server must set these headers for cross-origin requests
Access-Control-Allow-Origin: https://my-app.com
Access-Control-Allow-Methods: GET, POST, PUT, DELETE
Access-Control-Allow-Headers: Content-Type, Authorization
Access-Control-Allow-Credentials: true</pre>
</section>
"""

S26 = r"""
<section class="section-break">
<h2 id="s26">26. Networking &amp; APIs</h2>
<p><strong>Checklist items:</strong> HTTP methods, status codes, headers, CORS. REST design (naming, versioning, HATEOAS, idempotency, pagination, rate limiting). GraphQL (queries, mutations, fragments, Apollo). Data fetching: Fetch API, Axios, AbortController, retry, error handling, loading states, optimistic updates, polling vs WebSocket vs SSE, request deduplication. WebSockets (connection, Socket.io, reconnection, heartbeat).</p>

<h3>Hands-on Code</h3>
<pre>// Fetch with AbortController — cancel on component destroy
const controller = new AbortController();
try {
  const response = await fetch('/api/data', { signal: controller.signal });
  const data = await response.json();
} catch (error) {
  if (error.name === 'AbortError') console.log('Request cancelled');
  else throw error;
}
// On cleanup: controller.abort();

// Retry with exponential backoff
async function fetchWithRetry(url, maxRetries = 3) {
  for (let i = 0; i &lt; maxRetries; i++) {
    try {
      const res = await fetch(url);
      if (res.ok) return await res.json();
      if (res.status &lt; 500) throw new Error(`HTTP ${res.status}`); // don't retry 4xx
    } catch (error) {
      if (i === maxRetries - 1) throw error;
      await new Promise(r =&gt; setTimeout(r, 1000 * Math.pow(2, i))); // 1s, 2s, 4s
    }
  }
}

// Optimistic update pattern
function addTodo(newTodo) {
  const tempId = crypto.randomUUID();
  // 1. Update UI immediately (optimistic)
  todos.update(list =&gt; [...list, { ...newTodo, id: tempId }]);
  // 2. Send to server
  api.createTodo(newTodo).then(
    saved =&gt; todos.update(list =&gt; list.map(t =&gt; t.id === tempId ? saved : t)),
    error =&gt; { todos.update(list =&gt; list.filter(t =&gt; t.id !== tempId)); showError(error); }
  );
}

// HTTP Status codes every developer should know
// 200 OK, 201 Created, 204 No Content
// 301 Moved Permanently, 304 Not Modified
// 400 Bad Request, 401 Unauthorized, 403 Forbidden, 404 Not Found, 409 Conflict, 429 Too Many Requests
// 500 Internal Server Error, 502 Bad Gateway, 503 Service Unavailable</pre>
</section>
"""

# Testing & Build
S27 = r"""
<section class="section-break">
<h2 id="s27">27. Testing</h2>
<p><strong>Checklist items:</strong> Unit testing (Jest: describe/it, assertions, mocking, spies, timers, coverage). Integration testing (component interactions, API integration). E2E testing (Cypress, Playwright, selectors, network mocking, screenshots). TDD (red-green-refactor).</p>

<h3>Hands-on Code</h3>
<pre>// Jest unit test — testing a pure function
describe('calculateTotal', () =&gt; {
  it('should sum item prices with tax', () =&gt; {
    const items = [{ price: 100 }, { price: 200 }];
    expect(calculateTotal(items, 0.1)).toBe(330); // 300 + 10% tax
  });

  it('should return 0 for empty cart', () =&gt; {
    expect(calculateTotal([], 0.1)).toBe(0);
  });
});

// Mocking an API call
jest.mock('./api', () =&gt; ({
  fetchUser: jest.fn()
}));

import { fetchUser } from './api';

test('displays user name when fetch succeeds', async () =&gt; {
  (fetchUser as jest.Mock).mockResolvedValue({ name: 'Sid' });
  const result = await getUserDisplay(1);
  expect(result).toBe('Hello, Sid');
  expect(fetchUser).toHaveBeenCalledWith(1);
});

// Timer mocking
jest.useFakeTimers();
test('debounce calls function after delay', () =&gt; {
  const fn = jest.fn();
  const debounced = debounce(fn, 300);
  debounced('a');
  debounced('b');
  debounced('c');
  expect(fn).not.toHaveBeenCalled();
  jest.advanceTimersByTime(300);
  expect(fn).toHaveBeenCalledTimes(1);
  expect(fn).toHaveBeenCalledWith('c');
});

// Cypress E2E test
describe('Login flow', () =&gt; {
  it('should login with valid credentials', () =&gt; {
    cy.visit('/login');
    cy.get('[data-testid="email"]').type('user@example.com');
    cy.get('[data-testid="password"]').type('password123');
    cy.get('[data-testid="submit"]').click();
    cy.url().should('include', '/dashboard');
    cy.get('[data-testid="welcome"]').should('contain', 'Welcome');
  });
});</pre>
</section>
"""

S28 = r"""
<section class="section-break">
<h2 id="s28">28. Build Tools &amp; Dev Environment</h2>
<p><strong>Checklist items:</strong> Webpack (entry, loaders, plugins, code splitting, HMR, source maps). Vite (ESM dev, HMR, build). Babel (transpilation, presets, polyfills). Package managers (npm/yarn/pnpm, semver, lock files, workspaces). Linting (ESLint, Prettier, Husky, lint-staged). Environment variables.</p>

<h3>Theory &amp; Concept</h3>
<table>
<thead><tr><th>Tool</th><th>Purpose</th><th>Angular context</th></tr></thead>
<tbody>
<tr><td>Webpack</td><td>Module bundler — transforms &amp; bundles JS, CSS, assets</td><td>Angular CLI uses webpack (or esbuild in v17+) under the hood</td></tr>
<tr><td>Vite</td><td>Fast dev server (ESM) + Rollup build</td><td>Angular 17+ uses Vite-based dev server via <code>@angular/build</code></td></tr>
<tr><td>Babel</td><td>Transpile modern JS to older syntax</td><td>Angular uses TypeScript compiler + downleveling instead</td></tr>
<tr><td>ESLint</td><td>Static analysis for code quality</td><td>Angular uses <code>@angular-eslint</code> with project-specific rules</td></tr>
</tbody>
</table>

<h3>Hands-on Code</h3>
<pre>// Pre-commit hooks — catch issues before they reach CI
// .husky/pre-commit
npx lint-staged

// package.json
{
  "lint-staged": {
    "*.{ts,js}": ["eslint --fix", "prettier --write"],
    "*.{css,scss}": ["prettier --write"],
    "*.html": ["prettier --write"]
  }
}

// Semantic versioning
// MAJOR.MINOR.PATCH
// ^1.2.3 → allows 1.x.x (minor + patch updates)
// ~1.2.3 → allows 1.2.x (patch updates only)
// 1.2.3  → exact version only

// Environment variables in Angular
// environment.ts
export const environment = {
  production: false,
  apiUrl: 'http://localhost:3000/api'
};
// environment.prod.ts
export const environment = {
  production: true,
  apiUrl: 'https://api.example.com'
};</pre>
</section>
"""

# Design & Architecture
S29 = r"""
<section class="section-break">
<h2 id="s29">29. Design Patterns</h2>
<p><strong>Checklist items:</strong> Creational: Singleton, Factory, Constructor, Module. Structural: Facade, Adapter, Decorator, Proxy. Behavioral: Observer/PubSub, Strategy, Command, Iterator, Mediator. Architectural: MVC, MVVM, Flux, Atomic Design.</p>

<h3>Hands-on Code</h3>
<pre>// Singleton — Angular services with providedIn:'root' ARE singletons

// Factory pattern — creating objects based on type
function createNotification(type, message) {
  const base = { id: crypto.randomUUID(), message, timestamp: Date.now() };
  switch (type) {
    case 'success': return { ...base, icon: '✓', color: 'green', duration: 3000 };
    case 'error':   return { ...base, icon: '✕', color: 'red', duration: 0 };
    case 'info':    return { ...base, icon: 'ℹ', color: 'blue', duration: 5000 };
  }
}

// Observer pattern — PubSub
class EventBus {
  private listeners = new Map&lt;string, Set&lt;Function&gt;&gt;();

  on(event, callback) {
    if (!this.listeners.has(event)) this.listeners.set(event, new Set());
    this.listeners.get(event).add(callback);
    return () =&gt; this.listeners.get(event)?.delete(callback); // unsubscribe
  }

  emit(event, data) {
    this.listeners.get(event)?.forEach(cb =&gt; cb(data));
  }
}

// Strategy pattern — different sort strategies
const sortStrategies = {
  price:  (a, b) =&gt; a.price - b.price,
  name:   (a, b) =&gt; a.name.localeCompare(b.name),
  rating: (a, b) =&gt; b.rating - a.rating,
  newest: (a, b) =&gt; new Date(b.date) - new Date(a.date)
};
function sortProducts(products, strategy) {
  return [...products].sort(sortStrategies[strategy]);
}

// Facade pattern — simplify complex subsystem
class CheckoutFacade {
  constructor(private cart, private payment, private shipping, private order) {}

  async checkout(paymentDetails) {
    const items = this.cart.getItems();
    const total = this.cart.getTotal();
    const shipping = await this.shipping.calculate(items);
    const paymentResult = await this.payment.process(paymentDetails, total + shipping);
    const order = await this.order.create({ items, total, shipping, paymentResult });
    this.cart.clear();
    return order;
  }
}</pre>
</section>
"""

S30 = r"""
<section class="section-break">
<h2 id="s30">30. Frontend System Design</h2>
<p><strong>Checklist items:</strong> Component API design, props interface, composition vs configuration, theming, accessibility. Architecture: folder structure, feature vs type organization, separation of concerns, scalability. Components to design: autocomplete, dropdown, modal, tooltip, tabs, accordion, carousel, data table, infinite scroll, image gallery, form builder, notification system. Full apps: news feed, chat, e-commerce, video player, calendar, dashboard, search. Scalability: code splitting, lazy loading, state at scale, caching, error boundaries.</p>

<h3>Hands-on: Design an Autocomplete</h3>
<pre>// Component API design
&lt;app-autocomplete
  [items]="suggestions()"
  [loading]="isLoading()"
  [placeholder]="'Search products...'"
  [debounceMs]="300"
  [minChars]="2"
  [maxResults]="10"
  (search)="onSearch($event)"
  (select)="onSelect($event)"
/&gt;

// Internal implementation considerations:
// 1. Debounce input → emit search event
// 2. Show dropdown when results exist
// 3. Keyboard: ArrowUp/Down to navigate, Enter to select, Escape to close
// 4. Highlight matching text in results
// 5. Loading spinner while fetching
// 6. Empty state: "No results found"
// 7. Accessibility: role="combobox", aria-expanded, aria-activedescendant
// 8. Click outside to close (CDK overlay or document listener)
// 9. Mobile: full-screen mode on small screens

// Data flow:
// User types → debounce(300ms) → distinctUntilChanged → minLength check
// → emit search event → parent calls API → results flow back via [items]

// Performance:
// - Virtual scroll for long result lists
// - Cancel previous API request (switchMap)
// - Cache recent searches in a Map</pre>
</section>
"""

S31 = r"""
<section class="section-break">
<h2 id="s31">31. Data Structures &amp; Algorithms for Frontend</h2>
<p><strong>Checklist items:</strong> Arrays, linked lists, stacks, queues, hash tables/maps, sets, trees, graphs. Algorithms: linear/binary search, sorting algorithms, two pointers, sliding window, frequency counter, hash map lookups, recursion. Big O: time/space complexity, O(1), O(log n), O(n), O(n log n), O(n²).</p>

<h3>Hands-on Code</h3>
<pre>// Binary search — find item in sorted array
function binarySearch(arr, target) {
  let left = 0, right = arr.length - 1;
  while (left &lt;= right) {
    const mid = Math.floor((left + right) / 2);
    if (arr[mid] === target) return mid;
    if (arr[mid] &lt; target) left = mid + 1;
    else right = mid - 1;
  }
  return -1; // O(log n)
}

// Two pointers — check if string is palindrome
function isPalindrome(s) {
  let left = 0, right = s.length - 1;
  while (left &lt; right) {
    if (s[left].toLowerCase() !== s[right].toLowerCase()) return false;
    left++; right--;
  }
  return true; // O(n) time, O(1) space
}

// Sliding window — max sum of k consecutive elements
function maxSumSubarray(arr, k) {
  let windowSum = arr.slice(0, k).reduce((a, b) =&gt; a + b, 0);
  let maxSum = windowSum;
  for (let i = k; i &lt; arr.length; i++) {
    windowSum += arr[i] - arr[i - k]; // slide: add right, remove left
    maxSum = Math.max(maxSum, windowSum);
  }
  return maxSum; // O(n) — not O(n*k)
}

// Frequency counter — find duplicates
function findDuplicates(arr) {
  const freq = new Map();
  const dupes = [];
  for (const item of arr) {
    freq.set(item, (freq.get(item) || 0) + 1);
    if (freq.get(item) === 2) dupes.push(item);
  }
  return dupes; // O(n)
}

// Stack — validate balanced parentheses
function isBalanced(str) {
  const stack = [];
  const pairs = { ')': '(', ']': '[', '}': '{' };
  for (const ch of str) {
    if ('([{'.includes(ch)) stack.push(ch);
    else if (')]}').includes(ch)) {
      if (stack.pop() !== pairs[ch]) return false;
    }
  }
  return stack.length === 0;
}

// Real frontend use: undo/redo is a stack, BFS for DOM traversal,
// trie for autocomplete, graph for routing</pre>
</section>
"""

# Misc sections
S32 = r"""
<section class="section-break">
<h2 id="s32">32. Version Control (Git)</h2>
<p><strong>Checklist items:</strong> init, clone, add, commit, push, pull, fetch, branch, merge vs rebase, conflicts, stash, cherry-pick. Workflows: feature branch, Gitflow, trunk-based, PR process, code review. Advanced: interactive rebase, reflog, bisect, tags, submodules, hooks.</p>

<h3>Hands-on Code</h3>
<pre># Essential daily workflow
git checkout -b feature/user-profile     # create feature branch
git add -p                                # stage interactively (review each hunk)
git commit -m "feat: add user profile page"  # conventional commit
git push origin feature/user-profile

# Rebase vs merge
git checkout feature/user-profile
git rebase main                           # replay your commits on top of main
# Result: linear history, no merge commits
# Use for: feature branches before merging into main

git merge feature/user-profile            # creates a merge commit
# Use for: merging into main/develop (preserves branch history)

# Interactive rebase — squash/reword commits before PR
git rebase -i HEAD~3
# pick abc123 feat: add profile component
# squash def456 fix: typo in profile
# squash ghi789 fix: styling

# Stash — save work in progress
git stash push -m "WIP: profile validation"
git stash list                            # see all stashes
git stash pop                             # apply and remove latest
git stash apply stash@{1}                 # apply specific stash

# bisect — find which commit introduced a bug
git bisect start
git bisect bad                            # current commit is broken
git bisect good v1.5.0                    # this version was working
# Git checks out middle commits; you test and mark good/bad
# Finds the exact commit in O(log n) steps

# Cherry-pick — apply specific commit to another branch
git cherry-pick abc123                    # apply one commit
git cherry-pick abc123..def456            # apply range</pre>
</section>
"""

S33 = r"""
<section class="section-break">
<h2 id="s33">33. Web Fundamentals</h2>
<p><strong>Checklist items:</strong> Browser rendering (DOM → CSSOM → render tree → layout → paint → compositing), request-response cycle, DNS resolution, TCP/IP, TLS handshake. Progressive enhancement, feature detection, graceful degradation. Web standards (W3C, WHATWG, ECMAScript), browser compatibility, polyfills.</p>

<h3>Theory &amp; Concept</h3>
<h4>What happens when you type a URL and press Enter</h4>
<ol>
<li><strong>DNS lookup:</strong> Browser resolves domain → IP address (checks cache → OS → ISP → root DNS)</li>
<li><strong>TCP connection:</strong> Three-way handshake (SYN → SYN-ACK → ACK)</li>
<li><strong>TLS handshake:</strong> For HTTPS — negotiates encryption (adds ~1-2 RTTs)</li>
<li><strong>HTTP request:</strong> Browser sends GET request with headers</li>
<li><strong>Server response:</strong> HTML document returned</li>
<li><strong>HTML parsing:</strong> Build DOM tree (pauses for blocking scripts)</li>
<li><strong>CSS parsing:</strong> Build CSSOM tree</li>
<li><strong>Render tree:</strong> Combine DOM + CSSOM (skip <code>display:none</code> elements)</li>
<li><strong>Layout:</strong> Calculate geometry (position, size) of every element</li>
<li><strong>Paint:</strong> Fill in pixels — colors, images, text, borders</li>
<li><strong>Compositing:</strong> Combine layers and render to screen</li>
</ol>

<h3>Hands-on Code</h3>
<pre>// Feature detection — progressive enhancement
if ('IntersectionObserver' in window) {
  // Use IntersectionObserver for lazy loading
} else {
  // Fallback: load all images immediately
}

if ('serviceWorker' in navigator) {
  navigator.serviceWorker.register('/sw.js');
}

// Polyfill pattern
if (!Array.prototype.at) {
  Array.prototype.at = function(index) {
    return index >= 0 ? this[index] : this[this.length + index];
  };
}</pre>
</section>
"""

S34 = r"""
<section class="section-break">
<h2 id="s34">34. Mobile, Responsive &amp; PWA</h2>
<p><strong>Checklist items:</strong> Fluid grids, flexible images, media queries, mobile-first, breakpoints, touch targets (44×44px). Touch vs mouse events, viewport meta, device pixel ratio, offline functionality. PWA: Service Workers, manifest, add to home screen, push notifications, background sync, offline caching.</p>

<h3>Hands-on Code</h3>
<pre>// Service Worker — cache-first strategy
self.addEventListener('fetch', (event) =&gt; {
  event.respondWith(
    caches.match(event.request).then(cached =&gt; {
      return cached || fetch(event.request).then(response =&gt; {
        const clone = response.clone();
        caches.open('v1').then(cache =&gt; cache.put(event.request, clone));
        return response;
      });
    })
  );
});

// PWA manifest.json
{
  "name": "My App",
  "short_name": "App",
  "start_url": "/",
  "display": "standalone",
  "background_color": "#fffdf8",
  "theme_color": "#0f6b5f",
  "icons": [
    { "src": "icon-192.png", "sizes": "192x192", "type": "image/png" },
    { "src": "icon-512.png", "sizes": "512x512", "type": "image/png" }
  ]
}

// Touch-friendly CSS
button, a, [role="button"] {
  min-width: 44px;
  min-height: 44px;    /* WCAG touch target minimum */
  padding: 12px 16px;
}

// Viewport
&lt;meta name="viewport" content="width=device-width, initial-scale=1"&gt;</pre>
</section>
"""

S35 = r"""
<section class="section-break">
<h2 id="s35">35. Real-World Implementation Patterns</h2>
<p><strong>Checklist items:</strong> Debounce (leading/trailing/immediate), throttle, deep clone (recursive, circular refs), event emitter (subscribe/unsubscribe/once), flatten array (recursive/iterative/depth), Promise implementation (then/catch/finally/all/race), curry function (partial application, arity), memoization (cache, invalidation).</p>

<h3>Hands-on Code</h3>
<pre>// Deep clone — handling circular references
function deepClone(obj, seen = new WeakMap()) {
  if (obj === null || typeof obj !== 'object') return obj;
  if (obj instanceof Date) return new Date(obj);
  if (obj instanceof RegExp) return new RegExp(obj);
  if (seen.has(obj)) return seen.get(obj); // circular reference

  const clone = Array.isArray(obj) ? [] : {};
  seen.set(obj, clone);
  for (const key of Object.keys(obj)) {
    clone[key] = deepClone(obj[key], seen);
  }
  return clone;
}

// Event emitter — full implementation
class EventEmitter {
  #listeners = new Map();

  on(event, fn) {
    if (!this.#listeners.has(event)) this.#listeners.set(event, []);
    this.#listeners.get(event).push(fn);
    return () =&gt; this.off(event, fn);
  }

  once(event, fn) {
    const wrapper = (...args) =&gt; { fn(...args); this.off(event, wrapper); };
    this.on(event, wrapper);
  }

  off(event, fn) {
    const fns = this.#listeners.get(event);
    if (fns) this.#listeners.set(event, fns.filter(f =&gt; f !== fn));
  }

  emit(event, ...args) {
    this.#listeners.get(event)?.forEach(fn =&gt; fn(...args));
  }
}

// Flatten array with depth
function flatten(arr, depth = Infinity) {
  return depth > 0
    ? arr.reduce((acc, val) =&gt;
        acc.concat(Array.isArray(val) ? flatten(val, depth - 1) : val), [])
    : arr.slice();
}
flatten([1, [2, [3, [4]]]], 2); // [1, 2, 3, [4]]

// Simplified Promise implementation (interview-level)
class MyPromise {
  #state = 'pending';
  #value = undefined;
  #handlers = [];

  constructor(executor) {
    const resolve = (value) =&gt; {
      if (this.#state !== 'pending') return;
      this.#state = 'fulfilled';
      this.#value = value;
      this.#handlers.forEach(h =&gt; h.onFulfilled(value));
    };
    const reject = (reason) =&gt; {
      if (this.#state !== 'pending') return;
      this.#state = 'rejected';
      this.#value = reason;
      this.#handlers.forEach(h =&gt; h.onRejected(reason));
    };
    try { executor(resolve, reject); } catch (e) { reject(e); }
  }

  then(onFulfilled, onRejected) {
    return new MyPromise((resolve, reject) =&gt; {
      const handle = () =&gt; {
        try {
          if (this.#state === 'fulfilled') {
            resolve(onFulfilled ? onFulfilled(this.#value) : this.#value);
          } else {
            reject(onRejected ? onRejected(this.#value) : this.#value);
          }
        } catch (e) { reject(e); }
      };
      if (this.#state === 'pending') {
        this.#handlers.push({ onFulfilled: () =&gt; handle(), onRejected: () =&gt; handle() });
      } else {
        queueMicrotask(handle);
      }
    });
  }
}</pre>
</section>
"""

S36 = r"""
<section class="section-break">
<h2 id="s36">36. Additional Interview Topics</h2>
<p><strong>Checklist items:</strong> PWA features (service worker lifecycle, cache strategies, background sync, push notifications). Web Components (custom elements, shadow DOM, templates, slots). i18n (locale, number/date formatting, pluralization, RTL, libraries). Error tracking (Sentry, source maps, breadcrumbs). SEO for SPAs (SSR, SSG, meta tags, sitemap, structured data). Micro-frontends (module federation, independent deploy, shared deps). Monorepos (Nx, Turborepo, Lerna, workspaces). CI/CD (GitHub Actions, Jenkins, automated testing, deployment).</p>

<h3>Hands-on Code</h3>
<pre>// Web Components — custom element
class AppCounter extends HTMLElement {
  #count = 0;
  #shadow;

  constructor() {
    super();
    this.#shadow = this.attachShadow({ mode: 'open' });
  }

  connectedCallback() {
    this.render();
    this.#shadow.querySelector('button').addEventListener('click', () =&gt; {
      this.#count++;
      this.render();
      this.dispatchEvent(new CustomEvent('count-changed', { detail: this.#count }));
    });
  }

  render() {
    this.#shadow.innerHTML = `
      &lt;style&gt;
        button { padding: 8px 16px; font-size: 16px; cursor: pointer; }
        span { margin-left: 12px; font-weight: bold; }
      &lt;/style&gt;
      &lt;button&gt;Increment&lt;/button&gt;
      &lt;span&gt;Count: ${this.#count}&lt;/span&gt;
    `;
  }

  static get observedAttributes() { return ['initial']; }
  attributeChangedCallback(name, _, newVal) {
    if (name === 'initial') this.#count = parseInt(newVal) || 0;
  }
}
customElements.define('app-counter', AppCounter);
// Usage: &lt;app-counter initial="5"&gt;&lt;/app-counter&gt;

// Sentry error tracking setup
import * as Sentry from '@sentry/browser';
Sentry.init({
  dsn: 'https://key@sentry.io/project',
  release: '1.0.0',
  environment: 'production',
  integrations: [Sentry.browserTracingIntegration()],
  tracesSampleRate: 0.2
});
// Errors are automatically captured. Add context:
Sentry.setUser({ id: userId, email: userEmail });
Sentry.addBreadcrumb({ message: 'User clicked checkout', category: 'ui' });</pre>
</section>
"""

S37 = r"""
<section class="section-break">
<h2 id="s37">37. Soft Skills &amp; Interview Process</h2>
<p><strong>Checklist items:</strong> Code review skills (what to look for, constructive feedback). Communication (explaining decisions, trade-offs, clarifying requirements, thinking aloud). Problem-solving (understanding requirements, breaking down, edge cases, complexity, alternatives). Project discussion (architecture, challenges, solutions, collaboration, impact).</p>

<h3>Theory &amp; Concept</h3>

<h4>37.1 How to approach a coding interview question</h4>
<ol>
<li><strong>Clarify:</strong> Repeat the problem, ask about edge cases, confirm input/output format. "What happens if the array is empty? Can there be duplicates?"</li>
<li><strong>Plan:</strong> Describe your approach BEFORE coding. "I'll use a hash map for O(1) lookups..."</li>
<li><strong>Code:</strong> Write clean, readable code. Use meaningful variable names. Talk through your logic.</li>
<li><strong>Test:</strong> Walk through with a sample input. Check edge cases (empty, single element, duplicates).</li>
<li><strong>Optimize:</strong> Discuss time/space complexity. Can it be improved? "This is O(n²), but with a sorted array and two pointers it can be O(n log n)."</li>
</ol>

<h4>37.2 Code review best practices</h4>
<ul>
<li><strong>Constructive > Critical:</strong> "Consider using switchMap here to prevent race conditions" vs "This is wrong."</li>
<li><strong>Ask questions:</strong> "What happens if this API call fails?" encourages thinking without attacking.</li>
<li><strong>Review for:</strong> Correctness, performance, security, readability, testability, edge cases.</li>
<li><strong>Automate what you can:</strong> ESLint for style, Prettier for formatting, bundle budgets for size. Reserve human review for architecture and design.</li>
</ul>

<h4>37.3 Discussing past projects</h4>
<p>Use the <strong>STAR method:</strong> Situation → Task → Action → Result. Example: "We had a dashboard loading in 8 seconds (Situation). I was tasked with getting it under 3s (Task). I implemented lazy loading, virtual scroll for the data table, and added an HTTP cache layer (Action). Load time dropped to 2.1s, and user engagement increased 35% (Result)."</p>
</section>
"""

FOOTER = r"""
</main>

<script>
document.querySelectorAll('.sidebar-nav a[href^="#"]').forEach(link => {
  link.addEventListener('click', e => {
    e.preventDefault();
    const target = document.querySelector(link.getAttribute('href'));
    if (target) {
      target.scrollIntoView({ behavior: 'smooth', block: 'start' });
      document.querySelector('.sidebar-nav').classList.remove('open');
    }
  });
});

const navLinks = document.querySelectorAll('.sidebar-nav a[href^="#"]');
const sections = Array.from(navLinks).map(a => ({
  link: a, target: document.querySelector(a.getAttribute('href'))
})).filter(s => s.target);

let ticking = false;
window.addEventListener('scroll', () => {
  if (!ticking) {
    requestAnimationFrame(() => {
      const scrollY = window.scrollY + 100;
      let current = sections[0];
      for (const s of sections) { if (s.target.offsetTop <= scrollY) current = s; }
      navLinks.forEach(l => l.classList.remove('active'));
      if (current) current.link.classList.add('active');
      if (current && current.link) current.link.scrollIntoView({ block: 'nearest', behavior: 'smooth' });
      ticking = false;
    });
    ticking = true;
  }
});
if (sections.length) sections[0].link.classList.add('active');
</script>
</body>
</html>
"""

# BUILD THE FILE
parts = [HEAD, S1, S2, S3, S4, S5, S6, S7, S8, S9, S10,
         S11, S12, S13, S14, S15, S16, S17, S18, S19, S20, S21,
         S22, S23, S24, S25, S26, S27, S28, S29, S30, S31,
         S32, S33, S34, S35, S36, S37, FOOTER]

OUT.write_text("".join(parts), encoding="utf-8")
print(f"Generated: {OUT}")
print(f"Size: {OUT.stat().st_size / 1024:.0f} KB")
