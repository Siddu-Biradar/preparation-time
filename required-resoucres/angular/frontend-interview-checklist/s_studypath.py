"""
90-Day FAANG-Level Study Path — 4 Hours/Day — 360 Total Hours
Targeting SDE-2/SDE-3 at Google, Meta, Amazon, Apple, Microsoft, Netflix, etc.
"""

# ── CSS (same classes, no changes needed — already in HEAD) ──

SP_HEADER = r'''
<section id="study-path" class="study-path-section">
  <style>
    .study-path-section{margin:32px 0 40px;padding:0}
    .sp-header{background:linear-gradient(135deg,#059669 0%,#2563eb 50%,#7c3aed 100%);border-radius:16px 16px 0 0;padding:28px 32px;color:#fff;position:relative;overflow:hidden}
    .sp-header::before{content:'';position:absolute;top:-40%;right:-10%;width:300px;height:300px;background:rgba(255,255,255,0.06);border-radius:50%}
    .sp-header h2{margin:0 0 6px;font-size:1.6rem;color:#fff;background:none;-webkit-text-fill-color:#fff;border:none;padding:0}
    .sp-header p{margin:0;opacity:0.9;font-size:0.95rem}
    .sp-overview{display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:12px;padding:20px 32px;background:var(--paper);border-left:1px solid var(--line);border-right:1px solid var(--line)}
    .sp-stat{text-align:center;padding:14px 10px;border-radius:10px;background:var(--bg)}
    .sp-stat .sp-num{font-size:1.8rem;font-weight:800;background:linear-gradient(135deg,#059669,#2563eb);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text}
    .sp-stat .sp-label{font-size:0.78rem;color:var(--muted);margin-top:2px;text-transform:uppercase;letter-spacing:0.5px}
    .sp-phase{background:var(--paper);border-left:1px solid var(--line);border-right:1px solid var(--line);padding:0 32px}
    .sp-phase:last-of-type{border-bottom:1px solid var(--line);border-radius:0 0 16px 16px;padding-bottom:24px}
    .sp-phase-header{display:flex;align-items:center;gap:12px;padding:18px 0 10px;border-bottom:2px solid var(--line);margin-bottom:14px}
    .sp-phase-badge{display:inline-flex;align-items:center;justify-content:center;min-width:38px;height:38px;border-radius:10px;color:#fff;font-weight:800;font-size:0.82rem;flex-shrink:0;padding:0 10px}
    .sp-phase-title{font-size:1.1rem;font-weight:700;color:var(--ink)}
    .sp-phase-subtitle{font-size:0.82rem;color:var(--muted);margin-left:auto;text-align:right}
    .sp-day{display:grid;grid-template-columns:64px 1fr;gap:0 16px;padding:8px 0;border-bottom:1px solid rgba(0,0,0,0.04)}
    .sp-day:last-child{border-bottom:none}
    .sp-day-label{font-weight:700;font-size:0.82rem;color:var(--accent);padding-top:2px}
    .sp-day-content{font-size:0.88rem;line-height:1.6}
    .sp-day-content strong{color:var(--ink)}
    .sp-day-content .sp-time{display:inline-block;background:var(--accent-soft);color:var(--accent-dark);font-size:0.72rem;font-weight:600;padding:1px 7px;border-radius:4px;margin-right:4px}
    .sp-day-content .sp-tag-practice{background:#dbeafe;color:#1d4ed8;font-size:0.7rem;font-weight:600;padding:1px 7px;border-radius:4px;margin-right:4px}
    .sp-day-content .sp-tag-leetcode{background:#fce7f3;color:#be185d;font-size:0.7rem;font-weight:600;padding:1px 7px;border-radius:4px;margin-right:4px}
    .sp-day-content .sp-tag-mock{background:#fef3c7;color:#92400e;font-size:0.7rem;font-weight:600;padding:1px 7px;border-radius:4px;margin-right:4px}
    .sp-day-content .sp-tag-revise{background:#ede9fe;color:#5b21b6;font-size:0.7rem;font-weight:600;padding:1px 7px;border-radius:4px;margin-right:4px}
    .sp-tip{margin:16px 0 0;padding:14px 18px;background:linear-gradient(135deg,#fef3c7,#fffbeb);border-left:4px solid #d97706;border-radius:0 8px 8px 0;font-size:0.88rem;line-height:1.6}
    .sp-tip strong{color:#92400e}
    .sp-rest{text-align:center;padding:6px;font-size:0.85rem;color:var(--muted);font-style:italic}
    .sp-breakdown{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:10px;padding:16px 32px;background:var(--paper);border-left:1px solid var(--line);border-right:1px solid var(--line)}
    .sp-bk-item{padding:12px 14px;border-radius:8px;border:1px solid var(--line);font-size:0.85rem;line-height:1.5}
    .sp-bk-item strong{display:block;margin-bottom:4px;font-size:0.9rem}
    @media(max-width:600px){
      .sp-header,.sp-overview,.sp-phase,.sp-tip,.sp-breakdown{padding-left:16px;padding-right:16px}
      .sp-overview{grid-template-columns:repeat(2,1fr)}
      .sp-day{grid-template-columns:56px 1fr}
      .sp-breakdown{grid-template-columns:1fr}
    }
  </style>

  <div class="sp-header">
    <h2>&#128640; 90-Day FAANG Study Path &#8212; 4 Hours/Day &#8212; SDE-2/3 Level</h2>
    <p>A battle-tested, FAANG-caliber roadmap: 360 hours covering all 143 sections, 120+ LeetCode problems, 8 system design mocks, 10+ machine coding exercises, Angular projects, and behavioral rounds. This is what it takes to crack Google, Meta, Amazon, Apple, Microsoft at Senior level.</p>
  </div>

  <div class="sp-overview">
    <div class="sp-stat"><div class="sp-num">90</div><div class="sp-label">Days</div></div>
    <div class="sp-stat"><div class="sp-num">4h</div><div class="sp-label">Per Day</div></div>
    <div class="sp-stat"><div class="sp-num">360h</div><div class="sp-label">Total Hours</div></div>
    <div class="sp-stat"><div class="sp-num">143</div><div class="sp-label">Sections</div></div>
    <div class="sp-stat"><div class="sp-num">12</div><div class="sp-label">Phases</div></div>
    <div class="sp-stat"><div class="sp-num">120+</div><div class="sp-label">LeetCode</div></div>
  </div>

  <div class="sp-breakdown">
    <div class="sp-bk-item"><strong>&#128218; Theory &amp; Concepts</strong>~90 hours &#8212; Deep reading of all 143 sections. Not skimming &#8212; understanding internals, writing your own explanations, drawing diagrams</div>
    <div class="sp-bk-item"><strong>&#128187; Hands-on Coding</strong>~72 hours &#8212; All coding challenges (#131&#8211;143), polyfills (#122), machine coding (#123), build-from-scratch implementations. Every line typed by hand.</div>
    <div class="sp-bk-item"><strong>&#129504; DSA / LeetCode</strong>~72 hours &#8212; 120+ curated problems: arrays, strings, trees, graphs, DP, backtracking, sliding window, two pointers, monotonic stack, BFS/DFS, Trie, union-find</div>
    <div class="sp-bk-item"><strong>&#127959; System Design</strong>~48 hours &#8212; Frontend HLD + LLD, component APIs, state machines, performance budgets, accessibility audits. 8 full mock designs spoken aloud with timer</div>
    <div class="sp-bk-item"><strong>&#9878; Angular Deep Dive</strong>~32 hours &#8212; All 15 Angular sections + build 3 real projects from scratch (dashboard, e-commerce, realtime chat)</div>
    <div class="sp-bk-item"><strong>&#128483; Behavioral + Mock</strong>~30 hours &#8212; 15 STAR stories, leadership principles (Amazon LP, Google Googliness), 6 full mock interview simulations, speed rounds</div>
    <div class="sp-bk-item"><strong>&#128295; Revision &amp; Weak Areas</strong>~16 hours &#8212; Spaced repetition cycles, targeted drilling on weak topics, flashcard review, error pattern analysis</div>
  </div>
'''

