"""
Master builder for the Frontend Interview Checklist Guide v2.
Imports section content from s_*.py modules and assembles the final HTML.
"""
from pathlib import Path

OUT = Path(__file__).parent / "frontend-interview-checklist-guide.html"

# ── Import section modules ───────────────────────────────────────────
from s_js import SECTIONS as JS_SECTIONS
from s_dom_html import SECTIONS as DOM_HTML_SECTIONS
from s_css import SECTIONS as CSS_SECTIONS
from s_ts_perf import SECTIONS as TS_PERF_SECTIONS
from s_sec_net import SECTIONS as SEC_NET_SECTIONS
from s_test_build import SECTIONS as TEST_BUILD_SECTIONS
from s_a11y_patterns import SECTIONS as A11Y_PATTERNS_SECTIONS
from s_system_misc import SECTIONS as SYSTEM_MISC_SECTIONS
from s_angular import SECTIONS as ANGULAR_SECTIONS
from s_advanced import SECTIONS as ADVANCED_SECTIONS
from s_coding_1 import SECTIONS as CODING_1_SECTIONS
from s_coding_2 import SECTIONS as CODING_2_SECTIONS
from s_coding_3 import SECTIONS as CODING_3_SECTIONS
from s_studypath import STUDY_PATH

HEAD = r'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Frontend Interview Concepts — Complete Checklist Guide</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&family=Merriweather:wght@400;700&display=swap" rel="stylesheet">
  <style>
    @page{size:A4;margin:18mm 16mm}
    :root{
      --bg:#f8f9fc;--paper:#ffffff;--ink:#1e293b;--muted:#64748b;--line:#e5e7eb;
      --accent:#059669;--accent-dark:#047857;--accent-soft:#d1fae5;--accent-glow:rgba(5,150,105,0.06);
      --warning:#d97706;--warning-soft:#fef3c7;--code-bg:#263238;--code-text:#eeffff;
      --blue:#2563eb;--blue-soft:#dbeafe;--purple:#7c3aed;--purple-soft:#ede9fe;
      --shadow-sm:0 1px 3px rgba(0,0,0,0.04),0 1px 2px rgba(0,0,0,0.06);
      --shadow-md:0 4px 6px -1px rgba(0,0,0,0.06),0 2px 4px -2px rgba(0,0,0,0.04);
      --shadow-lg:0 10px 25px -5px rgba(0,0,0,0.08),0 8px 10px -6px rgba(0,0,0,0.04);
      --shadow-card:0 1px 3px rgba(0,0,0,0.05),0 1px 2px rgba(0,0,0,0.03);
      --radius:14px;--radius-sm:10px;--radius-xs:6px;
      --transition:0.2s cubic-bezier(0.4,0,0.2,1);
      --section-gap:36px
    }
    *{box-sizing:border-box}
    html{scroll-behavior:smooth;scroll-padding-top:24px}
    body{margin:0;font-family:'Inter',system-ui,-apple-system,sans-serif;color:var(--ink);background:var(--bg);line-height:1.78;font-size:15.5px;-webkit-font-smoothing:antialiased;text-rendering:optimizeLegibility}
    main{max-width:880px;margin:0 auto;padding:36px 44px 80px}

    /* ── Section cards ── */
    section{background:var(--paper);border-radius:var(--radius);padding:28px 32px 32px;margin-bottom:var(--section-gap);box-shadow:var(--shadow-card);border:1px solid var(--line);position:relative;transition:box-shadow 0.3s ease}
    section:hover{box-shadow:var(--shadow-md)}
    section::before{content:'';position:absolute;top:0;left:0;right:0;height:3px;background:linear-gradient(90deg,var(--accent),var(--blue),var(--purple));border-radius:var(--radius) var(--radius) 0 0;opacity:0;transition:opacity 0.3s}
    section:hover::before{opacity:1}

    /* ── Typography ── */
    h1,h2,h3,h4{font-family:'Inter',system-ui,sans-serif;line-height:1.3;margin:0 0 14px;color:#0f172a}
    h1{font-size:2.4rem;font-weight:800;letter-spacing:-0.03em;margin-bottom:14px;background:linear-gradient(135deg,#059669 0%,#0284c7 50%,#7c3aed 100%);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text}
    h2{font-size:1.5rem;font-weight:700;margin-top:0;margin-bottom:20px;padding:14px 20px;background:linear-gradient(135deg,var(--accent-glow),rgba(37,99,235,0.03));border-left:4px solid var(--accent);border-radius:0 var(--radius-sm) var(--radius-sm) 0;position:relative}
    h2::after{content:'';position:absolute;bottom:-1px;left:20px;right:20px;height:1px;background:linear-gradient(90deg,var(--accent),transparent)}
    h3{font-size:1.12rem;font-weight:600;margin-top:30px;margin-bottom:12px;color:#1e40af;display:flex;align-items:center;gap:8px}
    h3::before{content:'';width:8px;height:8px;background:linear-gradient(135deg,var(--accent),var(--blue));border-radius:50%;flex-shrink:0}
    h4{font-size:0.98rem;font-weight:600;margin-top:20px;color:#334155}
    p{margin:0 0 14px;color:#374151;line-height:1.78}
    ul,ol{margin:8px 0 16px 22px;padding:0}
    li{margin:0 0 8px;color:#374151;line-height:1.7}
    li::marker{color:var(--accent)}
    strong{color:#0f172a}

    /* ── Inline code ── */
    code{font-family:'JetBrains Mono',monospace;background:#eceff4;padding:2px 8px;border-radius:6px;font-size:0.86em;color:#c4532d;border:1px solid #d8dee9;font-weight:500}

    /* ── Code blocks ── */
    pre{background:var(--code-bg);color:var(--code-text);border:none;border-radius:var(--radius);padding:24px 24px 20px;overflow-x:auto;white-space:pre-wrap;word-break:break-word;font-size:13.5px;line-height:1.7;margin:14px 0 22px;position:relative;box-shadow:var(--shadow-lg);font-family:'JetBrains Mono',monospace;border-left:4px solid #80cbc4}
    pre code{background:none;padding:0;font-size:inherit;color:inherit;border:none;font-weight:400}
    pre::before{content:'CODE';position:absolute;top:10px;right:14px;font-size:9px;font-weight:700;letter-spacing:0.12em;color:#80cbc4;background:rgba(128,203,196,0.08);padding:2px 10px;border-radius:4px;font-family:'Inter',sans-serif;backdrop-filter:blur(4px)}

    /* ── Syntax coloring (comment-based) ── */
    .cm-comment{color:#546e7a;font-style:italic}
    .cm-keyword{color:#c792ea}
    .cm-string{color:#c3e88d}
    .cm-number{color:#f78c6c}
    .cm-function{color:#82aaff}
    .cm-type{color:#ffcb6b}

    /* ── Tables ── */
    table{width:100%;border-collapse:separate;border-spacing:0;margin:16px 0 22px;font-size:13.5px;border-radius:var(--radius);overflow:hidden;box-shadow:var(--shadow-md);border:1px solid var(--line)}
    th,td{padding:13px 16px;vertical-align:top;text-align:left;border-bottom:1px solid var(--line)}
    th{background:linear-gradient(135deg,#f0f4f8,#e8ecf1);font-weight:600;color:#0f172a;font-size:12px;text-transform:uppercase;letter-spacing:0.05em}
    td{background:var(--paper)}
    tr:nth-child(even) td{background:#f8fafc}
    tr:last-child td{border-bottom:none}
    tr:hover td{background:#eef2ff;transition:background var(--transition)}

    a{color:var(--blue);text-decoration:none;border-bottom:1px solid transparent;transition:all var(--transition)}
    a:hover{border-bottom-color:var(--blue);color:#1d4ed8}

    /* ── Hero Section ── */
    .hero{padding:44px 40px 36px;background:linear-gradient(135deg,#ecfdf5 0%,#eff6ff 40%,#faf5ff 70%,#fef2f2 100%);border-radius:var(--radius);margin-bottom:var(--section-gap);box-shadow:var(--shadow-lg);border:1px solid rgba(5,150,105,0.1);position:relative;overflow:hidden}
    .hero::before{content:'';position:absolute;top:-50%;right:-25%;width:500px;height:500px;background:radial-gradient(circle,rgba(5,150,105,0.06) 0%,transparent 70%);pointer-events:none;animation:heroPulse 6s ease-in-out infinite}
    .hero::after{content:'';position:absolute;bottom:-40%;left:-15%;width:400px;height:400px;background:radial-gradient(circle,rgba(37,99,235,0.05) 0%,transparent 70%);pointer-events:none;animation:heroPulse 8s ease-in-out infinite reverse}
    @keyframes heroPulse{0%,100%{opacity:0.6;transform:scale(1)}50%{opacity:1;transform:scale(1.1)}}
    .subtitle{font-family:'Inter',sans-serif;color:var(--muted);font-size:15.5px;margin-bottom:16px;line-height:1.7;max-width:640px}

    /* ── Pills ── */
    .pill-row{display:flex;flex-wrap:wrap;gap:8px;margin-top:16px}
    .pill{display:inline-flex;align-items:center;gap:4px;padding:6px 16px;border-radius:999px;font-family:'Inter',sans-serif;font-size:11.5px;font-weight:600;border:none;cursor:default;transition:transform var(--transition),box-shadow var(--transition);backdrop-filter:blur(4px)}
    .pill:hover{transform:translateY(-1px);box-shadow:var(--shadow-sm)}
    .pill:nth-child(odd){background:var(--accent-soft);color:#065f46}
    .pill:nth-child(even){background:var(--blue-soft);color:#1e40af}
    .pill:nth-child(3n){background:var(--purple-soft);color:#5b21b6}

    /* ── Callout ── */
    .callout{border-left:4px solid var(--accent);background:linear-gradient(135deg,#f0fdf4,#ecfdf5);padding:18px 20px;margin:16px 0 20px;border-radius:0 var(--radius-sm) var(--radius-sm) 0;box-shadow:var(--shadow-sm)}
    .callout.warning{border-left-color:var(--warning);background:linear-gradient(135deg,#fffbeb,var(--warning-soft))}
    .callout.blue{border-left-color:var(--blue);background:linear-gradient(135deg,#eff6ff,var(--blue-soft))}

    /* ── Interview Q&A boxes ── */
    .interview-q{background:linear-gradient(135deg,#fffbeb 0%,#fef3c7 50%,#fff7ed 100%);border:1px solid #fde68a;border-radius:var(--radius);padding:22px 24px;margin:20px 0 24px;box-shadow:var(--shadow-md);position:relative;overflow:hidden;border-left:4px solid #f59e0b}
    .interview-q::before{content:'💡';position:absolute;top:14px;right:16px;font-size:28px;opacity:0.3}
    .interview-q h4{color:#92400e;margin-top:0;font-size:13px;font-weight:700;letter-spacing:0.04em;text-transform:uppercase}
    .interview-q p{margin:8px 0;color:#451a03;font-size:14px;line-height:1.72}
    .interview-q strong{color:#78350f}
    .interview-q code{background:#fef3c7;border-color:#fde68a;color:#92400e}

    /* ── Checklist small text ── */
    .small{font-size:13px;color:var(--muted);background:linear-gradient(135deg,#f8fafc,#f1f5f9);padding:10px 16px;border-radius:var(--radius-sm);border:1px dashed var(--line);margin-bottom:16px;line-height:1.7}

    .section-break{page-break-before:always}
    .avoid-break{page-break-inside:avoid}

    /* ── Back to top ── */
    .back-to-top{position:fixed;bottom:28px;right:28px;width:46px;height:46px;border-radius:50%;background:linear-gradient(135deg,#059669,#0284c7);color:white;border:none;font-size:20px;cursor:pointer;display:flex;align-items:center;justify-content:center;box-shadow:0 4px 16px rgba(5,150,105,0.35);opacity:0;transform:translateY(20px);transition:all 0.3s ease;z-index:999}
    .back-to-top.visible{opacity:1;transform:translateY(0)}
    .back-to-top:hover{transform:translateY(-3px);box-shadow:0 6px 24px rgba(5,150,105,0.45)}

    /* ── Scroll progress bar ── */
    .scroll-progress{position:fixed;top:0;left:280px;right:0;height:3px;background:transparent;z-index:1001}
    .scroll-progress-bar{height:100%;width:0%;background:linear-gradient(90deg,#34d399,#60a5fa,#a78bfa,#f472b6);transition:width 0.1s linear;border-radius:0 2px 2px 0;box-shadow:0 0 8px rgba(96,165,250,0.3)}

    /* ── Sidebar nav ── */
    .sidebar-nav{position:fixed;top:0;left:0;width:280px;height:100vh;background:linear-gradient(180deg,#0a0f1e 0%,#131a2e 50%,#0f172a 100%);color:#cbd5e1;overflow-y:auto;padding:0 0 24px;z-index:1000;font-family:'Inter',sans-serif;scrollbar-width:thin;scrollbar-color:#334155 #1e293b}
    .sidebar-nav::-webkit-scrollbar{width:4px}
    .sidebar-nav::-webkit-scrollbar-track{background:transparent}
    .sidebar-nav::-webkit-scrollbar-thumb{background:#334155;border-radius:4px}
    .sidebar-nav .nav-header{padding:22px 18px 18px;background:linear-gradient(135deg,rgba(5,150,105,0.1),rgba(37,99,235,0.06));border-bottom:1px solid rgba(148,163,184,0.08);margin-bottom:6px}
    .sidebar-nav .nav-title{font-size:15px;font-weight:700;color:#6ee7b7;margin:0;letter-spacing:-0.01em}
    .sidebar-nav .nav-subtitle{font-size:11px;color:#64748b;margin-top:5px}
    .sidebar-nav .nav-group{font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:0.12em;color:#475569;padding:16px 18px 5px;margin:0}
    .sidebar-nav a{display:flex;align-items:center;gap:7px;padding:5px 14px 5px 16px;font-size:12.5px;color:#94a3b8;text-decoration:none;line-height:1.35;border-left:3px solid transparent;transition:all var(--transition);border-radius:0 6px 6px 0;margin:1px 8px 1px 0}
    .sidebar-nav a:hover{background:rgba(148,163,184,0.08);color:#e2e8f0;border-left-color:#6ee7b7}
    .sidebar-nav a.active{background:rgba(5,150,105,0.1);color:#6ee7b7;border-left-color:#6ee7b7;font-weight:600}
    /* ── Sidebar search ── */
    .nav-search-wrap{padding:6px 12px 4px;position:relative}
    .nav-search-input{width:100%;padding:7px 10px 7px 28px;border:1px solid #334155;background:#0f172a;color:#e2e8f0;border-radius:6px;font-size:12px;font-family:'Inter',sans-serif;outline:none;transition:border-color 0.2s}
    .nav-search-input:focus{border-color:#6ee7b7}
    .nav-search-input::placeholder{color:#475569}
    .nav-search-icon{position:absolute;left:22px;top:50%;transform:translateY(-50%);font-size:11px;color:#475569;pointer-events:none}
    /* ── Sidebar progress ── */
    .nav-progress-wrap{padding:4px 18px 6px}
    .nav-progress-info{display:flex;justify-content:space-between;font-size:10px;color:#94a3b8;margin-bottom:3px}
    .nav-progress-pct{font-weight:700;color:#6ee7b7}
    .nav-progress-track{height:3px;background:#0f172a;border-radius:3px;overflow:hidden}
    .nav-progress-fill{height:100%;background:linear-gradient(90deg,#059669,#34d399);border-radius:3px;transition:width 0.4s ease;width:0%}
    /* ── Nav group collapsible ── */
    .sidebar-nav .nav-group{cursor:pointer;display:flex;align-items:center;user-select:none;transition:color 0.2s}
    .sidebar-nav .nav-group:hover{color:#94a3b8}
    .nav-group-arrow{font-size:8px;color:#475569;transition:transform 0.25s ease;flex-shrink:0}
    .nav-group.collapsed .nav-group-arrow{transform:rotate(-90deg)}
    .nav-group-badge{font-size:9px;color:#64748b;margin-left:auto;margin-right:6px;font-weight:500;letter-spacing:0;text-transform:none}
    .nav-group-badge.done{color:#34d399}
    .nav-group-items{overflow:hidden;max-height:2000px;transition:max-height 0.3s ease}
    .nav-group-items.collapsed{max-height:0!important}
    /* ── Nav checkmark ── */
    .nav-check{width:13px;height:13px;min-width:13px;border:1.5px solid #475569;border-radius:3px;display:inline-flex;align-items:center;justify-content:center;transition:all 0.15s;cursor:pointer;font-size:8px;color:transparent;line-height:1}
    .nav-check:hover{border-color:#6ee7b7;background:rgba(110,231,183,0.1)}
    .nav-check.checked{background:#059669;border-color:#059669;color:#fff}
    .sidebar-nav a.completed .nav-link-text{text-decoration:line-through;text-decoration-color:#475569;opacity:0.55}
    .nav-reset-btn{display:block;padding:6px 14px;margin:4px 12px 4px;background:transparent;border:1px dashed #334155;color:#64748b;border-radius:6px;font-size:10px;font-family:'Inter',sans-serif;cursor:pointer;text-align:center;transition:all 0.2s}
    .nav-reset-btn:hover{border-color:#ef4444;color:#ef4444;background:rgba(239,68,68,0.06)}
    /* ── Nav action buttons row ── */
    .nav-actions{display:flex;gap:6px;padding:4px 12px 8px}
    .nav-action-btn{flex:1;padding:5px 6px;border:1px solid #334155;background:transparent;color:#94a3b8;border-radius:6px;font-size:9px;font-family:'Inter',sans-serif;cursor:pointer;text-align:center;transition:all 0.2s;white-space:nowrap}
    .nav-action-btn:hover{border-color:#6ee7b7;color:#e2e8f0;background:rgba(110,231,183,0.06)}
    .nav-action-btn.active{border-color:#6ee7b7;color:#6ee7b7;background:rgba(5,150,105,0.1)}
    /* ── Streak tracker ── */
    .streak-bar{display:flex;align-items:center;gap:8px;padding:6px 18px 8px;font-size:10px;color:#94a3b8}
    .streak-fire{font-size:14px}
    .streak-count{font-weight:700;color:#fb923c;font-size:13px}
    .streak-label{color:#64748b}
    .streak-days{display:flex;gap:2px;margin-left:auto}
    .streak-dot{width:8px;height:8px;border-radius:2px;background:#1e293b;border:1px solid #334155}
    .streak-dot.active{background:#059669;border-color:#34d399}
    .streak-dot.today{background:#fbbf24;border-color:#f59e0b}
    /* ── Bookmark star ── */
    .nav-star{font-size:10px;color:#334155;cursor:pointer;transition:all 0.15s;margin-left:auto;flex-shrink:0;opacity:0}
    .sidebar-nav a:hover .nav-star{opacity:1}
    .nav-star:hover{color:#fbbf24;transform:scale(1.3)}
    .nav-star.starred{color:#fbbf24;opacity:1}
    /* ── Font size controls ── */
    .font-controls{position:fixed;bottom:28px;right:140px;display:flex;gap:4px;z-index:999}
    .font-btn{width:34px;height:34px;border-radius:50%;background:#1e293b;color:#94a3b8;border:2px solid #334155;font-size:13px;font-weight:700;cursor:pointer;display:flex;align-items:center;justify-content:center;box-shadow:var(--shadow-md);transition:all 0.2s;font-family:'Inter',sans-serif}
    .font-btn:hover{background:#334155;color:#e2e8f0;transform:scale(1.1)}
    html.dark .font-btn{background:#f8fafc;color:#334155;border-color:#e2e8f0}
    /* ── Flashcard mode ── */
    .flashcard-overlay{display:none;position:fixed;inset:0;background:rgba(0,0,0,0.7);z-index:2000;align-items:center;justify-content:center;backdrop-filter:blur(4px)}
    .flashcard-overlay.active{display:flex}
    .flashcard{width:90%;max-width:600px;min-height:280px;perspective:1000px;cursor:pointer}
    .flashcard-inner{position:relative;width:100%;min-height:280px;transition:transform 0.6s;transform-style:preserve-3d}
    .flashcard.flipped .flashcard-inner{transform:rotateY(180deg)}
    .flashcard-front,.flashcard-back{position:absolute;inset:0;backface-visibility:hidden;border-radius:16px;padding:32px 28px;display:flex;flex-direction:column;justify-content:center}
    .flashcard-front{background:linear-gradient(135deg,#1e293b,#0f172a);color:#e2e8f0;border:2px solid #334155}
    .flashcard-back{background:linear-gradient(135deg,#059669,#047857);color:#fff;transform:rotateY(180deg);border:2px solid #34d399}
    .flashcard-label{font-size:11px;text-transform:uppercase;letter-spacing:0.1em;opacity:0.6;margin-bottom:12px}
    .flashcard-text{font-size:16px;line-height:1.7;font-family:'Inter',sans-serif}
    .flashcard-nav{display:flex;gap:12px;margin-top:16px;justify-content:center}
    .flashcard-nav button{padding:8px 20px;border-radius:8px;border:2px solid rgba(255,255,255,0.2);background:rgba(255,255,255,0.1);color:#fff;font-size:13px;font-family:'Inter',sans-serif;cursor:pointer;transition:all 0.2s}
    .flashcard-nav button:hover{background:rgba(255,255,255,0.2)}
    .flashcard-close{position:absolute;top:16px;right:20px;background:none;border:none;color:rgba(255,255,255,0.6);font-size:24px;cursor:pointer;z-index:2001}
    .flashcard-close:hover{color:#fff}
    .flashcard-counter{text-align:center;color:rgba(255,255,255,0.5);font-size:12px;margin-top:12px;font-family:'Inter',sans-serif}
    /* ── Reading time badge ── */
    .reading-time{font-size:9px;color:#475569;background:#0f172a;padding:1px 5px;border-radius:3px;margin-left:4px;flex-shrink:0;white-space:nowrap}
    /* ── Keyboard shortcut hint ── */
    .kbd-hint{position:fixed;bottom:80px;right:28px;background:#1e293b;border:1px solid #334155;border-radius:8px;padding:10px 14px;font-size:10px;color:#94a3b8;font-family:'Inter',sans-serif;z-index:998;opacity:0;transform:translateY(10px);transition:all 0.3s;pointer-events:none;line-height:1.8;white-space:nowrap}
    .kbd-hint.visible{opacity:1;transform:translateY(0);pointer-events:auto}
    .kbd-hint kbd{display:inline-block;padding:1px 5px;background:#0f172a;border:1px solid #475569;border-radius:3px;font-size:10px;color:#e2e8f0;font-family:'JetBrains Mono',monospace;margin:0 2px}
    html.dark .kbd-hint{background:#f8fafc;border-color:#e2e8f0;color:#64748b}
    html.dark .kbd-hint kbd{background:#f1f5f9;border-color:#cbd5e1;color:#334155}
    /* ── Personal Notes ── */
    .section-notes{margin:18px 0 24px;border:1px solid var(--line);border-radius:var(--radius);overflow:hidden;transition:all 0.3s ease}
    .section-notes.has-note{border-color:var(--accent);box-shadow:0 0 0 1px var(--accent-soft)}
    .notes-header{display:flex;align-items:center;gap:8px;padding:10px 16px;background:linear-gradient(135deg,#f8fafc,#f1f5f9);cursor:pointer;user-select:none;transition:background 0.2s}
    .notes-header:hover{background:#f1f5f9}
    .section-notes.has-note .notes-header{background:linear-gradient(135deg,var(--accent-soft),rgba(37,99,235,0.04))}
    .notes-icon{font-size:14px;flex-shrink:0}
    .notes-title{font-size:12px;font-weight:600;color:var(--ink);font-family:'Inter',sans-serif}
    .notes-badge{font-size:9px;background:var(--accent);color:#fff;padding:1px 7px;border-radius:99px;font-weight:600;display:none}
    .section-notes.has-note .notes-badge{display:inline-block}
    .notes-toggle-arrow{margin-left:auto;font-size:10px;color:var(--muted);transition:transform 0.25s}
    .section-notes.open .notes-toggle-arrow{transform:rotate(180deg)}
    .notes-body{max-height:0;overflow:hidden;transition:max-height 0.35s ease}
    .section-notes.open .notes-body{max-height:600px}
    .notes-textarea{width:100%;min-height:80px;max-height:300px;padding:12px 16px;border:none;border-top:1px solid var(--line);background:var(--paper);color:var(--ink);font-family:'Inter',sans-serif;font-size:13px;line-height:1.6;resize:vertical;outline:none;transition:background 0.2s}
    .notes-textarea::placeholder{color:var(--muted);font-style:italic}
    .notes-textarea:focus{background:#fefce8}
    .notes-actions{display:flex;gap:6px;padding:8px 16px;background:var(--paper);border-top:1px solid var(--line)}
    .notes-save-btn{padding:4px 14px;border:none;border-radius:5px;background:var(--accent);color:#fff;font-size:11px;font-weight:600;font-family:'Inter',sans-serif;cursor:pointer;transition:all 0.2s}
    .notes-save-btn:hover{background:var(--accent-dark)}
    .notes-save-btn:disabled{opacity:0.5;cursor:default}
    .notes-delete-btn{padding:4px 14px;border:1px solid #fca5a5;border-radius:5px;background:transparent;color:#ef4444;font-size:11px;font-weight:600;font-family:'Inter',sans-serif;cursor:pointer;transition:all 0.2s;display:none}
    .notes-delete-btn:hover{background:#fef2f2;border-color:#ef4444}
    .section-notes.has-note .notes-delete-btn{display:inline-block}
    .notes-saved-msg{font-size:10px;color:var(--accent);margin-left:auto;opacity:0;transition:opacity 0.3s;align-self:center}
    .notes-saved-msg.show{opacity:1}
    .notes-char-count{font-size:9px;color:var(--muted);margin-left:auto;padding:2px 16px 6px;background:var(--paper);font-family:'Inter',sans-serif}
    html.dark .notes-header{background:linear-gradient(135deg,#1e293b,#0f172a)}
    html.dark .notes-header:hover{background:#1e293b}
    html.dark .section-notes.has-note .notes-header{background:linear-gradient(135deg,rgba(52,211,153,0.08),rgba(96,165,250,0.04))}
    html.dark .notes-textarea{background:#0f172a}
    html.dark .notes-textarea:focus{background:rgba(251,191,36,0.04)}
    html.dark .notes-actions{background:#0f172a}
    /* ── Confetti ── */
    .confetti-canvas{position:fixed;inset:0;z-index:3000;pointer-events:none}
    body{margin-left:280px}
    .nav-toggle{display:none;position:fixed;top:14px;left:14px;z-index:1001;background:#0f172a;color:#6ee7b7;border:none;border-radius:var(--radius-sm);width:42px;height:42px;font-size:20px;cursor:pointer;align-items:center;justify-content:center;box-shadow:var(--shadow-lg);transition:transform var(--transition)}
    .nav-toggle:hover{transform:scale(1.05)}

    /* ── Section fade-in animation ── */
    section,h2,h3,pre,table,.interview-q,.callout{opacity:1;transform:none}
    section.fade-in,h2.fade-in,h3.fade-in{opacity:0;transform:translateY(16px);transition:opacity 0.5s ease,transform 0.5s ease}
    section.fade-in.visible,h2.fade-in.visible,h3.fade-in.visible{opacity:1;transform:none}

    /* ── Copy button for code blocks ── */
    .code-wrapper{position:relative}
    .copy-btn{position:absolute;top:8px;right:60px;background:#334155;color:#94a3b8;border:none;padding:4px 10px;border-radius:5px;font-size:11px;font-family:'Inter',sans-serif;font-weight:500;cursor:pointer;opacity:0;transition:all var(--transition);z-index:2}
    .code-wrapper:hover .copy-btn{opacity:1}
    .copy-btn:hover{background:#475569;color:#e2e8f0}
    .copy-btn.copied{background:#059669;color:white}

    /* ── Dark mode toggle ── */
    .theme-toggle{position:fixed;bottom:28px;right:84px;width:46px;height:46px;border-radius:50%;background:linear-gradient(135deg,#1e293b,#0f172a);color:#fbbf24;border:2px solid #334155;font-size:18px;cursor:pointer;display:flex;align-items:center;justify-content:center;box-shadow:var(--shadow-md);z-index:999;transition:all 0.3s ease}
    .theme-toggle:hover{transform:scale(1.1);box-shadow:var(--shadow-lg)}

    /* ── Dark mode ── */
    html.dark{
      --bg:#0c0f1a;--paper:#161b2e;--ink:#e2e8f0;--muted:#94a3b8;--line:#2a3149;
      --accent:#34d399;--accent-dark:#10b981;--accent-soft:rgba(52,211,153,0.1);--accent-glow:rgba(52,211,153,0.06);
      --code-bg:#1a2332;--code-text:#e8eaed;--blue:#60a5fa;--blue-soft:rgba(96,165,250,0.1);
      --shadow-card:0 1px 4px rgba(0,0,0,0.3),0 1px 2px rgba(0,0,0,0.2)
    }
    html.dark body{background:var(--bg)}
    html.dark main{background:transparent}
    html.dark section{background:var(--paper);border-color:var(--line)}
    html.dark section::before{opacity:0}
    html.dark section:hover::before{opacity:0.6}
    html.dark h1{background:linear-gradient(135deg,#34d399,#60a5fa,#c084fc);-webkit-background-clip:text;background-clip:text}
    html.dark h2{background:rgba(52,211,153,0.05);border-left-color:#34d399;color:#f1f5f9}
    html.dark h2::after{background:linear-gradient(90deg,#34d399,transparent)}
    html.dark h3{color:#60a5fa}
    html.dark h3::before{background:linear-gradient(135deg,#34d399,#60a5fa)}
    html.dark h4{color:#cbd5e1}
    html.dark p,html.dark li{color:#cbd5e1}
    html.dark strong{color:#f1f5f9}
    html.dark code{background:#1e2a3a;color:#f78c6c;border-color:#2e3d50}
    html.dark pre{background:#0d1a2a;border:none;box-shadow:0 4px 24px rgba(0,0,0,0.4);border-left:4px solid #80cbc4}
    html.dark pre::before{background:rgba(128,203,196,0.06);color:#5f8a84}
    html.dark table{border-color:var(--line)}
    html.dark th{background:#1a2035;color:#e2e8f0}
    html.dark td{background:var(--paper);border-color:var(--line);color:#cbd5e1}
    html.dark tr:nth-child(even) td{background:#131829}
    html.dark tr:hover td{background:#1e2744}
    html.dark .hero{background:linear-gradient(135deg,rgba(52,211,153,0.04),rgba(96,165,250,0.04),rgba(167,139,250,0.04));border-color:var(--line)}
    html.dark .interview-q{background:linear-gradient(135deg,rgba(251,191,36,0.06),rgba(245,158,11,0.04));border-color:#92400e;border-left-color:#f59e0b}
    html.dark .interview-q h4{color:#fbbf24}
    html.dark .interview-q p{color:#e2e8f0}
    html.dark .interview-q strong{color:#fcd34d}
    html.dark .interview-q code{background:rgba(251,191,36,0.1);border-color:#92400e;color:#fbbf24}
    html.dark .small{background:#1a2035;border-color:var(--line);color:#94a3b8}
    html.dark .callout{background:rgba(52,211,153,0.04)}
    html.dark .pill:nth-child(odd){background:rgba(52,211,153,0.1);color:#6ee7b7}
    html.dark .pill:nth-child(even){background:rgba(96,165,250,0.1);color:#93c5fd}
    html.dark .pill:nth-child(3n){background:rgba(167,139,250,0.1);color:#c4b5fd}
    html.dark a{color:#60a5fa}
    html.dark a:hover{color:#93c5fd}
    html.dark .theme-toggle{background:#f8fafc;color:#f59e0b;border-color:#e2e8f0}
    html.dark .back-to-top{background:#34d399;box-shadow:0 4px 14px rgba(52,211,153,0.35)}

    @media(max-width:1100px){
      .sidebar-nav{transform:translateX(-100%);transition:transform 0.3s cubic-bezier(0.4,0,0.2,1)}
      .sidebar-nav.open{transform:translateX(0);box-shadow:4px 0 30px rgba(0,0,0,0.4)}
      body{margin-left:0}
      main{padding:24px 20px 48px}
      section{padding:22px 20px 24px;margin-bottom:24px}
      .nav-toggle{display:flex}
      .scroll-progress{left:0}
    }
    @media(max-width:600px){
      h1{font-size:1.6rem}
      h2{font-size:1.2rem;padding:12px 14px}
      pre{font-size:12px;padding:16px 14px}
      .hero{padding:28px 20px 22px}
      section{padding:18px 16px 20px;border-radius:var(--radius-sm)}
    }
    @media print{.sidebar-nav,.nav-toggle,.back-to-top,.scroll-progress,.theme-toggle,.copy-btn,.font-controls{display:none!important}body{margin-left:0;background:#fff}main{max-width:none;padding:0}section{box-shadow:none;border:none;padding:16px 0;margin-bottom:16px}section::before{display:none}h2,h3,pre,table,.interview-q,.callout,section{opacity:1!important;transform:none!important}}
  </style>
</head>
<body>
<div class="scroll-progress"><div class="scroll-progress-bar" id="progressBar"></div></div>
<button class="nav-toggle" onclick="document.querySelector('.sidebar-nav').classList.toggle('open')" aria-label="Toggle navigation">&#9776;</button>
<button class="back-to-top" id="backToTop" onclick="window.scrollTo({top:0,behavior:'smooth'})" aria-label="Back to top">&#8593;</button>
<button class="theme-toggle" id="themeToggle" aria-label="Toggle dark mode">&#9790;</button>
<div class="font-controls">
  <button class="font-btn" id="fontDown" title="Decrease font size">A-</button>
  <button class="font-btn" id="fontUp" title="Increase font size">A+</button>
</div>
<div class="kbd-hint" id="kbdHint">
  <kbd>J</kbd>/<kbd>K</kbd> Navigate &nbsp; <kbd>Space</kbd> Check &nbsp; <kbd>/</kbd> Search<br>
  <kbd>B</kbd> Bookmark &nbsp; <kbd>F</kbd> Flashcards &nbsp; <kbd>?</kbd> Toggle shortcuts
</div>
<div class="flashcard-overlay" id="flashcardOverlay">
  <button class="flashcard-close" id="flashcardClose">&times;</button>
  <div style="text-align:center;width:90%;max-width:640px">
    <div class="flashcard" id="flashcard">
      <div class="flashcard-inner">
        <div class="flashcard-front">
          <div class="flashcard-label">&#128161; Question</div>
          <div class="flashcard-text" id="fcQuestion">Loading...</div>
        </div>
        <div class="flashcard-back">
          <div class="flashcard-label">&#9989; Answer</div>
          <div class="flashcard-text" id="fcAnswer">Click to flip</div>
        </div>
      </div>
    </div>
    <div class="flashcard-counter" id="fcCounter">1 / 1</div>
    <div class="flashcard-nav">
      <button id="fcPrev">&#8592; Prev</button>
      <button id="fcShuffle">&#128256; Shuffle</button>
      <button id="fcNext">Next &#8594;</button>
    </div>
  </div>
</div>
<nav class="sidebar-nav" id="sidebarNav">
  <div class="nav-header">
    <div class="nav-title">&#128203; Frontend Interview Guide</div>
    <div class="nav-subtitle">143 Sections &bull; Complete Checklist</div>
  </div>
  <div class="streak-bar">
    <span class="streak-fire">&#128293;</span>
    <span class="streak-count" id="streakCount">0</span>
    <span class="streak-label">day streak</span>
    <div class="streak-days" id="streakDots"></div>
  </div>
  <div class="nav-progress-wrap">
    <div class="nav-progress-info">
      <span id="navProgressText">0 / 143 completed</span>
      <span class="nav-progress-pct" id="navProgressPct">0%</span>
    </div>
    <div class="nav-progress-track"><div class="nav-progress-fill" id="navProgressFill"></div></div>
  </div>
  <div class="nav-search-wrap">
    <span class="nav-search-icon">&#128269;</span>
    <input class="nav-search-input" id="navSearch" type="text" placeholder="Search sections...">
  </div>

  <a href="#study-path" style="background:linear-gradient(135deg,#059669,#2563eb);color:#fff;font-weight:700;border-radius:8px;padding:8px 14px;margin:8px 12px 12px;display:block;text-align:center;text-decoration:none;font-size:14px;">&#128640; 90-Day FAANG Study Path (SDE-2/3)</a>

  <p class="nav-group">JavaScript Core</p>
  <a href="#js-fundamentals">Fundamentals</a>
  <a href="#js-scope-closures">Scope &amp; Closures</a>
  <a href="#js-this">The this Keyword</a>
  <a href="#js-prototypes">Prototypes</a>
  <a href="#js-async">Asynchronous JS</a>
  <a href="#js-es6">ES6+ Features</a>
  <a href="#js-advanced">Advanced Concepts</a>
  <a href="#js-array-methods">Array Methods</a>
  <a href="#js-object-methods">Object Methods</a>
  <a href="#js-error-handling">Error Handling</a>
  <a href="#js-modules">Modules</a>
  <a href="#js-regex">Regular Expressions</a>

  <p class="nav-group">DOM &amp; Browser</p>
  <a href="#dom-manipulation">DOM Manipulation</a>
  <a href="#dom-traversal">DOM Traversal</a>
  <a href="#dom-events">Events</a>
  <a href="#dom-storage">Browser Storage</a>
  <a href="#dom-browser-apis">Browser APIs</a>
  <a href="#dom-window-document">Window &amp; Document</a>
  <a href="#dom-forms">Forms</a>

  <p class="nav-group">HTML</p>
  <a href="#html-semantic">Semantic HTML</a>
  <a href="#html5-features">HTML5 Features</a>
  <a href="#html-metadata-seo">Metadata &amp; SEO</a>
  <a href="#html-media">Media Elements</a>
  <a href="#html-accessibility">Accessibility (HTML)</a>

  <p class="nav-group">CSS</p>
  <a href="#css-selectors">Selectors</a>
  <a href="#css-box-model">Box Model</a>
  <a href="#css-layout">Layout</a>
  <a href="#css-flexbox">Flexbox</a>
  <a href="#css-grid">Grid</a>
  <a href="#css-responsive">Responsive Design</a>
  <a href="#css-typography">Typography</a>
  <a href="#css-colors">Colors &amp; Backgrounds</a>
  <a href="#css-animations">Transforms &amp; Animations</a>
  <a href="#css-variables">CSS Variables</a>
  <a href="#css-modern">Modern CSS</a>
  <a href="#css-methodologies">Methodologies</a>
  <a href="#css-in-js">CSS-in-JS</a>
  <a href="#css-preprocessors">Preprocessors</a>
  <a href="#css-performance">CSS Performance</a>

  <p class="nav-group">TypeScript</p>
  <a href="#ts-basics">Basics</a>
  <a href="#ts-advanced-types">Advanced Types</a>
  <a href="#ts-generics">Generics</a>
  <a href="#ts-utility-types">Utility Types</a>
  <a href="#ts-functions">Functions</a>
  <a href="#ts-enums">Enums</a>
  <a href="#ts-modules">Modules &amp; Config</a>

  <p class="nav-group">Performance</p>
  <a href="#perf-loading">Loading Performance</a>
  <a href="#perf-runtime">Runtime Performance</a>
  <a href="#perf-rendering">Rendering Performance</a>
  <a href="#perf-caching">Caching Strategies</a>
  <a href="#perf-web-vitals">Core Web Vitals</a>
  <a href="#perf-images">Images &amp; Media</a>
  <a href="#perf-fonts">Fonts</a>
  <a href="#perf-measuring">Measuring Performance</a>

  <p class="nav-group">Security</p>
  <a href="#sec-vulnerabilities">Common Vulnerabilities</a>
  <a href="#sec-prevention">Prevention Techniques</a>
  <a href="#sec-auth">Authentication &amp; Auth</a>

  <p class="nav-group">Networking</p>
  <a href="#net-http">HTTP Basics</a>
  <a href="#net-rest">REST API Design</a>
  <a href="#net-graphql">GraphQL</a>
  <a href="#net-data-fetching">Data Fetching</a>
  <a href="#net-websockets">WebSockets</a>

  <p class="nav-group">State &amp; Testing</p>
  <a href="#state-management">State Management</a>
  <a href="#test-unit">Unit Testing</a>
  <a href="#test-integration">Integration Testing</a>
  <a href="#test-e2e">E2E Testing</a>
  <a href="#test-tdd">TDD</a>

  <p class="nav-group">Build Tools</p>
  <a href="#build-webpack">Webpack</a>
  <a href="#build-vite">Vite</a>
  <a href="#build-babel">Babel</a>
  <a href="#build-package-managers">Package Managers</a>
  <a href="#build-linting">Linting &amp; Formatting</a>
  <a href="#build-env-vars">Environment Variables</a>

  <p class="nav-group">Accessibility</p>
  <a href="#a11y-wcag">WCAG Guidelines</a>
  <a href="#a11y-keyboard">Keyboard Navigation</a>
  <a href="#a11y-screen-readers">Screen Readers</a>
  <a href="#a11y-aria">ARIA Attributes</a>
  <a href="#a11y-color">Color &amp; Contrast</a>
  <a href="#a11y-forms">Form Accessibility</a>

  <p class="nav-group">Design Patterns</p>
  <a href="#patterns-creational">Creational</a>
  <a href="#patterns-structural">Structural</a>
  <a href="#patterns-behavioral">Behavioral</a>
  <a href="#patterns-architectural">Architectural</a>

  <p class="nav-group">DSA</p>
  <a href="#dsa-structures">Data Structures</a>
  <a href="#dsa-algorithms">Common Algorithms</a>
  <a href="#dsa-complexity">Complexity Analysis</a>

  <p class="nav-group">System Design</p>
  <a href="#sd-component">Component Design</a>
  <a href="#sd-architecture">App Architecture</a>
  <a href="#sd-components">Common Components</a>
  <a href="#sd-full-apps">Full App Designs</a>
  <a href="#sd-scalability">Scalability</a>

  <p class="nav-group">Version Control</p>
  <a href="#git-basics">Git Basics</a>
  <a href="#git-workflows">Git Workflows</a>
  <a href="#git-advanced">Advanced Git</a>

  <p class="nav-group">Web Fundamentals</p>
  <a href="#web-rendering">Browser Rendering</a>
  <a href="#web-browsers">How Browsers Work</a>
  <a href="#web-progressive">Progressive Enhancement</a>
  <a href="#web-standards">Web Standards</a>

  <p class="nav-group">Angular Deep Dive</p>
  <a href="#ng-change-detection">Change Detection</a>
  <a href="#ng-di">Dependency Injection</a>
  <a href="#ng-lifecycle">Lifecycle Hooks</a>
  <a href="#ng-rxjs">RxJS Deep Dive</a>
  <a href="#ng-router">Router &amp; Guards</a>
  <a href="#ng-forms">Reactive Forms</a>
  <a href="#ng-http">HTTP &amp; Interceptors</a>
  <a href="#ng-standalone">Standalone &amp; Modern APIs</a>
  <a href="#ng-pipes">Pipes &amp; Directives</a>
  <a href="#ng-content-projection">Content Projection</a>
  <a href="#ng-performance">Angular Performance</a>
  <a href="#ng-testing">Angular Testing</a>
  <a href="#ng-ngrx">NgRx &amp; SignalStore</a>
  <a href="#ng-patterns">Best Practices</a>
  <a href="#ng-common-mistakes">Common Mistakes</a>

  <p class="nav-group">Interview Prep</p>
  <a href="#tricky-output">Tricky Output Questions</a>
  <a href="#challenge-polyfills">JS Polyfills</a>
  <a href="#challenge-machine">Machine Coding</a>
  <a href="#challenge-advanced-coding">Advanced Coding</a>
  <a href="#ts-advanced-patterns">Advanced TypeScript</a>
  <a href="#sd-frontend-lld">Frontend LLD</a>
  <a href="#challenge-system-design">System Design Patterns</a>
  <a href="#common-scenarios">Performance Case Studies</a>
  <a href="#behavioral-questions">Behavioral Questions</a>
  <a href="#frontend-security-advanced">Advanced Security</a>

  <p class="nav-group">Concept-Based Coding Challenges</p>
  <a href="#cc-closures-currying">Closures &amp; Currying</a>
  <a href="#cc-debounce-throttle">Debounce &amp; Throttle</a>
  <a href="#cc-promises-async">Promises &amp; Async</a>
  <a href="#cc-array-object">Arrays &amp; Objects</a>
  <a href="#cc-recursion-trees">Recursion &amp; Trees</a>
  <a href="#cc-event-emitter">Event Emitter &amp; Observer</a>
  <a href="#cc-this-proto">this Binding &amp; Prototypes</a>
  <a href="#cc-scope-hoisting">Scope &amp; Hoisting</a>
  <a href="#cc-event-loop">Event Loop Challenges</a>
  <a href="#cc-string-regex">Strings &amp; RegEx</a>
  <a href="#cc-data-structures">Data Structures</a>
  <a href="#cc-design-patterns">Design Patterns</a>
  <a href="#cc-dom-challenges">DOM Challenges</a>

  <p class="nav-group">Miscellaneous</p>
  <a href="#mobile-responsive">Mobile &amp; PWA</a>
  <a href="#css-architecture">CSS Architecture</a>
  <a href="#modern-js">Modern JavaScript</a>
  <a href="#framework-comparisons">Framework Comparisons</a>
  <a href="#soft-skills">Soft Skills</a>
  <a href="#impl-patterns">Implementation Patterns</a>
  <a href="#additional-topics">Additional Topics</a>
  <div class="nav-actions">
    <button class="nav-action-btn" id="navExportBtn">&#128229; Export</button>
    <button class="nav-action-btn" id="navImportBtn">&#128228; Import</button>
    <button class="nav-action-btn" id="navFlashcardBtn">&#127183; Quiz</button>
    <button class="nav-action-btn" id="navStarFilter">&#11088; Starred</button>
  </div>
  <button class="nav-reset-btn" id="navResetBtn">&#8635; Reset Progress</button>
  <input type="file" id="importFileInput" accept=".json" style="display:none">
</nav>

<main>
<section class="hero avoid-break" style="padding:48px 44px 40px">
  <h1 style="font-size:2.6rem;margin-bottom:8px">Frontend Interview Concepts</h1>
  <p style="font-size:1.25rem;font-weight:600;color:#334155;margin-bottom:18px;letter-spacing:-0.01em">Complete Checklist &mdash; 143 Sections</p>
  <div class="subtitle">Every concept from the Medium checklist &mdash; expanded with in-depth theory, real-time use cases, interview Q&amp;A, and hands-on code. React sections excluded.</div>
  <p style="margin-bottom:20px"><strong>Source:</strong> <a href="https://nagibaba.medium.com/frontend-interview-concepts-complete-checklist-c928c45b9aa2">Babek Naghiyev &mdash; Frontend Interview Concepts (Medium)</a></p>
  <div class="pill-row">
    <span class="pill">JavaScript Core</span><span class="pill">DOM &amp; Browser</span><span class="pill">HTML</span><span class="pill">CSS</span><span class="pill">TypeScript</span><span class="pill">Performance</span><span class="pill">Security</span><span class="pill">Networking</span><span class="pill">Testing</span><span class="pill">Build Tools</span><span class="pill">Accessibility</span><span class="pill">Design Patterns</span><span class="pill">DSA</span><span class="pill">System Design</span><span class="pill">Angular</span><span class="pill">RxJS</span><span class="pill">NgRx</span><span class="pill">Output Questions</span><span class="pill">Polyfills</span><span class="pill">Machine Coding</span><span class="pill">Coding Challenges</span><span class="pill">Git</span><span class="pill">PWA</span>
  </div>
</section>
'''

FOOTER = r'''
</main>
<script>
// ── Smooth sidebar nav click ──
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

// ── Active nav highlight on scroll ──
const navLinks = document.querySelectorAll('.sidebar-nav a[href^="#"]');
const sectionEls = Array.from(navLinks).map(a => ({
  link: a, target: document.querySelector(a.getAttribute('href'))
})).filter(s => s.target);

// ── Scroll progress bar ──
const progressBar = document.getElementById('progressBar');
const backToTop = document.getElementById('backToTop');

let lastActiveLink = null;
let ticking = false;
window.addEventListener('scroll', () => {
  if (!ticking) {
    requestAnimationFrame(() => {
      const scrollY = window.scrollY;
      const docHeight = document.documentElement.scrollHeight - window.innerHeight;
      const progress = docHeight > 0 ? (scrollY / docHeight) * 100 : 0;
      progressBar.style.width = progress + '%';

      // Back to top visibility
      backToTop.classList.toggle('visible', scrollY > 400);

      // Active nav link
      const offset = scrollY + 140;
      let current = sectionEls[0];
      for (const s of sectionEls) { if (s.target.offsetTop <= offset) current = s; }
      if (current && current.link !== lastActiveLink) {
        if (lastActiveLink) lastActiveLink.classList.remove('active');
        current.link.classList.add('active');
        lastActiveLink = current.link;
        current.link.scrollIntoView({ block: 'nearest' });
        const gi = current.link.closest('.nav-group-items');
        if (gi && gi.classList.contains('collapsed')) {
          gi.classList.remove('collapsed');
          const gh = gi.previousElementSibling;
          if (gh) gh.classList.remove('collapsed');
        }
      }
      ticking = false;
    });
    ticking = true;
  }
});
if (sectionEls.length) { sectionEls[0].link.classList.add('active'); lastActiveLink = sectionEls[0].link; }

// ── Intersection Observer for fade-in animations ──
const animObserver = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('visible');
      animObserver.unobserve(entry.target);
    }
  });
}, { threshold: 0.05, rootMargin: '0px 0px -20px 0px' });

document.querySelectorAll('main > section, main > h2').forEach(el => {
  el.classList.add('fade-in');
  animObserver.observe(el);
});

// ── Copy button for code blocks ──
document.querySelectorAll('pre').forEach(pre => {
  const wrapper = document.createElement('div');
  wrapper.className = 'code-wrapper';
  pre.parentNode.insertBefore(wrapper, pre);
  wrapper.appendChild(pre);

  const btn = document.createElement('button');
  btn.className = 'copy-btn';
  btn.textContent = 'Copy';
  btn.addEventListener('click', () => {
    navigator.clipboard.writeText(pre.textContent).then(() => {
      btn.textContent = 'Copied!';
      btn.classList.add('copied');
      setTimeout(() => { btn.textContent = 'Copy'; btn.classList.remove('copied'); }, 2000);
    });
  });
  wrapper.appendChild(btn);
});

// ── Basic syntax highlighting for code blocks ──
document.querySelectorAll('pre code, pre').forEach(block => {
  if (block.querySelector('code')) return; // skip pre that wraps code
  let html = block.innerHTML;
  // Comments
  html = html.replace(/(\/\/[^\n]*)/g, '<span class="cm-comment">$1</span>');
  // Strings
  html = html.replace(/('(?:[^'\\]|\\.)*')/g, '<span class="cm-string">$1</span>');
  // Keywords
  html = html.replace(/\b(const|let|var|function|return|if|else|for|while|class|new|import|export|from|async|await|try|catch|throw|typeof|instanceof|extends|implements|interface|type|enum|switch|case|default|break|continue|this|super|static|private|public|protected|readonly|abstract|declare|module|namespace|yield|of|in)\b/g, '<span class="cm-keyword">$1</span>');
  // Numbers
  html = html.replace(/\b(\d+\.?\d*)\b/g, '<span class="cm-number">$1</span>');
  block.innerHTML = html;
});

// ── Dark mode toggle ──
const themeToggle = document.getElementById('themeToggle');
const savedTheme = localStorage.getItem('guide-theme');
if (savedTheme === 'dark') document.documentElement.classList.add('dark');
themeToggle.textContent = document.documentElement.classList.contains('dark') ? '☀' : '☾';

themeToggle.addEventListener('click', () => {
  document.documentElement.classList.toggle('dark');
  const isDark = document.documentElement.classList.contains('dark');
  themeToggle.textContent = isDark ? '☀' : '☾';
  localStorage.setItem('guide-theme', isDark ? 'dark' : 'light');
});

// ── Close sidebar on outside click (mobile) ──
document.addEventListener('click', (e) => {
  const nav = document.querySelector('.sidebar-nav');
  const toggle = document.querySelector('.nav-toggle');
  if (nav.classList.contains('open') && !nav.contains(e.target) && !toggle.contains(e.target)) {
    nav.classList.remove('open');
  }
});

// ── Sidebar Enhancement: Checkmarks, Collapsible Groups, Search ──
(function() {
  const STORAGE_KEY = 'guide-completed-sections';
  const GROUP_KEY = 'guide-collapsed-groups';
  const sideNav = document.getElementById('sidebarNav');

  function getCompleted() {
    try { return JSON.parse(localStorage.getItem(STORAGE_KEY)) || {}; } catch(e) { return {}; }
  }
  function saveCompleted(d) { localStorage.setItem(STORAGE_KEY, JSON.stringify(d)); }
  function getCollapsedState() {
    try { return JSON.parse(localStorage.getItem(GROUP_KEY)) || {}; } catch(e) { return {}; }
  }
  function saveCollapsedState(d) { localStorage.setItem(GROUP_KEY, JSON.stringify(d)); }

  const completed = getCompleted();
  const collapsedGroups = getCollapsedState();

  // ── 1. Wrap nav-group links into collapsible containers ──
  const groupHeaders = sideNav.querySelectorAll('.nav-group');
  groupHeaders.forEach(function(groupEl, idx) {
    var groupId = 'g' + idx;

    // Add badge (X/Y count)
    var badge = document.createElement('span');
    badge.className = 'nav-group-badge';
    groupEl.appendChild(badge);

    // Add arrow
    var arrow = document.createElement('span');
    arrow.className = 'nav-group-arrow';
    arrow.textContent = '\u25BE';
    groupEl.appendChild(arrow);

    // Collect immediately following <a> siblings
    var wrapper = document.createElement('div');
    wrapper.className = 'nav-group-items';
    wrapper.dataset.group = groupId;

    var sibs = [];
    var nxt = groupEl.nextElementSibling;
    while (nxt && nxt.tagName === 'A') {
      sibs.push(nxt);
      nxt = nxt.nextElementSibling;
    }

    groupEl.after(wrapper);
    sibs.forEach(function(s) { wrapper.appendChild(s); });

    // Apply saved collapsed state
    if (collapsedGroups[groupId]) {
      groupEl.classList.add('collapsed');
      wrapper.classList.add('collapsed');
    }

    // Toggle on click
    groupEl.addEventListener('click', function() {
      var nowCollapsed = groupEl.classList.toggle('collapsed');
      wrapper.classList.toggle('collapsed', nowCollapsed);
      if (nowCollapsed) collapsedGroups[groupId] = true;
      else delete collapsedGroups[groupId];
      saveCollapsedState(collapsedGroups);
    });
  });

  // ── 2. Add checkmarks to every section link ──
  var allLinks = sideNav.querySelectorAll('.nav-group-items a[href^="#"]');
  var totalSections = allLinks.length;

  allLinks.forEach(function(link) {
    var id = link.getAttribute('href').slice(1);

    // Wrap existing content in a text span
    var textSpan = document.createElement('span');
    textSpan.className = 'nav-link-text';
    textSpan.innerHTML = link.innerHTML;
    link.innerHTML = '';

    // Create checkmark
    var chk = document.createElement('span');
    chk.className = 'nav-check' + (completed[id] ? ' checked' : '');
    chk.innerHTML = '&#10003;';
    chk.title = 'Mark as completed';

    link.appendChild(chk);
    link.appendChild(textSpan);
    if (completed[id]) link.classList.add('completed');

    chk.addEventListener('click', function(e) {
      e.preventDefault();
      e.stopPropagation();
      var isChecked = chk.classList.toggle('checked');
      link.classList.toggle('completed', isChecked);
      if (isChecked) completed[id] = true;
      else delete completed[id];
      saveCompleted(completed);
      refreshProgress();
      refreshGroupBadges();
    });
  });

  // ── 3. Progress bar ──
  var pText = document.getElementById('navProgressText');
  var pPct = document.getElementById('navProgressPct');
  var pFill = document.getElementById('navProgressFill');

  function refreshProgress() {
    var done = Object.keys(completed).length;
    var pct = totalSections > 0 ? Math.round((done / totalSections) * 100) : 0;
    if (pText) pText.textContent = done + ' / ' + totalSections + ' completed';
    if (pPct) pPct.textContent = pct + '%';
    if (pFill) pFill.style.width = pct + '%';
  }

  // ── 4. Group badges ──
  function refreshGroupBadges() {
    sideNav.querySelectorAll('.nav-group-items').forEach(function(wrapper) {
      var header = wrapper.previousElementSibling;
      if (!header || !header.classList.contains('nav-group')) return;
      var badge = header.querySelector('.nav-group-badge');
      if (!badge) return;
      var total = wrapper.querySelectorAll('a[href^="#"]').length;
      var done = wrapper.querySelectorAll('.nav-check.checked').length;
      badge.textContent = done + '/' + total;
      badge.classList.toggle('done', done === total && total > 0);
    });
  }

  // ── 5. Search ──
  var searchInput = document.getElementById('navSearch');
  if (searchInput) {
    searchInput.addEventListener('input', function() {
      var q = searchInput.value.toLowerCase().trim();
      sideNav.querySelectorAll('.nav-group-items').forEach(function(wrapper) {
        var links = wrapper.querySelectorAll('a');
        var hasMatch = false;
        links.forEach(function(a) {
          var txt = a.textContent.toLowerCase();
          var match = !q || txt.indexOf(q) !== -1;
          a.style.display = match ? '' : 'none';
          if (match) hasMatch = true;
        });
        wrapper.style.display = hasMatch ? '' : 'none';
        if (q && hasMatch) wrapper.classList.remove('collapsed');
        var hdr = wrapper.previousElementSibling;
        if (hdr && hdr.classList.contains('nav-group')) {
          hdr.style.display = hasMatch ? '' : 'none';
          if (q && hasMatch) hdr.classList.remove('collapsed');
        }
      });
    });
  }

  // ── 6. Reset ──
  var resetBtn = document.getElementById('navResetBtn');
  if (resetBtn) {
    resetBtn.addEventListener('click', function() {
      if (!confirm('Reset all progress? This cannot be undone.')) return;
      localStorage.removeItem(STORAGE_KEY);
      Object.keys(completed).forEach(function(k) { delete completed[k]; });
      sideNav.querySelectorAll('.nav-check').forEach(function(c) { c.classList.remove('checked'); });
      sideNav.querySelectorAll('a.completed').forEach(function(a) { a.classList.remove('completed'); });
      refreshProgress();
      refreshGroupBadges();
    });
  }

  refreshProgress();
  refreshGroupBadges();

  // ── 7. Bookmark / Star system ──
  var STAR_KEY = 'guide-starred-sections';
  function getStarred() { try { return JSON.parse(localStorage.getItem(STAR_KEY)) || {}; } catch(e) { return {}; } }
  function saveStarred(d) { localStorage.setItem(STAR_KEY, JSON.stringify(d)); }
  var starred = getStarred();
  var starFilterActive = false;

  allLinks.forEach(function(link) {
    var id = link.getAttribute('href').slice(1);
    var star = document.createElement('span');
    star.className = 'nav-star' + (starred[id] ? ' starred' : '');
    star.innerHTML = '&#9733;';
    star.title = 'Bookmark this section';
    link.appendChild(star);

    star.addEventListener('click', function(e) {
      e.preventDefault();
      e.stopPropagation();
      var isStarred = star.classList.toggle('starred');
      if (isStarred) starred[id] = true;
      else delete starred[id];
      saveStarred(starred);
    });
  });

  // Star filter button
  var starFilterBtn = document.getElementById('navStarFilter');
  if (starFilterBtn) {
    starFilterBtn.addEventListener('click', function() {
      starFilterActive = !starFilterActive;
      starFilterBtn.classList.toggle('active', starFilterActive);
      allLinks.forEach(function(link) {
        var id = link.getAttribute('href').slice(1);
        if (starFilterActive && !starred[id]) link.style.display = 'none';
        else link.style.display = '';
      });
    });
  }

  // ── 8. Export / Import progress ──
  var exportBtn = document.getElementById('navExportBtn');
  var importBtn = document.getElementById('navImportBtn');
  var importFileInput = document.getElementById('importFileInput');

  if (exportBtn) {
    exportBtn.addEventListener('click', function() {
      var data = {
        completed: completed,
        starred: starred,
        notes: window.__guideNotes || {},
        theme: localStorage.getItem('guide-theme'),
        exportedAt: new Date().toISOString(),
        version: 3
      };
      var blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
      var url = URL.createObjectURL(blob);
      var a = document.createElement('a');
      a.href = url;
      a.download = 'interview-guide-progress.json';
      a.click();
      URL.revokeObjectURL(url);
    });
  }
  if (importBtn && importFileInput) {
    importBtn.addEventListener('click', function() { importFileInput.click(); });
    importFileInput.addEventListener('change', function(e) {
      var file = e.target.files[0];
      if (!file) return;
      var reader = new FileReader();
      reader.onload = function(ev) {
        try {
          var data = JSON.parse(ev.target.result);
          if (data.completed) {
            Object.keys(data.completed).forEach(function(k) { completed[k] = true; });
            saveCompleted(completed);
          }
          if (data.starred) {
            Object.keys(data.starred).forEach(function(k) { starred[k] = true; });
            saveStarred(starred);
          }
          // Import notes
          if (data.notes) {
            var NOTES_KEY = 'guide-section-notes';
            var existingNotes = {};
            try { existingNotes = JSON.parse(localStorage.getItem(NOTES_KEY)) || {}; } catch(e) {}
            Object.keys(data.notes).forEach(function(k) { existingNotes[k] = data.notes[k]; });
            localStorage.setItem(NOTES_KEY, JSON.stringify(existingNotes));
            if (window.__guideNotes) Object.keys(data.notes).forEach(function(k) { window.__guideNotes[k] = data.notes[k]; });
          }
          // Refresh UI
          allLinks.forEach(function(link) {
            var id = link.getAttribute('href').slice(1);
            var chk = link.querySelector('.nav-check');
            var st = link.querySelector('.nav-star');
            if (chk) { chk.classList.toggle('checked', !!completed[id]); }
            link.classList.toggle('completed', !!completed[id]);
            if (st) { st.classList.toggle('starred', !!starred[id]); }
          });
          refreshProgress();
          refreshGroupBadges();
          var noteCount = Object.keys(data.notes || {}).length;
          alert('Progress imported successfully! (' + Object.keys(data.completed || {}).length + ' sections, ' + noteCount + ' notes)');
          if (noteCount > 0) location.reload(); // reload to show imported notes
        } catch(err) { alert('Invalid file format.'); }
      };
      reader.readAsText(file);
      importFileInput.value = '';
    });
  }

  // ── 9. Reading time estimates ──
  allLinks.forEach(function(link) {
    var id = link.getAttribute('href').slice(1);
    var target = document.getElementById(id);
    if (!target) return;
    // Estimate: find next h2 or end
    var text = '';
    var el = target;
    while (el = el.nextElementSibling) {
      if (el.tagName === 'H2') break;
      text += el.textContent + ' ';
    }
    var words = text.trim().split(/\s+/).length;
    var mins = Math.max(1, Math.round(words / 200));
    var badge = document.createElement('span');
    badge.className = 'reading-time';
    badge.textContent = mins + 'm';
    badge.title = mins + ' min read (~' + words + ' words)';
    link.appendChild(badge);
  });

  // ── 10. Confetti at 100% ──
  var confettiShown = false;
  function checkConfetti() {
    var done = Object.keys(completed).length;
    if (done >= totalSections && totalSections > 0 && !confettiShown) {
      confettiShown = true;
      launchConfetti();
    }
  }

  function launchConfetti() {
    var canvas = document.createElement('canvas');
    canvas.className = 'confetti-canvas';
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
    document.body.appendChild(canvas);
    var ctx = canvas.getContext('2d');
    var particles = [];
    var colors = ['#059669','#2563eb','#7c3aed','#f59e0b','#ef4444','#ec4899','#6ee7b7','#fbbf24'];
    for (var i = 0; i < 150; i++) {
      particles.push({
        x: Math.random() * canvas.width,
        y: Math.random() * canvas.height - canvas.height,
        w: Math.random() * 8 + 4,
        h: Math.random() * 6 + 2,
        color: colors[Math.floor(Math.random() * colors.length)],
        vx: (Math.random() - 0.5) * 4,
        vy: Math.random() * 3 + 2,
        rot: Math.random() * 360,
        vr: (Math.random() - 0.5) * 10
      });
    }
    var frame = 0;
    function animate() {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      var alive = false;
      particles.forEach(function(p) {
        p.x += p.vx;
        p.y += p.vy;
        p.vy += 0.05;
        p.rot += p.vr;
        if (p.y < canvas.height + 50) alive = true;
        ctx.save();
        ctx.translate(p.x, p.y);
        ctx.rotate(p.rot * Math.PI / 180);
        ctx.fillStyle = p.color;
        ctx.fillRect(-p.w/2, -p.h/2, p.w, p.h);
        ctx.restore();
      });
      frame++;
      if (alive && frame < 300) requestAnimationFrame(animate);
      else canvas.remove();
    }
    animate();
  }

  // Patch the original checkmark click to also check confetti
  var origRefresh = refreshProgress;
  refreshProgress = function() {
    origRefresh();
    checkConfetti();
  };
  refreshProgress();

})();

// ── Streak Tracker ──
(function() {
  var KEY = 'guide-streak-data';
  function getData() { try { return JSON.parse(localStorage.getItem(KEY)) || {}; } catch(e) { return {}; } }
  function saveData(d) { localStorage.setItem(KEY, JSON.stringify(d)); }

  var today = new Date().toISOString().slice(0, 10);
  var data = getData();
  if (!data.days) data.days = [];
  if (data.days[data.days.length - 1] !== today) {
    data.days.push(today);
    if (data.days.length > 60) data.days = data.days.slice(-60);
    saveData(data);
  }

  // Calculate streak
  var streak = 0;
  var d = new Date();
  for (var i = data.days.length - 1; i >= 0; i--) {
    var expected = d.toISOString().slice(0, 10);
    if (data.days[i] === expected) {
      streak++;
      d.setDate(d.getDate() - 1);
    } else break;
  }

  var countEl = document.getElementById('streakCount');
  var dotsEl = document.getElementById('streakDots');
  if (countEl) countEl.textContent = streak;

  // Show last 7 days
  if (dotsEl) {
    for (var j = 6; j >= 0; j--) {
      var dd = new Date();
      dd.setDate(dd.getDate() - j);
      var ds = dd.toISOString().slice(0, 10);
      var dot = document.createElement('span');
      dot.className = 'streak-dot';
      if (data.days.indexOf(ds) !== -1) dot.classList.add('active');
      if (ds === today) dot.classList.add('today');
      dot.title = ds;
      dotsEl.appendChild(dot);
    }
  }
})();

// ── Font Size Controls ──
(function() {
  var KEY = 'guide-font-size';
  var saved = parseInt(localStorage.getItem(KEY)) || 15;
  var min = 12, max = 22;
  document.querySelector('main').style.fontSize = saved + 'px';

  document.getElementById('fontUp').addEventListener('click', function() {
    saved = Math.min(max, saved + 1);
    document.querySelector('main').style.fontSize = saved + 'px';
    localStorage.setItem(KEY, saved);
  });
  document.getElementById('fontDown').addEventListener('click', function() {
    saved = Math.max(min, saved - 1);
    document.querySelector('main').style.fontSize = saved + 'px';
    localStorage.setItem(KEY, saved);
  });
})();

// ── Flashcard / Quiz Mode ──
(function() {
  var overlay = document.getElementById('flashcardOverlay');
  var card = document.getElementById('flashcard');
  var qEl = document.getElementById('fcQuestion');
  var aEl = document.getElementById('fcAnswer');
  var counterEl = document.getElementById('fcCounter');
  var cards = [];
  var idx = 0;

  // Build cards from .interview-q sections
  document.querySelectorAll('.interview-q').forEach(function(iq) {
    var h4 = iq.querySelector('h4');
    var ps = iq.querySelectorAll('p');
    var q = h4 ? h4.textContent : '';
    var a = '';
    ps.forEach(function(p) { a += p.textContent + '\n'; });
    if (q) cards.push({ q: q, a: a.trim() || 'See the section for details.' });
  });

  function show(i) {
    if (cards.length === 0) { qEl.textContent = 'No flashcards found.'; aEl.textContent = ''; return; }
    idx = ((i % cards.length) + cards.length) % cards.length;
    qEl.textContent = cards[idx].q;
    aEl.textContent = cards[idx].a;
    counterEl.textContent = (idx + 1) + ' / ' + cards.length;
    card.classList.remove('flipped');
  }

  card.addEventListener('click', function() { card.classList.toggle('flipped'); });
  document.getElementById('fcPrev').addEventListener('click', function(e) { e.stopPropagation(); show(idx - 1); });
  document.getElementById('fcNext').addEventListener('click', function(e) { e.stopPropagation(); show(idx + 1); });
  document.getElementById('fcShuffle').addEventListener('click', function(e) {
    e.stopPropagation();
    for (var i = cards.length - 1; i > 0; i--) {
      var j = Math.floor(Math.random() * (i + 1));
      var t = cards[i]; cards[i] = cards[j]; cards[j] = t;
    }
    show(0);
  });
  document.getElementById('flashcardClose').addEventListener('click', function() { overlay.classList.remove('active'); });
  overlay.addEventListener('click', function(e) { if (e.target === overlay) overlay.classList.remove('active'); });

  document.getElementById('navFlashcardBtn').addEventListener('click', function() {
    overlay.classList.add('active');
    show(0);
  });
})();

// ── Personal Notes per Section ──
(function() {
  var NOTES_KEY = 'guide-section-notes';

  function getNotes() {
    try { return JSON.parse(localStorage.getItem(NOTES_KEY)) || {}; } catch(e) { return {}; }
  }
  function saveNotes(d) {
    localStorage.setItem(NOTES_KEY, JSON.stringify(d));
  }

  var notes = getNotes();

  // Find all h2 section headers and inject notes widget after each
  document.querySelectorAll('h2[id]').forEach(function(h2) {
    var sectionId = h2.id;
    var existingNote = notes[sectionId] || '';

    var widget = document.createElement('div');
    widget.className = 'section-notes' + (existingNote ? ' has-note' : '');

    var header = document.createElement('div');
    header.className = 'notes-header';
    header.innerHTML = '<span class="notes-icon">&#128221;</span>' +
      '<span class="notes-title">My Notes</span>' +
      '<span class="notes-badge">Saved</span>' +
      '<span class="notes-toggle-arrow">&#9660;</span>';

    var body = document.createElement('div');
    body.className = 'notes-body';

    var textarea = document.createElement('textarea');
    textarea.className = 'notes-textarea';
    textarea.placeholder = 'Write your personal notes for this section...';
    textarea.value = existingNote;
    textarea.maxLength = 5000;

    var charCount = document.createElement('div');
    charCount.className = 'notes-char-count';
    charCount.textContent = existingNote.length + ' / 5000';

    var actions = document.createElement('div');
    actions.className = 'notes-actions';

    var saveBtn = document.createElement('button');
    saveBtn.className = 'notes-save-btn';
    saveBtn.textContent = '\u2714 Save Note';

    var deleteBtn = document.createElement('button');
    deleteBtn.className = 'notes-delete-btn';
    deleteBtn.textContent = '\u2716 Delete Note';

    var savedMsg = document.createElement('span');
    savedMsg.className = 'notes-saved-msg';
    savedMsg.textContent = '\u2713 Saved!';

    actions.appendChild(saveBtn);
    actions.appendChild(deleteBtn);
    actions.appendChild(savedMsg);

    body.appendChild(textarea);
    body.appendChild(charCount);
    body.appendChild(actions);
    widget.appendChild(header);
    widget.appendChild(body);

    // Insert after h2
    if (h2.nextSibling) h2.parentNode.insertBefore(widget, h2.nextSibling);
    else h2.parentNode.appendChild(widget);

    // If has existing note, auto-open
    if (existingNote) widget.classList.add('open');

    // Toggle open/close
    header.addEventListener('click', function() {
      widget.classList.toggle('open');
    });

    // Char count
    textarea.addEventListener('input', function() {
      charCount.textContent = textarea.value.length + ' / 5000';
    });

    // Save — persists immediately
    saveBtn.addEventListener('click', function() {
      var val = textarea.value.trim();
      if (!val) return; // empty = don't save blank
      notes[sectionId] = val;
      saveNotes(notes);
      widget.classList.add('has-note');
      savedMsg.classList.add('show');
      setTimeout(function() { savedMsg.classList.remove('show'); }, 2000);
    });

    // Also save on blur (auto-save if there's content)
    textarea.addEventListener('blur', function() {
      var val = textarea.value.trim();
      if (val && val !== (notes[sectionId] || '')) {
        notes[sectionId] = val;
        saveNotes(notes);
        widget.classList.add('has-note');
        savedMsg.classList.add('show');
        setTimeout(function() { savedMsg.classList.remove('show'); }, 2000);
      }
    });

    // Delete — requires double confirmation
    deleteBtn.addEventListener('click', function() {
      if (!confirm('Delete your note for this section?')) return;
      if (!confirm('Are you sure? This note will be permanently deleted.')) return;
      textarea.value = '';
      delete notes[sectionId];
      saveNotes(notes);
      widget.classList.remove('has-note');
      charCount.textContent = '0 / 5000';
    });
  });

  // Include notes in export (patch the export button)
  var origExportBtn = document.getElementById('navExportBtn');
  if (origExportBtn) {
    var origClick = origExportBtn.onclick;
    origExportBtn.addEventListener('click', function(e) {
      // The existing export will run, but let's override to include notes
    });
    // We'll patch via the export function below
  }

  // Make notes available globally for export
  window.__guideNotes = notes;
})();

// ── Keyboard Shortcuts ──
(function() {
  var kbdHint = document.getElementById('kbdHint');
  var hintVisible = false;
  var allNavLinks = Array.from(document.querySelectorAll('.nav-group-items a[href^="#"]'));
  var searchInput = document.getElementById('navSearch');
  var fcOverlay = document.getElementById('flashcardOverlay');

  function getActiveIdx() {
    for (var i = 0; i < allNavLinks.length; i++) {
      if (allNavLinks[i].classList.contains('active')) return i;
    }
    return 0;
  }

  function navigateToLink(link) {
    var href = link.getAttribute('href');
    var target = document.querySelector(href);
    if (target) target.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }

  document.addEventListener('keydown', function(e) {
    // Don't handle if typing in an input
    if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA' || e.target.isContentEditable) {
      if (e.key === 'Escape') e.target.blur();
      return;
    }
    // Close flashcard on Escape
    if (e.key === 'Escape') {
      if (fcOverlay.classList.contains('active')) { fcOverlay.classList.remove('active'); return; }
      if (hintVisible) { kbdHint.classList.remove('visible'); hintVisible = false; return; }
    }

    var key = e.key.toLowerCase();

    if (key === '?' || (key === '/' && e.shiftKey)) {
      e.preventDefault();
      hintVisible = !hintVisible;
      kbdHint.classList.toggle('visible', hintVisible);
      return;
    }
    if (key === '/') {
      e.preventDefault();
      searchInput.focus();
      return;
    }
    if (key === 'j' || key === 'k') {
      e.preventDefault();
      var ci = getActiveIdx();
      var ni = key === 'j' ? Math.min(ci + 1, allNavLinks.length - 1) : Math.max(ci - 1, 0);
      navigateToLink(allNavLinks[ni]);
      return;
    }
    if (key === ' ' && !e.shiftKey) {
      e.preventDefault();
      var ci2 = getActiveIdx();
      var chk = allNavLinks[ci2].querySelector('.nav-check');
      if (chk) chk.click();
      return;
    }
    if (key === 'b') {
      var ci3 = getActiveIdx();
      var star = allNavLinks[ci3].querySelector('.nav-star');
      if (star) star.click();
      return;
    }
    if (key === 'f') {
      e.preventDefault();
      document.getElementById('navFlashcardBtn').click();
      return;
    }
  });
})();
</script>
</body>
</html>
'''

# BUILD
parts = [HEAD, STUDY_PATH, JS_SECTIONS, DOM_HTML_SECTIONS, CSS_SECTIONS, TS_PERF_SECTIONS,
         SEC_NET_SECTIONS, TEST_BUILD_SECTIONS, A11Y_PATTERNS_SECTIONS,
         SYSTEM_MISC_SECTIONS, ANGULAR_SECTIONS, ADVANCED_SECTIONS,
         CODING_1_SECTIONS, CODING_2_SECTIONS, CODING_3_SECTIONS, FOOTER]
content = "\n".join(parts)
OUT.write_text(content, encoding="utf-8")
print(f"✅ Generated: {OUT}")
print(f"   Size: {OUT.stat().st_size / 1024:.0f} KB")
