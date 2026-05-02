SECTIONS = r"""

<!-- ═══════════════════════════════════════════════════════════════════
     CONCEPT-BASED CODING CHALLENGES — Part 3
     Scope & Hoisting · Event Loop · Generators & Iterators · String & Regex · Data Structures · Design Patterns · DOM Challenges
     ═══════════════════════════════════════════════════════════════════ -->

<h2 id="cc-scope-hoisting" class="section-break">138. Coding Challenges — Scope, Hoisting &amp; Execution Context</h2>
<p class="small"><strong>Concept Focus:</strong> var/let/const scoping · TDZ · IIFE patterns · block scoping · function vs block scope · module scope</p>

<h3>138.1 — IIFE Data Privacy Module</h3>
<pre>// Create a module with private state using IIFE
const UserModule = (function() {
  // Private
  let users = [];
  let nextId = 1;
  
  // Private helper
  function validate(user) {
    if (!user.name || typeof user.name !== 'string') {
      throw new Error('Invalid name');
    }
    if (!user.email || !user.email.includes('@')) {
      throw new Error('Invalid email');
    }
  }
  
  // Public API
  return {
    addUser(name, email) {
      const user = { id: nextId++, name, email };
      validate(user);
      users.push(user);
      return { ...user }; // return copy, not reference
    },
    getUser(id) {
      const user = users.find(u => u.id === id);
      return user ? { ...user } : null;
    },
    getAllUsers() {
      return users.map(u => ({ ...u })); // return copies
    },
    removeUser(id) {
      const idx = users.findIndex(u => u.id === id);
      if (idx !== -1) return users.splice(idx, 1)[0];
      return null;
    },
    get count() { return users.length; }
  };
})();

UserModule.addUser('Alice', 'alice@test.com');
UserModule.addUser('Bob', 'bob@test.com');
console.log(UserModule.count);         // 2
console.log(UserModule.getAllUsers());  // [{id:1,...}, {id:2,...}]
console.log(typeof users);            // 'undefined' — truly private</pre>

<h3>138.2 — Block Scoping Puzzles</h3>
<pre>// Puzzle 1: What's logged?
{
  var a = 1;     // function-scoped → leaks out of block
  let b = 2;     // block-scoped → stays inside
  const c = 3;   // block-scoped → stays inside
}
console.log(a);  // 1
// console.log(b); // ReferenceError
// console.log(c); // ReferenceError

// Puzzle 2: switch-case scoping trap
function processCommand(cmd) {
  switch(cmd) {
    case 'start':
      let result = 'started';  // This let is scoped to the switch BLOCK
      break;
    case 'stop':
      // let result = 'stopped';  // SyntaxError! 'result' already declared in same block
      // Fix: wrap each case in its own block
      break;
  }
}

// Fixed version:
function processCommandFixed(cmd) {
  switch(cmd) {
    case 'start': {
      let result = 'started';  // scoped to this { } block
      console.log(result);
      break;
    }
    case 'stop': {
      let result = 'stopped';  // different scope — no conflict
      console.log(result);
      break;
    }
  }
}

// Puzzle 3: for-loop var vs let with setTimeout (classic!)
for (var i = 0; i < 3; i++) {
  setTimeout(() => console.log('var:', i), 0);
}
// var: 3, var: 3, var: 3

for (let i = 0; i < 3; i++) {
  setTimeout(() => console.log('let:', i), 0);
}
// let: 0, let: 1, let: 2</pre>

<h3>138.3 — Temporal Dead Zone Challenges</h3>
<pre>// TDZ: let/const exist from block start but can't be accessed before declaration

// Challenge 1: typeof in TDZ
console.log(typeof undeclaredVar);  // 'undefined' — no error for undeclared
// console.log(typeof tdzVar);      // ReferenceError! — different from undeclared
// let tdzVar = 10;

// Challenge 2: Default param TDZ
// function bad(a = b, b = 1) {} // ReferenceError! 'b' not yet initialized when 'a' evaluates
function good(a = 1, b = a) { return [a, b]; } // OK — a is already initialized
console.log(good());  // [1, 1]

// Challenge 3: Class TDZ
const instance = new MyClass(); // ReferenceError — class declarations have TDZ too!
class MyClass { }

// But function declarations DON'T have TDZ (they're fully hoisted):
const result = hoistedFn(); // Works fine!
function hoistedFn() { return 'I am hoisted'; }</pre>


<h2 id="cc-event-loop" class="section-break">139. Coding Challenges — Event Loop &amp; Async Execution Order</h2>
<p class="small"><strong>Concept Focus:</strong> Microtasks vs macrotasks · Promise resolution timing · queueMicrotask · MutationObserver · requestAnimationFrame order · async/await desugaring</p>

<h3>139.1 — Predict the Output (Classic Event Loop)</h3>
<pre>// Challenge 1: What's the order?
console.log('1');

setTimeout(() => console.log('2'), 0);

Promise.resolve().then(() => console.log('3'));

console.log('4');

// Answer: 1, 4, 3, 2
// Explanation:
// - '1' → sync, runs immediately
// - setTimeout → schedules macrotask (task queue)
// - Promise.then → schedules microtask (microtask queue)
// - '4' → sync, runs immediately
// - Call stack empty → drain microtask queue → '3'
// - Then process next macrotask → '2'</pre>

<h3>139.2 — Complex Event Loop (nested microtasks &amp; macrotasks)</h3>
<pre>// Challenge 2: What's the order?
console.log('start');

setTimeout(() => {
  console.log('timeout 1');
  Promise.resolve().then(() => console.log('promise inside timeout'));
}, 0);

Promise.resolve().then(() => {
  console.log('promise 1');
  setTimeout(() => console.log('timeout inside promise'), 0);
});

Promise.resolve().then(() => console.log('promise 2'));

console.log('end');

// Answer: start, end, promise 1, promise 2, timeout 1, promise inside timeout, timeout inside promise
// Step-by-step:
// 1. "start" — sync
// 2. setTimeout cb → macrotask queue
// 3. Promise.then cb → microtask queue
// 4. Promise.then cb → microtask queue
// 5. "end" — sync
// 6. Drain microtasks: "promise 1" (schedules new macrotask), then "promise 2"
// 7. Next macrotask: "timeout 1" (schedules microtask)
// 8. Drain microtasks: "promise inside timeout"
// 9. Next macrotask: "timeout inside promise"</pre>

<h3>139.3 — async/await Execution Order</h3>
<pre>// Challenge 3: async/await is syntactic sugar over Promises
async function foo() {
  console.log('foo start');
  await bar();           // everything after await goes into microtask
  console.log('foo end'); // this is like .then(() => console.log('foo end'))
}

async function bar() {
  console.log('bar');
}

console.log('script start');
foo();
console.log('script end');

// Answer: script start, foo start, bar, script end, foo end
// Why? 'await bar()' resolves synchronously (bar returns resolved promise),
// but the code AFTER await is still scheduled as a microtask.</pre>

<h3>139.4 — Build Your Own Task Scheduler</h3>
<pre>// Scheduler that respects micro/macro task ordering
class TaskScheduler {
  #microTasks = [];
  #macroTasks = [];
  
  addMicrotask(fn) {
    this.#microTasks.push(fn);
    // queueMicrotask runs BEFORE next macrotask
    queueMicrotask(() => this.#processMicrotasks());
  }
  
  addMacrotask(fn, delay = 0) {
    this.#macroTasks.push(fn);
    setTimeout(() => {
      const task = this.#macroTasks.shift();
      if (task) task();
    }, delay);
  }
  
  #processMicrotasks() {
    while (this.#microTasks.length) {
      const task = this.#microTasks.shift();
      task();
    }
  }
  
  // Implement setImmediate-like behavior (next tick)
  nextTick(fn) {
    if (typeof MessageChannel !== 'undefined') {
      const channel = new MessageChannel();
      channel.port1.onmessage = fn;
      channel.port2.postMessage(undefined);
    } else {
      setTimeout(fn, 0);
    }
  }
}

// Implement setInterval using setTimeout (common interview question!)
function mySetInterval(fn, delay) {
  let cancelled = false;
  
  function tick() {
    if (!cancelled) {
      fn();
      setTimeout(tick, delay);
    }
  }
  
  setTimeout(tick, delay);
  
  return {
    clear() { cancelled = true; }
  };
}

const interval = mySetInterval(() => console.log('tick'), 1000);
setTimeout(() => interval.clear(), 5500); // stops after 5 ticks</pre>

<h3>139.5 — requestAnimationFrame vs setTimeout vs Microtask Ordering</h3>
<pre>// Challenge: What's the order?
setTimeout(() => console.log('setTimeout'), 0);
requestAnimationFrame(() => console.log('rAF'));
Promise.resolve().then(() => console.log('microtask'));
queueMicrotask(() => console.log('queueMicrotask'));

// Typical answer: microtask, queueMicrotask, rAF, setTimeout
// BUT: rAF timing varies — it runs before the next paint, which is
// usually before setTimeout, but NOT guaranteed to come before setTimeout
// in all browsers. The ONLY guarantee is:
// Microtasks always run before any macrotask/rAF

// Rule of thumb for priority:
// 1. Synchronous code
// 2. Microtasks (Promise.then, queueMicrotask, MutationObserver)
// 3. requestAnimationFrame (before paint)
// 4. Macrotasks (setTimeout, setInterval, I/O, UI events)</pre>

<div class="interview-q">
<p><strong>💡 Interview Tip — Event Loop:</strong></p>
<ul>
  <li><strong>Key rule:</strong> After each task (macrotask), ALL microtasks drain before the next task runs.</li>
  <li><strong>async/await:</strong> Code before first await is SYNCHRONOUS. Code after await becomes a microtask.</li>
  <li><strong>Common gotcha:</strong> Promise constructor callback is synchronous! Only .then/.catch/.finally are async.</li>
  <li><strong>Node.js difference:</strong> process.nextTick runs BEFORE Promise microtasks. setImmediate runs after I/O.</li>
</ul>
</div>


<h2 id="cc-string-regex" class="section-break">140. Coding Challenges — String Manipulation &amp; RegEx</h2>
<p class="small"><strong>Concept Focus:</strong> String parsing · template engines · regex patterns · Unicode handling · common string algorithms</p>

<h3>140.1 Basic — String Compression</h3>
<pre>// "aaabbbccca" → "a3b3c3a1"
function compress(str) {
  if (!str) return '';
  let result = '';
  let count = 1;
  
  for (let i = 1; i <= str.length; i++) {
    if (i < str.length && str[i] === str[i - 1]) {
      count++;
    } else {
      result += str[i - 1] + count;
      count = 1;
    }
  }
  
  return result.length < str.length ? result : str;
}

console.log(compress('aaabbbccca'));  // "a3b3c3a1"
console.log(compress('abcdef'));     // "abcdef" (compression is longer)

// Decompress: "a3b3c3a1" → "aaabbbccca"
function decompress(str) {
  return str.replace(/([a-zA-Z])(\d+)/g, (_, char, count) => 
    char.repeat(parseInt(count))
  );
}
console.log(decompress('a3b3c3a1')); // "aaabbbccca"</pre>

<h3>140.2 Intermediate — Simple Template Engine</h3>
<pre>// "Hello {{name}}, you have {{count}} messages" + data → filled string
function template(str, data) {
  return str.replace(/\{\{(\w+(?:\.\w+)*)\}\}/g, (match, path) => {
    const value = path.split('.').reduce((obj, key) => obj?.[key], data);
    return value !== undefined ? value : match;
  });
}

const result = template('Hello {{user.name}}, you have {{count}} messages', {
  user: { name: 'Alice' },
  count: 5
});
console.log(result); // "Hello Alice, you have 5 messages"

// Advanced version with conditionals and loops
function advancedTemplate(str, data) {
  // Handle {{#if condition}}...{{/if}}
  str = str.replace(/\{\{#if (\w+)\}\}([\s\S]*?)\{\{\/if\}\}/g, 
    (_, key, content) => data[key] ? content : ''
  );
  
  // Handle {{#each items}}...{{/each}}
  str = str.replace(/\{\{#each (\w+)\}\}([\s\S]*?)\{\{\/each\}\}/g, 
    (_, key, content) => {
      return (data[key] || []).map(item =>
        content.replace(/\{\{this(?:\.(\w+))?\}\}/g, (_, prop) =>
          prop ? item[prop] : item
        )
      ).join('');
    }
  );
  
  // Handle simple {{variable}}
  str = str.replace(/\{\{(\w+(?:\.\w+)*)\}\}/g, (match, path) => {
    const value = path.split('.').reduce((obj, key) => obj?.[key], data);
    return value !== undefined ? String(value) : match;
  });
  
  return str;
}</pre>

<h3>140.3 Intermediate — Parse Query String / Build Query String</h3>
<pre>// "?name=Alice&age=25&tags=js&tags=ts" → { name: 'Alice', age: '25', tags: ['js', 'ts'] }
function parseQueryString(qs) {
  const params = {};
  const search = qs.startsWith('?') ? qs.slice(1) : qs;
  if (!search) return params;
  
  for (const pair of search.split('&')) {
    const [rawKey, rawValue = ''] = pair.split('=');
    const key = decodeURIComponent(rawKey);
    const value = decodeURIComponent(rawValue);
    
    if (key in params) {
      params[key] = [].concat(params[key], value);
    } else {
      params[key] = value;
    }
  }
  
  return params;
}

// Reverse: build query string from object
function buildQueryString(params) {
  const parts = [];
  for (const [key, value] of Object.entries(params)) {
    const values = [].concat(value);
    for (const v of values) {
      parts.push(`${encodeURIComponent(key)}=${encodeURIComponent(v)}`);
    }
  }
  return parts.length ? `?${parts.join('&')}` : '';
}

console.log(parseQueryString('?name=Alice&tags=js&tags=ts'));
// { name: 'Alice', tags: ['js', 'ts'] }

console.log(buildQueryString({ name: 'Alice', tags: ['js', 'ts'] }));
// "?name=Alice&tags=js&tags=ts"</pre>

<h3>140.4 Advanced — Regex: Validate Complex Patterns</h3>
<pre>// Email validation (simplified but practical)
const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;

// Password: 8+ chars, uppercase, lowercase, digit, special char
const passwordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/;

// URL parsing with named groups
const urlRegex = /^(?&lt;protocol>https?):\/\/(?&lt;host>[^:\/\n]+)(?::(?&lt;port>\d+))?(?&lt;path>\/[^?#]*)?(?:\?(?&lt;query>[^#]*))?(?:#(?&lt;fragment>.*))?$/;

const match = 'https://example.com:8080/api/users?page=1#top'.match(urlRegex);
console.log(match.groups);
// { protocol: 'https', host: 'example.com', port: '8080',
//   path: '/api/users', query: 'page=1', fragment: 'top' }

// Highlight search terms (wrap in &lt;mark>)
function highlightText(text, searchTerm) {
  const escaped = searchTerm.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  const regex = new RegExp(`(${escaped})`, 'gi');
  return text.replace(regex, '&lt;mark>$1&lt;/mark>');
}

console.log(highlightText('JavaScript is great for scripting', 'script'));
// "Java&lt;mark>Script&lt;/mark> is great for &lt;mark>script&lt;/mark>ing"</pre>

<h3>140.5 Advanced — Longest Palindromic Substring</h3>
<pre>// Expand-around-center approach — O(n²)
function longestPalindrome(s) {
  if (s.length < 2) return s;
  let start = 0, maxLen = 1;
  
  function expandAroundCenter(left, right) {
    while (left >= 0 && right < s.length && s[left] === s[right]) {
      const len = right - left + 1;
      if (len > maxLen) {
        start = left;
        maxLen = len;
      }
      left--;
      right++;
    }
  }
  
  for (let i = 0; i < s.length; i++) {
    expandAroundCenter(i, i);     // odd-length palindromes
    expandAroundCenter(i, i + 1); // even-length palindromes
  }
  
  return s.substring(start, start + maxLen);
}

console.log(longestPalindrome('babad'));  // "bab" or "aba"
console.log(longestPalindrome('racecar')); // "racecar"</pre>

<div class="interview-q">
<p><strong>💡 Interview Tip — Strings &amp; RegEx:</strong></p>
<ul>
  <li><strong>Q: Why escape regex special chars?</strong> Characters like . * + ? have special meaning. Use <code>str.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')</code> to escape user input.</li>
  <li><strong>Q: String immutability in JS?</strong> Strings are immutable — every operation creates a new string. For many concatenations, use array + join().</li>
  <li><strong>Q: Named groups in regex?</strong> <code>(?&lt;name>pattern)</code> — accessed via <code>match.groups.name</code>. Much more readable than positional $1, $2.</li>
</ul>
</div>


<h2 id="cc-data-structures" class="section-break">141. Coding Challenges — Data Structures in JavaScript</h2>
<p class="small"><strong>Concept Focus:</strong> Stack · Queue · LinkedList · HashMap · Trie · Heap — all implemented from scratch in JS</p>

<h3>141.1 — Stack (with min/max tracking)</h3>
<pre>class MinMaxStack {
  #stack = [];
  #minStack = [];
  #maxStack = [];
  
  push(val) {
    this.#stack.push(val);
    this.#minStack.push(this.#minStack.length === 0 ? val : Math.min(val, this.min()));
    this.#maxStack.push(this.#maxStack.length === 0 ? val : Math.max(val, this.max()));
  }
  
  pop() {
    this.#minStack.pop();
    this.#maxStack.pop();
    return this.#stack.pop();
  }
  
  peek() { return this.#stack[this.#stack.length - 1]; }
  min()  { return this.#minStack[this.#minStack.length - 1]; }
  max()  { return this.#maxStack[this.#maxStack.length - 1]; }
  get size() { return this.#stack.length; }
  get isEmpty()  { return this.#stack.length === 0; }
}

const stack = new MinMaxStack();
stack.push(5); stack.push(2); stack.push(8); stack.push(1);
console.log(stack.min());  // 1
console.log(stack.max());  // 8
stack.pop();               // removes 1
console.log(stack.min());  // 2 — still O(1)!</pre>

<h3>141.2 — Queue (with two stacks)</h3>
<pre>// Implement Queue using two Stacks — amortized O(1) operations
class QueueWithStacks {
  #inStack = [];
  #outStack = [];
  
  enqueue(val) {
    this.#inStack.push(val);
  }
  
  dequeue() {
    if (this.#outStack.length === 0) {
      // Transfer all from inStack to outStack (reverses order)
      while (this.#inStack.length > 0) {
        this.#outStack.push(this.#inStack.pop());
      }
    }
    return this.#outStack.pop();
  }
  
  peek() {
    if (this.#outStack.length === 0) {
      while (this.#inStack.length > 0) {
        this.#outStack.push(this.#inStack.pop());
      }
    }
    return this.#outStack[this.#outStack.length - 1];
  }
  
  get size() { return this.#inStack.length + this.#outStack.length; }
  get isEmpty() { return this.size === 0; }
}

const q = new QueueWithStacks();
q.enqueue(1); q.enqueue(2); q.enqueue(3);
console.log(q.dequeue()); // 1 (FIFO)
console.log(q.dequeue()); // 2
q.enqueue(4);
console.log(q.dequeue()); // 3</pre>

<h3>141.3 — Linked List (with reverse)</h3>
<pre>class ListNode {
  constructor(val, next = null) {
    this.val = val;
    this.next = next;
  }
}

class LinkedList {
  #head = null;
  #size = 0;
  
  // Add to end
  append(val) {
    const node = new ListNode(val);
    if (!this.#head) { this.#head = node; }
    else {
      let current = this.#head;
      while (current.next) current = current.next;
      current.next = node;
    }
    this.#size++;
  }
  
  // Remove by value
  remove(val) {
    if (!this.#head) return false;
    if (this.#head.val === val) { this.#head = this.#head.next; this.#size--; return true; }
    
    let current = this.#head;
    while (current.next) {
      if (current.next.val === val) {
        current.next = current.next.next;
        this.#size--;
        return true;
      }
      current = current.next;
    }
    return false;
  }
  
  // Reverse in-place — O(n) time, O(1) space
  reverse() {
    let prev = null, current = this.#head;
    while (current) {
      const next = current.next;
      current.next = prev;
      prev = current;
      current = next;
    }
    this.#head = prev;
  }
  
  // Detect cycle (Floyd's Tortoise and Hare)
  hasCycle() {
    let slow = this.#head, fast = this.#head;
    while (fast && fast.next) {
      slow = slow.next;
      fast = fast.next.next;
      if (slow === fast) return true;
    }
    return false;
  }
  
  // Find middle node
  findMiddle() {
    let slow = this.#head, fast = this.#head;
    while (fast && fast.next) {
      slow = slow.next;
      fast = fast.next.next;
    }
    return slow?.val;
  }
  
  toArray() {
    const arr = [];
    let current = this.#head;
    while (current) { arr.push(current.val); current = current.next; }
    return arr;
  }
  
  get size() { return this.#size; }
}

const ll = new LinkedList();
ll.append(1); ll.append(2); ll.append(3); ll.append(4);
console.log(ll.findMiddle()); // 3
ll.reverse();
console.log(ll.toArray());   // [4, 3, 2, 1]</pre>

<h3>141.4 — Trie (Prefix Tree)</h3>
<pre>class TrieNode {
  constructor() {
    this.children = new Map();
    this.isEnd = false;
  }
}

class Trie {
  #root = new TrieNode();
  
  insert(word) {
    let node = this.#root;
    for (const char of word) {
      if (!node.children.has(char)) {
        node.children.set(char, new TrieNode());
      }
      node = node.children.get(char);
    }
    node.isEnd = true;
  }
  
  search(word) {
    const node = this.#traverse(word);
    return node !== null && node.isEnd;
  }
  
  startsWith(prefix) {
    return this.#traverse(prefix) !== null;
  }
  
  // Autocomplete: return all words with given prefix
  autocomplete(prefix, limit = 10) {
    const node = this.#traverse(prefix);
    if (!node) return [];
    
    const results = [];
    const dfs = (current, path) => {
      if (results.length >= limit) return;
      if (current.isEnd) results.push(prefix + path);
      for (const [char, child] of current.children) {
        dfs(child, path + char);
      }
    };
    dfs(node, '');
    return results;
  }
  
  #traverse(str) {
    let node = this.#root;
    for (const char of str) {
      if (!node.children.has(char)) return null;
      node = node.children.get(char);
    }
    return node;
  }
}

const trie = new Trie();
['apple', 'app', 'application', 'apply', 'banana', 'band'].forEach(w => trie.insert(w));
console.log(trie.search('app'));           // true
console.log(trie.search('ap'));            // false
console.log(trie.startsWith('ap'));        // true
console.log(trie.autocomplete('app'));     // ['app', 'apple', 'application', 'apply']</pre>

<h3>141.5 — Min Heap (Priority Queue)</h3>
<pre>class MinHeap {
  #heap = [];
  
  insert(val) {
    this.#heap.push(val);
    this.#bubbleUp(this.#heap.length - 1);
  }
  
  extractMin() {
    if (this.#heap.length === 0) return null;
    const min = this.#heap[0];
    const last = this.#heap.pop();
    if (this.#heap.length > 0) {
      this.#heap[0] = last;
      this.#sinkDown(0);
    }
    return min;
  }
  
  peek() { return this.#heap[0] ?? null; }
  get size() { return this.#heap.length; }
  
  #bubbleUp(idx) {
    while (idx > 0) {
      const parent = Math.floor((idx - 1) / 2);
      if (this.#heap[parent] <= this.#heap[idx]) break;
      [this.#heap[parent], this.#heap[idx]] = [this.#heap[idx], this.#heap[parent]];
      idx = parent;
    }
  }
  
  #sinkDown(idx) {
    const length = this.#heap.length;
    while (true) {
      let smallest = idx;
      const left = 2 * idx + 1, right = 2 * idx + 2;
      if (left < length && this.#heap[left] < this.#heap[smallest]) smallest = left;
      if (right < length && this.#heap[right] < this.#heap[smallest]) smallest = right;
      if (smallest === idx) break;
      [this.#heap[smallest], this.#heap[idx]] = [this.#heap[idx], this.#heap[smallest]];
      idx = smallest;
    }
  }
}

// Usage: find K largest elements
function kLargest(arr, k) {
  const heap = new MinHeap();
  for (const num of arr) {
    heap.insert(num);
    if (heap.size > k) heap.extractMin();
  }
  const result = [];
  while (heap.size) result.push(heap.extractMin());
  return result;
}

console.log(kLargest([3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5], 3));
// [5, 6, 9] — top 3 largest</pre>

<div class="interview-q">
<p><strong>💡 Interview Tip — Data Structures:</strong></p>
<ul>
  <li><strong>Q: When to use a Trie?</strong> Autocomplete, spell check, IP routing, dictionary problems. O(L) lookup where L = word length.</li>
  <li><strong>Q: Queue vs Stack use cases?</strong> Queue = BFS, task scheduling, print queue. Stack = DFS, undo/redo, expression parsing, call stack.</li>
  <li><strong>Q: Why implement Queue with 2 stacks?</strong> Shows understanding of amortized analysis. Each element is moved at most twice → O(1) amortized per operation.</li>
</ul>
</div>


<h2 id="cc-design-patterns" class="section-break">142. Coding Challenges — Design Patterns in Action</h2>
<p class="small"><strong>Concept Focus:</strong> Singleton · Factory · Strategy · Observer · Decorator · Middleware pattern · Dependency injection</p>

<h3>142.1 — Singleton (multiple approaches)</h3>
<pre>// Approach 1: Closure-based
const Database = (() => {
  let instance;
  
  function createInstance(config) {
    return {
      config,
      query(sql) { return `Executing: ${sql}`; },
      connect() { console.log(`Connected to ${config.host}`); }
    };
  }
  
  return {
    getInstance(config) {
      if (!instance) instance = createInstance(config);
      return instance;
    }
  };
})();

const db1 = Database.getInstance({ host: 'localhost' });
const db2 = Database.getInstance({ host: 'remote' }); // ignored
console.log(db1 === db2); // true

// Approach 2: ES Module (modules are cached by default!)
// db.js
// const connection = createConnection(config);
// export default connection;
// Every import gets the SAME instance — natural singleton</pre>

<h3>142.2 — Strategy Pattern (payment processing)</h3>
<pre>// Different payment strategies, swappable at runtime
const paymentStrategies = {
  creditCard: {
    validate: (details) => details.number?.length === 16,
    process: (amount, details) => ({
      status: 'success',
      method: 'Credit Card',
      last4: details.number.slice(-4),
      amount
    })
  },
  
  upi: {
    validate: (details) => details.upiId?.includes('@'),
    process: (amount, details) => ({
      status: 'success',
      method: 'UPI',
      upiId: details.upiId,
      amount
    })
  },
  
  wallet: {
    validate: (details) => details.balance >= 0,
    process: (amount, details) => {
      if (details.balance < amount) {
        return { status: 'failed', reason: 'Insufficient balance' };
      }
      return { status: 'success', method: 'Wallet', amount };
    }
  }
};

class PaymentProcessor {
  constructor(strategy) {
    this.strategy = paymentStrategies[strategy];
    if (!this.strategy) throw new Error(`Unknown strategy: ${strategy}`);
  }
  
  setStrategy(name) {
    this.strategy = paymentStrategies[name];
  }
  
  pay(amount, details) {
    if (!this.strategy.validate(details)) {
      throw new Error('Invalid payment details');
    }
    return this.strategy.process(amount, details);
  }
}

const processor = new PaymentProcessor('creditCard');
console.log(processor.pay(1000, { number: '4111111111111111' }));
// { status: 'success', method: 'Credit Card', last4: '1111', amount: 1000 }

processor.setStrategy('upi');
console.log(processor.pay(500, { upiId: 'user@paytm' }));
// { status: 'success', method: 'UPI', upiId: 'user@paytm', amount: 500 }</pre>

<h3>142.3 — Middleware Pattern (like Express.js)</h3>
<pre>// Build a middleware pipeline from scratch
class MiddlewarePipeline {
  #middlewares = [];
  
  use(fn) {
    this.#middlewares.push(fn);
    return this;
  }
  
  execute(context) {
    let index = 0;
    
    const next = () => {
      if (index < this.#middlewares.length) {
        const middleware = this.#middlewares[index++];
        middleware(context, next);
      }
    };
    
    next();
    return context;
  }
}

// Usage: HTTP request pipeline
const pipeline = new MiddlewarePipeline();

// Logger
pipeline.use((ctx, next) => {
  console.log(`${ctx.method} ${ctx.url}`);
  ctx.startTime = Date.now();
  next();
  console.log(`Completed in ${Date.now() - ctx.startTime}ms`);
});

// Auth check
pipeline.use((ctx, next) => {
  if (!ctx.headers?.authorization) {
    ctx.status = 401;
    ctx.body = 'Unauthorized';
    return; // don't call next — stops pipeline
  }
  ctx.user = { id: 1, name: 'Alice' };
  next();
});

// Route handler
pipeline.use((ctx, next) => {
  ctx.status = 200;
  ctx.body = `Hello, ${ctx.user.name}!`;
  next();
});

const result = pipeline.execute({
  method: 'GET',
  url: '/api/profile',
  headers: { authorization: 'Bearer xxx' }
});
console.log(result.body); // "Hello, Alice!"</pre>

<h3>142.4 — Decorator Pattern (function enhancement)</h3>
<pre>// Decorators wrap functions to add behavior without modifying them

// Logging decorator
function withLogging(fn, label = fn.name) {
  return function(...args) {
    console.log(`[${label}] called with:`, args);
    const result = fn.apply(this, args);
    console.log(`[${label}] returned:`, result);
    return result;
  };
}

// Timing decorator
function withTiming(fn) {
  return function(...args) {
    const start = performance.now();
    const result = fn.apply(this, args);
    console.log(`${fn.name} took ${(performance.now() - start).toFixed(2)}ms`);
    return result;
  };
}

// Retry decorator
function withRetry(fn, maxRetries = 3) {
  return async function(...args) {
    for (let attempt = 1; attempt <= maxRetries; attempt++) {
      try {
        return await fn.apply(this, args);
      } catch (err) {
        if (attempt === maxRetries) throw err;
        console.log(`Attempt ${attempt} failed, retrying...`);
      }
    }
  };
}

// Compose decorators
const fetchUser = withLogging(withTiming(withRetry(async (id) => {
  const res = await fetch(`/api/users/${id}`);
  if (!res.ok) throw new Error('Failed');
  return res.json();
})), 'fetchUser');</pre>

<div class="interview-q">
<p><strong>💡 Interview Tip — Design Patterns:</strong></p>
<ul>
  <li><strong>Q: Singleton in JS?</strong> ES Modules are natural singletons (cached). Explicit singleton only when you need lazy initialization or config-dependent creation.</li>
  <li><strong>Q: Strategy vs Factory?</strong> Strategy = choose ALGORITHM at runtime. Factory = choose which OBJECT to create. Strategy composes behavior; Factory composes structure.</li>
  <li><strong>Q: Middleware pattern benefits?</strong> Separation of concerns, composable, order-dependent pipeline. Used in Express, Redux, Angular interceptors.</li>
</ul>
</div>


<h2 id="cc-dom-challenges" class="section-break">143. Coding Challenges — DOM &amp; Browser APIs</h2>
<p class="small"><strong>Concept Focus:</strong> Virtual DOM diff · event delegation · infinite scroll · drag &amp; drop · intersection observer · web workers</p>

<h3>143.1 — Event Delegation System</h3>
<pre>// Handle clicks on dynamic elements efficiently
class EventDelegator {
  #handlers = new Map();
  
  constructor(root) {
    this.root = root;
    this.root.addEventListener('click', this.#handleClick.bind(this));
  }
  
  on(selector, callback) {
    if (!this.#handlers.has(selector)) {
      this.#handlers.set(selector, []);
    }
    this.#handlers.get(selector).push(callback);
    return this;
  }
  
  off(selector, callback) {
    const handlers = this.#handlers.get(selector);
    if (handlers) {
      this.#handlers.set(selector, handlers.filter(h => h !== callback));
    }
    return this;
  }
  
  #handleClick(event) {
    for (const [selector, handlers] of this.#handlers) {
      const target = event.target.closest(selector);
      if (target && this.root.contains(target)) {
        handlers.forEach(h => h(event, target));
      }
    }
  }
}

// Usage: handle clicks on dynamic list items
const delegator = new EventDelegator(document.getElementById('app'));
delegator
  .on('.btn-delete', (e, el) => {
    el.closest('.item')?.remove();
  })
  .on('.btn-edit', (e, el) => {
    const item = el.closest('.item');
    console.log('Edit:', item.dataset.id);
  });</pre>

<h3>143.2 — Simple Virtual DOM Diff &amp; Patch</h3>
<pre>// Minimal vDOM: create, diff, and patch
// vNode = { tag, props, children }

function createElement(tag, props = {}, ...children) {
  return { tag, props, children: children.flat() };
}

function render(vNode) {
  if (typeof vNode === 'string') return document.createTextNode(vNode);
  
  const el = document.createElement(vNode.tag);
  
  for (const [key, value] of Object.entries(vNode.props || {})) {
    if (key.startsWith('on')) {
      el.addEventListener(key.slice(2).toLowerCase(), value);
    } else {
      el.setAttribute(key, value);
    }
  }
  
  vNode.children.forEach(child => el.appendChild(render(child)));
  return el;
}

function diff(oldVNode, newVNode) {
  // Node removed
  if (!newVNode) return (node) => { node.remove(); };
  
  // Text node changed
  if (typeof oldVNode === 'string' || typeof newVNode === 'string') {
    if (oldVNode !== newVNode) {
      return (node) => node.replaceWith(render(newVNode));
    }
    return () => {};
  }
  
  // Tag changed — replace entire node
  if (oldVNode.tag !== newVNode.tag) {
    return (node) => node.replaceWith(render(newVNode));
  }
  
  // Same tag — diff props and children
  return (node) => {
    // Update props
    const allProps = new Set([
      ...Object.keys(oldVNode.props || {}),
      ...Object.keys(newVNode.props || {})
    ]);
    for (const key of allProps) {
      if (key.startsWith('on')) continue;
      if (!(key in (newVNode.props || {}))) {
        node.removeAttribute(key);
      } else if ((oldVNode.props || {})[key] !== (newVNode.props || {})[key]) {
        node.setAttribute(key, newVNode.props[key]);
      }
    }
    
    // Diff children
    const maxLen = Math.max(oldVNode.children.length, newVNode.children.length);
    for (let i = 0; i < maxLen; i++) {
      if (i >= oldVNode.children.length) {
        node.appendChild(render(newVNode.children[i]));
      } else if (i >= newVNode.children.length) {
        node.lastChild.remove();
      } else {
        diff(oldVNode.children[i], newVNode.children[i])(node.childNodes[i]);
      }
    }
  };
}

// Usage:
const vApp1 = createElement('div', { class: 'app' },
  createElement('h1', {}, 'Hello'),
  createElement('p', {}, 'World')
);

const vApp2 = createElement('div', { class: 'app updated' },
  createElement('h1', {}, 'Hello!'),
  createElement('p', {}, 'World'),
  createElement('button', {}, 'Click me')
);

const rootEl = render(vApp1);
document.body.appendChild(rootEl);
diff(vApp1, vApp2)(rootEl); // patches in-place!</pre>

<h3>143.3 — Infinite Scroll with Intersection Observer</h3>
<pre>// Efficient infinite scroll — no scroll event listeners needed
class InfiniteScroll {
  #page = 1;
  #loading = false;
  #hasMore = true;
  #observer;
  
  constructor(container, loadMore) {
    this.container = container;
    this.loadMore = loadMore;
    
    // Sentinel element at bottom
    this.sentinel = document.createElement('div');
    this.sentinel.className = 'scroll-sentinel';
    this.container.appendChild(this.sentinel);
    
    this.#observer = new IntersectionObserver(
      (entries) => {
        if (entries[0].isIntersecting && !this.#loading && this.#hasMore) {
          this.#fetchNext();
        }
      },
      { rootMargin: '200px' } // trigger 200px before visible
    );
    
    this.#observer.observe(this.sentinel);
  }
  
  async #fetchNext() {
    this.#loading = true;
    this.#showLoader();
    
    try {
      const items = await this.loadMore(this.#page);
      
      if (items.length === 0) {
        this.#hasMore = false;
        this.#observer.disconnect();
        this.sentinel.textContent = 'No more items';
        return;
      }
      
      // Insert items BEFORE sentinel
      items.forEach(item => {
        this.container.insertBefore(item, this.sentinel);
      });
      
      this.#page++;
    } finally {
      this.#loading = false;
      this.#hideLoader();
    }
  }
  
  #showLoader() { this.sentinel.textContent = 'Loading...'; }
  #hideLoader() { this.sentinel.textContent = ''; }
  
  destroy() {
    this.#observer.disconnect();
    this.sentinel.remove();
  }
}

// Usage:
const scroller = new InfiniteScroll(
  document.getElementById('feed'),
  async (page) => {
    const res = await fetch(`/api/posts?page=${page}`);
    const posts = await res.json();
    return posts.map(post => {
      const div = document.createElement('div');
      div.className = 'post';
      div.textContent = post.title;
      return div;
    });
  }
);</pre>

<div class="interview-q">
<p><strong>💡 Interview Tip — DOM Challenges:</strong></p>
<ul>
  <li><strong>Q: Why event delegation?</strong> Single listener handles all current AND future child elements. O(1) listeners instead of O(n). Crucial for dynamic lists.</li>
  <li><strong>Q: Virtual DOM purpose?</strong> Batch DOM mutations, minimize reflows/repaints. Diff algorithm determines minimal required changes.</li>
  <li><strong>Q: IntersectionObserver vs scroll event?</strong> IO is non-blocking (runs off main thread), no need for debounce/throttle, battery-efficient. Scroll events are synchronous and need throttling.</li>
</ul>
</div>

"""
