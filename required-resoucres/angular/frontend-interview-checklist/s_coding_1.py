SECTIONS = r"""

<!-- ═══════════════════════════════════════════════════════════════════
     CONCEPT-BASED CODING CHALLENGES — Part 1
     Closures & Currying · Debounce & Throttle · Promises & Async
     ═══════════════════════════════════════════════════════════════════ -->

<h2 id="cc-closures-currying" class="section-break">131. Coding Challenges — Closures &amp; Currying</h2>
<p class="small"><strong>Concept Focus:</strong> Lexical scope · closure over variables · partial application · infinite currying · function composition via closures</p>

<h3>131.1 Basic — Counter with Private State</h3>
<pre>// Create a counter using closures (no class, no global variable)
function createCounter(initial = 0) {
  let count = initial;
  return {
    increment()  { return ++count; },
    decrement()  { return --count; },
    getCount()   { return count; },
    reset()      { count = initial; return count; }
  };
}

const counter = createCounter(10);
console.log(counter.increment()); // 11
console.log(counter.increment()); // 12
console.log(counter.decrement()); // 11
console.log(counter.reset());     // 10
console.log(counter.count);       // undefined — truly private!</pre>

<h3>131.2 Basic — once() Function (run only first time)</h3>
<pre>// Create once() — the function only executes the first time
function once(fn) {
  let called = false;
  let result;
  return function(...args) {
    if (!called) {
      called = true;
      result = fn.apply(this, args);
    }
    return result;
  };
}

const initialize = once(() => {
  console.log('DB connected');
  return { status: 'connected' };
});

initialize(); // logs "DB connected", returns {status:'connected'}
initialize(); // no log, returns same {status:'connected'}
initialize(); // no log, returns same {status:'connected'}</pre>

<h3>131.3 Intermediate — Simple Curry (fixed arity)</h3>
<pre>// Implement curry() that transforms f(a,b,c) → f(a)(b)(c)
function curry(fn) {
  return function curried(...args) {
    if (args.length >= fn.length) {
      return fn.apply(this, args);
    }
    return function(...nextArgs) {
      return curried.apply(this, [...args, ...nextArgs]);
    };
  };
}

// Usage:
const add = (a, b, c) => a + b + c;
const curriedAdd = curry(add);

console.log(curriedAdd(1)(2)(3));    // 6
console.log(curriedAdd(1, 2)(3));    // 6
console.log(curriedAdd(1)(2, 3));    // 6
console.log(curriedAdd(1, 2, 3));    // 6</pre>

<h3>131.4 Intermediate — Infinite Currying (sum(1)(2)(3)...())</h3>
<pre>// sum(1)(2)(3)() → 6 — call with no args to get result
function sum(a) {
  return function(b) {
    if (b === undefined) return a;
    return sum(a + b);
  };
}

console.log(sum(1)(2)(3)());        // 6
console.log(sum(5)(10)(15)(20)());  // 50
console.log(sum(1)());              // 1

// Variant: using toString/valueOf for automatic coercion
function sumAuto(a) {
  function inner(b) {
    return sumAuto(a + b);
  }
  inner.valueOf = () => a;
  inner.toString = () => String(a);
  return inner;
}

console.log(+sumAuto(1)(2)(3));     // 6 — the + triggers valueOf
console.log(`${sumAuto(1)(2)}`);    // "3" — template literal triggers toString</pre>

<h3>131.5 Advanced — Generic Partial Application</h3>
<pre>// partial(fn, ...presetArgs) — like bind without "this"
// Support placeholder _ for skipping arguments
const _ = Symbol('placeholder');

function partial(fn, ...presetArgs) {
  return function(...laterArgs) {
    const args = [];
    let laterIdx = 0;
    
    // Fill in preset args, replacing placeholders
    for (const arg of presetArgs) {
      if (arg === _) {
        args.push(laterArgs[laterIdx++]);
      } else {
        args.push(arg);
      }
    }
    // Append remaining later args
    while (laterIdx < laterArgs.length) {
      args.push(laterArgs[laterIdx++]);
    }
    
    return fn(...args);
  };
}

// Usage:
const divide = (a, b) => a / b;
const halve = partial(divide, _, 2);   // skip first arg, preset second
console.log(halve(10));                // 5

const greet = (greeting, name, punct) => `${greeting}, ${name}${punct}`;
const hello = partial(greet, 'Hello');
console.log(hello('World', '!'));      // "Hello, World!"

const exclaim = partial(greet, _, _, '!');
console.log(exclaim('Hi', 'Dev'));     // "Hi, Dev!"</pre>

<h3>131.6 Advanced — Compose &amp; Pipe with Curried Functions</h3>
<pre>// Compose: right-to-left execution   compose(f, g, h)(x) = f(g(h(x)))
// Pipe:    left-to-right execution    pipe(h, g, f)(x) = f(g(h(x)))

const compose = (...fns) => (x) =>
  fns.reduceRight((acc, fn) => fn(acc), x);

const pipe = (...fns) => (x) =>
  fns.reduce((acc, fn) => fn(acc), x);

// Real-world example: data transformation pipeline
const trim      = (s) => s.trim();
const lower     = (s) => s.toLowerCase();
const split     = (sep) => (s) => s.split(sep);  // curried!
const join      = (sep) => (arr) => arr.join(sep);
const capitalize = (s) => s[0].toUpperCase() + s.slice(1);
const map       = (fn) => (arr) => arr.map(fn);

const slugify = pipe(
  trim,
  lower,
  split(/\s+/),
  join('-')
);
console.log(slugify('  Hello World Example  ')); // "hello-world-example"

const titleCase = pipe(
  trim,
  lower,
  split(/\s+/),
  map(capitalize),
  join(' ')
);
console.log(titleCase('  hello world  ')); // "Hello World"</pre>

<h3>131.7 Advanced — Memoize with Closure (LRU-style)</h3>
<pre>// Memoize that handles multiple arguments, uses Map for O(1) lookup
function memoize(fn, maxSize = 100) {
  const cache = new Map();
  
  function memoized(...args) {
    const key = JSON.stringify(args); // simple key strategy
    
    if (cache.has(key)) {
      // Move to end (most recently used)
      const value = cache.get(key);
      cache.delete(key);
      cache.set(key, value);
      return value;
    }
    
    const result = fn.apply(this, args);
    cache.set(key, result);
    
    // Evict oldest if over capacity
    if (cache.size > maxSize) {
      const firstKey = cache.keys().next().value;
      cache.delete(firstKey);
    }
    
    return result;
  }
  
  memoized.cache = cache;
  memoized.clear = () => cache.clear();
  return memoized;
}

// Usage:
const expensiveFib = memoize(function fib(n) {
  if (n <= 1) return n;
  return expensiveFib(n - 1) + expensiveFib(n - 2);
});

console.log(expensiveFib(50));   // 12586269025 — instant!
console.log(expensiveFib.cache.size); // entries cached</pre>

<div class="interview-q">
<p><strong>💡 Interview Tip — Closures &amp; Currying:</strong></p>
<ul>
  <li><strong>Q: What is a closure?</strong> A function that retains access to its lexical scope even when executed outside that scope.</li>
  <li><strong>Q: Curry vs Partial Application?</strong> Curry transforms f(a,b,c) into f(a)(b)(c). Partial fixes some args upfront: partial(f, 1) → f(1, b, c).</li>
  <li><strong>Q: When is currying useful?</strong> Reusable config (loggers, validators), point-free function composition, event handler factories.</li>
  <li><strong>Q: Name a closure pitfall.</strong> Closing over loop variables (var in for-loop), accidental memory retention of large objects.</li>
</ul>
</div>


<h2 id="cc-debounce-throttle" class="section-break">132. Coding Challenges — Debounce &amp; Throttle</h2>
<p class="small"><strong>Concept Focus:</strong> Timer management · leading/trailing edge · cancel/flush · requestAnimationFrame throttle · real-world patterns</p>

<h3>132.1 Basic — Simple Debounce</h3>
<pre>// debounce(fn, delay) — delays execution until after delay ms of silence
function debounce(fn, delay) {
  let timerId;
  return function(...args) {
    clearTimeout(timerId);
    timerId = setTimeout(() => {
      fn.apply(this, args);
    }, delay);
  };
}

// Usage: search input
const searchInput = document.getElementById('search');
const handleSearch = debounce((e) => {
  console.log('API call:', e.target.value);
}, 300);
searchInput?.addEventListener('input', handleSearch);</pre>

<h3>132.2 Basic — Simple Throttle</h3>
<pre>// throttle(fn, limit) — executes at most once per limit ms
function throttle(fn, limit) {
  let inThrottle = false;
  return function(...args) {
    if (!inThrottle) {
      fn.apply(this, args);
      inThrottle = true;
      setTimeout(() => {
        inThrottle = false;
      }, limit);
    }
  };
}

// Usage: scroll handler
const handleScroll = throttle(() => {
  console.log('Scroll position:', window.scrollY);
}, 200);
window.addEventListener('scroll', handleScroll);</pre>

<h3>132.3 Intermediate — Debounce with Leading &amp; Trailing Options</h3>
<pre>// Full-featured debounce: leading edge, trailing edge, or both
function debounce(fn, delay, { leading = false, trailing = true } = {}) {
  let timerId;
  let lastArgs;
  
  function debounced(...args) {
    lastArgs = args;
    const callNow = leading && !timerId;
    
    clearTimeout(timerId);
    timerId = setTimeout(() => {
      timerId = null;
      if (trailing && lastArgs) {
        fn.apply(this, lastArgs);
        lastArgs = null;
      }
    }, delay);
    
    if (callNow) {
      fn.apply(this, args);
      lastArgs = null; // prevent trailing call for same invocation
    }
  }
  
  debounced.cancel = () => {
    clearTimeout(timerId);
    timerId = null;
    lastArgs = null;
  };
  
  debounced.flush = () => {
    if (timerId && lastArgs) {
      fn.apply(null, lastArgs);
      debounced.cancel();
    }
  };
  
  return debounced;
}

// Leading-only: fires immediately, ignores subsequent calls within delay
const btnHandler = debounce(submitForm, 1000, { leading: true, trailing: false });

// Both: fires immediately AND after delay of silence
const autosave = debounce(saveData, 2000, { leading: true, trailing: true });</pre>

<h3>132.4 Intermediate — Throttle with Trailing Call</h3>
<pre>// Throttle that also fires on the trailing edge (last call isn't lost)
function throttle(fn, limit) {
  let lastTime = 0;
  let timerId;
  
  return function(...args) {
    const now = Date.now();
    const remaining = limit - (now - lastTime);
    
    clearTimeout(timerId);
    
    if (remaining <= 0) {
      // Enough time has passed — execute immediately
      lastTime = now;
      fn.apply(this, args);
    } else {
      // Schedule trailing call
      timerId = setTimeout(() => {
        lastTime = Date.now();
        fn.apply(this, args);
      }, remaining);
    }
  };
}

// This ensures the LAST call always fires, even if it comes during throttle window
const resize = throttle(() => recalcLayout(), 150);
window.addEventListener('resize', resize);</pre>

<h3>132.5 Advanced — requestAnimationFrame Throttle</h3>
<pre>// Best for visual updates — syncs with browser's paint cycle (~16ms / 60fps)
function rafThrottle(fn) {
  let rafId = null;
  let lastArgs = null;
  
  function throttled(...args) {
    lastArgs = args;
    if (rafId === null) {
      rafId = requestAnimationFrame(() => {
        fn.apply(this, lastArgs);
        rafId = null;
        lastArgs = null;
      });
    }
  }
  
  throttled.cancel = () => {
    if (rafId !== null) {
      cancelAnimationFrame(rafId);
      rafId = null;
      lastArgs = null;
    }
  };
  
  return throttled;
}

// Usage: smooth drag or scroll animations
const onMouseMove = rafThrottle((e) => {
  tooltip.style.transform = `translate(${e.clientX}px, ${e.clientY}px)`;
});
document.addEventListener('mousemove', onMouseMove);</pre>

<h3>132.6 Advanced — Debounce with maxWait (Lodash-style)</h3>
<pre>// If continuous calls keep resetting the debounce, maxWait ensures
// the function fires at least once within maxWait ms
function debounce(fn, delay, { maxWait = Infinity, leading = false } = {}) {
  let timerId, maxTimerId;
  let lastArgs, lastThis;
  let lastCallTime;
  
  function invoke() {
    const args = lastArgs;
    const thisArg = lastThis;
    lastArgs = lastThis = undefined;
    clearTimeout(timerId);
    clearTimeout(maxTimerId);
    timerId = maxTimerId = null;
    fn.apply(thisArg, args);
  }
  
  function debounced(...args) {
    lastArgs = args;
    lastThis = this;
    lastCallTime = Date.now();
    
    const callNow = leading && !timerId;
    
    clearTimeout(timerId);
    timerId = setTimeout(invoke, delay);
    
    // Set maxWait timer if not already running
    if (maxWait !== Infinity && !maxTimerId) {
      maxTimerId = setTimeout(invoke, maxWait);
    }
    
    if (callNow) invoke();
  }
  
  debounced.cancel = () => {
    clearTimeout(timerId);
    clearTimeout(maxTimerId);
    timerId = maxTimerId = null;
    lastArgs = lastThis = undefined;
  };
  
  return debounced;
}

// Usage: autocomplete that fires at most every 3s even if user keeps typing
const search = debounce(fetchResults, 300, { maxWait: 3000 });</pre>

<div class="interview-q">
<p><strong>💡 Interview Tip — Debounce vs Throttle:</strong></p>
<ul>
  <li><strong>Debounce:</strong> Wait until user STOPS doing something. Use for: search input, form validation, window resize end.</li>
  <li><strong>Throttle:</strong> Execute at regular intervals WHILE user is doing something. Use for: scroll events, mouse move, game loops.</li>
  <li><strong>maxWait:</strong> Hybrid — debounce with guaranteed max delay. Lodash's _.debounce supports this.</li>
  <li><strong>RAF throttle:</strong> Best for visual/paint updates — automatically aligns to 60fps.</li>
  <li><strong>Common follow-up:</strong> "Implement cancel and flush methods" — shows you understand lifecycle management.</li>
</ul>
</div>


<h2 id="cc-promises-async" class="section-break">133. Coding Challenges — Promises &amp; Async Patterns</h2>
<p class="small"><strong>Concept Focus:</strong> Promise constructor · chaining · error handling · Promise combinators · async iteration · concurrency control · retry patterns</p>

<h3>133.1 Basic — Promisify a Callback Function</h3>
<pre>// Convert callback-style function to Promise-based
function promisify(fn) {
  return function(...args) {
    return new Promise((resolve, reject) => {
      fn(...args, (err, result) => {
        if (err) reject(err);
        else resolve(result);
      });
    });
  };
}

// Usage:
const fs = require('fs');
const readFileAsync = promisify(fs.readFile);
readFileAsync('config.json', 'utf8')
  .then(data => console.log(data))
  .catch(err => console.error(err));</pre>

<h3>133.2 Basic — Sleep / Delay Promise</h3>
<pre>// sleep(ms) — returns a promise that resolves after ms
const sleep = (ms) => new Promise(resolve => setTimeout(resolve, ms));

// Timeout wrapper — race between promise and timer
function withTimeout(promise, ms, message = 'Timeout') {
  const timeout = new Promise((_, reject) =>
    setTimeout(() => reject(new Error(message)), ms)
  );
  return Promise.race([promise, timeout]);
}

// Usage:
async function fetchWithTimeout(url) {
  try {
    const data = await withTimeout(fetch(url), 5000, 'Request timed out');
    return data.json();
  } catch (e) {
    console.error(e.message);
  }
}</pre>

<h3>133.3 Intermediate — Sequential Async Execution</h3>
<pre>// Execute async functions one after another (NOT parallel)
// Method 1: reduce
async function sequential(tasks) {
  return tasks.reduce(async (prevPromise, task) => {
    const results = await prevPromise;
    const result = await task();
    return [...results, result];
  }, Promise.resolve([]));
}

// Method 2: for-of (cleaner)
async function sequential2(tasks) {
  const results = [];
  for (const task of tasks) {
    results.push(await task());
  }
  return results;
}

// Usage:
const apis = [
  () => fetch('/api/users').then(r => r.json()),
  () => fetch('/api/posts').then(r => r.json()),
  () => fetch('/api/comments').then(r => r.json()),
];
const [users, posts, comments] = await sequential(apis);</pre>

<h3>133.4 Intermediate — Retry with Exponential Backoff</h3>
<pre>// Retry a promise-returning function with exponential backoff
async function retry(fn, { retries = 3, delay = 1000, backoff = 2 } = {}) {
  let lastError;
  
  for (let attempt = 0; attempt <= retries; attempt++) {
    try {
      return await fn();
    } catch (err) {
      lastError = err;
      if (attempt < retries) {
        const waitTime = delay * Math.pow(backoff, attempt);
        console.log(`Retry ${attempt + 1}/${retries} in ${waitTime}ms...`);
        await new Promise(r => setTimeout(r, waitTime));
      }
    }
  }
  
  throw lastError;
}

// Usage:
const data = await retry(
  () => fetch('https://flaky-api.com/data').then(r => {
    if (!r.ok) throw new Error(`HTTP ${r.status}`);
    return r.json();
  }),
  { retries: 3, delay: 500, backoff: 2 }
);
// Waits: 500ms → 1000ms → 2000ms before giving up</pre>

<h3>133.5 Advanced — Parallel with Concurrency Limit</h3>
<pre>// Run N promises at a time (like p-limit / Promise pool)
async function parallelLimit(tasks, concurrency) {
  const results = new Array(tasks.length);
  let currentIndex = 0;
  
  async function worker() {
    while (currentIndex < tasks.length) {
      const index = currentIndex++;
      results[index] = await tasks[index]();
    }
  }
  
  // Create N workers
  const workers = Array.from({ length: Math.min(concurrency, tasks.length) }, worker);
  await Promise.all(workers);
  
  return results;
}

// Usage: download 100 images, 5 at a time
const imageURLs = Array.from({ length: 100 }, (_, i) => `https://img.com/${i}.jpg`);
const tasks = imageURLs.map(url => () => fetch(url).then(r => r.blob()));

const images = await parallelLimit(tasks, 5);
// Only 5 fetches run simultaneously!</pre>

<h3>133.6 Advanced — Implement Promise.allSettled</h3>
<pre>// Returns array of {status, value/reason} for ALL promises (never rejects)
function allSettled(promises) {
  return Promise.all(
    promises.map(p =>
      Promise.resolve(p)
        .then(value => ({ status: 'fulfilled', value }))
        .catch(reason => ({ status: 'rejected', reason }))
    )
  );
}

// Usage:
const results = await allSettled([
  fetch('/api/fast'),         // succeeds
  fetch('/api/broken'),       // fails
  Promise.resolve(42),        // succeeds
]);
// [
//   { status: 'fulfilled', value: Response },
//   { status: 'rejected',  reason: Error },
//   { status: 'fulfilled', value: 42 }
// ]</pre>

<h3>133.7 Advanced — Async Queue (process tasks in FIFO order)</h3>
<pre>// Process async tasks one at a time in the order they're added
class AsyncQueue {
  #queue = [];
  #processing = false;
  
  enqueue(asyncFn) {
    return new Promise((resolve, reject) => {
      this.#queue.push({ asyncFn, resolve, reject });
      this.#process();
    });
  }
  
  async #process() {
    if (this.#processing) return;
    this.#processing = true;
    
    while (this.#queue.length > 0) {
      const { asyncFn, resolve, reject } = this.#queue.shift();
      try {
        const result = await asyncFn();
        resolve(result);
      } catch (err) {
        reject(err);
      }
    }
    
    this.#processing = false;
  }
  
  get size() { return this.#queue.length; }
}

// Usage: ensure API calls happen sequentially
const queue = new AsyncQueue();

// These all return promises, but execute one at a time
queue.enqueue(() => saveUser(data));
queue.enqueue(() => sendNotification(userId));
queue.enqueue(() => updateAnalytics('user_created'));</pre>

<h3>133.8 Expert — Cancellable Promise with AbortController</h3>
<pre>// Make any async operation cancellable
function cancellable(asyncFn) {
  const controller = new AbortController();
  
  const promise = new Promise(async (resolve, reject) => {
    controller.signal.addEventListener('abort', () => {
      reject(new DOMException('Cancelled', 'AbortError'));
    });
    
    try {
      const result = await asyncFn(controller.signal);
      if (!controller.signal.aborted) {
        resolve(result);
      }
    } catch (err) {
      if (!controller.signal.aborted) {
        reject(err);
      }
    }
  });
  
  return { promise, cancel: () => controller.abort() };
}

// Usage:
const { promise, cancel } = cancellable(async (signal) => {
  const resp = await fetch('/api/data', { signal });
  return resp.json();
});

// Cancel after 2 seconds if still running
setTimeout(cancel, 2000);

try {
  const data = await promise;
} catch (e) {
  if (e.name === 'AbortError') console.log('Request was cancelled');
}</pre>

<div class="interview-q">
<p><strong>💡 Interview Tip — Promises &amp; Async:</strong></p>
<ul>
  <li><strong>Q: Promise.all vs allSettled vs race vs any?</strong> all = fail-fast on first rejection. allSettled = wait for all, no rejection. race = first to settle wins. any = first to fulfill wins (ignores rejections).</li>
  <li><strong>Q: How to limit concurrency?</strong> Worker pool pattern — create N workers that pull from a shared task queue.</li>
  <li><strong>Q: Retry strategy?</strong> Exponential backoff with jitter (randomized delay) to avoid thundering herd.</li>
  <li><strong>Common mistake:</strong> Forgetting to handle errors in Promise.all causes unhandledrejection.</li>
</ul>
</div>

"""
