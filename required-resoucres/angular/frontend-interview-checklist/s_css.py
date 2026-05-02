SECTIONS = r"""

<!-- ═══════════════════════════════════════════════════════════════════
     CSS — 15 SUB-SECTIONS
     ═══════════════════════════════════════════════════════════════════ -->

<h2 id="css-selectors" class="section-break">25. CSS Selectors</h2>
<p class="small"><strong>Checklist:</strong> Type/class/ID selectors · attribute selectors · pseudo-classes (:hover, :focus, :nth-child, :nth-of-type, :is, :where, :has, :not) · pseudo-elements (::before, ::after, ::first-letter, ::first-line) · combinators · specificity calculation</p>

<h3>Specificity Calculation</h3>
<table>
<thead><tr><th>Category</th><th>Weight</th><th>Examples</th></tr></thead>
<tbody>
<tr><td>Inline styles</td><td>1,0,0,0</td><td><code>style="..."</code></td></tr>
<tr><td>ID selectors</td><td>0,1,0,0</td><td><code>#header</code></td></tr>
<tr><td>Classes, attributes, pseudo-classes</td><td>0,0,1,0</td><td><code>.card</code>, <code>[type="text"]</code>, <code>:hover</code></td></tr>
<tr><td>Elements, pseudo-elements</td><td>0,0,0,1</td><td><code>div</code>, <code>::before</code></td></tr>
<tr><td><code>:where()</code></td><td>0,0,0,0</td><td>Always zero — great for base styles</td></tr>
<tr><td><code>!important</code></td><td>Overrides everything</td><td>Avoid in application code</td></tr>
</tbody>
</table>

<pre>/* :has() — the "parent selector" (game-changer) */
.card:has(img) { grid-template-rows: 200px auto; }
.form-group:has(:invalid) { border-color: red; }
a:has(> img) { border: none; } /* link containing image */

/* :is() — grouping without repeating */
:is(h1, h2, h3, h4):hover { color: var(--accent); }
/* Specificity = highest argument: :is(#id, .class) has ID specificity */

/* :where() — like :is() but ZERO specificity */
:where(.btn) { padding: 8px 16px; } /* easily overridable */

/* :not() */
.list-item:not(:last-child) { border-bottom: 1px solid #ddd; }
input:not([type="submit"]):not([type="button"]) { border: 1px solid #ccc; }

/* :nth-child patterns */
li:nth-child(odd) { background: #f5f5f5; }
li:nth-child(3n) { font-weight: bold; } /* every 3rd */
li:nth-child(n+4) { color: gray; }       /* 4th and beyond */
li:nth-last-child(-n+3) { color: red; }   /* last 3 items */

/* Attribute selectors */
a[href^="https"] { color: green; }  /* starts with */
a[href$=".pdf"] { color: red; }     /* ends with */
a[href*="example"] { color: blue; } /* contains */
input[type="text" i] { }            /* case-insensitive */

/* Combinators */
div p { }     /* descendant — any depth */
div > p { }   /* child — direct children only */
h2 + p { }    /* adjacent sibling — immediately after */
h2 ~ p { }    /* general sibling — all after */</pre>

<div class="interview-q">
<h4>🎯 Interview Questions — CSS Selectors</h4>
<p><strong>Q: Calculate the specificity: <code>div#header .nav li.active a:hover</code></strong></p>
<p><strong>A:</strong> ID(#header)=1, classes(.nav, .active, :hover)=3, elements(div, li, a)=3 → <code>0,1,3,3</code>.</p>
</div>

<h2 id="css-box-model" class="section-break">26. CSS Box Model</h2>
<p class="small"><strong>Checklist:</strong> Content/padding/border/margin · box-sizing · margin collapse · negative margins</p>

<pre>/* box-sizing — the single most important CSS reset */
*, *::before, *::after {
  box-sizing: border-box; /* width includes padding + border */
}

/* Without border-box:
   width: 300px + padding: 20px×2 + border: 1px×2 = 342px actual width
   With border-box:
   width: 300px total, content shrinks to accommodate padding + border */

/* Margin collapse — vertical margins of adjacent blocks collapse */
/* The LARGER margin wins, they don't add up */
.box1 { margin-bottom: 30px; }
.box2 { margin-top: 20px; }
/* Gap between them: 30px (not 50px!) */

/* Margin collapse does NOT happen with: */
/* ✗ flexbox/grid items */
/* ✗ floated elements */
/* ✗ absolute/fixed positioned elements */  
/* ✗ elements with overflow other than visible */
/* ✗ inline-block elements */

/* Negative margins — pulling elements */
.overlap { margin-top: -20px; }    /* pulls element UP */
.bleed { margin-left: -16px; margin-right: -16px; } /* full-width in padded parent */</pre>

<h2 id="css-layout" class="section-break">27. CSS Layout</h2>
<p class="small"><strong>Checklist:</strong> display (block/inline/inline-block/none) · position (static/relative/absolute/fixed/sticky) · float &amp; clear · vertical alignment · z-index &amp; stacking context</p>

<pre>/* Display values */
.block { display: block; }         /* full width, stacks vertically */
.inline { display: inline; }       /* flows with text, no width/height */
.inline-block { display: inline-block; } /* inline + can set width/height */
.none { display: none; }           /* removed from layout entirely */
.contents { display: contents; }   /* box disappears, children remain */

/* Position */
.relative { position: relative; top: 10px; } /* offset from normal position, keeps space */
.absolute { position: absolute; top: 0; right: 0; } /* relative to nearest positioned ancestor */
.fixed { position: fixed; top: 0; } /* relative to viewport, stays on scroll */
.sticky { position: sticky; top: 0; } /* relative → fixed when scrolled past offset */

/* Stacking context — z-index only works within a context */
/* A new stacking context is created by: */
/* position: relative/absolute/fixed + z-index */
/* opacity < 1, transform, filter, will-change */
/* isolation: isolate */
.parent { position: relative; z-index: 1; } /* creates stacking context */
.child { position: absolute; z-index: 999; } /* only counts within parent */

/* Center anything — modern approaches */
.center-grid { display: grid; place-items: center; }
.center-flex { display: flex; justify-content: center; align-items: center; }
.center-abs {
  position: absolute; top: 50%; left: 50%;
  transform: translate(-50%, -50%);
}
.center-margin { margin-inline: auto; } /* horizontal centering for block elements */</pre>

<h2 id="css-flexbox" class="section-break">28. CSS Flexbox</h2>
<p class="small"><strong>Checklist:</strong> flex-direction · flex-wrap · justify-content · align-items · align-content · flex-grow/shrink/basis · flex shorthand · align-self · order · gap</p>

<pre>/* Flexbox cheat sheet */
.container {
  display: flex;
  flex-direction: row;          /* row | row-reverse | column | column-reverse */
  flex-wrap: wrap;               /* nowrap | wrap | wrap-reverse */
  justify-content: space-between; /* flex-start|end | center | space-between|around|evenly */
  align-items: center;           /* stretch | flex-start|end | center | baseline */
  gap: 16px;                     /* row-gap column-gap */
}

.item {
  flex: 1 0 200px;  /* grow:1 shrink:0 basis:200px */
  /* flex-grow: how much extra space to take (0 = don't grow) */
  /* flex-shrink: how much to shrink when space is tight (0 = don't shrink) */
  /* flex-basis: initial size before growing/shrinking (like width) */
  align-self: flex-end; /* override align-items for this item */
  order: -1;            /* move this item first (default order is 0) */
}

/* Common patterns */
/* Navbar: logo left, nav right */
.navbar { display: flex; justify-content: space-between; align-items: center; }

/* Card with footer pushed to bottom */
.card { display: flex; flex-direction: column; height: 100%; }
.card-body { flex: 1; }     /* takes remaining space */
.card-footer { margin-top: auto; } /* pushed to bottom */

/* Equal-width columns */
.cols { display: flex; gap: 16px; }
.cols > * { flex: 1; } /* each child gets equal space */

/* Wrap with minimum width */
.grid-flex { display: flex; flex-wrap: wrap; gap: 16px; }
.grid-flex > * { flex: 1 1 300px; } /* min 300px, grows to fill */</pre>

<h2 id="css-grid" class="section-break">29. CSS Grid</h2>
<p class="small"><strong>Checklist:</strong> grid-template-columns/rows · grid-template-areas · fr · repeat() · minmax() · auto-fill/fit · grid gap · grid item placement · implicit vs explicit grid · named grid lines · align/justify/place-items</p>

<pre>/* Responsive grid — no media queries needed */
.product-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 24px;
}
/* auto-fill: creates empty columns if space allows */
/* auto-fit: collapses empty columns, stretches existing items */

/* Dashboard layout with named areas */
.dashboard {
  display: grid;
  grid-template-areas:
    "header  header  header"
    "sidebar main    aside"
    "footer  footer  footer";
  grid-template-columns: 250px 1fr 200px;
  grid-template-rows: 60px 1fr 40px;
  min-height: 100vh;
  gap: 0;
}
.header  { grid-area: header; }
.sidebar { grid-area: sidebar; }
.main    { grid-area: main; }
.aside   { grid-area: aside; }
.footer  { grid-area: footer; }

/* Explicit item placement */
.hero {
  grid-column: 1 / -1;    /* span full width */
  grid-row: 1 / 3;        /* span 2 rows */
}
.featured {
  grid-column: span 2;    /* span 2 columns */
}

/* Alignment */
.grid {
  justify-items: center;  /* horizontal alignment of items within cells */
  align-items: center;    /* vertical alignment of items within cells */
  place-items: center;    /* shorthand for both */
  justify-content: space-between; /* horizontal alignment of grid tracks */
  align-content: center;          /* vertical alignment of grid tracks */
}

/* Subgrid (children inherit parent grid lines) */
.parent { display: grid; grid-template-columns: repeat(3, 1fr); }
.child  { display: grid; grid-template-columns: subgrid; grid-column: span 3; }</pre>

<div class="interview-q">
<h4>🎯 Interview Questions — Flexbox &amp; Grid</h4>
<p><strong>Q: When would you choose Flexbox over Grid?</strong></p>
<p><strong>A:</strong> <strong>Flexbox</strong> for one-dimensional layouts (row OR column): navbars, card footers, centering items, flexible wrapping. <strong>Grid</strong> for two-dimensional layouts (rows AND columns): page layouts, dashboards, galleries. They can be combined — Grid for the page layout, Flexbox inside each grid cell.</p>
</div>

<h2 id="css-responsive" class="section-break">30. Responsive Design</h2>
<p class="small"><strong>Checklist:</strong> Media queries · mobile-first vs desktop-first · breakpoints · fluid typography · container queries · clamp() · min/max · aspect-ratio</p>

<pre>/* Mobile-first approach — start with mobile, enhance for larger */
.card { padding: 12px; font-size: 14px; }

@media (min-width: 768px) {
  .card { padding: 20px; font-size: 16px; display: flex; }
}
@media (min-width: 1200px) {
  .card { padding: 32px; max-width: 1200px; margin: 0 auto; }
}

/* Fluid typography — no breakpoints needed */
h1 { font-size: clamp(1.5rem, 4vw + 0.5rem, 3.5rem); }
p  { font-size: clamp(0.9rem, 1.5vw + 0.5rem, 1.15rem); }
/* clamp(minimum, preferred, maximum) */

/* Container queries — responsive to PARENT, not viewport */
.card-wrapper { container-type: inline-size; container-name: card; }

@container card (min-width: 400px) {
  .card { display: flex; gap: 16px; }
  .card-image { width: 40%; }
}
@container card (max-width: 399px) {
  .card-image { width: 100%; }
}

/* Aspect ratio */
.video-container { aspect-ratio: 16 / 9; width: 100%; }
.avatar { aspect-ratio: 1; border-radius: 50%; object-fit: cover; }

/* min() and max() */
.container { width: min(90vw, 1200px); }    /* whichever is smaller */
.sidebar  { width: max(200px, 20vw); }       /* whichever is larger */</pre>

<h2 id="css-typography" class="section-break">31. CSS Typography</h2>
<p class="small"><strong>Checklist:</strong> font-family/size/weight · line-height · letter/word-spacing · text-align/decoration/transform · @font-face · font-display · WOFF/WOFF2 · system font stacks · variable fonts</p>

<pre>/* System font stack — fastest loading (no downloads) */
body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto,
               'Helvetica Neue', Arial, sans-serif;
  line-height: 1.5;         /* 1.5× font size — good readability */
  -webkit-font-smoothing: antialiased;
}

/* @font-face with font-display strategy */
@font-face {
  font-family: 'Inter';
  src: url('/fonts/inter-var.woff2') format('woff2');
  font-display: swap;       /* show fallback → swap when loaded */
  font-weight: 100 900;     /* variable font: all weights in one file */
  unicode-range: U+0000-00FF; /* subset: only latin characters */
}

/* font-display values:
   auto:     browser decides
   swap:     show fallback immediately, swap when ready (FOUT)
   block:    invisible text for short period, then show (FOIT)
   fallback: very short block, then fallback (swap if loads quickly)
   optional: browser may not swap at all (best for slow connections) */

/* Variable fonts — single file, infinite weights/widths */
.heading {
  font-family: 'Inter', sans-serif;
  font-weight: 750;          /* any value 100-900, not just 400/700 */
  font-variation-settings: 'wght' 750, 'slnt' -5;
}</pre>

<h2 id="css-colors" class="section-break">32. Colors &amp; Backgrounds</h2>
<p class="small"><strong>Checklist:</strong> hex/rgb/rgba/hsl/hsla · currentColor · gradients (linear/radial/conic) · background-size/position/attachment · multiple backgrounds · opacity vs rgba</p>

<pre>/* Color formats */
.box {
  color: #0f6b5f;                    /* hex */
  color: rgb(15, 107, 95);           /* rgb */
  color: rgba(15, 107, 95, 0.8);     /* rgb + alpha */
  color: hsl(170, 75%, 24%);         /* hue 0-360, saturation %, lightness % */
  color: hsla(170, 75%, 24%, 0.8);   /* hsl + alpha */
  color: oklch(50% 0.15 170);        /* modern: perceptually uniform */
}

/* currentColor — inherits the text color */
.btn {
  color: #0f6b5f;
  border: 2px solid currentColor;    /* border matches text color */
  box-shadow: 0 2px 0 currentColor;  /* shadow matches text color */
}
.btn:hover { color: #0a4f45; }       /* everything updates together! */

/* Gradients */
.hero { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }
.radial { background: radial-gradient(circle at top right, #fff, #eee); }
.conic { background: conic-gradient(red, yellow, green, blue, red); }

/* Multiple backgrounds — layered (first on top) */
.card {
  background:
    linear-gradient(rgba(0,0,0,0.3), rgba(0,0,0,0.7)),
    url('bg.jpg') center/cover no-repeat;
}

/* opacity vs rgba */
.overlay { opacity: 0.5; }                     /* affects ENTIRE element + children */
.overlay-bg { background: rgba(0, 0, 0, 0.5); } /* only background is transparent */</pre>

<h2 id="css-animations" class="section-break">33. Transforms &amp; Animations</h2>
<p class="small"><strong>Checklist:</strong> transform (translate/rotate/scale/skew) · transform-origin · 3D transforms · transitions · @keyframes · animation properties · will-change · GPU acceleration</p>

<pre>/* Performant animations — ONLY transform + opacity trigger GPU layer */
.card {
  transition: transform 0.2s ease-out, box-shadow 0.2s ease-out;
}
.card:hover {
  transform: translateY(-4px) scale(1.01);
  box-shadow: 0 12px 24px rgba(0,0,0,0.12);
}

/* Transition shorthand */
.btn {
  transition: all 0.2s ease;
  /* property | duration | timing-function | delay */
  /* timing: ease | linear | ease-in | ease-out | ease-in-out | cubic-bezier() */
}

/* @keyframes — complex multi-step animation */
@keyframes slideInUp {
  from {
    transform: translateY(30px);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}
.animate-in {
  animation: slideInUp 0.4s ease-out forwards;
  /* name | duration | timing | fill-mode */
  /* fill-mode: forwards = keeps final state */
}

/* Loading spinner */
@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}
.spinner {
  width: 24px; height: 24px;
  border: 3px solid #e0e0e0;
  border-top-color: var(--accent);
  border-radius: 50%;
  animation: spin 0.6s linear infinite;
}

/* GPU acceleration — will-change */
.animated-element {
  will-change: transform, opacity; /* hint: these will animate soon */
  /* WARNING: don't overuse — each element with will-change creates a GPU layer */
}

/* 3D transforms */
.flip-card {
  perspective: 1000px;
}
.flip-card-inner {
  transition: transform 0.6s;
  transform-style: preserve-3d;
}
.flip-card:hover .flip-card-inner {
  transform: rotateY(180deg);
}</pre>

<h2 id="css-variables" class="section-break">34. CSS Variables</h2>
<p class="small"><strong>Checklist:</strong> Custom properties declaration · var() function · scope &amp; inheritance · fallback values · runtime manipulation with JavaScript</p>

<pre>/* Declaration — scoped to the element and its descendants */
:root {
  --color-primary: #0f6b5f;
  --color-bg: #fffdf8;
  --radius: 8px;
  --spacing-sm: 8px;
  --spacing-md: 16px;
  --spacing-lg: 24px;
  --font-sans: 'Inter', system-ui, sans-serif;
}

/* Usage with fallback */
.btn {
  background: var(--color-primary);
  border-radius: var(--radius);
  padding: var(--spacing-sm) var(--spacing-md);
  font-family: var(--font-heading, var(--font-sans)); /* nested fallback */
}

/* Scoped overrides — theming */
[data-theme="dark"] {
  --color-primary: #8bf0cc;
  --color-bg: #1a1a2e;
}
/* All components using these variables automatically update! */

/* Component-level variables */
.card {
  --card-padding: 16px;
  padding: var(--card-padding);
}
.card.compact { --card-padding: 8px; } /* override for variant */

/* JS manipulation — dynamic theming */
document.documentElement.style.setProperty('--color-primary', '#e74c3c');
const value = getComputedStyle(document.documentElement)
  .getPropertyValue('--color-primary').trim();</pre>

<h2 id="css-modern" class="section-break">35. Modern CSS</h2>
<p class="small"><strong>Checklist:</strong> Subgrid · aspect-ratio · gap (flexbox/grid) · logical properties · scroll-snap · backdrop-filter · mix-blend-mode · filter · clip-path · shape-outside</p>

<pre>/* Logical properties — work with any writing direction (LTR/RTL) */
.card {
  margin-inline: auto;       /* replaces margin-left + margin-right */
  padding-block: 16px;        /* replaces padding-top + padding-bottom */
  border-inline-start: 4px solid var(--accent); /* left in LTR, right in RTL */
}

/* Scroll snap — carousel without JavaScript */
.carousel {
  display: flex;
  overflow-x: auto;
  scroll-snap-type: x mandatory;  /* snap required after scrolling */
  gap: 16px;
  scrollbar-width: none;
}
.carousel-item {
  scroll-snap-align: start;       /* snap to start of each item */
  flex: 0 0 80%;
}

/* backdrop-filter — frosted glass effect */
.modal-overlay {
  backdrop-filter: blur(12px) saturate(180%);
  background: rgba(0, 0, 0, 0.25);
}

/* clip-path — non-rectangular shapes */
.hero-section {
  clip-path: polygon(0 0, 100% 0, 100% 85%, 0 100%);
}
.circle-avatar {
  clip-path: circle(50%);
}

/* filter effects */
.grayscale { filter: grayscale(100%); }
.blur { filter: blur(4px); }
.image:hover { filter: brightness(1.1) contrast(1.05); }

/* :has() — style parent based on child state */
.form-group:has(input:focus) {
  border-color: var(--accent);
  box-shadow: 0 0 0 3px var(--accent-soft);
}</pre>

<h2 id="css-methodologies" class="section-break">36. CSS Methodologies</h2>
<p class="small"><strong>Checklist:</strong> BEM · SMACSS · OOCSS · Atomic CSS · CSS Modules · utility-first CSS</p>

<pre>/* BEM — Block__Element--Modifier */
.product-card {}                        /* Block */
.product-card__title {}                 /* Element */
.product-card__title--highlighted {}    /* Modifier */
.product-card__image {}                 /* Element */
.product-card--featured {}              /* Block modifier */

/* SCSS with BEM */
.product-card {
  border: 1px solid #ddd;
  
  &__title {
    font-size: 18px;
    &--highlighted { color: red; }
  }
  &__image { width: 100%; border-radius: 8px; }
  &--featured { border-color: gold; }
}

/* Utility-first (Tailwind-style) */
/* &lt;div class="flex items-center gap-4 p-4 rounded-lg bg-white shadow-md"&gt; */

/* CSS Modules — local scope (generated class names) */
/* styles.module.css */
.card { padding: 16px; }  /* → .card_a1b2c3 in output */
/* import styles from './styles.module.css'; */
/* &lt;div className={styles.card}&gt; */</pre>

<div class="interview-q">
<h4>🎯 Interview — CSS Methodologies</h4>
<p><strong>Q: What is BEM and why use it?</strong></p>
<p><strong>A:</strong> BEM (Block-Element-Modifier) is a naming convention: <code>.block__element--modifier</code>. It makes CSS predictable, reusable, and avoids specificity wars. Each component (block) is self-contained, elements are parts of the block, modifiers are variations. Flat specificity (one class per rule) makes overrides predictable.</p>
</div>

<h2 id="css-in-js" class="section-break">37. CSS-in-JS</h2>
<p class="small"><strong>Checklist:</strong> Styled Components · Emotion · CSS Modules · inline styles · trade-offs &amp; performance</p>

<pre>// Styled Components (React ecosystem — understand for comparisons)
const Button = styled.button`
  background: ${props => props.primary ? '#0f6b5f' : 'white'};
  color: ${props => props.primary ? 'white' : '#0f6b5f'};
  padding: 8px 16px;
  border-radius: 6px;
  &:hover { opacity: 0.9; }
`;

// Angular equivalent: component styles with ViewEncapsulation
@Component({
  styles: [`
    :host { display: block; }
    .btn { background: var(--color-primary); }
    .btn--primary { background: var(--accent); color: white; }
  `],
  encapsulation: ViewEncapsulation.Emulated // default — scoped styles
})
</pre>

<table>
<thead><tr><th>Approach</th><th>Pros</th><th>Cons</th></tr></thead>
<tbody>
<tr><td>CSS-in-JS</td><td>Scoped, dynamic theming, co-located</td><td>Runtime cost, bundle size, framework-specific</td></tr>
<tr><td>CSS Modules</td><td>Scoped, no runtime, works with any framework</td><td>No dynamic styles without classes</td></tr>
<tr><td>Utility CSS (Tailwind)</td><td>No naming, small bundle (purging), fast</td><td>Verbose HTML, learning curve</td></tr>
<tr><td>BEM + SCSS</td><td>No tooling needed, clear structure</td><td>Naming discipline required, global scope</td></tr>
</tbody>
</table>

<h2 id="css-preprocessors" class="section-break">38. CSS Preprocessors</h2>
<p class="small"><strong>Checklist:</strong> SASS/SCSS (variables, nesting, mixins, extends) · Less · PostCSS · Autoprefixer</p>

<pre>// SCSS — most widely used preprocessor
// Variables (legacy — prefer CSS custom properties)
$primary: #0f6b5f;
$spacing: 8px;

// Nesting
.card {
  padding: $spacing * 2;
  
  &:hover { box-shadow: 0 4px 12px rgba(0,0,0,0.1); }
  
  &__title { font-weight: bold; }
  
  @media (min-width: 768px) {
    display: flex;
  }
}

// Mixins — reusable style blocks
@mixin respond-to($breakpoint) {
  @if $breakpoint == 'tablet' { @media (min-width: 768px) { @content; } }
  @if $breakpoint == 'desktop' { @media (min-width: 1200px) { @content; } }
}
.card {
  padding: 12px;
  @include respond-to('tablet') { padding: 24px; }
}

// Extend — share styles (use sparingly)
%flex-center {
  display: flex;
  justify-content: center;
  align-items: center;
}
.modal { @extend %flex-center; }
.popup { @extend %flex-center; }

// PostCSS — CSS transformations via plugins
// Popular plugins: autoprefixer, postcss-preset-env, cssnano
// Angular CLI uses PostCSS under the hood</pre>

<h2 id="css-performance" class="section-break">39. CSS Performance</h2>
<p class="small"><strong>Checklist:</strong> Critical CSS · CSS containment · content-visibility · reducing reflows &amp; repaints · will-change · layer separation</p>

<pre>/* Critical CSS — inline above-fold styles for faster FCP */
&lt;head&gt;
  &lt;style&gt;
    /* ONLY styles needed for first viewport render */
    .header, .hero, .nav { ... }
  &lt;/style&gt;
  &lt;!-- Load full CSS asynchronously --&gt;
  &lt;link rel="stylesheet" href="full.css" media="print" onload="this.media='all'"&gt;
  &lt;noscript&gt;&lt;link rel="stylesheet" href="full.css"&gt;&lt;/noscript&gt;
&lt;/head&gt;

/* CSS containment — isolate subtree from rest of page */
.widget {
  contain: layout style paint; /* browser can optimize rendering of this subtree */
  /* layout: size doesn't affect parent */
  /* style: counters/quotes don't leak */
  /* paint: content doesn't render outside bounds */
}

/* content-visibility — skip rendering of off-screen content */
.section {
  content-visibility: auto;           /* render only when in/near viewport */
  contain-intrinsic-size: 0 500px;    /* estimated height for scrollbar */
}
/* Can save massive rendering time for long pages! */

/* Reducing reflows (layout recalculations) */
/* 🚫 Causes reflow: changing width/height, padding, margin, font-size, 
       adding/removing DOM nodes, reading offsetHeight/offsetWidth */
/* ✅ Cheap: transform, opacity, visibility, color, background-color */

/* Layer separation — promote animated elements to GPU layer */
.animated {
  will-change: transform;  /* creates separate composite layer */
  transform: translateZ(0); /* force GPU layer (old hack) */
}

/* will-change best practices */
/* ✅ Add before animation starts, remove after */
element.addEventListener('mouseenter', () => {
  element.style.willChange = 'transform';
});
element.addEventListener('animationend', () => {
  element.style.willChange = 'auto';
});
/* 🚫 Don't set will-change on everything — each layer costs GPU memory */</pre>

<div class="interview-q">
<h4>🎯 Interview Questions — CSS Performance</h4>
<p><strong>Q: What triggers reflow vs repaint?</strong></p>
<p><strong>A:</strong> <strong>Reflow</strong> (expensive): changes to geometry — width, height, padding, margin, font-size, adding/removing elements. <strong>Repaint</strong> (cheaper): changes to appearance — color, background, visibility, box-shadow. <strong>Neither</strong> (cheapest): transform, opacity — these run on the compositor thread (GPU).</p>

<p><strong>Q: What is <code>content-visibility: auto</code> and when would you use it?</strong></p>
<p><strong>A:</strong> It tells the browser to skip rendering elements that are off-screen. The browser doesn't compute layout, paint, or style for those elements until they're near the viewport. Use on long pages with many sections — can reduce initial render time by 50%+ on content-heavy pages.</p>
</div>
"""
