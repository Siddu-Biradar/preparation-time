#!/usr/bin/env python3
"""Restructure the performance guide:
1. Merge theory from sections 29-35 into the relevant earlier sections
2. Distribute video links to relevant sections
3. Remove the standalone theory appendix sections 29-35
"""
import re

INPUT  = "angular-frontend-performance-guide.html"
OUTPUT = INPUT  # overwrite

with open(INPUT, "r", encoding="utf-8") as f:
    html = f.read()

# ── Video link blocks to inject ──────────────────────────────────────────────

VIDEOS_ANGULAR = """
      <h4>Recommended videos for this section</h4>
      <ul class="small">
        <li><a href="https://www.youtube.com/watch?v=G5O4hP1pk7M">Angular Performance Optimization Strategy</a></li>
        <li><a href="https://www.youtube.com/playlist?list=PL4cSPhAvl8xXN4A5hxg7H5QbzaKUT1oiz">Angular Performance Optimization playlist</a></li>
        <li><a href="https://angular.dev/best-practices/runtime-performance">Angular runtime performance official guide</a></li>
        <li><a href="https://www.youtube.com/watch?v=64TMz93YMq8">Boost Angular Performance Top Optimization Techniques</a></li>
        <li><a href="https://www.youtube.com/watch?v=MB1E_vvhS78">Angular Performance Optimization Best Practices</a></li>
      </ul>
"""

VIDEOS_ANGULAR_DEFER = """
      <h4>Recommended videos for this section</h4>
      <ul class="small">
        <li><a href="https://angular.dev/guide/templates/defer">Angular @defer official guide</a></li>
        <li><a href="https://www.youtube.com/playlist?list=PL4cSPhAvl8xXN4A5hxg7H5QbzaKUT1oiz">Angular Performance Optimization playlist</a></li>
      </ul>
"""

VIDEOS_ANGULAR_PROFILING = """
      <h4>Recommended videos for this section</h4>
      <ul class="small">
        <li><a href="https://www.youtube.com/watch?v=FjyX_hkscII">Official Angular video guide for profiling with Chrome DevTools</a></li>
        <li><a href="https://angular.dev/best-practices/runtime-performance">Angular runtime performance official guide</a></li>
      </ul>
"""

VIDEOS_CWV = """
      <h4>Recommended videos for this section</h4>
      <ul class="small">
        <li><a href="https://www.youtube.com/watch?v=PTNoWeFuWv4">Core Web Vitals Workshop</a></li>
        <li><a href="https://www.youtube.com/watch?v=qGvHcWQsbOI">Core Web Vitals: What Google actually measures about your website</a></li>
        <li><a href="https://www.youtube.com/playlist?list=PL0OjOPrubarbcYX4DX4cwQ8x05LQoMrIh">Core Web Vitals playlist</a></li>
        <li><a href="https://web.dev/explore/learn-core-web-vitals">web.dev Learn Core Web Vitals</a></li>
        <li><a href="https://www.youtube.com/watch?v=bEUkN5mxOw4">Core Web Vitals full course in Hindi</a></li>
        <li><a href="https://www.youtube.com/watch?v=MgbqpQeCG8g">What is Core Web Vitals? Tutorial in-depth [Hindi]</a></li>
      </ul>
"""

VIDEOS_GENERAL_FRONTEND = """
      <h4>Recommended videos for this section</h4>
      <ul class="small">
        <li><a href="https://www.youtube.com/playlist?list=PLAwxTw4SYaPmKmNX-INgcxQWf30KuWa_A">Web Performance Optimization playlist</a></li>
        <li><a href="https://www.youtube.com/watch?v=nRrehoJxYUE">Web Performance Optimization matlab kya hota hai? [Hindi]</a></li>
        <li><a href="https://www.youtube.com/watch?v=RvbJh-wBxwA">JavaScript Performance Optimization in JS [Hindi]</a></li>
        <li><a href="https://www.youtube.com/watch?v=QUdqKFxJnfs">JavaScript Performance Optimization: Techniques for Faster Web Apps [Hindi]</a></li>
      </ul>
"""

