SECTIONS = r"""

<!-- ═══════════════════════════════════════════════════════════════════
     CONCEPT-BASED CODING CHALLENGES — Part 2
     Array & Object Manipulation · Recursion & Trees · Event Emitter & Observables
     ═══════════════════════════════════════════════════════════════════ -->

<h2 id="cc-array-object" class="section-break">134. Coding Challenges — Array &amp; Object Manipulation</h2>
<p class="small"><strong>Concept Focus:</strong> map/filter/reduce patterns · flat/groupBy · deep clone · object diff · immutable updates · custom iterators</p>

<h3>134.1 Basic — Group By Property</h3>
<pre>// groupBy(array, keyFn) — group items by a computed key
function groupBy(arr, keyFn) {
  return arr.reduce((groups, item) => {
    const key = typeof keyFn === 'function' ? keyFn(item) : item[keyFn];
    (groups[key] ??= []).push(item);
    return groups;
  }, {});
}

const users = [
  { name: 'Alice', role: 'admin' },
  { name: 'Bob',   role: 'user'  },
  { name: 'Carol', role: 'admin' },
  { name: 'Dave',  role: 'user'  },
];

console.log(groupBy(users, 'role'));
// {
//   admin: [{name:'Alice',role:'admin'}, {name:'Carol',role:'admin'}],
//   user:  [{name:'Bob',role:'user'}, {name:'Dave',role:'user'}]
// }

// With function key:
console.log(groupBy([1,2,3,4,5,6], n => n % 2 === 0 ? 'even' : 'odd'));
// { odd: [1,3,5], even: [2,4,6] }</pre>

<h3>134.2 Basic — Flatten Array to Depth</h3>
<pre>// flat(arr, depth) — flatten nested arrays to specified depth
function flat(arr, depth = 1) {
  if (depth <= 0) return arr.slice();
  
  return arr.reduce((acc, item) => {
    if (Array.isArray(item)) {
      acc.push(...flat(item, depth - 1));
    } else {
      acc.push(item);
    }
    return acc;
  }, []);
}

console.log(flat([1, [2, [3, [4]]]], 1));     // [1, 2, [3, [4]]]
console.log(flat([1, [2, [3, [4]]]], 2));     // [1, 2, 3, [4]]
console.log(flat([1, [2, [3, [4]]]], Infinity)); // [1, 2, 3, 4]

// Iterative version (no recursion, no stack overflow):
function flatIterative(arr, depth = 1) {
  let result = [...arr];
  for (let d = 0; d < depth; d++) {
    const next = [];
    let didFlatten = false;
    for (const item of result) {
      if (Array.isArray(item)) {
        next.push(...item);
        didFlatten = true;
      } else {
        next.push(item);
      }
    }
    result = next;
    if (!didFlatten) break;
  }
  return result;
}</pre>

<h3>134.3 Intermediate — Deep Clone (handle all types)</h3>
<pre>// Deep clone that handles: objects, arrays, Date, RegExp, Map, Set, circular refs
function deepClone(obj, seen = new WeakMap()) {
  // Primitives + functions
  if (obj === null || typeof obj !== 'object') return obj;
  
  // Circular reference
  if (seen.has(obj)) return seen.get(obj);
  
  // Special types
  if (obj instanceof Date) return new Date(obj.getTime());
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
  
  // Arrays and plain objects
  const clone = Array.isArray(obj) ? [] : Object.create(Object.getPrototypeOf(obj));
  seen.set(obj, clone);
  
  for (const key of Reflect.ownKeys(obj)) {
    clone[key] = deepClone(obj[key], seen);
  }
  
  return clone;
}

// Test circular reference:
const a = { x: 1 };
a.self = a;
const b = deepClone(a);
console.log(b.self === b);      // true (correctly cloned circular ref)
console.log(b.self === a);      // false (different object)</pre>

<h3>134.4 Intermediate — Object Diff (find changes between two objects)</h3>
<pre>// diff(oldObj, newObj) — returns what changed, added, removed
function diff(oldObj, newObj, path = '') {
  const changes = [];
  const allKeys = new Set([...Object.keys(oldObj), ...Object.keys(newObj)]);
  
  for (const key of allKeys) {
    const fullPath = path ? `${path}.${key}` : key;
    const oldVal = oldObj[key];
    const newVal = newObj[key];
    
    if (!(key in oldObj)) {
      changes.push({ type: 'added', path: fullPath, value: newVal });
    } else if (!(key in newObj)) {
      changes.push({ type: 'removed', path: fullPath, oldValue: oldVal });
    } else if (typeof oldVal === 'object' && typeof newVal === 'object'
               && oldVal !== null && newVal !== null
               && !Array.isArray(oldVal) && !Array.isArray(newVal)) {
      changes.push(...diff(oldVal, newVal, fullPath));
    } else if (oldVal !== newVal) {
      changes.push({ type: 'changed', path: fullPath, oldValue: oldVal, newValue: newVal });
    }
  }
  
  return changes;
}

const before = { name: 'Alice', age: 25, address: { city: 'NYC', zip: '10001' } };
const after  = { name: 'Alice', age: 26, address: { city: 'LA',  zip: '10001' }, role: 'admin' };

console.log(diff(before, after));
// [
//   { type: 'changed', path: 'age', oldValue: 25, newValue: 26 },
//   { type: 'changed', path: 'address.city', oldValue: 'NYC', newValue: 'LA' },
//   { type: 'added',   path: 'role', value: 'admin' }
// ]</pre>

<h3>134.5 Advanced — Immutable Update Helper (like immer's produce)</h3>
<pre>// setIn(obj, path, value) — returns NEW object with value set at path
function setIn(obj, pathStr, value) {
  const path = pathStr.split('.');
  
  function helper(current, index) {
    if (index === path.length) return value;
    
    const key = path[index];
    const isArray = Array.isArray(current);
    const clone = isArray ? [...current] : { ...current };
    
    clone[key] = helper(current?.[key] ?? {}, index + 1);
    return clone;
  }
  
  return helper(obj, 0);
}

// deleteIn — returns NEW object with key removed at path
function deleteIn(obj, pathStr) {
  const path = pathStr.split('.');
  const lastKey = path.pop();
  
  if (path.length === 0) {
    const { [lastKey]: _, ...rest } = obj;
    return rest;
  }
  
  const parent = path.reduce((o, k) => o?.[k], obj);
  if (!parent) return obj;
  
  return setIn(obj, path.join('.'), (() => {
    const { [lastKey]: _, ...rest } = parent;
    return rest;
  })());
}

const state = { user: { name: 'Alice', settings: { theme: 'dark' } } };
const next = setIn(state, 'user.settings.theme', 'light');

console.log(next.user.settings.theme);  // 'light'
console.log(state.user.settings.theme); // 'dark' — original unchanged
console.log(next === state);            // false
console.log(next.user.name === state.user.name); // true — shared ref!</pre>

<h3>134.6 Advanced — Custom Iterable + Lazy Evaluation</h3>
<pre>// Create a lazy range that supports chaining (like Lodash lazy)
class LazySeq {
  constructor(iterable) {
    this._iterable = iterable;
  }
  
  static range(start, end, step = 1) {
    return new LazySeq(function*() {
      for (let i = start; i < end; i += step) yield i;
    }());
  }
  
  static from(arr) {
    return new LazySeq(arr[Symbol.iterator]());
  }
  
  map(fn) {
    const source = this._iterable;
    return new LazySeq(function*() {
      for (const item of source) yield fn(item);
    }());
  }
  
  filter(fn) {
    const source = this._iterable;
    return new LazySeq(function*() {
      for (const item of source) {
        if (fn(item)) yield item;
      }
    }());
  }
  
  take(n) {
    const source = this._iterable;
    return new LazySeq(function*() {
      let count = 0;
      for (const item of source) {
        if (count++ >= n) return;
        yield item;
      }
    }());
  }
  
  toArray() {
    return [...this._iterable];
  }
  
  [Symbol.iterator]() {
    return this._iterable[Symbol.iterator]();
  }
}

// None of these intermediate steps create full arrays!
const result = LazySeq.range(1, 10000000)
  .filter(n => n % 2 === 0)  // lazy
  .map(n => n * n)            // lazy
  .take(5)                    // lazy — stops after 5
  .toArray();                 // only NOW does it execute

console.log(result); // [4, 16, 36, 64, 100]</pre>

<div class="interview-q">
<p><strong>💡 Interview Tip — Array &amp; Object:</strong></p>
<ul>
  <li><strong>Q: structuredClone vs JSON.parse(JSON.stringify)?</strong> structuredClone handles circular refs, Date, Map, Set, ArrayBuffer. JSON method loses them all and fails on circular refs.</li>
  <li><strong>Q: Why immutable updates?</strong> Reference equality checks (===) become O(1) change detection. Crucial for React/Angular OnPush.</li>
  <li><strong>Q: Lazy vs eager evaluation?</strong> Lazy processes items one at a time through the chain. Eager creates intermediate arrays. Lazy = less memory for large datasets.</li>
</ul>
</div>


<h2 id="cc-recursion-trees" class="section-break">135. Coding Challenges — Recursion &amp; Tree Traversal</h2>
<p class="small"><strong>Concept Focus:</strong> Base cases · tree DFS/BFS · nested data structures · DOM traversal · flatten/unflatten · recursive backtracking</p>

<h3>135.1 Basic — Flatten Nested Object to Dot Notation</h3>
<pre>// { a: { b: { c: 1 } } } → { 'a.b.c': 1 }
function flattenObject(obj, prefix = '', result = {}) {
  for (const [key, value] of Object.entries(obj)) {
    const path = prefix ? `${prefix}.${key}` : key;
    
    if (typeof value === 'object' && value !== null && !Array.isArray(value)) {
      flattenObject(value, path, result);
    } else {
      result[path] = value;
    }
  }
  return result;
}

// Reverse: unflatten
function unflattenObject(flat) {
  const result = {};
  for (const [path, value] of Object.entries(flat)) {
    const keys = path.split('.');
    let current = result;
    for (let i = 0; i < keys.length - 1; i++) {
      current[keys[i]] ??= {};
      current = current[keys[i]];
    }
    current[keys[keys.length - 1]] = value;
  }
  return result;
}

const nested = { user: { name: 'Alice', address: { city: 'NYC', zip: '10001' } } };
const flat = flattenObject(nested);
console.log(flat);
// { 'user.name': 'Alice', 'user.address.city': 'NYC', 'user.address.zip': '10001' }

console.log(unflattenObject(flat));
// Original nested structure restored!</pre>

<h3>135.2 Intermediate — DOM Tree Traversal (DFS &amp; BFS)</h3>
<pre>// DFS — depth-first traversal of DOM tree
function dfsDOM(node, callback) {
  callback(node);
  for (const child of node.children) {
    dfsDOM(child, callback);
  }
}

// BFS — breadth-first traversal of DOM tree
function bfsDOM(root, callback) {
  const queue = [root];
  while (queue.length > 0) {
    const node = queue.shift();
    callback(node);
    for (const child of node.children) {
      queue.push(child);
    }
  }
}

// Find all text nodes
function getAllTextNodes(root) {
  const texts = [];
  const walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT);
  while (walker.nextNode()) {
    const text = walker.currentNode.textContent.trim();
    if (text) texts.push(text);
  }
  return texts;
}

// Get DOM depth
function getDepth(node) {
  if (!node.children.length) return 0;
  return 1 + Math.max(...[...node.children].map(getDepth));
}</pre>

<h3>135.3 Intermediate — File System Tree (render like "tree" command)</h3>
<pre>// Given a file-system-like tree structure, render it like the 'tree' command
const fileSystem = {
  name: 'root',
  children: [
    { name: 'src', children: [
      { name: 'index.ts', children: [] },
      { name: 'utils', children: [
        { name: 'helpers.ts', children: [] },
        { name: 'constants.ts', children: [] },
      ]},
    ]},
    { name: 'package.json', children: [] },
    { name: 'README.md', children: [] },
  ],
};

function printTree(node, prefix = '', isLast = true) {
  const connector = isLast ? '└── ' : '├── ';
  const line = prefix + connector + node.name;
  console.log(line);
  
  const children = node.children || [];
  children.forEach((child, index) => {
    const childPrefix = prefix + (isLast ? '    ' : '│   ');
    printTree(child, childPrefix, index === children.length - 1);
  });
}

printTree(fileSystem, '', true);
// └── root
//     ├── src
//     │   ├── index.ts
//     │   └── utils
//     │       ├── helpers.ts
//     │       └── constants.ts
//     ├── package.json
//     └── README.md</pre>

<h3>135.4 Advanced — JSON Path Query (like $.store.book[*].author)</h3>
<pre>// Simple JSONPath-like query engine
function jsonQuery(obj, path) {
  const tokens = path.replace('$', '').split('.').filter(Boolean);
  let results = [obj];
  
  for (const token of tokens) {
    const nextResults = [];
    
    for (const current of results) {
      if (token === '*') {
        // Wildcard — all values
        if (Array.isArray(current)) {
          nextResults.push(...current);
        } else if (typeof current === 'object' && current !== null) {
          nextResults.push(...Object.values(current));
        }
      } else if (token.includes('[') && token.includes(']')) {
        // Array access: books[0] or books[*]
        const [key, indexStr] = token.split('[');
        const idx = indexStr.replace(']', '');
        const arr = current[key];
        if (!Array.isArray(arr)) continue;
        if (idx === '*') nextResults.push(...arr);
        else nextResults.push(arr[parseInt(idx)]);
      } else {
        if (current && current[token] !== undefined) {
          nextResults.push(current[token]);
        }
      }
    }
    
    results = nextResults;
  }
  
  return results;
}

const data = {
  store: {
    books: [
      { title: 'JS Guide', author: 'Alice', price: 29 },
      { title: 'CSS Magic', author: 'Bob', price: 19 },
      { title: 'TS Deep', author: 'Carol', price: 35 },
    ]
  }
};

console.log(jsonQuery(data, '$.store.books[*].author'));
// ['Alice', 'Bob', 'Carol']

console.log(jsonQuery(data, '$.store.books[0].title'));
// ['JS Guide']</pre>

<h3>135.5 Advanced — Recursive Backtracking (generate permutations)</h3>
<pre>// Generate all permutations of an array
function permutations(arr) {
  if (arr.length <= 1) return [arr];
  
  const result = [];
  for (let i = 0; i < arr.length; i++) {
    const rest = [...arr.slice(0, i), ...arr.slice(i + 1)];
    for (const perm of permutations(rest)) {
      result.push([arr[i], ...perm]);
    }
  }
  return result;
}

console.log(permutations([1, 2, 3]));
// [[1,2,3],[1,3,2],[2,1,3],[2,3,1],[3,1,2],[3,2,1]]

// Generate all subsets (power set)
function subsets(arr) {
  const result = [[]];
  for (const item of arr) {
    const len = result.length;
    for (let i = 0; i < len; i++) {
      result.push([...result[i], item]);
    }
  }
  return result;
}

console.log(subsets([1, 2, 3]));
// [[], [1], [2], [1,2], [3], [1,3], [2,3], [1,2,3]]

// Generate balanced parentheses
function generateParens(n) {
  const result = [];
  
  function backtrack(current, open, close) {
    if (current.length === 2 * n) {
      result.push(current);
      return;
    }
    if (open < n) backtrack(current + '(', open + 1, close);
    if (close < open) backtrack(current + ')', open, close + 1);
  }
  
  backtrack('', 0, 0);
  return result;
}

console.log(generateParens(3));
// ['((()))', '(()())', '(())()', '()(())', '()()()']</pre>

<div class="interview-q">
<p><strong>💡 Interview Tip — Recursion:</strong></p>
<ul>
  <li><strong>Q: How to avoid stack overflow?</strong> (1) Convert to iterative with explicit stack/queue. (2) Tail-call optimization (limited support). (3) Trampoline pattern.</li>
  <li><strong>Q: DFS vs BFS for DOM?</strong> DFS is natural for DOM (parent→child). BFS useful for level-order rendering, finding nearest element matching a condition.</li>
  <li><strong>Q: Time complexity of permutations?</strong> O(n!) — can't do better since there ARE n! permutations.</li>
</ul>
</div>


<h2 id="cc-event-emitter" class="section-break">136. Coding Challenges — Event Emitter &amp; Observer Pattern</h2>
<p class="small"><strong>Concept Focus:</strong> Pub-sub pattern · event namespacing · once listeners · wildcard events · typed events · RxJS-like Observable from scratch</p>

<h3>136.1 Basic — Simple EventEmitter</h3>
<pre>// Core EventEmitter — on, off, emit
class EventEmitter {
  #events = new Map();
  
  on(event, listener) {
    if (!this.#events.has(event)) {
      this.#events.set(event, []);
    }
    this.#events.get(event).push(listener);
    return this; // allow chaining
  }
  
  off(event, listener) {
    const listeners = this.#events.get(event);
    if (listeners) {
      this.#events.set(event, listeners.filter(l => l !== listener && l._original !== listener));
    }
    return this;
  }
  
  emit(event, ...args) {
    const listeners = this.#events.get(event) || [];
    listeners.forEach(l => l(...args));
    return listeners.length > 0;
  }
}

const emitter = new EventEmitter();
const handler = (msg) => console.log(`Received: ${msg}`);
emitter.on('message', handler);
emitter.emit('message', 'Hello');  // "Received: Hello"
emitter.off('message', handler);
emitter.emit('message', 'Hello');  // nothing</pre>

<h3>136.2 Intermediate — once() + removeAllListeners()</h3>
<pre>class EventEmitter {
  #events = new Map();
  
  on(event, listener) {
    if (!this.#events.has(event)) this.#events.set(event, []);
    this.#events.get(event).push(listener);
    return this;
  }
  
  once(event, listener) {
    const wrapper = (...args) => {
      this.off(event, wrapper);
      listener(...args);
    };
    wrapper._original = listener; // for off() to find it
    return this.on(event, wrapper);
  }
  
  off(event, listener) {
    const listeners = this.#events.get(event);
    if (listeners) {
      this.#events.set(event, listeners.filter(l => l !== listener && l._original !== listener));
    }
    return this;
  }
  
  emit(event, ...args) {
    const listeners = [...(this.#events.get(event) || [])]; // copy to handle once()
    listeners.forEach(l => l(...args));
    return listeners.length > 0;
  }
  
  removeAllListeners(event) {
    if (event) this.#events.delete(event);
    else this.#events.clear();
    return this;
  }
  
  listenerCount(event) {
    return (this.#events.get(event) || []).length;
  }
}

const ee = new EventEmitter();
ee.once('connect', () => console.log('Connected!'));
ee.emit('connect'); // "Connected!"
ee.emit('connect'); // nothing — listener was auto-removed</pre>

<h3>136.3 Advanced — Observable from Scratch (simplified RxJS)</h3>
<pre>// Simplified Observable with map, filter, subscribe, unsubscribe
class Observable {
  constructor(subscribeFn) {
    this._subscribeFn = subscribeFn;
  }
  
  subscribe(observer) {
    // Normalize: accept function or { next, error, complete }
    const obs = typeof observer === 'function'
      ? { next: observer, error: () => {}, complete: () => {} }
      : { next: observer.next || (() => {}),
          error: observer.error || (() => {}),
          complete: observer.complete || (() => {}) };
    
    let isUnsubscribed = false;
    const safeObserver = {
      next: (v) => { if (!isUnsubscribed) obs.next(v); },
      error: (e) => { if (!isUnsubscribed) { obs.error(e); isUnsubscribed = true; } },
      complete: () => { if (!isUnsubscribed) { obs.complete(); isUnsubscribed = true; } },
    };
    
    const teardown = this._subscribeFn(safeObserver);
    
    return {
      unsubscribe() {
        isUnsubscribed = true;
        if (typeof teardown === 'function') teardown();
      }
    };
  }
  
  // Operators return NEW Observables (immutable chain)
  map(fn) {
    return new Observable((observer) => {
      return this.subscribe({
        next: (v) => observer.next(fn(v)),
        error: (e) => observer.error(e),
        complete: () => observer.complete(),
      }).unsubscribe;
    });
  }
  
  filter(fn) {
    return new Observable((observer) => {
      return this.subscribe({
        next: (v) => { if (fn(v)) observer.next(v); },
        error: (e) => observer.error(e),
        complete: () => observer.complete(),
      }).unsubscribe;
    });
  }
  
  take(n) {
    return new Observable((observer) => {
      let count = 0;
      const sub = this.subscribe({
        next: (v) => {
          observer.next(v);
          if (++count >= n) {
            observer.complete();
            sub.unsubscribe();
          }
        },
        error: (e) => observer.error(e),
        complete: () => observer.complete(),
      });
      return () => sub.unsubscribe();
    });
  }
  
  // Static creators
  static fromEvent(element, eventName) {
    return new Observable((observer) => {
      const handler = (e) => observer.next(e);
      element.addEventListener(eventName, handler);
      return () => element.removeEventListener(eventName, handler);
    });
  }
  
  static interval(ms) {
    return new Observable((observer) => {
      let i = 0;
      const id = setInterval(() => observer.next(i++), ms);
      return () => clearInterval(id);
    });
  }
}

// Usage (mirrors RxJS patterns):
const clicks$ = Observable.fromEvent(document, 'click')
  .map(e => ({ x: e.clientX, y: e.clientY }))
  .filter(pos => pos.x > 100);

const sub = clicks$.subscribe({
  next: pos => console.log('Click at', pos),
  complete: () => console.log('Done'),
});

// After 10 seconds, unsubscribe
setTimeout(() => sub.unsubscribe(), 10000);

// Interval with take:
Observable.interval(1000)
  .map(n => n * 2)
  .take(5)
  .subscribe({
    next: v => console.log(v),     // 0, 2, 4, 6, 8
    complete: () => console.log('Done!'),
  });</pre>

<div class="interview-q">
<p><strong>💡 Interview Tip — Event Emitter &amp; Observer:</strong></p>
<ul>
  <li><strong>Q: EventEmitter vs Observable?</strong> EventEmitter is push-based, imperative. Observable is lazy — nothing happens until subscribe(). Observable supports operators (map, filter) natively.</li>
  <li><strong>Q: Memory leak risk?</strong> Forgetting to call off()/unsubscribe(). Always clean up in component destroy.</li>
  <li><strong>Q: Why copy listeners array before emit?</strong> A listener might call off() during emit, modifying the array mid-iteration.</li>
</ul>
</div>


<h2 id="cc-this-proto" class="section-break">137. Coding Challenges — this Binding &amp; Prototypes</h2>
<p class="small"><strong>Concept Focus:</strong> call/apply/bind · prototype chain · inheritance without class · method borrowing · new keyword · Object.create patterns</p>

<h3>137.1 Basic — Implement Function.prototype.myBind</h3>
<pre>// myBind — returns a new function with 'this' bound + partial args
Function.prototype.myBind = function(context, ...boundArgs) {
  const fn = this;
  
  return function boundFunction(...callArgs) {
    // Handle 'new' — don't bind context when called as constructor
    if (new.target) {
      return new fn(...boundArgs, ...callArgs);
    }
    return fn.apply(context, [...boundArgs, ...callArgs]);
  };
};

function greet(greeting, punct) {
  return `${greeting}, ${this.name}${punct}`;
}

const bob = { name: 'Bob' };
const greetBob = greet.myBind(bob, 'Hello');
console.log(greetBob('!'));  // "Hello, Bob!"
console.log(greetBob('.')); // "Hello, Bob."</pre>

<h3>137.2 Basic — Implement Function.prototype.myCall &amp; myApply</h3>
<pre>// myCall — invoke function with specified 'this' and args
Function.prototype.myCall = function(context, ...args) {
  context = context ?? globalThis; // null/undefined → global
  context = Object(context);       // primitives → wrapper object
  
  const sym = Symbol('fn');        // unique key to avoid collision
  context[sym] = this;
  const result = context[sym](...args);
  delete context[sym];
  return result;
};

// myApply — same but takes array of args
Function.prototype.myApply = function(context, args = []) {
  return this.myCall(context, ...args);
};

function introduce(age) {
  return `I'm ${this.name}, age ${age}`;
}

console.log(introduce.myCall({ name: 'Alice' }, 25)); // "I'm Alice, age 25"
console.log(introduce.myApply({ name: 'Bob' }, [30])); // "I'm Bob, age 30"</pre>

<h3>137.3 Intermediate — Implement new Keyword</h3>
<pre>// myNew(Constructor, ...args) — simulates the 'new' operator
function myNew(Constructor, ...args) {
  // 1. Create new object with Constructor's prototype
  const obj = Object.create(Constructor.prototype);
  
  // 2. Execute constructor with 'this' = new object
  const result = Constructor.apply(obj, args);
  
  // 3. If constructor returns an object, use that; otherwise use our obj
  return result instanceof Object ? result : obj;
}

function Person(name, age) {
  this.name = name;
  this.age = age;
}
Person.prototype.greet = function() {
  return `Hi, I'm ${this.name}`;
};

const p = myNew(Person, 'Alice', 25);
console.log(p.name);    // 'Alice'
console.log(p.greet()); // "Hi, I'm Alice"
console.log(p instanceof Person); // true ✓</pre>

<h3>137.4 Intermediate — Prototypal Inheritance without Class</h3>
<pre>// Classical OOP via prototypes (pre-ES6 style — still asked in interviews!)
function Animal(name) {
  this.name = name;
}
Animal.prototype.speak = function() {
  return `${this.name} makes a sound.`;
};

function Dog(name, breed) {
  Animal.call(this, name);  // Super constructor call
  this.breed = breed;
}

// Set up inheritance chain
Dog.prototype = Object.create(Animal.prototype);
Dog.prototype.constructor = Dog; // Fix constructor reference

Dog.prototype.speak = function() {
  return `${this.name} barks!`;
};

Dog.prototype.fetch = function(item) {
  return `${this.name} fetches the ${item}`;
};

const rex = new Dog('Rex', 'Labrador');
console.log(rex.speak());              // "Rex barks!"
console.log(rex.fetch('ball'));         // "Rex fetches the ball"
console.log(rex instanceof Dog);       // true
console.log(rex instanceof Animal);    // true

// Verify prototype chain:
console.log(Object.getPrototypeOf(rex) === Dog.prototype);           // true
console.log(Object.getPrototypeOf(Dog.prototype) === Animal.prototype); // true</pre>

<h3>137.5 Advanced — Implement instanceof</h3>
<pre>// myInstanceof — check if obj's prototype chain includes Constructor.prototype
function myInstanceof(obj, Constructor) {
  if (obj === null || typeof obj !== 'object') return false;
  
  let proto = Object.getPrototypeOf(obj);
  const target = Constructor.prototype;
  
  while (proto !== null) {
    if (proto === target) return true;
    proto = Object.getPrototypeOf(proto);
  }
  
  return false;
}

console.log(myInstanceof(rex, Dog));    // true
console.log(myInstanceof(rex, Animal)); // true
console.log(myInstanceof(rex, Array));  // false
console.log(myInstanceof([], Array));   // true
console.log(myInstanceof([], Object));  // true</pre>

<h3>137.6 Advanced — Method Chaining Builder with Proxies</h3>
<pre>// Create a chainable query builder using Proxy
function createQueryBuilder() {
  const query = { table: '', conditions: [], columns: '*', orderBy: '', limit: null };
  
  const builder = new Proxy({}, {
    get(target, prop) {
      if (prop === 'build') {
        return () => {
          let sql = `SELECT ${query.columns} FROM ${query.table}`;
          if (query.conditions.length) sql += ` WHERE ${query.conditions.join(' AND ')}`;
          if (query.orderBy) sql += ` ORDER BY ${query.orderBy}`;
          if (query.limit) sql += ` LIMIT ${query.limit}`;
          return sql;
        };
      }
      if (prop === 'select') return (cols) => { query.columns = cols; return builder; };
      if (prop === 'from') return (table) => { query.table = table; return builder; };
      if (prop === 'where') return (cond) => { query.conditions.push(cond); return builder; };
      if (prop === 'order') return (col) => { query.orderBy = col; return builder; };
      if (prop === 'limit') return (n) => { query.limit = n; return builder; };
    }
  });
  
  return builder;
}

const sql = createQueryBuilder()
  .select('name, email')
  .from('users')
  .where('age > 18')
  .where('active = true')
  .order('name ASC')
  .limit(10)
  .build();

console.log(sql);
// SELECT name, email FROM users WHERE age > 18 AND active = true ORDER BY name ASC LIMIT 10</pre>

<div class="interview-q">
<p><strong>💡 Interview Tip — this &amp; Prototypes:</strong></p>
<ul>
  <li><strong>Q: 4 rules for this?</strong> (1) new → new object. (2) call/apply/bind → specified object. (3) obj.method() → obj. (4) standalone → globalThis (or undefined in strict mode).</li>
  <li><strong>Q: Arrow functions and this?</strong> Arrows don't have their own this — they inherit from lexical scope. Cannot be used as constructors.</li>
  <li><strong>Q: Why Object.create(Parent.prototype) instead of new Parent()?</strong> new Parent() runs the constructor, which might have side effects or require args. Object.create just sets up the prototype link.</li>
</ul>
</div>

"""