# ═══════════════════════════════════════════════════════════════════
# PHASE 1: JavaScript Deep Foundations — Days 1-12, 48h
# ═══════════════════════════════════════════════════════════════════
PHASE_1 = r'''
  <div class="sp-phase">
    <div class="sp-phase-header">
      <div class="sp-phase-badge" style="background:linear-gradient(135deg,#059669,#10b981)">P1</div>
      <div class="sp-phase-title">Phase 1 &#8212; JavaScript Deep Foundations</div>
      <div class="sp-phase-subtitle">Days 1&#8211;12<br>48 hours</div>
    </div>
    <div class="sp-day"><div class="sp-day-label">Day 1</div><div class="sp-day-content">
      <span class="sp-time">2.5h</span> <strong>#1&#8211;2:</strong> JS Fundamentals + Scope &amp; Closures &#8212; read deeply, make notes on lexical scope, closure gotchas, temporal dead zone<br>
      <span class="sp-time">1.5h</span> <strong>#131:</strong> Coding &#8212; Closures: counter, once, memoize, private variables &#8212; TYPE every solution, do NOT copy-paste
    </div></div>
    <div class="sp-day"><div class="sp-day-label">Day 2</div><div class="sp-day-content">
      <span class="sp-time">2h</span> <strong>#3&#8211;4:</strong> this Keyword + Prototypes &#8212; draw the prototype chain diagram on paper. Understand `__proto__` vs `prototype`<br>
      <span class="sp-time">1h</span> <strong>#137:</strong> Coding &#8212; myBind, myCall, myApply, myNew &#8212; implement from scratch<br>
      <span class="sp-time">1h</span> <strong>#138:</strong> Coding &#8212; Scope &amp; Hoisting puzzles (IIFE, TDZ, block scoping, var vs let in loops)
    </div></div>
    <div class="sp-day"><div class="sp-day-label">Day 3</div><div class="sp-day-content">
      <span class="sp-time">2.5h</span> <strong>#5:</strong> Async JS &#8212; Promises deep dive (microtask queue, Promise chaining, error propagation, unhandled rejection). Do NOT rush this.<br>
      <span class="sp-time">1.5h</span> <strong>#133:</strong> Coding &#8212; promisify, sleep, Promise.allSettled, sequential execution
    </div></div>
    <div class="sp-day"><div class="sp-day-label">Day 4</div><div class="sp-day-content">
      <span class="sp-time">2h</span> <strong>#6&#8211;7:</strong> ES6+ Features + Advanced Concepts (generators, iterators, symbols, Proxy, Reflect, WeakMap/WeakSet)<br>
      <span class="sp-time">1h</span> <strong>#133:</strong> Coding &#8212; retry with exponential backoff, concurrency limiter, async queue, cancellable promise<br>
      <span class="sp-time">1h</span> <span class="sp-tag-leetcode">LEETCODE</span> 5 easy array problems: Two Sum, Best Time to Buy Stock, Contains Duplicate, Move Zeroes, Merge Sorted Array
    </div></div>
    <div class="sp-day"><div class="sp-day-label">Day 5</div><div class="sp-day-content">
      <span class="sp-time">2h</span> <strong>#8&#8211;10:</strong> Array Methods, Object Methods, Error Handling &#8212; know every trap (sparse arrays, Object.is, custom errors)<br>
      <span class="sp-time">1h</span> <strong>#134:</strong> Coding &#8212; groupBy, flat, deep clone with circular refs, object diff<br>
      <span class="sp-time">1h</span> <strong>#131:</strong> Coding &#8212; curry (fixed arity), infinite currying, partial application, compose/pipe
    </div></div>
    <div class="sp-day"><div class="sp-day-label">Day 6</div><div class="sp-day-content">
      <span class="sp-time">2h</span> <strong>#11&#8211;12:</strong> Modules (ESM vs CJS, tree shaking, circular deps) + Regular Expressions (groups, lookahead, named captures)<br>
      <span class="sp-time">1h</span> <strong>#140:</strong> Coding &#8212; String compression, template engine, query string parser, regex patterns<br>
      <span class="sp-time">1h</span> <span class="sp-tag-leetcode">LEETCODE</span> 5 easy string problems: Valid Anagram, Reverse String, Longest Common Prefix, Valid Palindrome, Roman to Integer
    </div></div>
    <div class="sp-day"><div class="sp-day-label">Day 7</div><div class="sp-day-content">
      <span class="sp-time">2.5h</span> <strong>#121:</strong> Tricky Output Questions &#8212; solve EVERY question with pen &amp; paper FIRST, then verify in console<br>
      <span class="sp-time">1.5h</span> <strong>#139:</strong> Event Loop challenges &#8212; predict output for ALL micro/macro task ordering problems. Draw the queue diagram.
    </div></div>
    <div class="sp-rest">Day 8 &#8212; REST DAY. Revision: re-read your notes for #1&#8211;12. Redo 3 tricky output questions without looking at answers.</div>
    <div class="sp-day"><div class="sp-day-label">Day 9</div><div class="sp-day-content">
      <span class="sp-time">2.5h</span> <strong>#122:</strong> Polyfills Round 1 &#8212; Promise.all, Promise.race, Promise.any, Promise.allSettled from scratch<br>
      <span class="sp-time">1.5h</span> <strong>#122:</strong> Polyfills Round 2 &#8212; Array.map, Array.filter, Array.reduce, Array.flat from scratch
    </div></div>
    <div class="sp-day"><div class="sp-day-label">Day 10</div><div class="sp-day-content">
      <span class="sp-time">2h</span> <strong>#132:</strong> Coding &#8212; debounce (leading/trailing/both options), throttle (with leading/trailing), requestAnimationFrame throttle<br>
      <span class="sp-time">1h</span> <strong>#136:</strong> Coding &#8212; EventEmitter (on, off, once, emit), PubSub, Observable pattern<br>
      <span class="sp-time">1h</span> <span class="sp-tag-leetcode">LEETCODE</span> 3 medium problems: 3Sum, Group Anagrams, Product of Array Except Self
    </div></div>
    <div class="sp-day"><div class="sp-day-label">Day 11</div><div class="sp-day-content">
      <span class="sp-time">2h</span> <strong>#135:</strong> Coding &#8212; Recursion &amp; Trees: flatten nested array/object, deep equal, tree traversal (BFS/DFS), serialize/deserialize<br>
      <span class="sp-time">1h</span> <strong>#141:</strong> Coding &#8212; LRU Cache, Stack, Queue, LinkedList from scratch<br>
      <span class="sp-time">1h</span> <span class="sp-tag-leetcode">LEETCODE</span> 3 medium: Valid BST, Level Order Traversal, Invert Binary Tree
    </div></div>
    <div class="sp-day"><div class="sp-day-label">Day 12</div><div class="sp-day-content">
      <span class="sp-time">2h</span> <strong>#142:</strong> Design Patterns in JS &#8212; Singleton, Factory, Observer, Strategy, Module, Decorator, Command pattern<br>
      <span class="sp-time">1h</span> <strong>JS Mastery Test:</strong> Time yourself: implement Promise.all + debounce + curry + EventEmitter in under 40 min total<br>
      <span class="sp-time">1h</span> <span class="sp-tag-leetcode">LEETCODE</span> 3 medium: Maximum Subarray, Coin Change, Climbing Stairs DP
    </div></div>
  </div>
'''