VIDEOS_ANGULAR_SIGNALS_HINDI = """
      <h4>Recommended videos for this section</h4>
      <ul class="small">
        <li><a href="https://www.youtube.com/watch?v=zcZFltJ4bSA">Angular Tutorial in Hindi: Computed Signals</a></li>
        <li><a href="https://www.youtube.com/watch?v=G5O4hP1pk7M">Angular Performance Optimization Strategy</a></li>
      </ul>
"""

# ── Theory blocks to inject into sections that don't have them yet ──────────

THEORY_SEC6 = """
      <h3>Theory behind these examples</h3>
      <p>Every concrete code example in this section represents a deeper performance principle. Moving methods out of templates avoids repeated computation in hot paths. Using OnPush with immutable updates makes the framework's traversal contract stricter and cheaper. Cancelling stale requests with <code>switchMap</code> prevents wasted async work and lifecycle leaks. Deferring UI with <code>@defer</code> separates page importance from page membership. Virtualizing lists reduces the rendering surface area. Using workers moves CPU-heavy work away from the interaction-critical main thread.</p>
      <p>Theory lesson: every optimization should map to a general principle you can explain in your own words, not just code syntax you memorized. If you can articulate <strong>why</strong> an example works, you can apply the same thinking to new situations in interviews.</p>
"""

THEORY_SEC7 = """
      <h3>Theory behind general frontend examples</h3>
      <p>These examples illustrate core browser performance principles. Debouncing reduces frequency of expensive operations. Reserving image dimensions prevents the browser from recalculating layout after late media loads. Lazy loading non-critical images reduces initial bandwidth and rendering work. Avoiding layout thrashing prevents forced synchronous layout flushes that break the browser's batching efficiency. Preconnecting saves connection setup time for critical origins. Facade patterns defer heavy embed loading until the user actually needs them.</p>
      <p><strong>Layout thrashing theory:</strong> the browser prefers to batch rendering work. If your code reads layout information (like element size), then writes to the DOM, then reads again, the browser may be forced to flush pending layout work synchronously. The rule is: <strong>batch reads together, batch writes together</strong>.</p>
"""

THEORY_SEC9 = """
      <h3>Theory: why these mistakes matter</h3>
      <p>Each mistake on this list maps to a core performance principle. Calling heavy functions in templates means repeated work in Angular's hot path. Default change detection everywhere means Angular traverses more of the tree than necessary. Untracked lists cause DOM churn. Leaked subscriptions cause memory growth and stale state. Eager loading means users pay for features they haven't requested. Understanding the <strong>why</strong> behind each mistake turns a checklist into a diagnostic skill.</p>
"""

THEORY_SEC10 = """
      <h3>Theory: common root causes</h3>
      <p>Most general frontend mistakes share a root cause: treating performance as an afterthought rather than a constraint. Optimizing only Lighthouse scores ignores real user flows. Loading too many fonts wastes bandwidth and delays rendering. Shipping large bundles for simple pages violates the principle of shipping only what's needed. Ignoring CLS means ignoring user trust. Keeping inactive DOM nodes wastes memory and increases rendering cost. Third-party scripts are performance debt with uncertain costs. Theory-wise, each mistake is a violation of one of the three core laws: ship less, request less, render less.</p>
"""

THEORY_SEC11 = """
      <h3>Theory: performance as a lifecycle practice</h3>
      <p>This checklist reflects a key theory: performance is not a one-time fix but a lifecycle practice. Planning sets constraints. Development builds within those constraints. Pre-release verifies them. Release enables observability. Post-release closes the feedback loop. Without this cycle, performance work is fragile — gains made during development can silently erode after release.</p>
"""

THEORY_SEC12 = """
      <h3>Theory: what interviewers are really testing</h3>
      <p>Interview questions about performance are rarely testing whether you memorized definitions. They test whether you can <strong>connect user symptoms to engineering layers</strong>, choose the right measurement tool, propose an optimization with tradeoffs, and explain how you'd prove improvement. That is why this list emphasizes "explain" and "diagnose" rather than "list" or "define."</p>
"""

