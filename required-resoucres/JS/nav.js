(function () {
  const pages = [
    { file: 'index.html', label: '📚 Index' },
    { file: 'phase1-foundations-how-js-works.html', label: 'P1 · Foundations: How JS Works' },
    { file: 'phase2-functions-scope-closures.html', label: 'P2 · Functions, Scope & Closures' },
    { file: 'phase3-objects-arrays-deep-dive.html', label: 'P3 · Objects & Arrays Deep Dive' },
    { file: 'phase4-prototypes-classes-oop.html', label: 'P4 · Prototypes, Classes & OOP' },
    { file: 'phase5-async-event-loop.html', label: 'P5 · Async & Event Loop' },
    { file: 'phase5A-generators-output-drills.html', label: 'P5A · Generators & Output Drills' },
    { file: 'phase5B-interview-qa-nodejs.html', label: 'P5B · Interview Q&A & Node.js' },
    { file: 'phase6-dom-events-browser-apis.html', label: 'P6 · DOM, Events & Browser APIs' },
    { file: 'phase6A-rendering-webcomponents-lifecycle.html', label: 'P6A · Rendering & Web Components' },
    { file: 'phase6B-interview-qa-exercises.html', label: 'P6B · Interview Q&A Exercises' },
    { file: 'phase7-es6-design-patterns.html', label: 'P7 · ES6+ & Design Patterns' },
    { file: 'phase8-advanced-interview-masterclass.html', label: 'P8 · Advanced Interview Masterclass' },
    { file: 'phase9-polyfills-machine-coding.html', label: 'P9 · Polyfills & Machine Coding' },
    { file: 'phase10-output-prediction-tricky.html', label: 'P10 · Output Prediction & Tricky' },
    { file: 'phase11-frontend-system-design.html', label: 'P11 · Frontend System Design' },
    { file: 'phase12-javascript-performance-mastery.html', label: 'P12 · JS Performance Mastery' },
    { file: 'phase13-real-interview-questions.html', label: 'P13 · Real Interview Questions' },
    { file: 'phase14-senior-architect-patterns.html', label: 'P14 · Senior Architect Patterns' },
    { file: 'machine-coding-part1-ui-components.html', label: 'MC1 · UI Components', section: 'Machine Coding' },
    { file: 'machine-coding-part2-utility-implementations.html', label: 'MC2 · Utility Implementations' },
    { file: 'machine-coding-part3-advanced-patterns.html', label: 'MC3 · Advanced Patterns' },
    { file: 'machine-coding-part4-high-frequency.html', label: 'MC4 · High Frequency' },
    { file: 'machine-coding-part5-games-utilities.html', label: 'MC5 · Games & Utilities' },
    { file: 'machine-coding-part6-utilities.html', label: 'MC6 · Utilities' },
    { file: 'machine-coding-part7-production-scale.html', label: 'MC7 · Production Scale' },
    { file: 'machine-coding-async-patterns.html', label: 'MCA · Async Patterns' },
    { file: 'js-notes.html', label: '📝 JS Notes', section: 'Extras' },
    { file: 'js-progress-tracker.html', label: '📊 Progress Tracker' },
  ];

  const currentFile = location.pathname.split('/').pop();

  const style = document.createElement('style');
  style.textContent = `
    .sidebar-nav {
      position: fixed; top: 0; left: 0; z-index: 9990;
      width: 300px; height: 100vh; overflow-y: auto;
      background: #fffdf8; border-right: 1px solid #e8e0d4;
      box-shadow: 2px 0 12px rgba(0,0,0,0.06);
      padding: 0 0 24px;
      font-family: "Avenir Next", "Helvetica Neue", sans-serif;
      transition: transform 0.25s ease;
    }
    .sidebar-nav::-webkit-scrollbar { width: 5px; }
    .sidebar-nav::-webkit-scrollbar-thumb { background: #d8d0c3; border-radius: 4px; }

    .sidebar-nav .sidebar-brand {
      position: sticky; top: 0; z-index: 2;
      padding: 14px 16px; font-weight: 800; font-size: 14px;
      color: #e65100; letter-spacing: 0.3px;
      background: #fffdf8; border-bottom: 1px solid #ffe0b2;
    }

    .sidebar-nav .nav-divider {
      padding: 10px 16px 4px; font-weight: 800; font-size: 10px;
      color: #888; text-transform: uppercase; letter-spacing: 0.8px;
      border-top: 1px solid #e8e0d4; margin-top: 6px;
    }

    .sidebar-nav a.phase-link {
      display: block; padding: 7px 16px; text-decoration: none;
      color: #333; font-size: 13px; font-weight: 500;
      border-left: 3px solid transparent;
      transition: background 0.12s, color 0.12s, border-color 0.12s;
    }
    .sidebar-nav a.phase-link:hover { background: #fff3e0; color: #e65100; }
    .sidebar-nav a.phase-link.active {
      background: #fff3e0; border-left-color: #f5a623;
      color: #e65100; font-weight: 700;
    }

    .sidebar-nav .section-list {
      overflow: hidden; background: #fdf8f2;
      border-left: 3px solid #ffe0b2; margin-left: 0;
    }
    .sidebar-nav .section-list a {
      display: block; padding: 5px 14px 5px 28px; text-decoration: none;
      color: #666; font-size: 12px;
      transition: all 0.1s;
    }
    .sidebar-nav .section-list a:hover { color: #e65100; background: #fff8f0; }
    .sidebar-nav .section-list a.sec-active {
      color: #e65100; font-weight: 600; background: #fff8f0;
    }

    body { margin-left: 270px !important; }
    main { max-width: 900px !important; }

    .sidebar-toggle {
      display: none; position: fixed; top: 12px; left: 12px; z-index: 9999;
      width: 44px; height: 44px; border-radius: 8px;
      background: #f5a623; color: #fff; border: none; cursor: pointer;
      font-size: 22px; align-items: center; justify-content: center;
      box-shadow: 0 2px 8px rgba(245,166,35,0.3);
    }
    @media (max-width: 900px) {
      .sidebar-nav { transform: translateX(-100%); }
      .sidebar-nav.open { transform: translateX(0); box-shadow: 4px 0 20px rgba(0,0,0,0.15); }
      body { margin-left: 0 !important; }
      main { max-width: 100% !important; }
      .sidebar-toggle { display: flex; }
    }
  `;
  document.head.appendChild(style);

  const sidebar = document.createElement('nav');
  sidebar.className = 'sidebar-nav';
  sidebar.innerHTML = '<div class="sidebar-brand">⚡ JavaScript Mastery</div>';

  let lastSection = '';
  pages.forEach(p => {
    if (p.section && p.section !== lastSection) {
      lastSection = p.section;
      const div = document.createElement('div');
      div.className = 'nav-divider';
      div.textContent = p.section;
      sidebar.appendChild(div);
    }

    const isCurrent = (p.file === currentFile);
    const a = document.createElement('a');
    a.className = 'phase-link' + (isCurrent ? ' active' : '');
    a.href = isCurrent ? '#' : p.file;
    a.textContent = p.label;
    if (isCurrent) a.addEventListener('click', (e) => { e.preventDefault(); window.scrollTo({ top: 0, behavior: 'smooth' }); });
    sidebar.appendChild(a);

    if (isCurrent) {
      const secDiv = document.createElement('div');
      secDiv.className = 'section-list';
      sidebar.appendChild(secDiv);

      window.addEventListener('DOMContentLoaded', () => {
        const headings = document.querySelectorAll('h2[id]');
        headings.forEach(h => {
          const link = document.createElement('a');
          link.href = '#' + h.id;
          link.textContent = h.textContent.replace(/^\d+\.\s*/, '').trim();
          link.addEventListener('click', (e) => {
            e.preventDefault();
            h.scrollIntoView({ behavior: 'smooth', block: 'start' });
          });
          secDiv.appendChild(link);
        });

        if (headings.length) {
          const links = secDiv.querySelectorAll('a');
          const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
              if (entry.isIntersecting) {
                links.forEach(l => l.classList.remove('sec-active'));
                const match = secDiv.querySelector('a[href="#' + entry.target.id + '"]');
                if (match) match.classList.add('sec-active');
              }
            });
          }, { rootMargin: '-5% 0px -75% 0px' });
          headings.forEach(h => observer.observe(h));
        }
      });
    }
  });

  document.body.appendChild(sidebar);

  const toggleBtn = document.createElement('button');
  toggleBtn.className = 'sidebar-toggle';
  toggleBtn.innerHTML = '☰';
  toggleBtn.addEventListener('click', () => sidebar.classList.toggle('open'));
  document.body.appendChild(toggleBtn);

  sidebar.addEventListener('click', (e) => {
    if (e.target.tagName === 'A' && window.innerWidth <= 900) {
      setTimeout(() => sidebar.classList.remove('open'), 200);
    }
  });
})();