# ═══════════════════════════════════════════════════════════════════
# PHASE 2: DOM, Browser, HTML — Days 13-20, 32h
# ═══════════════════════════════════════════════════════════════════
PHASE_2 = r'''
  <div class="sp-phase">
    <div class="sp-phase-header">
      <div class="sp-phase-badge" style="background:linear-gradient(135deg,#2563eb,#3b82f6)">P2</div>
      <div class="sp-phase-title">Phase 2 &#8212; DOM, Browser &amp; HTML Mastery</div>
      <div class="sp-phase-subtitle">Days 13&#8211;20<br>32 hours</div>
    </div>
    <div class="sp-day"><div class="sp-day-label">Day 13</div><div class="sp-day-content">
      <span class="sp-time">2h</span> <strong>#13&#8211;14:</strong> DOM Manipulation + DOM Traversal &#8212; understand reflow vs repaint, DocumentFragment, virtual DOM concept<br>
      <span class="sp-time">1h</span> <strong>#143:</strong> Coding &#8212; DOM Challenges: build a querySelector, event delegation utility, DOM differ<br>
      <span class="sp-time">1h</span> <span class="sp-tag-leetcode">LEETCODE</span> 3 medium: Implement Trie, Word Search, Longest Substring Without Repeating Characters
    </div></div>
    <div class="sp-day"><div class="sp-day-label">Day 14</div><div class="sp-day-content">
      <span class="sp-time">2h</span> <strong>#15&#8211;16:</strong> Events (bubbling/capturing/delegation) + Browser Storage (localStorage, sessionStorage, IndexedDB, cookies)<br>
      <span class="sp-time">1h</span> <strong>#143:</strong> Coding &#8212; Virtual scroll implementation, infinite scroll, intersection observer utility<br>
      <span class="sp-time">1h</span> <span class="sp-tag-practice">PRACTICE</span> Build a lightweight jQuery clone: $(), .on(), .off(), .css(), .addClass(), .html()
    </div></div>
    <div class="sp-day"><div class="sp-day-label">Day 15</div><div class="sp-day-content">
      <span class="sp-time">2h</span> <strong>#17&#8211;19:</strong> Browser APIs + Window &amp; Document + Forms &#8212; Service Workers, Web Workers, requestIdleCallback, Broadcast Channel<br>
      <span class="sp-time">1h</span> <strong>Machine Coding #1:</strong> Build a form validator library from scratch (required, email, minLength, pattern, custom rules)<br>
      <span class="sp-time">1h</span> <span class="sp-tag-leetcode">LEETCODE</span> 3 medium: Number of Islands, Rotting Oranges, Flood Fill (BFS/DFS practice)
    </div></div>
    <div class="sp-day"><div class="sp-day-label">Day 16</div><div class="sp-day-content">
      <span class="sp-time">2h</span> <strong>#20&#8211;24:</strong> Semantic HTML + HTML5 Features + Metadata/SEO + Media + HTML Accessibility<br>
      <span class="sp-time">2h</span> <strong>#95&#8211;98:</strong> Browser Rendering + How Browsers Work + Progressive Enhancement + Web Standards &#8212; understand Critical Rendering Path end-to-end
    </div></div>
    <div class="sp-day"><div class="sp-day-label">Day 17</div><div class="sp-day-content">
      <span class="sp-time">2.5h</span> <strong>#123 Part 1:</strong> Machine Coding &#8212; Build an autocomplete/typeahead from scratch: debounced API, keyboard nav, highlight matches, accessibility<br>
      <span class="sp-time">1.5h</span> <span class="sp-tag-leetcode">LEETCODE</span> Sliding window: Minimum Window Substring, Max Sum Subarray of Size K, Longest Repeating Character Replacement
    </div></div>
    <div class="sp-day"><div class="sp-day-label">Day 18</div><div class="sp-day-content">
      <span class="sp-time">2.5h</span> <strong>#123 Part 2:</strong> Machine Coding &#8212; Build a drag-and-drop Kanban board (HTML5 DnD API, state management, persistence)<br>
      <span class="sp-time">1.5h</span> <span class="sp-tag-leetcode">LEETCODE</span> Two pointers: Container With Most Water, Trapping Rain Water, Sort Colors
    </div></div>
    <div class="sp-rest">Day 19 &#8212; REST DAY. Revision: Review #13&#8211;24. Can you explain the Critical Rendering Path without notes? Redo Event Loop output questions.</div>
    <div class="sp-day"><div class="sp-day-label">Day 20</div><div class="sp-day-content">
      <span class="sp-time">2.5h</span> <strong>#123 Part 3:</strong> Machine Coding &#8212; Build a star rating widget, tooltip system, and modal/dialog (focus trapping, ESC close, ARIA)<br>
      <span class="sp-time">1.5h</span> <span class="sp-tag-leetcode">LEETCODE</span> Stack/Queue: Valid Parentheses, Min Stack, Daily Temperatures, Next Greater Element
    </div></div>
  </div>
'''

# ═══════════════════════════════════════════════════════════════════
# PHASE 3: CSS Deep Dive — Days 21-28, 32h
# ═══════════════════════════════════════════════════════════════════
PHASE_3 = r'''
  <div class="sp-phase">
    <div class="sp-phase-header">
      <div class="sp-phase-badge" style="background:linear-gradient(135deg,#7c3aed,#8b5cf6)">P3</div>
      <div class="sp-phase-title">Phase 3 &#8212; CSS, TypeScript &amp; Tooling</div>
      <div class="sp-phase-subtitle">Days 21&#8211;28<br>32 hours</div>
    </div>
    <div class="sp-day"><div class="sp-day-label">Day 21</div><div class="sp-day-content">
      <span class="sp-time">2h</span> <strong>#25&#8211;27:</strong> CSS Selectors + Box Model + Layout &#8212; specificity calculation, margin collapse, BFC, stacking contexts<br>
      <span class="sp-time">1h</span> <strong>#28&#8211;29:</strong> Flexbox + Grid &#8212; solve 20 Flexbox/Grid layout challenges. Know every property by heart.<br>
      <span class="sp-time">1h</span> <span class="sp-tag-practice">PRACTICE</span> Recreate a complex layout: Netflix homepage grid OR a dashboard sidebar+content layout using only CSS Grid
    </div></div>
    <div class="sp-day"><div class="sp-day-label">Day 22</div><div class="sp-day-content">
      <span class="sp-time">2h</span> <strong>#30&#8211;35:</strong> Responsive Design + Typography + Colors + Transforms &amp; Animations + CSS Variables + Modern CSS<br>
      <span class="sp-time">1h</span> <strong>#36&#8211;39:</strong> Methodologies (BEM, OOCSS) + CSS-in-JS + Preprocessors + CSS Performance<br>
      <span class="sp-time">1h</span> <span class="sp-tag-practice">PRACTICE</span> Build a fully responsive card component with hover animations, dark mode support, and container queries
    </div></div>
    <div class="sp-day"><div class="sp-day-label">Day 23</div><div class="sp-day-content">
      <span class="sp-time">2.5h</span> <strong>#40&#8211;46:</strong> TypeScript &#8212; Basics + Advanced Types + Generics + Utility Types + Functions + Enums + Modules. Focus on generics deeply.<br>
      <span class="sp-time">1.5h</span> <strong>#125:</strong> Advanced TypeScript Patterns &#8212; conditional types, mapped types, template literal types, infer keyword
    </div></div>
    <div class="sp-day"><div class="sp-day-label">Day 24</div><div class="sp-day-content">
      <span class="sp-time">2h</span> <span class="sp-tag-practice">PRACTICE</span> TypeScript challenge: Type a full REST API client with generics, discriminated unions, and branded types<br>
      <span class="sp-time">1h</span> <span class="sp-tag-leetcode">LEETCODE</span> 3 medium: LRU Cache, Design HashMap, Design Browser History<br>
      <span class="sp-time">1h</span> <span class="sp-tag-leetcode">LEETCODE</span> Binary Search: Search in Rotated Array, Find Minimum in Rotated Sorted Array, Koko Eating Bananas
    </div></div>
    <div class="sp-day"><div class="sp-day-label">Day 25</div><div class="sp-day-content">
      <span class="sp-time">2h</span> <strong>#68&#8211;73:</strong> Build Tools &#8212; Webpack (loaders, plugins, code splitting, HMR), Vite, Babel, Package Managers, Linting, Env Variables<br>
      <span class="sp-time">2h</span> <span class="sp-tag-practice">PRACTICE</span> Set up a project from scratch: Webpack config with code splitting, tree shaking, CSS extraction, source maps. Then the same with Vite &#8212; compare.
    </div></div>
    <div class="sp-day"><div class="sp-day-label">Day 26</div><div class="sp-day-content">
      <span class="sp-time">2h</span> <strong>#63&#8211;67:</strong> Testing &#8212; Unit Testing + Integration + E2E + TDD + State Management patterns<br>
      <span class="sp-time">1h</span> <span class="sp-tag-practice">PRACTICE</span> Write 15 unit tests for your polyfills (Promise.all, debounce, curry) using Jest/Vitest<br>
      <span class="sp-time">1h</span> <span class="sp-tag-leetcode">LEETCODE</span> 4 medium: Merge Intervals, Insert Interval, Meeting Rooms II, Non-overlapping Intervals
    </div></div>
    <div class="sp-rest">Day 27 &#8212; REST DAY. Revision: Re-read CSS selectors specificity, TypeScript generics, Webpack internals. Practice explaining them aloud.</div>
    <div class="sp-day"><div class="sp-day-label">Day 28</div><div class="sp-day-content">
      <span class="sp-time">2h</span> <strong>Cumulative Review:</strong> Speed run through #25&#8211;73 headers. Flag any topic you can't explain in 30 seconds. Deep-read those.<br>
      <span class="sp-time">1h</span> <span class="sp-tag-leetcode">LEETCODE</span> 3 medium: Longest Palindromic Substring, Decode Ways, Word Break (DP)<br>
      <span class="sp-time">1h</span> <strong>Polyfill Speed Test:</strong> Implement these 5 under 5 min each: Promise.all, Array.reduce, debounce, curry, EventEmitter
    </div></div>
  </div>
'''