THEORY_SEC13 = """
      <h3>Theory: skill progression</h3>
      <p>Performance expertise follows a natural progression: understand what the browser does (Level 1), control what your app does within that browser (Level 2), and design systems that stay fast under real-world pressure (Level 3). Each level builds on the previous one. Skipping fundamentals leads to superstitious optimization — applying tricks without understanding causality.</p>
"""

THEORY_SEC17 = """
      <h3>Theory: end-to-end model</h3>
      <p>Architecture determines where cost can accumulate. A strong engineer is not just someone who knows each performance area individually — it is someone who can connect them. Example: if a user says "the dashboard is visible fast but still unusable for a second," that could mean SSR improved LCP, but hydration, bundle execution, or deferred widget boot is still dominating INP. That is an end-to-end explanation that separates a strong answer from a surface-level one.</p>
      <p>The key theory is that performance problems are rarely isolated to one layer. They cascade: slow servers produce late HTML, late HTML delays resource discovery, late resources increase boot time, heavy boot blocks interaction. Understanding the cascade is what makes an answer senior-level.</p>
"""

THEORY_SEC18 = """
      <h3>Theory deep dive: how Angular mechanisms actually work</h3>

      <h4>How change detection traversal works</h4>
      <p>At the theory level, Angular change detection is a structured tree walk over component views and bindings. Angular stores metadata about components and template instructions, then re-evaluates bindings to check whether visible output should change. For a simple binding like <code>{{ user.name }}</code>, Angular reads the current value during a check cycle and compares it with what it previously rendered. For a large tree, the cost comes from the total number of bindings evaluated and how expensive each evaluation is.</p>
      <p><strong>Why OnPush helps at the mechanism level:</strong> OnPush allows Angular to skip checking a subtree unless there is a reason to believe something changed — a new input reference, an event inside the subtree, or an explicit <code>markForCheck()</code> call. A new reference is a strong signal; unchanged references allow Angular to skip expensive reevaluation of that branch entirely.</p>
      <p><strong>What markForCheck() means:</strong> it does not mutate data. It changes Angular's scheduling decision by telling the framework that a previously skippable subtree must be reconsidered in the next detection run.</p>

      <h4>How Zone.js causes change detection to run</h4>
      <p>Zone.js monkey-patches async browser APIs so Angular is notified when asynchronous work completes. When a patched async task finishes, Angular gets a chance to run change detection because the framework assumes state may have changed. Macrotasks (setTimeout, events, network callbacks) and microtasks (resolved promises) both trigger this.</p>
      <p>If many patched callbacks fire frequently, Angular may keep re-entering change detection even when the UI hasn't meaningfully changed. That is zone pollution. In zoneless mode, Angular no longer gets automatic notifications — developers need more explicit reactive triggers and cleaner state boundaries. The reward is better control and often less runtime noise.</p>

      <h4>How signals track dependencies</h4>
      <p>Signals build a dependency graph. When one signal is read inside a computed value or reactive consumer, Angular records that dependency. Later, when the source signal changes, only dependent computations need updating. This is more precise than broad tree-based checking because it is data-centric instead of tree-centric.</p>
      <p>However, if too many computed layers depend on one another, the reactive graph can become complex. That complexity is the signal-world version of broad update complexity.</p>

      <h4>Template compilation and why some bindings cost more</h4>
      <p>Different template constructs imply different runtime costs:</p>
      <ul>
        <li><strong>Interpolation:</strong> generally cheap — reads a value and updates text if needed.</li>
        <li><strong>Property binding:</strong> may trigger DOM property updates when values differ.</li>
        <li><strong>Event binding:</strong> creates event listener paths with interaction cost when fired.</li>
        <li><strong>Structural control flow:</strong> can create, destroy, or skip blocks of DOM and embedded views.</li>
        <li><strong>Method calls:</strong> risky because Angular executes them repeatedly during checks and cannot assume they are pure.</li>
      </ul>
"""

