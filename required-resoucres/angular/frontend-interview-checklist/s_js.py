SECTIONS = r"""

<!-- ═══════════════════════════════════════════════════════════════════
     JAVASCRIPT CORE — 12 SUB-SECTIONS
     ═══════════════════════════════════════════════════════════════════ -->

<h2 id="js-fundamentals" class="section-break">1. JavaScript Fundamentals</h2>
<p class="small"><strong>Checklist:</strong> Primitive types · type coercion · strict equality · truthy/falsy · var/let/const · TDZ · hoisting · function declarations vs expressions · arrow functions · IIFE</p>

<h3>1.1 Primitive Types</h3>
<p>JavaScript has <strong>7 primitive types</strong>: <code>string</code>, <code>number</code>, <code>boolean</code>, <code>null</code>, <code>undefined</code>, <code>symbol</code> (ES6), <code>bigint</code> (ES2020). Primitives are <strong>immutable</strong> and compared <strong>by value</strong>. Everything else (<code>Object</code>, <code>Array</code>, <code>Function</code>, <code>Date</code>, <code>Map</code>, etc.) is an <strong>object</strong> — compared by reference.</p>
<pre>typeof 'hello'     // 'string'
typeof 42          // 'number'
typeof true        // 'boolean'
typeof undefined   // 'undefined'
typeof null        // 'object'  ← historical bug, never fixed
typeof Symbol()    // 'symbol'
typeof 42n         // 'bigint'
typeof {}          // 'object'
typeof []          // 'object'  ← arrays are objects
typeof function(){} // 'function'

// Check array properly
Array.isArray([1,2,3]); // true</pre>

<h3>1.2 Type Coercion &amp; Strict Equality</h3>
<p><code>==</code> (loose equality) converts operands to the same type before comparison. <code>===</code> (strict equality) checks both type and value — <strong>always prefer <code>===</code></strong>.</p>
<pre>// Loose equality surprises
0 == ''           // true  ('' → 0)
0 == '0'          // true  ('0' → 0)
'' == '0'         // false (string comparison)
false == '0'      // true  (both → 0)
false == null     // false (null only == undefined)
null == undefined // true  (special rule)
NaN == NaN        // false (NaN is never equal to anything)

// Always use strict equality
0 === ''          // false
null === undefined // false

// Object.is — like === but handles edge cases
Object.is(NaN, NaN)   // true
Object.is(+0, -0)     // false (=== says true)</pre>

<h3>1.3 Truthy &amp; Falsy Values</h3>
<p><strong>Falsy values (only 8):</strong> <code>false</code>, <code>0</code>, <code>-0</code>, <code>0n</code>, <code>""</code>, <code>null</code>, <code>undefined</code>, <code>NaN</code>. <strong>Everything else is truthy</strong> — including <code>[]</code>, <code>{}</code>, <code>"0"</code>, <code>"false"</code>, <code>new Boolean(false)</code>.</p>
<pre>// Common interview traps
Boolean([])          // true  — empty array is truthy!
Boolean({})          // true  — empty object is truthy!
Boolean("0")         // true  — non-empty string is truthy!
Boolean(new Boolean(false)) // true — object wrapper is truthy!

// Practical: guard patterns
const name = user.name || 'Anonymous';   // problem: '' is falsy
const name2 = user.name ?? 'Anonymous';  // better: ?? only checks null/undefined</pre>

<h3>1.4 var, let, const &amp; Temporal Dead Zone</h3>
<table>
<thead><tr><th>Feature</th><th><code>var</code></th><th><code>let</code></th><th><code>const</code></th></tr></thead>
<tbody>
<tr><td>Scope</td><td>Function-scoped</td><td>Block-scoped</td><td>Block-scoped</td></tr>
<tr><td>Hoisting</td><td>Yes → initialized as <code>undefined</code></td><td>Yes → but in TDZ</td><td>Yes → but in TDZ</td></tr>
<tr><td>Redeclaration</td><td>Allowed</td><td>❌ SyntaxError</td><td>❌ SyntaxError</td></tr>
<tr><td>Reassignment</td><td>✅</td><td>✅</td><td>❌ (binding is const, not value)</td></tr>
<tr><td>Global object property</td><td>Yes (<code>window.x</code>)</td><td>No</td><td>No</td></tr>
</tbody>
</table>
<p><strong>Temporal Dead Zone (TDZ):</strong> The period between entering a block scope and reaching the <code>let</code>/<code>const</code> declaration. Accessing the variable during TDZ throws <code>ReferenceError</code>. This exists to catch bugs — using a variable before it's declared is almost always a mistake.</p>
<pre>// TDZ demonstration
{
  // TDZ for `x` starts here
  console.log(x); // ReferenceError: Cannot access 'x' before initialization
  let x = 10;     // TDZ ends here
}

// var does NOT have TDZ
console.log(y); // undefined (hoisted)
var y = 20;

// const with objects — the binding is constant, not the value
const arr = [1, 2, 3];
arr.push(4);      // ✅ mutating the array is fine
// arr = [5, 6];  // ❌ TypeError: Assignment to constant variable</pre>

<h3>1.5 Hoisting</h3>
<p>JavaScript moves declarations to the top of their scope during the compilation phase. <strong>Only declarations are hoisted, not initializations.</strong></p>
<pre>// Function declaration — fully hoisted (you can call before definition)
greet(); // "Hello!" — works!
function greet() { console.log("Hello!"); }

// Function expression — NOT hoisted (only the var declaration is)
// sayHi(); // TypeError: sayHi is not a function
var sayHi = function() { console.log("Hi!"); };

// Arrow function — NOT hoisted
// add(1,2); // ReferenceError (TDZ if using let/const)
const add = (a, b) => a + b;

// Class declarations — hoisted but IN TDZ (like let)
// const p = new Person(); // ReferenceError
class Person { constructor() {} }</pre>

<h3>1.6 Function Declarations vs Expressions vs Arrow Functions</h3>
<table>
<thead><tr><th>Feature</th><th>Declaration</th><th>Expression</th><th>Arrow</th></tr></thead>
<tbody>
<tr><td>Syntax</td><td><code>function foo() {}</code></td><td><code>const foo = function() {}</code></td><td><code>const foo = () =&gt; {}</code></td></tr>
<tr><td>Hoisted?</td><td>Yes (fully)</td><td>No</td><td>No</td></tr>
<tr><td>Has own <code>this</code>?</td><td>Yes (dynamic)</td><td>Yes (dynamic)</td><td>No (lexical — inherits from parent)</td></tr>
<tr><td>Has <code>arguments</code>?</td><td>Yes</td><td>Yes</td><td>No (use rest params)</td></tr>
<tr><td>Can be constructor?</td><td>Yes (<code>new</code>)</td><td>Yes</td><td>No (<code>new</code> throws TypeError)</td></tr>
<tr><td><code>prototype</code> property?</td><td>Yes</td><td>Yes</td><td>No</td></tr>
</tbody>
</table>

<h3>1.7 IIFE (Immediately Invoked Function Expression)</h3>
<p>A function that runs the moment it's defined. Before ES6 modules, IIFEs were the primary way to create private scope and avoid polluting the global namespace.</p>
<pre>// Classic IIFE
(function() {
  var secret = 42; // not accessible outside
  console.log('Runs immediately');
})();

// Arrow IIFE
(() => {
  const config = { debug: false };
  // ... initialization code
})();

// IIFE returning a module (Module Pattern)
const Counter = (() => {
  let count = 0; // private
  return {
    increment: () => ++count,
    decrement: () => --count,
    getCount: () => count
  };
})();
Counter.increment(); // 1
Counter.increment(); // 2
Counter.getCount();  // 2
// Counter.count → undefined (private!)</pre>

<div class="interview-q">
<h4>🎯 Interview Questions — JS Fundamentals</h4>
<p><strong>Q: What is the output?</strong></p>
<pre>console.log(typeof null);
console.log(typeof NaN);
console.log(NaN === NaN);
console.log(null == undefined);
console.log(null === undefined);</pre>
<p><strong>A:</strong> <code>'object'</code>, <code>'number'</code>, <code>false</code>, <code>true</code>, <code>false</code>. <code>typeof null</code> is a historical bug. <code>NaN</code> is type <code>number</code> but never equals itself. <code>null == undefined</code> is true by spec, but <code>===</code> checks type too.</p>

<p><strong>Q: When would you use <code>var</code> over <code>let</code>/<code>const</code>?</strong></p>
<p><strong>A:</strong> Almost never in modern code. The only edge case is when you specifically need function-scoping or want the variable on <code>window</code> (global scope). In practice, use <code>const</code> by default, <code>let</code> when rebinding is needed, <code>var</code> never.</p>

<p><strong>Q: What's the difference between <code>==</code> and <code>===</code>? When would you use <code>==</code>?</strong></p>
<p><strong>A:</strong> <code>==</code> coerces types before comparison, <code>===</code> does not. The only acceptable use of <code>==</code> is <code>x == null</code> which checks both <code>null</code> and <code>undefined</code> in one expression (equivalent to <code>x === null || x === undefined</code>).</p>
</div>

<!-- ─── Section 2: Scope & Closures ─────────────────────────────── -->
<h2 id="js-scope-closures" class="section-break">2. Scope &amp; Closures</h2>
<p class="small"><strong>Checklist:</strong> Global/function/block scope · lexical scoping · closure creation &amp; use cases · module pattern · private variables · memory implications</p>

<h3>2.1 Scope Types</h3>
<p><strong>Global scope:</strong> Variables declared outside any function/block. Accessible everywhere. In browsers, <code>var</code> globals become properties of <code>window</code>.</p>
<p><strong>Function scope:</strong> <code>var</code> is scoped to the nearest enclosing function.</p>
<p><strong>Block scope:</strong> <code>let</code>/<code>const</code> are scoped to the nearest enclosing <code>{}</code> block (if, for, while, etc.).</p>
<pre>var globalVar = 'global'; // global scope

function outer() {
  var functionVar = 'function'; // function scope
  
  if (true) {
    var stillFunction = 'var ignores blocks'; // function scope!
    let blockScoped = 'only in this if';      // block scope
    const alsoBlock = 'also only here';       // block scope
  }
  
  console.log(stillFunction); // ✅ 'var ignores blocks'
  // console.log(blockScoped); // ❌ ReferenceError
}</pre>

<h3>2.2 Lexical Scoping</h3>
<p>A function's scope is determined by <strong>where it is written</strong> in the source code, not where it is called. Inner functions can access variables of outer functions. This is the basis for closures.</p>

<h3>2.3 Closures — Deep Dive</h3>
<p>A <strong>closure</strong> is created when a function retains access to its outer (enclosing) scope's variables even after the outer function has returned. Every function in JavaScript creates a closure over its surrounding scope.</p>
<pre>// Closure in action
function createMultiplier(factor) {
  // 'factor' is enclosed (closed over)
  return function(number) {
    return number * factor; // accesses 'factor' from outer scope
  };
}
const double = createMultiplier(2);
const triple = createMultiplier(3);
double(5);  // 10 — 'factor' is 2
triple(5);  // 15 — 'factor' is 3
// createMultiplier has already returned, but 'factor' is still accessible!</pre>

<h3>2.4 Closure Use Cases</h3>

<h4>Private Variables &amp; Data Encapsulation</h4>
<pre>function createBankAccount(initialBalance) {
  let balance = initialBalance; // private — not accessible from outside
  const transactions = [];      // private
  
  return {
    deposit(amount) {
      if (amount <= 0) throw new Error('Amount must be positive');
      balance += amount;
      transactions.push({ type: 'deposit', amount, date: new Date() });
      return balance;
    },
    withdraw(amount) {
      if (amount > balance) throw new Error('Insufficient funds');
      balance -= amount;
      transactions.push({ type: 'withdraw', amount, date: new Date() });
      return balance;
    },
    getBalance() { return balance; },
    getStatement() { return [...transactions]; } // return copy
  };
}
const account = createBankAccount(1000);
account.deposit(500);   // 1500
account.withdraw(200);  // 1300
account.getBalance();   // 1300
// account.balance → undefined (truly private!)</pre>

<h4>Function Factories</h4>
<pre>// Creating specialized validators
function createValidator(regex, errorMsg) {
  return function(value) {
    if (!regex.test(value)) return errorMsg;
    return null;
  };
}
const isEmail = createValidator(/^[^@]+@[^@]+\.[^@]+$/, 'Invalid email');
const isPhone = createValidator(/^\d{10}$/, 'Must be 10 digits');
isEmail('test@example.com'); // null (valid)
isEmail('bad');              // 'Invalid email'</pre>

<h4>Event Handlers &amp; Callbacks</h4>
<pre>function setupButton(buttonId, message) {
  const button = document.getElementById(buttonId);
  let clickCount = 0; // enclosed in closure
  button.addEventListener('click', () => {
    clickCount++;
    console.log(`${message} — clicked ${clickCount} times`);
  });
}</pre>

<h3>2.5 Classic Closure Trap — Loop with var</h3>
<pre>// THE BUG: all callbacks share the same 'i'
for (var i = 0; i < 3; i++) {
  setTimeout(() => console.log(i), 100);
}
// Output: 3, 3, 3 (not 0, 1, 2!)

// FIX 1: Use let (block scoping creates new 'i' per iteration)
for (let i = 0; i < 3; i++) {
  setTimeout(() => console.log(i), 100);
}
// Output: 0, 1, 2

// FIX 2: IIFE (creates new scope per iteration)
for (var i = 0; i < 3; i++) {
  ((j) => { setTimeout(() => console.log(j), 100); })(i);
}

// FIX 3: Function factory
for (var i = 0; i < 3; i++) {
  setTimeout(((j) => () => console.log(j))(i), 100);
}</pre>

<h3>2.6 Memory Implications of Closures</h3>
<p>Closures keep their outer scope variables alive in memory as long as the closure itself exists. This can cause <strong>memory leaks</strong> if not handled carefully — especially with event listeners, timers, and subscriptions.</p>
<pre>// Memory leak example
function setupHandler() {
  const hugeArray = new Array(1000000).fill('data');
  const element = document.getElementById('btn');
  element.addEventListener('click', () => {
    // This closure keeps 'hugeArray' alive even if we only need its length
    console.log(hugeArray.length);
  });
}
// Fix: only close over what you need
function setupHandlerFixed() {
  const hugeArray = new Array(1000000).fill('data');
  const len = hugeArray.length; // extract what you need
  const element = document.getElementById('btn');
  element.addEventListener('click', () => {
    console.log(len); // only 'len' is enclosed, hugeArray can be GC'd
  });
}</pre>

<div class="interview-q">
<h4>🎯 Interview Questions — Scope &amp; Closures</h4>
<p><strong>Q: What is the output and why?</strong></p>
<pre>for (var i = 0; i < 5; i++) {
  setTimeout(function() { console.log(i); }, i * 1000);
}</pre>
<p><strong>A:</strong> Prints <code>5</code> five times (at 0s, 1s, 2s, 3s, 4s intervals). All five callbacks share the same <code>var i</code> (function-scoped). By the time any callback runs, the loop has finished and <code>i === 5</code>. Fix: use <code>let i</code> instead.</p>

<p><strong>Q: How do closures enable the Module Pattern?</strong></p>
<p><strong>A:</strong> An IIFE returns an object with methods that close over private variables. The returned object is the public API, while internal state stays hidden. This provides encapsulation without classes — used extensively before ES6 modules.</p>

<p><strong>Q: Can closures cause memory leaks? How?</strong></p>
<p><strong>A:</strong> Yes. If a closure references a large object from its outer scope, and the closure lives long (e.g., event listener never removed, timer never cleared), the large object can't be garbage collected. Fix: null out references, remove listeners, extract only needed values.</p>
</div>

<!-- ─── Section 3: The this Keyword ─────────────────────────────── -->
<h2 id="js-this" class="section-break">3. The <code>this</code> Keyword</h2>
<p class="small"><strong>Checklist:</strong> Implicit binding · explicit binding (call/apply/bind) · new binding · arrow function binding · default binding · precedence rules</p>

<h3>3.1 The Five Binding Rules</h3>
<table>
<thead><tr><th>Rule</th><th><code>this</code> equals</th><th>Example</th></tr></thead>
<tbody>
<tr><td><strong>Default binding</strong></td><td><code>window</code> (sloppy) / <code>undefined</code> (strict)</td><td><code>foo()</code> — standalone call</td></tr>
<tr><td><strong>Implicit binding</strong></td><td>The object before the dot</td><td><code>obj.foo()</code> → <code>this === obj</code></td></tr>
<tr><td><strong>Explicit binding</strong></td><td>Whatever you pass</td><td><code>foo.call(myObj)</code>, <code>foo.apply(myObj)</code>, <code>foo.bind(myObj)</code></td></tr>
<tr><td><strong>new binding</strong></td><td>The newly created object</td><td><code>new Foo()</code> → <code>this</code> is the new instance</td></tr>
<tr><td><strong>Arrow function</strong></td><td>Lexical — inherits from enclosing scope</td><td><code>() =&gt; this</code> — <code>this</code> is determined at definition time</td></tr>
</tbody>
</table>

<h3>3.2 Binding Precedence (highest → lowest)</h3>
<p><code>new</code> → <code>call</code>/<code>apply</code>/<code>bind</code> → implicit (obj.method) → default (standalone)</p>

<h3>3.3 call vs apply vs bind</h3>
<pre>function introduce(greeting, punctuation) {
  console.log(`${greeting}, I'm ${this.name}${punctuation}`);
}

const person = { name: 'Sid' };

// call — invokes immediately, args passed individually
introduce.call(person, 'Hello', '!');    // "Hello, I'm Sid!"

// apply — invokes immediately, args passed as array
introduce.apply(person, ['Hi', '.']);     // "Hi, I'm Sid."

// bind — returns a NEW function with 'this' permanently set
const boundIntro = introduce.bind(person, 'Hey');
boundIntro('?');  // "Hey, I'm Sid?"
// Can be called later, passed as callback, etc.</pre>

<h3>3.4 Implicit Binding &amp; the "Lost this" Problem</h3>
<pre>const user = {
  name: 'Sid',
  greet() { console.log(`Hi, I'm ${this.name}`); }
};

user.greet();           // "Hi, I'm Sid" — implicit: this = user

const fn = user.greet;  // extracting the method
fn();                   // "Hi, I'm undefined" — default binding: this = window/undefined

// This is why event handlers lose 'this':
// button.addEventListener('click', user.greet); // 'this' will be the button, not user

// Fixes:
// 1. bind
// button.addEventListener('click', user.greet.bind(user));
// 2. Arrow wrapper
// button.addEventListener('click', () => user.greet());
// 3. Arrow method (defined in constructor/class field)
class Component {
  name = 'Angular';
  handleClick = () => { console.log(this.name); }; // arrow: lexical this
}</pre>

<h3>3.5 Arrow Functions &amp; Lexical this</h3>
<pre>const team = {
  name: 'Frontend',
  members: ['Alice', 'Bob', 'Charlie'],
  
  // Arrow function inherits 'this' from team object's method
  listMembers() {
    this.members.forEach(member => {
      console.log(`${member} is on ${this.name}`);
      // Arrow: 'this' is the team object (from listMembers scope)
    });
  },
  
  // Regular function would have its own 'this' (undefined in forEach)
  listMembersBroken() {
    this.members.forEach(function(member) {
      console.log(`${member} is on ${this.name}`);
      // 'this' is undefined (strict) or window (sloppy) — NOT team!
    });
  }
};
team.listMembers(); // Works: "Alice is on Frontend", etc.</pre>

<div class="interview-q">
<h4>🎯 Interview Questions — this Keyword</h4>
<p><strong>Q: What will this code print?</strong></p>
<pre>const obj = {
  value: 42,
  getValue: function() { return this.value; },
  getValueArrow: () => this.value
};
console.log(obj.getValue());
console.log(obj.getValueArrow());</pre>
<p><strong>A:</strong> <code>42</code> and <code>undefined</code>. <code>getValue</code> is a regular method — implicit binding gives <code>this === obj</code>. <code>getValueArrow</code> is an arrow function — it inherits <code>this</code> from the surrounding scope (module/global), not from <code>obj</code>. Arrow functions should not be used as object methods.</p>

<p><strong>Q: Can you use <code>call</code>/<code>apply</code> to change the <code>this</code> of an arrow function?</strong></p>
<p><strong>A:</strong> No. Arrow functions have lexical <code>this</code> that is determined at definition time and cannot be changed by <code>call</code>, <code>apply</code>, <code>bind</code>, or <code>new</code>.</p>
</div>

<!-- ─── Section 4: Prototypes ─────────────────────────────────────── -->
<h2 id="js-prototypes" class="section-break">4. Prototypes &amp; Inheritance</h2>
<p class="small"><strong>Checklist:</strong> Prototype chain · __proto__ vs prototype · Object.create() · constructor functions · class syntax · prototypal inheritance · hasOwnProperty() · Object.getPrototypeOf()</p>

<h3>4.1 The Prototype Chain</h3>
<p>Every JavaScript object has a hidden internal link called <code>[[Prototype]]</code> (accessible via <code>__proto__</code> or <code>Object.getPrototypeOf()</code>). When you access a property on an object, JS first looks on the object itself, then walks up the prototype chain until it finds the property or reaches <code>null</code>.</p>
<pre>const animal = {
  alive: true,
  speak() { return `${this.name} makes a sound`; }
};

const dog = Object.create(animal); // dog's prototype is animal
dog.name = 'Rex';
dog.bark = function() { return `${this.name} barks!`; };

dog.bark();  // "Rex barks!" — found on dog itself
dog.speak(); // "Rex makes a sound" — found on prototype (animal)
dog.alive;   // true — found on prototype

// Chain: dog → animal → Object.prototype → null
Object.getPrototypeOf(dog) === animal; // true
dog.hasOwnProperty('name');  // true — own property
dog.hasOwnProperty('speak'); // false — inherited</pre>

<h3>4.2 __proto__ vs prototype</h3>
<table>
<thead><tr><th>Term</th><th>What it is</th><th>Who has it</th></tr></thead>
<tbody>
<tr><td><code>__proto__</code></td><td>Reference to the object's prototype (the thing it inherits from)</td><td>Every object</td></tr>
<tr><td><code>.prototype</code></td><td>An object that will become <code>__proto__</code> of instances created with <code>new</code></td><td>Only functions (constructors)</td></tr>
</tbody>
</table>
<pre>function Person(name) { this.name = name; }
Person.prototype.greet = function() { return `Hi, I'm ${this.name}`; };

const p = new Person('Sid');
p.__proto__ === Person.prototype;        // true
Person.prototype.constructor === Person; // true
Object.getPrototypeOf(p) === Person.prototype; // true (preferred over __proto__)</pre>

<h3>4.3 Constructor Functions &amp; Class Syntax</h3>
<pre>// Constructor function (ES5)
function Vehicle(make, model) {
  this.make = make;
  this.model = model;
}
Vehicle.prototype.describe = function() {
  return `${this.make} ${this.model}`;
};

// Class syntax (ES6) — syntactic sugar over prototypes
class Car extends Vehicle {
  constructor(make, model, year) {
    super(make, model); // calls Vehicle constructor
    this.year = year;
  }
  describe() {
    return `${this.year} ${super.describe()}`;
  }
  static compare(a, b) { return a.year - b.year; }
}

const c = new Car('Toyota', 'Camry', 2024);
c.describe(); // "2024 Toyota Camry"
c instanceof Car;     // true
c instanceof Vehicle; // true</pre>

<div class="interview-q">
<h4>🎯 Interview Questions — Prototypes</h4>
<p><strong>Q: How would you implement inheritance without using classes?</strong></p>
<p><strong>A:</strong> Use <code>Object.create()</code> to set up the prototype chain and <code>ParentConstructor.call(this, ...)</code> in the child constructor to inherit instance properties. Set <code>Child.prototype = Object.create(Parent.prototype)</code> then fix <code>Child.prototype.constructor = Child</code>.</p>

<p><strong>Q: What does <code>new</code> actually do under the hood?</strong></p>
<p><strong>A:</strong> Four steps: (1) Creates a new empty object, (2) Sets its <code>__proto__</code> to the constructor's <code>prototype</code>, (3) Calls the constructor with <code>this</code> bound to the new object, (4) Returns the new object (unless constructor explicitly returns an object).</p>
</div>

<!-- ─── Section 5: Asynchronous JavaScript ────────────────────────── -->
<h2 id="js-async" class="section-break">5. Asynchronous JavaScript</h2>
<p class="small"><strong>Checklist:</strong> Callbacks · callback hell · Promises (states, methods) · Promise.all/race/allSettled/any · async/await · try/catch · microtasks vs macrotasks · event loop · call stack · task queue · setTimeout/setInterval · requestAnimationFrame</p>

<h3>5.1 The Event Loop</h3>
<p>JavaScript is <strong>single-threaded</strong>. The event loop is the mechanism that allows async operations. It works with:</p>
<ul>
<li><strong>Call Stack:</strong> executes synchronous code, one frame at a time.</li>
<li><strong>Web APIs:</strong> browser-provided (setTimeout, fetch, DOM events) — run outside the JS engine.</li>
<li><strong>Microtask Queue:</strong> Promises, <code>queueMicrotask()</code>, <code>MutationObserver</code>. Processed <strong>after each task, before rendering</strong>.</li>
<li><strong>Macrotask Queue:</strong> <code>setTimeout</code>, <code>setInterval</code>, I/O, UI events. Processed <strong>one per loop iteration</strong>.</li>
</ul>
<p><strong>Priority:</strong> Call stack → ALL microtasks → ONE macrotask → ALL microtasks → render → next macrotask...</p>

<pre>// Classic event loop question
console.log('1');                          // sync → call stack
setTimeout(() => console.log('2'), 0);     // macrotask queue
Promise.resolve().then(() => console.log('3')); // microtask queue
queueMicrotask(() => console.log('4'));    // microtask queue  
console.log('5');                          // sync → call stack

// Output: 1, 5, 3, 4, 2
// Sync first (1, 5) → microtasks (3, 4) → macrotask (2)</pre>

<h3>5.2 Callbacks &amp; Callback Hell</h3>
<pre>// Callback hell — deeply nested, hard to read/maintain
getUser(userId, function(user) {
  getOrders(user.id, function(orders) {
    getOrderDetails(orders[0].id, function(details) {
      getShipping(details.shippingId, function(shipping) {
        console.log(shipping); // pyramid of doom!
      });
    });
  });
});</pre>

<h3>5.3 Promises — States &amp; Methods</h3>
<table>
<thead><tr><th>State</th><th>Description</th><th>Transition</th></tr></thead>
<tbody>
<tr><td><code>pending</code></td><td>Initial state — operation in progress</td><td>→ fulfilled OR rejected</td></tr>
<tr><td><code>fulfilled</code></td><td>Operation completed successfully</td><td>Final (immutable)</td></tr>
<tr><td><code>rejected</code></td><td>Operation failed</td><td>Final (immutable)</td></tr>
</tbody>
</table>
<pre>// Creating promises
const promise = new Promise((resolve, reject) => {
  // async operation...
  if (success) resolve(data);
  else reject(new Error('Failed'));
});

// Chaining — each .then returns a new promise
fetch('/api/user')
  .then(res => res.json())           // returns new promise
  .then(user => fetch(`/api/orders/${user.id}`))
  .then(res => res.json())
  .catch(err => console.error(err))  // catches ANY error in the chain
  .finally(() => hideSpinner());      // runs regardless</pre>

<h3>5.4 Promise Static Methods</h3>
<table>
<thead><tr><th>Method</th><th>Resolves when</th><th>Rejects when</th><th>Use case</th></tr></thead>
<tbody>
<tr><td><code>Promise.all([])</code></td><td>ALL fulfill</td><td>FIRST rejects</td><td>Parallel API calls where all are needed</td></tr>
<tr><td><code>Promise.race([])</code></td><td>FIRST settles</td><td>FIRST settles</td><td>Timeout pattern, fastest response</td></tr>
<tr><td><code>Promise.allSettled([])</code></td><td>ALL settle</td><td>Never rejects</td><td>Batch operations, partial success OK</td></tr>
<tr><td><code>Promise.any([])</code></td><td>FIRST fulfills</td><td>ALL reject (AggregateError)</td><td>Fastest CDN, fallback APIs</td></tr>
</tbody>
</table>
<pre>// Promise.allSettled — dashboard loading multiple widgets
const results = await Promise.allSettled([
  fetch('/api/users'),
  fetch('/api/orders'),
  fetch('/api/analytics')
]);
results.forEach((result, i) => {
  if (result.status === 'fulfilled') renderWidget(i, result.value);
  else showWidgetError(i, result.reason);
});

// Promise.race — timeout pattern
function fetchWithTimeout(url, ms) {
  return Promise.race([
    fetch(url),
    new Promise((_, reject) => setTimeout(() => reject(new Error('Timeout')), ms))
  ]);
}</pre>

<h3>5.5 async/await</h3>
<pre>// Syntactic sugar over Promises — makes async code look synchronous
async function loadDashboard(userId) {
  try {
    const user = await fetchUser(userId);           // waits for promise
    const [orders, prefs] = await Promise.all([     // parallel await
      fetchOrders(user.id),
      fetchPreferences(user.id)
    ]);
    return { user, orders, prefs };
  } catch (error) {
    if (error instanceof NetworkError) {
      return getCachedDashboard(userId); // graceful fallback
    }
    throw error; // re-throw unknown errors
  } finally {
    hideLoadingSpinner();
  }
}

// Top-level await (ES2022, in modules)
const config = await fetch('/config.json').then(r => r.json());</pre>

<h3>5.6 requestAnimationFrame</h3>
<pre>// Smooth animation — runs before next repaint (~60fps)
function animateProgress(current, target) {
  if (current < target) {
    current += 2;
    progressBar.style.width = `${current}%`;
    requestAnimationFrame(() => animateProgress(current, target));
  }
}
requestAnimationFrame(() => animateProgress(0, 100));</pre>

<div class="interview-q">
<h4>🎯 Interview Questions — Async JavaScript</h4>
<p><strong>Q: What's the output?</strong></p>
<pre>async function foo() { return 1; }
const p = foo();
console.log(p);
p.then(v => console.log(v));</pre>
<p><strong>A:</strong> First logs <code>Promise { &lt;fulfilled&gt;: 1 }</code>, then <code>1</code>. <code>async</code> always returns a promise. The <code>.then</code> callback is a microtask, so it logs after the synchronous <code>console.log</code>.</p>

<p><strong>Q: Difference between microtask and macrotask?</strong></p>
<p><strong>A:</strong> Microtasks (Promises, queueMicrotask) are processed immediately after the current task completes, before any macrotask. Macrotasks (setTimeout, setInterval) are processed one per event loop iteration. This means one <code>setTimeout</code> callback + ALL queued promise callbacks before the next <code>setTimeout</code> callback.</p>

<p><strong>Q: How would you implement parallel API calls with error handling for each?</strong></p>
<p><strong>A:</strong> Use <code>Promise.allSettled()</code> which waits for all promises and returns their statuses, or wrap each <code>fetch</code> in its own try/catch and use <code>Promise.all()</code> on the wrapped versions.</p>
</div>

<!-- ─── Section 6: ES6+ Features ──────────────────────────────────── -->
<h2 id="js-es6" class="section-break">6. ES6+ Features</h2>
<p class="small"><strong>Checklist:</strong> Destructuring · spread/rest · template literals · default params · enhanced object literals · computed property names · for...of · iterators &amp; generators · Symbol · Map/Set · WeakMap/WeakSet · optional chaining · nullish coalescing · logical assignment operators</p>

<h3>6.1 Destructuring</h3>
<pre>// Object destructuring — rename, default, nested
const response = { data: { user: { name: 'Sid', age: 28 } }, status: 200 };
const { data: { user: { name: userName, age, role = 'user' } }, status } = response;
// userName='Sid', age=28, role='user' (default), status=200

// Array destructuring — skip elements, rest
const [first, , third, ...remaining] = [1, 2, 3, 4, 5];
// first=1, third=3, remaining=[4,5]

// Swap variables
let a = 1, b = 2;
[a, b] = [b, a]; // a=2, b=1

// Function parameter destructuring
function createUser({ name, email, role = 'viewer' }) {
  return { name, email, role, createdAt: new Date() };
}</pre>

<h3>6.2 Spread &amp; Rest Operators</h3>
<pre>// Spread — expand iterable into individual elements
const arr1 = [1, 2, 3];
const arr2 = [...arr1, 4, 5];  // [1,2,3,4,5]
const obj1 = { a: 1, b: 2 };
const obj2 = { ...obj1, c: 3, b: 99 }; // { a:1, b:99, c:3 } — last wins

// Rest — collect remaining elements
function sum(...numbers) { return numbers.reduce((a, b) => a + b, 0); }
sum(1, 2, 3, 4); // 10

// Immutable array operations (critical for Angular signals/state)
const items = [1, 2, 3];
const added = [...items, 4];                    // add
const removed = items.filter(x => x !== 2);     // remove
const updated = items.map(x => x === 2 ? 99 : x); // update</pre>

<h3>6.3 Template Literals &amp; Tagged Templates</h3>
<pre>// Multi-line strings + interpolation
const html = `
  &lt;div class="card"&gt;
    &lt;h3&gt;${user.name}&lt;/h3&gt;
    &lt;p&gt;${user.bio || 'No bio provided'}&lt;/p&gt;
  &lt;/div&gt;
`;

// Tagged templates — custom string processing
function highlight(strings, ...values) {
  return strings.reduce((result, str, i) => {
    return result + str + (values[i] ? `<mark>${values[i]}</mark>` : '');
  }, '');
}
const name = 'Sid';
highlight`Hello ${name}, welcome!`; // "Hello <mark>Sid</mark>, welcome!"</pre>

<h3>6.4 Map, Set, WeakMap, WeakSet</h3>
<pre>// Map — keys can be ANY type (not just strings)
const cache = new Map();
cache.set(userObj, { data: 'cached', timestamp: Date.now() });
cache.get(userObj);  // { data: 'cached', ... }
cache.has(userObj);  // true
cache.size;          // 1
cache.delete(userObj);

// Set — unique values only
const unique = new Set([1, 2, 2, 3, 3, 3]); // Set {1, 2, 3}
unique.add(4);
unique.has(2); // true
[...unique];   // [1, 2, 3, 4]

// WeakMap — keys must be objects, entries are garbage-collectable
const metadata = new WeakMap();
function process(element) {
  if (!metadata.has(element)) {
    metadata.set(element, { processed: true, timestamp: Date.now() });
  }
}
// When 'element' is GC'd, the WeakMap entry is automatically removed
// → No memory leaks! Perfect for caching DOM node metadata.</pre>

<h3>6.5 Iterators &amp; Generators</h3>
<pre>// Iterator protocol — any object with next() method
const range = {
  from: 1, to: 5,
  [Symbol.iterator]() {
    let current = this.from;
    const last = this.to;
    return {
      next() {
        return current <= last
          ? { value: current++, done: false }
          : { done: true };
      }
    };
  }
};
for (const n of range) console.log(n); // 1, 2, 3, 4, 5

// Generator — lazy evaluation, produces values on demand
function* fibonacci() {
  let [a, b] = [0, 1];
  while (true) {
    yield a;
    [a, b] = [b, a + b];
  }
}
const fib = fibonacci();
fib.next().value; // 0
fib.next().value; // 1
fib.next().value; // 1
fib.next().value; // 2</pre>

<h3>6.6 Optional Chaining &amp; Nullish Coalescing</h3>
<pre>// Optional chaining (?.) — short-circuits to undefined
const street = user?.address?.street;           // property access
const city = user?.addresses?.[0]?.city;        // array access
const result = user?.getProfile?.();            // method call

// Nullish coalescing (??) — only checks null/undefined (NOT falsy)
const port = config.port ?? 3000;    // uses 3000 only if port is null/undefined
const port2 = config.port || 3000;   // uses 3000 if port is 0, '', false, null, undefined
// For port=0: ?? gives 0, || gives 3000

// Logical assignment operators (ES2021)
let opts = { timeout: 0, retries: null, debug: undefined };
opts.timeout ||= 5000;  // stays 0 (0 is falsy, ||= assigns)
opts.timeout ??= 5000;  // stays 0 (0 is not null/undefined)
opts.retries ??= 3;     // becomes 3 (null is nullish)
opts.debug ??= false;   // becomes false
opts.name &&= opts.name.trim(); // only trims if name is truthy</pre>

<div class="interview-q">
<h4>🎯 Interview Questions — ES6+</h4>
<p><strong>Q: When would you use Map over a plain object?</strong></p>
<p><strong>A:</strong> Use <code>Map</code> when: keys are not strings (objects, functions, numbers), you need to know the size (<code>.size</code>), you need ordered iteration, or you frequently add/remove entries (Maps are optimized for this). Use plain objects for simple string-key config/data.</p>

<p><strong>Q: What's the difference between <code>||</code> and <code>??</code>?</strong></p>
<p><strong>A:</strong> <code>||</code> returns the right side if the left is <strong>falsy</strong> (false, 0, '', null, undefined, NaN). <code>??</code> returns the right side only if the left is <strong>null or undefined</strong>. Use <code>??</code> when 0, false, or '' are valid values.</p>
</div>

<!-- ─── Section 7: Advanced Concepts ───────────────────────────────── -->
<h2 id="js-advanced" class="section-break">7. Advanced JavaScript Concepts</h2>
<p class="small"><strong>Checklist:</strong> Higher-order functions · pure functions · function composition · currying · partial application · memoization · recursion · tail call optimization · debouncing · throttling · Proxy &amp; Reflect · property descriptors · Object.defineProperty · getters/setters · immutability</p>

<h3>7.1 Higher-Order Functions &amp; Pure Functions</h3>
<p>A <strong>higher-order function</strong> takes a function as argument or returns a function. Examples: <code>map</code>, <code>filter</code>, <code>reduce</code>, <code>forEach</code>, <code>setTimeout</code>, event listeners.</p>
<p>A <strong>pure function</strong> always returns the same output for the same input and has no side effects (no mutations, no I/O, no global state changes).</p>
<pre>// Pure function — predictable, testable
const add = (a, b) => a + b; // always returns same result, no side effects

// Impure function — depends on external state
let total = 0;
const addToTotal = (n) => { total += n; return total; }; // side effect!</pre>

<h3>7.2 Currying &amp; Partial Application</h3>
<pre>// Currying — transforms f(a, b, c) into f(a)(b)(c)
const curry = (fn) => {
  const arity = fn.length;
  return function curried(...args) {
    if (args.length >= arity) return fn(...args);
    return (...moreArgs) => curried(...args, ...moreArgs);
  };
};

const multiply = curry((a, b, c) => a * b * c);
multiply(2)(3)(4);     // 24
multiply(2, 3)(4);     // 24
multiply(2)(3, 4);     // 24

// Practical: reusable config
const log = curry((level, timestamp, message) => {
  console.log(`[${level}] ${timestamp}: ${message}`);
});
const errorLog = log('ERROR');
const errorLogNow = errorLog(new Date().toISOString());
errorLogNow('Server unreachable'); // "[ERROR] 2024-...: Server unreachable"</pre>

<h3>7.3 Debounce &amp; Throttle</h3>
<pre>// Debounce — waits for pause in calls, then executes ONCE
function debounce(fn, delay, immediate = false) {
  let timer;
  return function(...args) {
    const callNow = immediate && !timer;
    clearTimeout(timer);
    timer = setTimeout(() => {
      timer = null;
      if (!immediate) fn.apply(this, args);
    }, delay);
    if (callNow) fn.apply(this, args);
  };
}
// Use: search input → API call after user stops typing (300ms)
const search = debounce((term) => fetchResults(term), 300);

// Throttle — max one execution per interval
function throttle(fn, limit) {
  let inThrottle = false;
  return function(...args) {
    if (!inThrottle) {
      fn.apply(this, args);
      inThrottle = true;
      setTimeout(() => inThrottle = false, limit);
    }
  };
}
// Use: scroll handler — fire at most once per 100ms
window.addEventListener('scroll', throttle(updatePosition, 100));</pre>

<h3>7.4 Proxy &amp; Reflect</h3>
<pre>// Proxy — intercept and customize object operations
const validator = new Proxy({}, {
  set(target, prop, value) {
    if (prop === 'age') {
      if (typeof value !== 'number') throw new TypeError('Age must be a number');
      if (value < 0 || value > 150) throw new RangeError('Invalid age');
    }
    target[prop] = value;
    return true;
  },
  get(target, prop) {
    if (prop in target) return target[prop];
    throw new ReferenceError(`Property '${prop}' does not exist`);
  }
});
validator.age = 25;   // ✅
// validator.age = -5; // RangeError

// Reflect — provides default behavior for Proxy traps
const logged = new Proxy(apiService, {
  get(target, prop, receiver) {
    console.log(`Accessing: ${String(prop)}`);
    return Reflect.get(target, prop, receiver);
  }
});</pre>

<h3>7.5 Property Descriptors &amp; Getters/Setters</h3>
<pre>// Object.defineProperty — fine-grained control
const config = {};
Object.defineProperty(config, 'apiKey', {
  value: 'secret123',
  writable: false,     // cannot be changed
  enumerable: false,   // won't show in for...in or Object.keys
  configurable: false  // cannot be deleted or reconfigured
});
config.apiKey = 'hacked'; // silently fails (throws in strict mode)

// Getters and setters
class Temperature {
  #celsius;
  constructor(celsius) { this.#celsius = celsius; }
  
  get fahrenheit() { return this.#celsius * 9/5 + 32; }
  set fahrenheit(f) { this.#celsius = (f - 32) * 5/9; }
  get celsius() { return this.#celsius; }
  set celsius(c) { this.#celsius = c; }
}
const temp = new Temperature(100);
temp.fahrenheit; // 212 — computed on access
temp.fahrenheit = 32;
temp.celsius;    // 0</pre>

<h3>7.6 Memoization</h3>
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
const factorial = memoize(function f(n) {
  return n <= 1 ? 1 : n * f(n - 1);
});
factorial(10); // calculates
factorial(10); // returns from cache instantly</pre>

<div class="interview-q">
<h4>🎯 Interview Questions — Advanced Concepts</h4>
<p><strong>Q: Implement a debounce function from scratch.</strong></p>
<p><strong>A:</strong> See section 7.3 above. Key points: use <code>clearTimeout</code> to cancel previous timer, <code>setTimeout</code> to set new one, preserve <code>this</code> context with <code>.apply()</code>, and support immediate execution for leading-edge debounce.</p>

<p><strong>Q: What's the difference between debounce and throttle?</strong></p>
<p><strong>A:</strong> <strong>Debounce</strong> waits for a pause in activity and then fires once. <strong>Throttle</strong> fires at regular intervals during continuous activity. Debounce for search input (wait for user to stop typing). Throttle for scroll/resize (fire regularly while scrolling).</p>
</div>

<!-- ─── Section 8: Array Methods ───────────────────────────────────── -->
<h2 id="js-array-methods" class="section-break">8. Array Methods</h2>
<p class="small"><strong>Checklist:</strong> map · filter · reduce · forEach · some · every · find · findIndex · slice · splice · concat · join · split · sort · flat · flatMap · Array.from/of · includes · indexOf</p>

<h3>8.1 Transforming: map, filter, reduce</h3>
<pre>const products = [
  { name: 'Laptop', price: 1200, inStock: true },
  { name: 'Phone', price: 800, inStock: false },
  { name: 'Tablet', price: 500, inStock: true },
  { name: 'Watch', price: 300, inStock: true }
];

// map — transform each element (returns new array)
const names = products.map(p => p.name); // ['Laptop', 'Phone', 'Tablet', 'Watch']

// filter — keep elements matching condition
const available = products.filter(p => p.inStock); // 3 items

// reduce — accumulate into single value
const totalValue = products.reduce((sum, p) => sum + p.price, 0); // 2800

// Chaining — real-world data pipeline
const avgInStockPrice = products
  .filter(p => p.inStock)
  .map(p => p.price)
  .reduce((sum, price, _, arr) => sum + price / arr.length, 0);
// (1200 + 500 + 300) / 3 = 666.67</pre>

<h3>8.2 Searching: find, findIndex, some, every, includes</h3>
<pre>// find — returns first matching element (or undefined)
const phone = products.find(p => p.name === 'Phone'); // { name: 'Phone', ... }

// findIndex — returns index (or -1)
const idx = products.findIndex(p => p.price > 1000); // 0

// some — returns true if ANY element matches
const hasExpensive = products.some(p => p.price > 1000); // true

// every — returns true if ALL elements match
const allInStock = products.every(p => p.inStock); // false

// includes — simple value check
[1, 2, 3].includes(2); // true</pre>

<h3>8.3 Mutating vs Non-Mutating</h3>
<table>
<thead><tr><th>Non-mutating (returns new)</th><th>Mutating (changes original)</th></tr></thead>
<tbody>
<tr><td><code>map</code>, <code>filter</code>, <code>reduce</code></td><td><code>push</code>, <code>pop</code>, <code>shift</code>, <code>unshift</code></td></tr>
<tr><td><code>slice</code>, <code>concat</code>, <code>flat</code></td><td><code>splice</code>, <code>sort</code>, <code>reverse</code>, <code>fill</code></td></tr>
<tr><td><code>find</code>, <code>some</code>, <code>every</code></td><td></td></tr>
</tbody>
</table>
<pre>// slice vs splice
const arr = [1, 2, 3, 4, 5];
arr.slice(1, 3);    // [2, 3] — does NOT modify arr
arr.splice(1, 2);   // [2, 3] — REMOVES from arr, arr is now [1, 4, 5]

// sort — MUTATES! Always copy first
const prices = [300, 1200, 500, 800];
const sorted = [...prices].sort((a, b) => a - b); // [300, 500, 800, 1200]
// prices is still [300, 1200, 500, 800]

// flat & flatMap
const nested = [1, [2, 3], [4, [5, 6]]];
nested.flat();    // [1, 2, 3, 4, [5, 6]]
nested.flat(Infinity); // [1, 2, 3, 4, 5, 6]

// flatMap = map + flat(1)
const sentences = ['hello world', 'foo bar'];
sentences.flatMap(s => s.split(' ')); // ['hello', 'world', 'foo', 'bar']

// Array.from — convert iterables/array-like to arrays
Array.from({ length: 5 }, (_, i) => i * 2); // [0, 2, 4, 6, 8]
Array.from(document.querySelectorAll('li')); // NodeList → Array</pre>

<div class="interview-q">
<h4>🎯 Interview Questions — Array Methods</h4>
<p><strong>Q: Implement <code>Array.prototype.reduce</code> from scratch.</strong></p>
<pre>Array.prototype.myReduce = function(callback, initialValue) {
  let accumulator = initialValue;
  let startIndex = 0;
  if (accumulator === undefined) {
    if (this.length === 0) throw new TypeError('Reduce of empty array with no initial value');
    accumulator = this[0];
    startIndex = 1;
  }
  for (let i = startIndex; i < this.length; i++) {
    accumulator = callback(accumulator, this[i], i, this);
  }
  return accumulator;
};</pre>
<p><strong>Q: What's the difference between <code>map</code> and <code>forEach</code>?</strong></p>
<p><strong>A:</strong> <code>map</code> returns a new array with transformed values. <code>forEach</code> returns <code>undefined</code> — it's for side effects only. <code>map</code> is chainable, <code>forEach</code> is not. If you need the result, use <code>map</code>.</p>
</div>

<!-- ─── Section 9: Object Methods ──────────────────────────────────── -->
<h2 id="js-object-methods" class="section-break">9. Object Methods</h2>
<p class="small"><strong>Checklist:</strong> Object.keys/values/entries · Object.assign · Object.freeze/seal · Object.is · spread syntax · shallow vs deep cloning</p>

<pre>const user = { name: 'Sid', age: 28, role: 'developer' };

// Iteration methods
Object.keys(user);    // ['name', 'age', 'role']
Object.values(user);  // ['Sid', 28, 'developer']
Object.entries(user); // [['name','Sid'], ['age',28], ['role','developer']]

// Object.fromEntries — reverse of entries
const params = new URLSearchParams('page=1&sort=name');
const obj = Object.fromEntries(params); // { page: '1', sort: 'name' }

// Object.assign — merge objects (shallow)
const defaults = { theme: 'light', lang: 'en', debug: false };
const overrides = { theme: 'dark', debug: true };
const config = Object.assign({}, defaults, overrides);
// { theme: 'dark', lang: 'en', debug: true }

// Object.freeze vs Object.seal
const frozen = Object.freeze({ a: 1, nested: { b: 2 } });
// frozen.a = 99;          // ❌ silently fails (throws in strict)
// frozen.newProp = 'x';   // ❌ cannot add
frozen.nested.b = 99;      // ✅ freeze is SHALLOW — nested objects still mutable!

const sealed = Object.seal({ x: 1, y: 2 });
sealed.x = 99;             // ✅ can modify existing
// sealed.z = 3;           // ❌ cannot add new
// delete sealed.x;        // ❌ cannot delete

// Deep clone
const original = { a: 1, nested: { b: 2 }, arr: [1, 2] };
const deepCopy = structuredClone(original); // modern JS (2022)
deepCopy.nested.b = 99;
console.log(original.nested.b); // 2 — independent!</pre>

<div class="interview-q">
<h4>🎯 Interview Questions — Object Methods</h4>
<p><strong>Q: How do you deep clone an object in JavaScript?</strong></p>
<p><strong>A:</strong> (1) <code>structuredClone(obj)</code> — modern, handles circular refs, dates, maps. (2) <code>JSON.parse(JSON.stringify(obj))</code> — works for simple data but loses functions, undefined, Date objects, and fails on circular refs. (3) Recursive manual clone. (4) Libraries like lodash's <code>_.cloneDeep</code>.</p>
</div>

<!-- ─── Section 10: Error Handling ─────────────────────────────────── -->
<h2 id="js-error-handling" class="section-break">10. Error Handling</h2>
<p class="small"><strong>Checklist:</strong> try/catch/finally · error types (TypeError, ReferenceError, SyntaxError) · custom error classes · error propagation · async error handling</p>

<pre>// Built-in Error types
// TypeError: wrong type operation — e.g., null.toString()
// ReferenceError: accessing undeclared variable
// SyntaxError: invalid code — caught at parse time (can't catch with try/catch)
// RangeError: value out of range — e.g., new Array(-1)
// URIError: malformed URI — e.g., decodeURIComponent('%')

// Custom Error class
class HttpError extends Error {
  constructor(statusCode, message, endpoint) {
    super(message);
    this.name = 'HttpError';
    this.statusCode = statusCode;
    this.endpoint = endpoint;
  }
  
  get isClientError() { return this.statusCode >= 400 && this.statusCode < 500; }
  get isServerError() { return this.statusCode >= 500; }
}

// Error handling patterns
async function fetchData(url) {
  try {
    const res = await fetch(url);
    if (!res.ok) throw new HttpError(res.status, res.statusText, url);
    return await res.json();
  } catch (error) {
    if (error instanceof HttpError && error.isClientError) {
      console.warn(`Client error at ${error.endpoint}: ${error.statusCode}`);
      return null; // graceful fallback
    }
    throw error; // re-throw server errors and network errors
  } finally {
    hideLoadingSpinner(); // always runs — cleanup
  }
}

// Global error handlers
window.addEventListener('error', (event) => {
  sendToErrorTracking({ message: event.message, stack: event.error?.stack });
});
window.addEventListener('unhandledrejection', (event) => {
  sendToErrorTracking({ message: event.reason?.message || 'Unhandled rejection' });
  event.preventDefault(); // prevent default browser logging
});</pre>

<div class="interview-q">
<h4>🎯 Interview Questions — Error Handling</h4>
<p><strong>Q: Does <code>finally</code> always execute?</strong></p>
<p><strong>A:</strong> Yes, <code>finally</code> always executes whether try succeeds, fails, or throws. Even if there's a <code>return</code> in try or catch, finally runs before the return actually completes. A <code>return</code> in finally overrides the return value from try/catch.</p>
</div>

<!-- ─── Section 11: Modules ────────────────────────────────────────── -->
<h2 id="js-modules" class="section-break">11. Modules</h2>
<p class="small"><strong>Checklist:</strong> ES6 modules (import/export) · named vs default exports · dynamic imports · CommonJS (require/module.exports) · module bundling concepts</p>

<pre>// ─── Named exports ───
// utils.js
export function formatDate(d) { return d.toISOString().split('T')[0]; }
export function formatCurrency(n) { return `$${n.toFixed(2)}`; }
export const API_URL = '/api/v1';

// Importing named exports
import { formatDate, formatCurrency } from './utils.js';
import { formatDate as fmtDate } from './utils.js'; // rename
import * as Utils from './utils.js'; // namespace

// ─── Default export ───
// logger.js
export default class Logger {
  log(msg) { console.log(`[LOG] ${msg}`); }
}
import Logger from './logger.js'; // any name works for default

// ─── Re-exporting (barrel files) ───
// index.js
export { formatDate, formatCurrency } from './utils.js';
export { default as Logger } from './logger.js';

// ─── Dynamic imports — lazy loading ───
async function loadChart() {
  const { Chart } = await import('./chart-library.js'); // loaded on demand
  return new Chart(canvas, config);
}
// Use case: Angular lazy-loaded routes, heavy libraries

// ─── CommonJS (Node.js) ───
// math.js
module.exports = { add: (a, b) => a + b };
// app.js
const { add } = require('./math.js');
// Key difference: CommonJS is synchronous, ES modules are async-capable</pre>

<div class="interview-q">
<h4>🎯 Interview Questions — Modules</h4>
<p><strong>Q: What's tree shaking and how do modules enable it?</strong></p>
<p><strong>A:</strong> Tree shaking removes unused code during bundling. It works with ES modules because their imports/exports are <strong>static</strong> — determined at compile time, not runtime. CommonJS <code>require()</code> is dynamic and can't be tree-shaken reliably.</p>
</div>

<!-- ─── Section 12: Regular Expressions ────────────────────────────── -->
<h2 id="js-regex" class="section-break">12. Regular Expressions</h2>
<p class="small"><strong>Checklist:</strong> Pattern matching · flags (g, i, m, s, u, y) · character classes · quantifiers · groups &amp; capturing · lookahead/lookbehind · string methods (match, search, replace, split)</p>

<pre>// Common patterns for interviews
const patterns = {
  email: /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/,
  phone: /^\+?\d{1,3}[-.\s]?\(?\d{1,4}\)?[-.\s]?\d{1,4}[-.\s]?\d{1,9}$/,
  url: /^https?:\/\/(www\.)?[\w.-]+(:\d+)?(\/[\w./%-]*)?(\?[&\w=%-]*)?(#[\w-]*)?$/,
  strongPassword: /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/
};

// Named capture groups
const dateStr = '2024-03-15';
const { groups: { year, month, day } } =
  dateStr.match(/(?<year>\d{4})-(?<month>\d{2})-(?<day>\d{2})/);

// Lookahead & lookbehind
'100px 200em 50%'.match(/\d+(?=px)/g);    // ['100'] — followed by 'px'
'$100 €200 £50'.match(/(?<=\$)\d+/g);      // ['100'] — preceded by '$'

// Replace with function
const camelCase = 'backgroundColor'.replace(/([A-Z])/g, '-$1').toLowerCase();
// 'background-color'

// Template parsing
const template = 'Hello {{name}}, you have {{count}} messages';
const data = { name: 'Sid', count: 42 };
template.replace(/\{\{(\w+)\}\}/g, (_, key) => data[key] ?? '');
// 'Hello Sid, you have 42 messages'

// Flags
// g: global — find all matches
// i: case-insensitive
// m: multiline — ^ and $ match line boundaries
// s: dotAll — . matches newlines
// u: unicode — correct unicode handling
// y: sticky — match at exact position</pre>

<div class="interview-q">
<h4>🎯 Interview Questions — Regex</h4>
<p><strong>Q: Write a regex to validate an email address.</strong></p>
<p><strong>A:</strong> <code>/^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/</code>. Note: true email validation per RFC 5322 is extremely complex. In production, send a verification email instead of relying solely on regex.</p>
</div>
"""