# ═══════════════════════════════════════════════════════════════════
# PHASE 4: Performance, Security, Networking — Days 29-36, 32h
# ═══════════════════════════════════════════════════════════════════
PHASE_4 = r'''
  <div class="sp-phase">
    <div class="sp-phase-header">
      <div class="sp-phase-badge" style="background:linear-gradient(135deg,#d97706,#f59e0b)">P4</div>
      <div class="sp-phase-title">Phase 4 &#8212; Performance, Security &amp; Networking</div>
      <div class="sp-phase-subtitle">Days 29&#8211;36<br>32 hours</div>
    </div>
    <div class="sp-day"><div class="sp-day-label">Day 29</div><div class="sp-day-content">
      <span class="sp-time">2h</span> <strong>#47&#8211;48:</strong> Loading Performance + Runtime Performance &#8212; lazy loading, code splitting, tree shaking, requestIdleCallback<br>
      <span class="sp-time">1h</span> <strong>#49&#8211;50:</strong> Rendering Performance + Caching &#8212; avoid layout thrashing, will-change, composite layers, cache headers<br>
      <span class="sp-time">1h</span> <strong>#128:</strong> Performance Case Studies &#8212; real-world optimization stories at FAANG scale
    </div></div>
    <div class="sp-day"><div class="sp-day-label">Day 30</div><div class="sp-day-content">
      <span class="sp-time">2h</span> <strong>#51&#8211;54:</strong> Core Web Vitals + Images/Media + Fonts + Measuring Performance (Lighthouse, WebPageTest, Chrome DevTools)<br>
      <span class="sp-time">2h</span> <span class="sp-tag-practice">PRACTICE</span> Performance audit: Take any live website, run Lighthouse, identify top 5 issues, write a fix plan. Then actually fix 2 of them.
    </div></div>
    <div class="sp-day"><div class="sp-day-label">Day 31</div><div class="sp-day-content">
      <span class="sp-time">2h</span> <strong>#55&#8211;57:</strong> Security &#8212; Common Vulnerabilities (XSS, CSRF, SSRF) + Prevention + Authentication (OAuth, JWT, PKCE, session management)<br>
      <span class="sp-time">1h</span> <strong>#130:</strong> Advanced Security &#8212; CSP headers, subresource integrity, supply chain attacks, CORS deep dive<br>
      <span class="sp-time">1h</span> <span class="sp-tag-leetcode">LEETCODE</span> Graph: Clone Graph, Course Schedule, Pacific Atlantic Water Flow
    </div></div>
    <div class="sp-day"><div class="sp-day-label">Day 32</div><div class="sp-day-content">
      <span class="sp-time">2h</span> <strong>#58&#8211;62:</strong> Networking &#8212; HTTP/2/3, REST API Design, GraphQL, Data Fetching patterns, WebSockets, SSE<br>
      <span class="sp-time">1h</span> <span class="sp-tag-practice">PRACTICE</span> Build a real-time chat using WebSockets (vanilla JS, no libraries). Handle reconnection, heartbeat, message queuing.<br>
      <span class="sp-time">1h</span> <span class="sp-tag-leetcode">LEETCODE</span> Heap: Top K Frequent Elements, Kth Largest Element, Merge K Sorted Lists
    </div></div>
    <div class="sp-day"><div class="sp-day-label">Day 33</div><div class="sp-day-content">
      <span class="sp-time">2h</span> <strong>#74&#8211;79:</strong> Accessibility &#8212; WCAG, Keyboard Nav, Screen Readers, ARIA, Color/Contrast, Form Accessibility<br>
      <span class="sp-time">1h</span> <span class="sp-tag-practice">PRACTICE</span> Accessibility audit: Test your autocomplete and Kanban from Phase 2. Fix every a11y issue &#8212; screen reader testing, keyboard-only navigation.<br>
      <span class="sp-time">1h</span> <span class="sp-tag-leetcode">LEETCODE</span> 3 medium DP: House Robber, Unique Paths, Minimum Path Sum
    </div></div>
    <div class="sp-day"><div class="sp-day-label">Day 34</div><div class="sp-day-content">
      <span class="sp-time">2h</span> <strong>#80&#8211;86:</strong> Design Patterns &#8212; Creational, Structural, Behavioral, Architectural (MVC, MVVM, Flux, Clean Architecture)<br>
      <span class="sp-time">2h</span> <span class="sp-tag-practice">PRACTICE</span> Implement Observer, Mediator, Strategy, and Command patterns in a real mini-app (e.g., a text editor with undo/redo)
    </div></div>
    <div class="sp-rest">Day 35 &#8212; REST DAY. Revision: Review security headers, CORS, performance metrics. Practice explaining Core Web Vitals and XSS prevention aloud in 2 min each.</div>
    <div class="sp-day"><div class="sp-day-label">Day 36</div><div class="sp-day-content">
      <span class="sp-time">2h</span> <strong>#87&#8211;91:</strong> DSA &#8212; Data Structures + Common Algorithms + Complexity Analysis<br>
      <span class="sp-time">1h</span> <span class="sp-tag-leetcode">LEETCODE</span> 3 medium: Implement Trie, Design Add and Search Words, Word Search II (Trie+DFS)<br>
      <span class="sp-time">1h</span> <span class="sp-tag-leetcode">LEETCODE</span> 2 hard: Serialize/Deserialize Binary Tree, Median of Two Sorted Arrays
    </div></div>
  </div>
'''