THEORY_SEC19 = """
      <h3>Theory deep dive: render-blocking and priority</h3>
      <p>Not all critical resources are critical for the same reason:</p>
      <ul>
        <li><strong>Render-blocking:</strong> resources the browser needs before safe rendering (usually CSS). A stylesheet discovered early can still delay first render if the browser must wait for it.</li>
        <li><strong>Parse-blocking:</strong> resources that interrupt HTML parsing and delay discovery of later resources. A script without <code>defer</code> or <code>async</code> pauses HTML parsing.</li>
        <li><strong>Priority-sensitive:</strong> resources that are not strictly blocking but must arrive early enough to avoid delaying main content.</li>
      </ul>
      <p>Fonts are a good example of conditional criticality — they may not fully block rendering, but poor font strategy can degrade LCP, visual stability, and perceived polish.</p>
      <p><code>defer</code> delays script execution until HTML parsing is complete. <code>async</code> allows earlier independent execution but can change ordering assumptions. This is why script placement, attributes, and stylesheet strategy are so important in the critical rendering path.</p>
"""

THEORY_SEC20 = """
      <h3>Theory deep dive: layout thrashing and long tasks</h3>

      <h4>Why layout thrashing happens</h4>
      <p>The browser prefers to batch rendering work. If your code reads layout information (element size or position), then writes to the DOM, then reads again, the browser may be forced to flush pending layout work synchronously to answer the next read correctly. Each forced flush reduces batching efficiency and increases task cost. The rule is: <strong>batch reads together, batch writes together</strong>.</p>

      <h4>Long tasks and their relation to INP</h4>
      <p>A long task is work on the main thread that runs long enough to noticeably delay responsiveness (commonly referenced as &gt;50ms). If the main thread is occupied too long, user interactions wait in the queue. INP and long tasks are related but not identical:</p>
      <ul>
        <li>A long task can delay when an interaction handler even starts.</li>
        <li>The interaction handler itself can be expensive.</li>
        <li>Rendering work after the handler can delay the next visible paint.</li>
      </ul>
      <p>If INP is bad and the handler is short, the missing time may come from previously queued work or from post-handler rendering cost. A single long task can damage INP even if total page JavaScript time seems reasonable — because interactions care about the worst blocking near the event, not total work done overall.</p>

      <h4>CSSOM, selector matching, and style cost</h4>
      <p>The browser builds a CSSOM — a structured representation of CSS rules — then matches those rules against DOM elements during style calculation. Large stylesheets and repeated invalidation over large DOM regions can create noticeable cost. Selector performance matters less than many older myths suggest, but broad descendant matching and large invalidation scopes can increase style work. In practice, oversized CSS and large DOM surfaces are usually bigger problems than tiny selector micro-optimizations.</p>
"""

THEORY_SEC21 = """
      <h3>Theory: debugging as causality reading</h3>
      <p>A performance trace is a time-structured story. You use it to ask: what happened first, what blocked what, and where did time go? Theoretical skill in profiling is <strong>causality reading</strong>, not simply looking at colored bars. Each debugging path in this section follows the same meta-pattern: observe the symptom, attach a metric, isolate the layer, find the root cause, fix it, and verify the result.</p>
"""

THEORY_SEC22_23 = """
      <h3>Theory: what scenario questions really test</h3>
      <p>Interview scenarios are rarely testing whether you know one trick. They test whether you can <strong>structure uncertainty</strong>. The expected pattern is: (1) clarify the symptom, (2) attach the right metric, (3) identify the likely bottleneck layer, (4) name the tools and evidence you would use, (5) propose optimizations with tradeoffs, (6) explain how you would prove improvement. Random lists of tips are weaker than this reasoning framework.</p>
"""

THEORY_SEC24_25 = """
      <h3>Theory: tradeoff engineering</h3>
      <p>Decision tables exist because performance engineering is tradeoff engineering. There is rarely one universally correct optimization — there is only a better choice under a given workload, user context, and business goal. Examples:</p>
      <ul>
        <li>SSR may improve perceived speed but worsen server complexity.</li>
        <li>Debouncing may reduce CPU but worsen immediacy.</li>
        <li>Heavy caching may improve repeat visits but create stale-data risk.</li>
        <li>Virtualization may reduce DOM cost but complicate UI behavior.</li>
      </ul>
      <p>A strong interview answer always includes both sides of the tradeoff.</p>
"""

