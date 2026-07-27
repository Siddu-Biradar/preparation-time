(function () {
  const pages = [
    { file: 'angular-index.html', label: '📚 Index' },
    { file: 'phase1-angular-fundamentals.html', label: 'P1 · Fundamentals & Architecture' },
    { file: 'phase2-components-templates.html', label: 'P2 · Components & Templates' },
    { file: 'phase3-dependency-injection.html', label: 'P3 · Dependency Injection' },
    { file: 'phase4-rxjs-reactive-patterns.html', label: 'P4 · RxJS & Reactive Patterns' },
    { file: 'phase5-change-detection-performance.html', label: 'P5 · Change Detection & Perf' },
    { file: 'phase6-routing-navigation.html', label: 'P6 · Routing & Navigation' },
    { file: 'phase7-forms-validation.html', label: 'P7 · Forms & Validation' },
    { file: 'phase8-state-management.html', label: 'P8 · State Management' },
    { file: 'phase9-testing.html', label: 'P9 · Testing' },
    { file: 'phase10-advanced-patterns.html', label: 'P10 · Advanced Patterns' },
    { file: 'phase11-signals-modern-angular.html', label: 'P11 · Signals & Modern Angular' },
    { file: 'phase12-machine-coding.html', label: 'P12 · Machine Coding' },
    { file: 'phase13-interview-qa-masterclass.html', label: 'P13 · Interview Q&A' },
    { file: 'phase14-advanced-topics.html', label: 'P14 · Animations, CDK, i18n, PWA' },
    { file: 'phase15-internals-output-prediction.html', label: 'P15 · Internals & Output Prediction' },
    { file: 'phase16-ngrx-rxjs-advanced.html', label: 'P16 · NgRx & RxJS Advanced' },
  ];

  const currentFile = location.pathname.split('/').pop();

  const style = document.createElement('style');
  style.textContent = `
    .sidebar-nav {
      position: fixed; top: 0; left: 0; z-index: 9990;
      width: 270px; height: 100vh; overflow-y: auto;
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
      padding: 14px 16px; font-weight: 800; font-size: 13px;
      color: #c3002f; letter-spacing: 0.3px;
      background: #fffdf8; border-bottom: 1px solid #f8bbd0;
    }

    .sidebar-nav a.phase-link {
      display: block; padding: 8px 16px; text-decoration: none;
      color: #333; font-size: 12.5px; font-weight: 500;
      border-left: 3px solid transparent;
      transition: background 0.12s, color 0.12s, border-color 0.12s;
    }
    .sidebar-nav a.phase-link:hover { background: #fce4ec; color: #c3002f; }
    .sidebar-nav a.phase-link.active {
      background: #fce4ec; border-left-color: #c3002f;
      color: #c3002f; font-weight: 700;
    }

    .sidebar-nav .section-list {
      overflow: hidden; background: #fdf6f2;
      border-left: 3px solid #f8bbd0; margin-left: 0;
    }
    .sidebar-nav .section-list a {
      display: block; padding: 5px 14px 5px 28px; text-decoration: none;
      color: #666; font-size: 11px;
      transition: all 0.1s;
    }
    .sidebar-nav .section-list a:hover { color: #c3002f; background: #fff0f3; }
    .sidebar-nav .section-list a.sec-active {
      color: #c3002f; font-weight: 600; background: #fff0f3;
    }

    body { margin-left: 270px !important; }
    main { max-width: 900px !important; }

    .sidebar-toggle {
      display: none; position: fixed; top: 12px; left: 12px; z-index: 9999;
      width: 40px; height: 40px; border-radius: 8px;
      background: #c3002f; color: #fff; border: none; cursor: pointer;
      font-size: 18px; align-items: center; justify-content: center;
      box-shadow: 0 2px 8px rgba(195,0,47,0.3);
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
  sidebar.innerHTML = '<div class="sidebar-brand">🅰️ Angular Mastery</div>';

  pages.forEach(p => {
    const isCurrent = (p.file === currentFile);
    const a = document.createElement('a');
    a.className = 'phase-link' + (isCurrent ? ' active' : '');
    a.href = isCurrent ? '#' : p.file;
    a.textContent = p.label;
    if (isCurrent) a.addEventListener('click', (e) => { e.preventDefault(); window.scrollTo({ top: 0, behavior: 'smooth' }); });
    sidebar.appendChild(a);

    // Show sections for current page
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

        // Highlight on scroll
        if (headings.length) {
          const links = secDiv.querySelectorAll('a');
          const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
              if (entry.isIntersecting) {
                links.forEach(l => l.classList.remove('sec-active'));
                const match = secDiv.querySelector(`a[href="#${entry.target.id}"]`);
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

  // Mobile toggle
  const toggleBtn = document.createElement('button');
  toggleBtn.className = 'sidebar-toggle';
  toggleBtn.innerHTML = '☰';
  toggleBtn.addEventListener('click', () => sidebar.classList.toggle('open'));
  document.body.appendChild(toggleBtn);

  // Close on mobile after navigation
  sidebar.addEventListener('click', (e) => {
    if (e.target.tagName === 'A' && window.innerWidth <= 900) {
      setTimeout(() => sidebar.classList.remove('open'), 200);
    }
  });
})();