# ═══════════════════════════════════════════════════════════════════
# PHASE 5: System Design — Days 37-46, 40h
# ═══════════════════════════════════════════════════════════════════
PHASE_5 = r'''
  <div class="sp-phase">
    <div class="sp-phase-header">
      <div class="sp-phase-badge" style="background:linear-gradient(135deg,#dc2626,#ef4444)">P5</div>
      <div class="sp-phase-title">Phase 5 &#8212; Frontend System Design (FAANG-Level)</div>
      <div class="sp-phase-subtitle">Days 37&#8211;46<br>40 hours</div>
    </div>
    <div class="sp-day"><div class="sp-day-label">Day 37</div><div class="sp-day-content">
      <span class="sp-time">2h</span> <strong>#92&#8211;93:</strong> Component Design + App Architecture &#8212; micro-frontends, module federation, monorepo patterns<br>
      <span class="sp-time">2h</span> <strong>#126:</strong> Frontend LLD &#8212; component API design, state machine modeling, dependency injection patterns, interface contracts
    </div></div>
    <div class="sp-day"><div class="sp-day-label">Day 38</div><div class="sp-day-content">
      <span class="sp-time">2h</span> <strong>#94&#8211;96:</strong> Common Components + Full App Designs + Scalability<br>
      <span class="sp-time">2h</span> <strong>#127:</strong> System Design Patterns &#8212; BFF, API Gateway, caching layers, CDN strategy, edge computing, SSR vs CSR vs ISR decision framework
    </div></div>
    <div class="sp-day"><div class="sp-day-label">Day 39</div><div class="sp-day-content">
      <span class="sp-time">4h</span> <span class="sp-tag-mock">MOCK #1</span> <strong>Design Google Search Frontend</strong> &#8212; 45 min timed, speak aloud:<br>
      &bull; Requirements gathering (5 min) &bull; High-level architecture (10 min) &bull; Component breakdown (10 min) &bull; Data flow &amp; state (10 min) &bull; Performance &amp; edge cases (10 min)<br>
      Then spend 1h writing up what you missed and improving your answer. Record yourself if possible.
    </div></div>
    <div class="sp-day"><div class="sp-day-label">Day 40</div><div class="sp-day-content">
      <span class="sp-time">4h</span> <span class="sp-tag-mock">MOCK #2</span> <strong>Design a Real-Time Collaborative Document Editor (Google Docs)</strong> &#8212; 45 min timed:<br>
      &bull; Conflict resolution (OT vs CRDT) &bull; WebSocket architecture &bull; Cursor sync &bull; Offline support &bull; Version history<br>
      Spend 1.5h improving your answer. Research OT/CRDT trade-offs. This is a classic FAANG question.
    </div></div>
    <div class="sp-day"><div class="sp-day-label">Day 41</div><div class="sp-day-content">
      <span class="sp-time">2h</span> <span class="sp-tag-mock">MOCK #3</span> <strong>Design Facebook News Feed</strong> &#8212; infinite scroll, virtualization, optimistic updates, cache invalidation, real-time updates<br>
      <span class="sp-time">2h</span> <span class="sp-tag-leetcode">LEETCODE</span> Backtracking: Subsets, Permutations, Combination Sum, N-Queens, Sudoku Solver
    </div></div>
    <div class="sp-day"><div class="sp-day-label">Day 42</div><div class="sp-day-content">
      <span class="sp-time">2h</span> <span class="sp-tag-mock">MOCK #4</span> <strong>Design Figma (Collaborative Design Tool)</strong> &#8212; Canvas rendering, layer management, real-time multi-user, zoom/pan, asset library<br>
      <span class="sp-time">2h</span> <span class="sp-tag-practice">PRACTICE</span> Machine Coding: Build a mini drawing canvas app (HTML5 Canvas, undo/redo stack, shape tools, export as PNG)
    </div></div>
    <div class="sp-rest">Day 43 &#8212; REST DAY. Review all 4 system design answers. Write a 1-page template for your system design approach. Memorize the structure.</div>
    <div class="sp-day"><div class="sp-day-label">Day 44</div><div class="sp-day-content">
      <span class="sp-time">2h</span> <span class="sp-tag-mock">MOCK #5</span> <strong>Design Spotify Web Player</strong> &#8212; audio streaming, playlist state, offline mode, search with debounce, responsive player UI<br>
      <span class="sp-time">2h</span> <span class="sp-tag-leetcode">LEETCODE</span> Graph advanced: Dijkstra's, Topological Sort, Network Delay Time, Alien Dictionary
    </div></div>
    <div class="sp-day"><div class="sp-day-label">Day 45</div><div class="sp-day-content">
      <span class="sp-time">2h</span> <span class="sp-tag-mock">MOCK #6</span> <strong>Design Twitter/X Frontend</strong> &#8212; tweet timeline, real-time updates, infinite scroll, media previews, notifications, PWA<br>
      <span class="sp-time">2h</span> <span class="sp-tag-practice">PRACTICE</span> Machine Coding: Build an image carousel with swipe gestures, lazy loading, keyboard nav, touch support, responsive
    </div></div>
    <div class="sp-day"><div class="sp-day-label">Day 46</div><div class="sp-day-content">
      <span class="sp-time">2h</span> <strong>System Design Consolidation:</strong> Re-do your weakest system design mock from scratch. Compare with your first attempt.<br>
      <span class="sp-time">1h</span> <span class="sp-tag-leetcode">LEETCODE</span> 2 hard: LFU Cache, Trapping Rainwater II<br>
      <span class="sp-time">1h</span> <span class="sp-tag-leetcode">LEETCODE</span> 3 medium: Task Scheduler, Reorganize String, Partition Labels (Greedy)
    </div></div>
  </div>
'''

# ═══════════════════════════════════════════════════════════════════
# PHASE 6: Angular Deep Dive — Days 47-56, 40h
# ═══════════════════════════════════════════════════════════════════
PHASE_6 = r'''
  <div class="sp-phase">
    <div class="sp-phase-header">
      <div class="sp-phase-badge" style="background:linear-gradient(135deg,#be185d,#ec4899)">P6</div>
      <div class="sp-phase-title">Phase 6 &#8212; Angular Deep Dive &amp; Projects</div>
      <div class="sp-phase-subtitle">Days 47&#8211;56<br>40 hours</div>
    </div>
    <div class="sp-day"><div class="sp-day-label">Day 47</div><div class="sp-day-content">
      <span class="sp-time">2h</span> <strong>#106&#8211;107:</strong> Angular Change Detection + Dependency Injection &#8212; zone.js internals, OnPush strategy, hierarchical injectors<br>
      <span class="sp-time">2h</span> <strong>#108&#8211;109:</strong> Lifecycle Hooks + RxJS Deep Dive &#8212; marble diagrams, switchMap vs mergeMap vs concatMap, memory leak patterns
    </div></div>
    <div class="sp-day"><div class="sp-day-label">Day 48</div><div class="sp-day-content">
      <span class="sp-time">2h</span> <strong>#110&#8211;111:</strong> Router &amp; Guards + Reactive Forms &#8212; lazy loading routes, preloading strategies, custom validators, dynamic forms<br>
      <span class="sp-time">2h</span> <strong>#112&#8211;113:</strong> HTTP &amp; Interceptors + Standalone &amp; Modern APIs &#8212; signals, deferrable views, new control flow
    </div></div>
    <div class="sp-day"><div class="sp-day-label">Day 49</div><div class="sp-day-content">
      <span class="sp-time">2h</span> <strong>#114&#8211;116:</strong> Pipes &amp; Directives + Content Projection + Angular Performance<br>
      <span class="sp-time">2h</span> <strong>#117&#8211;120:</strong> Angular Testing + NgRx &amp; SignalStore + Best Practices + Common Mistakes
    </div></div>
    <div class="sp-day"><div class="sp-day-label">Day 50</div><div class="sp-day-content">
      <span class="sp-time">4h</span> <span class="sp-tag-practice">PRACTICE</span> <strong>Angular Project #1 &#8212; Admin Dashboard:</strong><br>
      &bull; Standalone components, lazy-loaded routes, reactive forms<br>
      &bull; NgRx/SignalStore for state, HTTP interceptors for auth<br>
      &bull; Data table with sorting, filtering, pagination<br>
      &bull; Dark mode toggle, responsive sidebar, chart integration
    </div></div>
    <div class="sp-day"><div class="sp-day-label">Day 51</div><div class="sp-day-content">
      <span class="sp-time">4h</span> <span class="sp-tag-practice">PRACTICE</span> <strong>Angular Project #1 continued:</strong><br>
      &bull; Add unit tests (Jasmine/Karma) for 3 components + 2 services<br>
      &bull; Add E2E test (Cypress) for login flow<br>
      &bull; Performance audit: implement OnPush everywhere, trackBy, lazy images
    </div></div>
    <div class="sp-rest">Day 52 &#8212; REST DAY. Review Angular notes. Can you explain Change Detection, DI hierarchy, and RxJS operators without looking at notes? Test yourself.</div>
    <div class="sp-day"><div class="sp-day-label">Day 53</div><div class="sp-day-content">
      <span class="sp-time">4h</span> <span class="sp-tag-practice">PRACTICE</span> <strong>Angular Project #2 &#8212; E-Commerce Storefront:</strong><br>
      &bull; Product listing with virtual scroll, search with debounce<br>
      &bull; Cart with NgRx, optimistic updates<br>
      &bull; Checkout form with multi-step reactive forms, validation<br>
      &bull; Route guards, HTTP interceptors, error handling
    </div></div>
    <div class="sp-day"><div class="sp-day-label">Day 54</div><div class="sp-day-content">
      <span class="sp-time">2h</span> <span class="sp-tag-practice">PRACTICE</span> <strong>Angular Project #2 continued:</strong> Add SSR with Angular Universal, SEO meta tags, PWA manifest<br>
      <span class="sp-time">2h</span> <span class="sp-tag-leetcode">LEETCODE</span> DP marathon: Longest Increasing Subsequence, Edit Distance, Longest Common Subsequence, 0/1 Knapsack
    </div></div>
    <div class="sp-day"><div class="sp-day-label">Day 55</div><div class="sp-day-content">
      <span class="sp-time">4h</span> <span class="sp-tag-practice">PRACTICE</span> <strong>Angular Project #3 &#8212; Real-Time Chat App:</strong><br>
      &bull; WebSocket service with RxJS (reconnection, heartbeat)<br>
      &bull; Message list with virtual scroll, typing indicators<br>
      &bull; File upload with drag-and-drop, image preview<br>
      &bull; Push notifications, online/offline status, unread counts
    </div></div>
    <div class="sp-day"><div class="sp-day-label">Day 56</div><div class="sp-day-content">
      <span class="sp-time">2h</span> <span class="sp-tag-practice">PRACTICE</span> <strong>Angular Project #3 continued:</strong> Testing, performance tuning, a11y audit<br>
      <span class="sp-time">2h</span> <strong>Angular Mastery Test:</strong> Explain these without notes in 2 min each: Change Detection, RxJS switchMap vs mergeMap, Standalone components, Signals, NgRx flow, DI resolution
    </div></div>
  </div>
'''