THEORY_SEC26 = """
      <h3>Theory: confidence through application</h3>
      <p>Confidence on theory does not come from rereading definitions. It comes from repeatedly mapping the same concepts across different situations. The confidence loop is: (1) learn the theory, (2) apply it to a concrete example, (3) measure the result, (4) explain the tradeoff in plain language, (5) repeat until the explanation feels natural. If you can explain the theory without looking at the page, you are interview-ready on that topic.</p>
"""

THEORY_SEC27 = """
      <h3>Theory: hydration reconciliation at the mechanism level</h3>
      <p>During hydration, the client attempts to attach framework behavior to existing server-rendered DOM rather than replacing it. This requires the client and server to agree on what should be in the DOM. If the client's expectation differs, the framework must reconcile or report a mismatch. Hydration mismatches come from non-deterministic rendering: different timestamps, locale-dependent formatting, browser-only APIs, or inconsistent data between server and client.</p>
      <p>Incremental hydration exists to reduce the cost of making the whole page interactive at once. Instead of hydrating everything immediately, the app can prioritize higher-value interactive regions first.</p>
"""

THEORY_SEC28 = """
      <h3>Theory: performance as a team system</h3>
      <p>At senior level, interviewers may test whether you think in terms of team systems. Performance work is fragile unless it becomes part of engineering culture. That means budgets, dashboards, release comparison, dependency review, route ownership, and post-release monitoring. The theory is simple: <strong>you do not really control performance unless your team can detect and stop regressions continuously</strong>.</p>

      <h4>Final theory summary to carry into interviews</h4>
      <ul>
        <li><strong>Performance is user perception converted into measurable engineering behavior.</strong></li>
        <li><strong>Every slowdown belongs to some layer: network, server, JavaScript, framework, rendering, or memory.</strong></li>
        <li><strong>Angular performance is mostly about controlling update frequency, update scope, and shipped code.</strong></li>
        <li><strong>Frontend performance is mostly about critical-path discipline, main-thread discipline, and rendering discipline.</strong></li>
        <li><strong>Senior-level performance thinking always includes proof, tradeoffs, and regression prevention.</strong></li>
      </ul>
"""

THEORY_PARSE_COMPILE = """
      <h4>Parse, compile, and execute: why shipping less JavaScript matters</h4>
      <p>JavaScript cost has multiple phases: <strong>download</strong> (network transfer), <strong>parse</strong> (browser reads source and builds internal structures), <strong>compile</strong> (browser prepares executable representations), and <strong>execute</strong> (the code runs and may trigger more work). On slower devices, parse and compile time can be large enough to be user-visible. This is why a library is not only "20KB more download" — it also adds parse cost, execution cost, memory overhead, and garbage collection pressure.</p>
      <p>Tree shaking helps by removing unused exports, but it only works well when libraries are structured for it and imports are done carefully. Poor import patterns or side-effect-heavy libraries reduce tree shaking effectiveness.</p>
"""

THEORY_CSSOM_DEEP = """
      <h4>CSSOM: why CSS is part of the critical rendering path</h4>
      <p>The browser builds a CSSOM alongside the DOM. The CSSOM is needed because the browser must know which styles apply before computing layout and paint. CSS can block useful rendering not because the file is large in bytes alone, but because visual correctness depends on it. Large stylesheets, many rule matches, and broad invalidation can all increase CSSOM-related work. Critical CSS delivery, stylesheet size, and style recalculation scope directly affect LCP and visual stability.</p>
"""

THEORY_HYDRATION_DEEP = """
      <h4>What hydration really does at the mechanism level</h4>
      <p>Hydration begins with server-rendered HTML already visible. The client-side runtime attaches interactive behavior, component state, and framework ownership to that HTML, trying to reuse existing DOM instead of rebuilding it. Hydration still costs performance because the browser must: download client JavaScript, parse and execute framework code, recreate component instances, attach listeners and reactive state, and verify DOM consistency.</p>
      <p>If server-rendered output and client-rendered expectation differ, hydration mismatches happen. Common reasons: random values, time-dependent rendering, locale-dependent formatting, browser-only APIs, or inconsistent data. Hydration therefore requires <strong>deterministic rendering assumptions</strong> more strongly than plain CSR.</p>
"""

# ── Helper: insert content before the closing </section> of a section ────────