# ═══════════════════════════════════════════════════════════════════
# PHASE 7: Misc + Version Control + Patterns — Days 57-62, 24h
# ═══════════════════════════════════════════════════════════════════
PHASE_7 = r'''
  <div class="sp-phase">
    <div class="sp-phase-header">
      <div class="sp-phase-badge" style="background:linear-gradient(135deg,#0891b2,#06b6d4)">P7</div>
      <div class="sp-phase-title">Phase 7 &#8212; Miscellaneous, Git &amp; Soft Skills</div>
      <div class="sp-phase-subtitle">Days 57&#8211;62<br>24 hours</div>
    </div>
    <div class="sp-day"><div class="sp-day-label">Day 57</div><div class="sp-day-content">
      <span class="sp-time">2h</span> <strong>#99&#8211;105:</strong> Mobile/PWA + CSS Architecture + Modern JS + Framework Comparisons + Soft Skills + Implementation Patterns + Additional Topics<br>
      <span class="sp-time">2h</span> <strong>#87&#8211;91:</strong> Git Basics + Git Workflows + Advanced Git &#8212; rebase vs merge, cherry-pick, bisect, reflog, worktrees
    </div></div>
    <div class="sp-day"><div class="sp-day-label">Day 58</div><div class="sp-day-content">
      <span class="sp-time">2h</span> <strong>#124:</strong> Advanced Coding Challenges &#8212; implement JSON.stringify, JSON.parse, lodash.get, lodash.set, deep merge<br>
      <span class="sp-time">2h</span> <span class="sp-tag-leetcode">LEETCODE</span> Mixed hard: Regular Expression Matching, Merge K Sorted Lists, Sliding Window Maximum, Word Ladder
    </div></div>
    <div class="sp-day"><div class="sp-day-label">Day 59</div><div class="sp-day-content">
      <span class="sp-time">2h</span> <strong>Machine Coding #4:</strong> Build a spreadsheet/grid component &#8212; editable cells, formulas, cell references, undo/redo<br>
      <span class="sp-time">2h</span> <span class="sp-tag-practice">PRACTICE</span> Machine Coding #5: Build a rich text editor with toolbar &#8212; bold, italic, list, link insertion, keyboard shortcuts
    </div></div>
    <div class="sp-day"><div class="sp-day-label">Day 60</div><div class="sp-day-content">
      <span class="sp-time">2h</span> <strong>Machine Coding #6:</strong> Build a file explorer tree &#8212; expand/collapse, lazy loading children, drag to move, right-click context menu, keyboard nav<br>
      <span class="sp-time">2h</span> <span class="sp-tag-leetcode">LEETCODE</span> Union-Find: Number of Connected Components, Redundant Connection, Accounts Merge, Smallest String With Swaps
    </div></div>
    <div class="sp-rest">Day 61 &#8212; REST DAY. Big revision: Skim ALL 143 section headers. Write down every topic where you feel &lt;70% confident. These are your targets for Phase 8.</div>
    <div class="sp-day"><div class="sp-day-label">Day 62</div><div class="sp-day-content">
      <span class="sp-time">2h</span> <strong>Weak Area Deep Dive:</strong> From your Day 61 list, pick the 5 weakest topics and re-read them thoroughly.<br>
      <span class="sp-time">1h</span> <span class="sp-tag-leetcode">LEETCODE</span> 3 problems from your weakest DSA pattern<br>
      <span class="sp-time">1h</span> <strong>Polyfill Speed Test #2:</strong> All 10 polyfills from memory, aim for &lt;6 min each now. Time yourself strictly.
    </div></div>
  </div>
'''

# ═══════════════════════════════════════════════════════════════════
# PHASE 8: Behavioral & Leadership — Days 63-68, 24h
# ═══════════════════════════════════════════════════════════════════
PHASE_8 = r'''
  <div class="sp-phase">
    <div class="sp-phase-header">
      <div class="sp-phase-badge" style="background:linear-gradient(135deg,#ea580c,#f97316)">P8</div>
      <div class="sp-phase-title">Phase 8 &#8212; Behavioral &amp; Leadership (FAANG-Specific)</div>
      <div class="sp-phase-subtitle">Days 63&#8211;68<br>24 hours</div>
    </div>
    <div class="sp-day"><div class="sp-day-label">Day 63</div><div class="sp-day-content">
      <span class="sp-time">2h</span> <strong>#129:</strong> Behavioral Questions &#8212; STAR method deep dive. Write your first 5 stories:<br>
      &bull; 1. Biggest technical challenge you solved &bull; 2. Time you disagreed with your manager &bull; 3. Project you led &bull; 4. Failure and what you learned &bull; 5. Time you mentored someone<br>
      <span class="sp-time">2h</span> <strong>Amazon Leadership Principles:</strong> Map each of your 5 stories to LPs: Customer Obsession, Ownership, Bias for Action, Dive Deep, Earn Trust, Deliver Results
    </div></div>
    <div class="sp-day"><div class="sp-day-label">Day 64</div><div class="sp-day-content">
      <span class="sp-time">2h</span> <strong>Write 5 more STAR stories:</strong><br>
      &bull; 6. Scaling a system under pressure &bull; 7. Cross-team collaboration &bull; 8. Ambiguous problem with no clear solution &bull; 9. Taking initiative beyond your role &bull; 10. Handling conflicting priorities<br>
      <span class="sp-time">2h</span> <strong>Google Googliness + Meta Core Values:</strong> Map stories to "Collaboration," "Transparency," "Move Fast." Write company-specific versions.
    </div></div>
    <div class="sp-day"><div class="sp-day-label">Day 65</div><div class="sp-day-content">
      <span class="sp-time">2h</span> <strong>Additional 5 STAR stories for SDE-3:</strong><br>
      &bull; 11. Tech debt reduction strategy &bull; 12. Architecture decision with trade-offs &bull; 13. Driving team productivity improvement &bull; 14. Influencing without authority &bull; 15. Handling production incident<br>
      <span class="sp-time">2h</span> <span class="sp-tag-mock">BEHAVIORAL MOCK</span> Practice all 15 stories aloud. Each must be 2 min or less. Record yourself. Watch the recording. Fix filler words.
    </div></div>
    <div class="sp-day"><div class="sp-day-label">Day 66</div><div class="sp-day-content">
      <span class="sp-time">2h</span> <strong>SDE-3 Leadership Deep Dive:</strong> Prepare answers for:<br>
      &bull; "How do you make technical decisions?" &bull; "How do you handle underperformers?" &bull; "Describe your code review philosophy" &bull; "How do you balance tech debt vs features?"<br>
      <span class="sp-time">2h</span> <span class="sp-tag-leetcode">LEETCODE</span> Monotonic Stack: Largest Rectangle in Histogram, Maximal Rectangle, Stock Span, Remove K Digits
    </div></div>
    <div class="sp-day"><div class="sp-day-label">Day 67</div><div class="sp-day-content">
      <span class="sp-time">2h</span> <strong>"Why this company?" Prep:</strong> Research 3-5 target companies deeply. Write genuine reasons for each. Prepare 3 questions to ask each interviewer.<br>
      <span class="sp-time">2h</span> <span class="sp-tag-practice">PRACTICE</span> Machine Coding: Build a notification system &#8212; toast stack, auto-dismiss, priority queue, action buttons, ARIA live regions
    </div></div>
    <div class="sp-day"><div class="sp-day-label">Day 68</div><div class="sp-day-content">
      <span class="sp-time">4h</span> <span class="sp-tag-mock">FULL MOCK INTERVIEW #1</span> Simulate a complete FAANG interview (find a friend or use Pramp/interviewing.io):<br>
      &bull; Round 1: 45 min &#8212; DSA (1 medium + 1 hard)<br>
      &bull; Round 2: 45 min &#8212; Machine coding (timed, unfamiliar component)<br>
      &bull; Round 3: 45 min &#8212; System design<br>
      &bull; Round 4: 45 min &#8212; Behavioral<br>
      Score yourself 1&#8211;5 on each. Be brutally honest.
    </div></div>
  </div>
'''