def insert_before_next_section(text, section_heading, content):
    """Insert content right before the next <section> or </section> that follows after section_heading."""
    # Find the heading
    idx = text.find(section_heading)
    if idx == -1:
        print(f"WARNING: Could not find: {section_heading}")
        return text
    
    # Find the next section start or the end of the current section
    # Look for the next <h2> which marks the start of a new section
    # We need to insert just before the </section> that precedes the next <h2>
    after = text[idx:]
    # Find the next h2 after this one
    next_h2 = re.search(r'\n\s*</section>\s*\n', after[len(section_heading):])
    if next_h2:
        insert_pos = idx + len(section_heading) + next_h2.start()
        return text[:insert_pos] + "\n" + content + "\n" + text[insert_pos:]
    else:
        print(f"WARNING: Could not find section end after: {section_heading}")
        return text

# ── Apply theory insertions ──────────────────────────────────────────────────

# Section 6: Hands-on Angular Examples
html = insert_before_next_section(html, "<h2>6. Hands-on Angular Examples</h2>", THEORY_SEC6 + VIDEOS_ANGULAR)

# Section 7: Hands-on General Frontend Examples
html = insert_before_next_section(html, "<h2>7. Hands-on General Frontend Examples</h2>", THEORY_SEC7 + VIDEOS_GENERAL_FRONTEND)

# Section 9: Common Angular Performance Mistakes
html = insert_before_next_section(html, "<h2>9. Common Angular Performance Mistakes</h2>", THEORY_SEC9)

# Section 10: Common General Frontend Performance Mistakes
html = insert_before_next_section(html, "<h2>10. Common General Frontend Performance Mistakes</h2>", THEORY_SEC10)

# Section 11: E2E Checklist
html = insert_before_next_section(html, "<h2>11. End-to-End Performance Checklist for Real Projects</h2>", THEORY_SEC11)

# Section 12: Interview Readiness
html = insert_before_next_section(html, "<h2>12. Interview and Career Readiness", THEORY_SEC12)

# Section 13: Study Roadmap
html = insert_before_next_section(html, "<h2>13. Study Roadmap", THEORY_SEC13)

# Section 16: Final Practical Guidance (no theory needed, already has guidance)

# Section 17: E2E Architecture View
html = insert_before_next_section(html, "<h2>17. End-to-End Performance Architecture View</h2>", THEORY_SEC17)

# Section 18: Angular Internals - add deep mechanism theory
html = insert_before_next_section(html, "<h2>18. Angular Internals You Should Understand</h2>", THEORY_SEC18 + VIDEOS_ANGULAR_SIGNALS_HINDI)

# Section 19: Network Deep Dive - add render-blocking theory
html = insert_before_next_section(html, "<h2>19. Network, Caching, and Delivery Deep Dive</h2>", THEORY_SEC19)

# Section 20: Rendering Deep Dive - add layout thrashing and long task theory
html = insert_before_next_section(html, "<h2>20. Rendering and Main Thread Deep Dive</h2>", THEORY_SEC20)

# Section 21: Debugging Playbook
html = insert_before_next_section(html, "<h2>21. End-to-End Debugging Playbook</h2>", THEORY_SEC21)

# Section 22: Scenario Questions
html = insert_before_next_section(html, "<h2>22. Real-World Scenario Questions", THEORY_SEC22_23)

# Section 24: Decision Tables (covers 24 + 25)
html = insert_before_next_section(html, "<h2>24. Advanced Decision Tables", THEORY_SEC24_25)

# Section 26: Practice Exercises
html = insert_before_next_section(html, "<h2>26. Practice Exercises", THEORY_SEC26)

# Section 27: Senior Interviewers
html = insert_before_next_section(html, "<h2>27. What Senior Interviewers", THEORY_SEC27)

# Section 28: Production and Measurement Depth
html = insert_before_next_section(html, "<h2>28. Production and Measurement Depth</h2>", THEORY_SEC28)

# ── Add video links to sections that already have theory (1-5, 8) ────────────

# Section 3: Metrics → Core Web Vitals videos (insert before </section>)
html = insert_before_next_section(html, "<h2>3. Important Metrics", VIDEOS_CWV)