# ═══════════════════════════════════════════════════════════════════
# PHASE 9: LeetCode Intensive — Days 69-76, 32h
# ═══════════════════════════════════════════════════════════════════
PHASE_9 = r'''
  <div class="sp-phase">
    <div class="sp-phase-header">
      <div class="sp-phase-badge" style="background:linear-gradient(135deg,#be185d,#f43f5e)">P9</div>
      <div class="sp-phase-title">Phase 9 &#8212; LeetCode Intensive Sprint</div>
      <div class="sp-phase-subtitle">Days 69&#8211;76<br>32 hours</div>
    </div>
    <div class="sp-day"><div class="sp-day-label">Day 69</div><div class="sp-day-content">
      <span class="sp-time">4h</span> <span class="sp-tag-leetcode">LEETCODE</span> <strong>Arrays &amp; Hashing:</strong> 4Sum, Encode/Decode Strings, Longest Consecutive Sequence, Top K Frequent Words, Subarray Sum Equals K
    </div></div>
    <div class="sp-day"><div class="sp-day-label">Day 70</div><div class="sp-day-content">
      <span class="sp-time">4h</span> <span class="sp-tag-leetcode">LEETCODE</span> <strong>Trees &amp; Graphs:</strong> Binary Tree Max Path Sum, Lowest Common Ancestor, Graph Valid Tree, Word Ladder II, All Nodes Distance K
    </div></div>
    <div class="sp-day"><div class="sp-day-label">Day 71</div><div class="sp-day-content">
      <span class="sp-time">4h</span> <span class="sp-tag-leetcode">LEETCODE</span> <strong>DP Advanced:</strong> Burst Balloons, Partition Equal Subset Sum, Target Sum, Palindrome Partitioning, Interleaving String
    </div></div>
    <div class="sp-day"><div class="sp-day-label">Day 72</div><div class="sp-day-content">
      <span class="sp-time">4h</span> <span class="sp-tag-leetcode">LEETCODE</span> <strong>Intervals &amp; Greedy:</strong> Minimum Number of Arrows, Car Pooling, Jump Game I+II, Gas Station, Candy
    </div></div>
    <div class="sp-rest">Day 73 &#8212; REST DAY. Review all LeetCode solutions. For every problem you got wrong, write down WHY and the pattern you missed.</div>
    <div class="sp-day"><div class="sp-day-label">Day 74</div><div class="sp-day-content">
      <span class="sp-time">4h</span> <span class="sp-tag-leetcode">LEETCODE</span> <strong>Sliding Window &amp; Two Pointers:</strong> Minimum Window Substring, Subarrays with K Different Integers, Shortest Subarray with Sum at Least K, Fruit into Baskets
    </div></div>
    <div class="sp-day"><div class="sp-day-label">Day 75</div><div class="sp-day-content">
      <span class="sp-time">4h</span> <span class="sp-tag-leetcode">LEETCODE</span> <strong>Design Problems:</strong> Design Twitter, Design Hit Counter, Design File System, Design Snake Game, Design Tic-Tac-Toe
    </div></div>
    <div class="sp-day"><div class="sp-day-label">Day 76</div><div class="sp-day-content">
      <span class="sp-time">2h</span> <span class="sp-tag-leetcode">LEETCODE</span> <strong>Hard problems:</strong> Wildcard Matching, Minimum Window Substring, Alien Dictionary, Critical Connections<br>
      <span class="sp-time">2h</span> <strong>Pattern Review:</strong> Write a cheat sheet of all DSA patterns: Two Pointers, Sliding Window, BFS/DFS, DP table, Backtracking template, Monotonic Stack, Union-Find template
    </div></div>
  </div>
'''

# ═══════════════════════════════════════════════════════════════════
# PHASE 10: Advanced Machine Coding — Days 77-82, 24h
# ═══════════════════════════════════════════════════════════════════
PHASE_10 = r'''
  <div class="sp-phase">
    <div class="sp-phase-header">
      <div class="sp-phase-badge" style="background:linear-gradient(135deg,#4f46e5,#6366f1)">P10</div>
      <div class="sp-phase-title">Phase 10 &#8212; Advanced Machine Coding</div>
      <div class="sp-phase-subtitle">Days 77&#8211;82<br>24 hours</div>
    </div>
    <div class="sp-day"><div class="sp-day-label">Day 77</div><div class="sp-day-content">
      <span class="sp-time">4h</span> <span class="sp-tag-practice">PRACTICE</span> <strong>Machine Coding &#8212; Multi-Select Dropdown:</strong> Search, keyboard nav, tag display, virtual scroll for 10k options, accessible, async options loading, group headers, create new option
    </div></div>
    <div class="sp-day"><div class="sp-day-label">Day 78</div><div class="sp-day-content">
      <span class="sp-time">4h</span> <span class="sp-tag-practice">PRACTICE</span> <strong>Machine Coding &#8212; Data Table:</strong> Column sorting, multi-column sort, inline editing, row selection, column resizing, pagination, CSV export, custom cell renderers, sticky headers
    </div></div>
    <div class="sp-day"><div class="sp-day-label">Day 79</div><div class="sp-day-content">
      <span class="sp-time">4h</span> <span class="sp-tag-practice">PRACTICE</span> <strong>Machine Coding &#8212; Calendar/Date Picker:</strong> Month/week/day views, event creation with drag, recurring events, timezone support, responsive, range selection
    </div></div>
    <div class="sp-day"><div class="sp-day-label">Day 80</div><div class="sp-day-content">
      <span class="sp-time">4h</span> <span class="sp-tag-practice">PRACTICE</span> <strong>Machine Coding &#8212; Nested Comment Thread:</strong> Infinite nesting, collapse/expand, vote system, lazy load replies, optimistic updates, reply editor with mentions
    </div></div>
    <div class="sp-rest">Day 81 &#8212; REST DAY. Review all machine coding projects. For each, write down: What you'd improve, accessibility gaps, performance bottlenecks.</div>
    <div class="sp-day"><div class="sp-day-label">Day 82</div><div class="sp-day-content">
      <span class="sp-time">2h</span> <span class="sp-tag-practice">PRACTICE</span> <strong>Speed Machine Coding:</strong> Build a countdown timer with lap functionality in 30 min. Build a color picker in 30 min. Build a tabs component in 20 min.<br>
      <span class="sp-time">2h</span> <span class="sp-tag-practice">PRACTICE</span> <strong>Speed Machine Coding:</strong> Build an accordion in 15 min. Build a tooltip in 15 min. Build a progress stepper in 20 min. Build a tag input in 20 min.
    </div></div>
  </div>
'''