# Section 4: General Frontend → General frontend videos
html = insert_before_next_section(html, "<h2>4. General Frontend Performance", VIDEOS_GENERAL_FRONTEND.replace("Recommended videos for this section", "Recommended videos for general frontend performance"))

# Section 4.2: add parse/compile/execute deep theory
# Find existing 4.2 section and add deep theory after it
idx_42 = html.find("<h3>4.2 JavaScript optimization</h3>")
if idx_42 != -1:
    # Find the end of the JS optimization bullet list
    next_h3 = html.find("<h3>4.3 Rendering optimization</h3>", idx_42)
    if next_h3 != -1:
        html = html[:next_h3] + THEORY_PARSE_COMPILE + "\n      " + html[next_h3:]

# Section 4.6: add CSSOM deep theory
idx_46 = html.find("<h3>4.6 CSS optimization</h3>")
if idx_46 != -1:
    next_h3 = html.find("<h3>4.7 Build toolchain", idx_46)
    if next_h3 != -1:
        html = html[:next_h3] + THEORY_CSSOM_DEEP + "\n      " + html[next_h3:]

# Section 5: Angular Performance → Angular videos
html = insert_before_next_section(html, "<h2>5. Angular Performance Optimization From Basic to Advanced</h2>", VIDEOS_ANGULAR.replace("Recommended videos for this section", "Recommended videos for Angular performance"))

# Section 5.5: add @defer video link
idx_55 = html.find("<h3>5.5 Bundle and loading performance</h3>")
if idx_55 != -1:
    next_h3 = html.find("<h3>5.6 RxJS and async", idx_55)
    if next_h3 != -1:
        html = html[:next_h3] + VIDEOS_ANGULAR_DEFER + "\n      " + html[next_h3:]

# Section 5.8.1: add hydration mechanism theory
idx_581 = html.find("<h3>5.8.1 When SSR, hydration, or hybrid rendering are worth it</h3>")
if idx_581 != -1:
    # Find end of section 5 - look for section 6
    next_sec = html.find("<h2>6. Hands-on Angular Examples</h2>", idx_581)
    if next_sec != -1:
        # Insert before the </section> that precedes section 6
        insert_at = html.rfind("</section>", idx_581, next_sec)
        if insert_at != -1:
            html = html[:insert_at] + THEORY_HYDRATION_DEEP + "\n    " + html[insert_at:]

# Section 8: Tooling → Profiling video
html = insert_before_next_section(html, "<h2>8. Performance Tooling You Should Know</h2>", VIDEOS_ANGULAR_PROFILING)

# ── Remove sections 29-35 (standalone theory appendix) ───────────────────────

# Find the start of section 29
sec29_marker = "<h2>29. Section-wise Theory Deep Dive: Foundations</h2>"
idx_sec29 = html.find(sec29_marker)
if idx_sec29 != -1:
    # Find the <section that contains it - go backwards
    section_start = html.rfind("<section", 0, idx_sec29)
    if section_start == -1:
        section_start = html.rfind("<section>", 0, idx_sec29)
    
    # Find the end: </main></body></html>
    end_marker = "  </main>\n</body>"
    idx_end = html.find(end_marker)
    if idx_end != -1:
        html = html[:section_start] + "\n    " + html[idx_end:]
    else:
        print("WARNING: Could not find </main></body> end marker")
else:
    print("WARNING: Could not find section 29 marker")

# ── Update section 14 to note videos are now inline ─────────────────────────

old_14_intro = '<p class="small">These links were selected to cover Angular performance, general web performance, and India-friendly or Hindi options. Video titles can evolve over time, but the links are direct and topic-focused.</p>'
new_14_intro = '<p class="small">These links are also placed inline in their relevant sections throughout the guide. This consolidated list is provided as a quick reference. Video titles can evolve over time, but the links are direct and topic-focused.</p>'
html = html.replace(old_14_intro, new_14_intro)

# ── Write output ─────────────────────────────────────────────────────────────

with open(OUTPUT, "w", encoding="utf-8") as f:
    f.write(html)

print(f"Done. Wrote restructured guide to {OUTPUT}")
print(f"Total size: {len(html)} characters")