# ═══════════════════════════════════════════════════════════════════
# PHASE 11: Full Mock Interviews — Days 83-86, 16h
# ═══════════════════════════════════════════════════════════════════
PHASE_11 = r'''
  <div class="sp-phase">
    <div class="sp-phase-header">
      <div class="sp-phase-badge" style="background:linear-gradient(135deg,#b91c1c,#dc2626)">P11</div>
      <div class="sp-phase-title">Phase 11 &#8212; Full Mock Interview Simulations</div>
      <div class="sp-phase-subtitle">Days 83&#8211;86<br>16 hours</div>
    </div>
    <div class="sp-day"><div class="sp-day-label">Day 83</div><div class="sp-day-content">
      <span class="sp-time">4h</span> <span class="sp-tag-mock">FULL MOCK #2 &#8212; Google Style</span><br>
      &bull; 45 min DSA: 2 problems (medium+hard), optimize for time complexity<br>
      &bull; 45 min Frontend: Build accessible autocomplete from scratch with tests<br>
      &bull; 45 min System Design: "Design YouTube Frontend" &#8212; video player, recommendations, search, comments<br>
      &bull; 45 min Googliness: Leadership, collaboration, handling ambiguity stories
    </div></div>
    <div class="sp-day"><div class="sp-day-label">Day 84</div><div class="sp-day-content">
      <span class="sp-time">4h</span> <span class="sp-tag-mock">FULL MOCK #3 &#8212; Meta Style</span><br>
      &bull; 45 min Coding: 2 medium LC problems, clean code, explain trade-offs aloud<br>
      &bull; 45 min Frontend: Machine coding &#8212; build something UNFAMILIAR in 40 min<br>
      &bull; 45 min System Design: "Design Instagram Stories" &#8212; upload, feed, expiry, analytics<br>
      &bull; 45 min Behavioral: Values (Move Fast, Be Bold, Focus on Impact, Build Social Value)
    </div></div>
    <div class="sp-day"><div class="sp-day-label">Day 85</div><div class="sp-day-content">
      <span class="sp-time">4h</span> <span class="sp-tag-mock">FULL MOCK #4 &#8212; Amazon Style</span><br>
      &bull; 45 min Online Assessment simulation: 2 problems, strict time limit<br>
      &bull; 45 min System Design: "Design Amazon Product Page" &#8212; recommendations, reviews, buy box, a11y<br>
      &bull; 45 min LP Deep Dive: Customer Obsession, Ownership, Bias for Action, Dive Deep, Earn Trust, Deliver Results &#8212; 2 stories per LP<br>
      &bull; 45 min Bar Raiser: Hardest behavioral questions &#8212; "Tell me about a time you failed spectacularly"
    </div></div>
    <div class="sp-day"><div class="sp-day-label">Day 86</div><div class="sp-day-content">
      <span class="sp-time">2h</span> <strong>Mock Debrief:</strong> Review recordings of all 4 full mocks. Write down patterns: Where do you stumble? What do you skip? What sounds weak?<br>
      <span class="sp-time">2h</span> <strong>Gap Filling:</strong> Spend time on your 3 biggest weaknesses identified from mocks. Deep study + practice.
    </div></div>
  </div>
'''

# ═══════════════════════════════════════════════════════════════════
# PHASE 12: Final Week — Days 87-90, 16h
# ═══════════════════════════════════════════════════════════════════
PHASE_12 = r'''
  <div class="sp-phase">
    <div class="sp-phase-header">
      <div class="sp-phase-badge" style="background:linear-gradient(135deg,#059669,#2563eb,#7c3aed)">P12</div>
      <div class="sp-phase-title">Phase 12 &#8212; Final Polish &amp; Interview Week</div>
      <div class="sp-phase-subtitle">Days 87&#8211;90<br>16 hours</div>
    </div>
    <div class="sp-day"><div class="sp-day-label">Day 87</div><div class="sp-day-content">
      <span class="sp-time">2h</span> <span class="sp-tag-revise">REVISE</span> <strong>Grand Review &#8212; Theory:</strong> Speed-read ALL 143 section headers + key concepts. Use your personal notes and flashcards.<br>
      <span class="sp-time">1h</span> <span class="sp-tag-revise">REVISE</span> <strong>Polyfill Final Run:</strong> All 10 from memory, &lt;5 min each: Promise.all, Array.map, reduce, filter, bind, call, new, debounce, throttle, EventEmitter<br>
      <span class="sp-time">1h</span> <span class="sp-tag-revise">REVISE</span> <strong>Angular Rapid Review:</strong> Change Detection, DI, RxJS operators, Signals, NgRx &#8212; explain each in 60 seconds
    </div></div>
    <div class="sp-day"><div class="sp-day-label">Day 88</div><div class="sp-day-content">
      <span class="sp-time">2h</span> <span class="sp-tag-revise">REVISE</span> <strong>System Design Template:</strong> Review your 8 system designs. Write a universal template: Requirements &#8594; Architecture &#8594; Components &#8594; Data Flow &#8594; Performance &#8594; Edge Cases<br>
      <span class="sp-time">1h</span> <span class="sp-tag-revise">REVISE</span> <strong>DSA Pattern Sheet:</strong> Review your pattern cheat sheet. Solve 3 random mediums in under 20 min each.<br>
      <span class="sp-time">1h</span> <span class="sp-tag-revise">REVISE</span> <strong>Behavioral Stories:</strong> Rehearse your top 10 STAR stories. Each under 2 min. Confident, specific, impactful.
    </div></div>
    <div class="sp-rest">Day 89 &#8212; REST DAY. No studying. Sleep 8+ hours. Exercise. Eat well. Your brain is consolidating 360 hours of knowledge. Trust the process.</div>
    <div class="sp-day"><div class="sp-day-label">Day 90</div><div class="sp-day-content">
      <span class="sp-time">1h</span> <strong>Final Cheat Sheet:</strong> Write your 1-page personal summary of the 20 most-asked topics. Keep it in your pocket.<br>
      <span class="sp-time">1h</span> <strong>Behavioral Stories:</strong> Rehearse your top 5 stories one final time. Confident, concise, 90 seconds each.<br>
      <span class="sp-time">1h</span> <strong>Logistics:</strong> Quiet room, camera, mic test, water, notepad, pen, stable internet. Review company info. Know your interviewer's name if available.<br>
      <span class="sp-time">1h</span> <strong>Confidence Boost:</strong> Solve 3 EASY coding problems fast. Remind yourself: <strong>You have invested 360 hours. You have built 3 Angular projects, solved 120+ LeetCode problems, done 8 system design mocks, practiced 15 STAR stories, built 10+ machine coding components. You are ready.</strong> &#128170;&#128293;
    </div></div>
  </div>
'''

SP_FOOTER = r'''
  <div class="sp-tip">
    <strong>&#128293; FAANG Interview Reality Check:</strong><br>
    &#8226; <strong>360 hours is the FAANG standard.</strong> Top engineers at Google/Meta/Amazon typically spend 300&#8211;500h preparing for Senior (L5/E5/SDE-3) interviews. This plan is calibrated to that level.<br>
    &#8226; <strong>120+ LeetCode problems</strong> across 12 patterns: Arrays, Strings, Trees, Graphs, DP, Backtracking, Sliding Window, Two Pointers, Stack/Queue, Heap, Trie, Union-Find.<br>
    &#8226; <strong>8 system design mocks</strong> covering: Search, Docs, News Feed, Figma, Spotify, Twitter, YouTube, Instagram. You should be able to design ANY frontend system.<br>
    &#8226; <strong>10+ machine coding components</strong> from scratch: autocomplete, Kanban, data table, calendar, comment thread, spreadsheet, file explorer, carousel, notification system, and speed builds.<br>
    &#8226; <strong>15 STAR stories</strong> covering: Amazon LPs, Google Googliness, Meta values, general SDE-3 leadership. 40% of senior rejections are behavioral &#8212; DO NOT skip this.<br>
    &#8226; <strong>3 Angular projects:</strong> Dashboard, E-Commerce, Real-Time Chat. Each with tests, performance tuning, and a11y audits.<br>
    &#8226; <strong>4 full mock interviews:</strong> Google-style, Meta-style, Amazon-style, and one general. If you can pass these, you can pass the real thing.<br>
    &#8226; <strong>If you have only 60 days:</strong> Do Phases 1&#8211;5, then pick 10 days from Phases 6&#8211;9 based on your weaknesses, then do Phase 12.<br>
    &#8226; <strong>If you have only 30 days:</strong> Do Days 1&#8211;7, 13&#8211;15, 21&#8211;24, 29&#8211;31, 37&#8211;42, 63&#8211;65, 69&#8211;71, 87&#8211;90.<br>
    &#8226; <strong>Record every mock interview.</strong> Watch your recordings. Fix filler words ("um," "like"), long pauses, and vague answers. This single habit can move you from "borderline" to "strong hire."
  </div>
</section>
'''

# ── Assemble the full study path ──
STUDY_PATH = SP_HEADER + PHASE_1 + PHASE_2 + PHASE_3 + PHASE_4 + PHASE_5 + PHASE_6 + PHASE_7 + PHASE_8 + PHASE_9 + PHASE_10 + PHASE_11 + PHASE_12 + SP_FOOTER
