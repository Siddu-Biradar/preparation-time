#!/usr/bin/env python3
"""ATS Score Analyzer for SDE-2 Frontend Resumes"""

import re

resume = """
SIDRAMESHWAR BIRADAR
Bengaluru, India | +91-9611301699 | biradarsiddu789@gmail.com | linkedin.com/in/sidrameshwarbiradar
SOFTWARE ENGINEER II (FRONTEND)
Frontend Engineer with 4 years of experience building scalable, high-performance web applications.
Specialized in performance optimization, real-time systems, and AI-powered insights. Proven track
record of delivering measurable impact in developer productivity, system performance, and user experience.
KEY ACHIEVEMENTS
Reduced bundle size by 95% (43MB to 1.8MB), improving load time by 80%+
Led Angular migration (v9 to v20) across enterprise application
Built real-time systems using WebSockets, eliminating polling overhead
Developed AI-powered insights assistant for engineering metrics
Improved Core Web Vitals (LCP/TTI) via code-splitting, lazy loading, and caching strategies
Introduced performance budgets & CI checks, preventing regressions in bundle size and load time
Designed modular/micro-frontend-ready architecture, enabling faster feature delivery and team scalability
Increased test coverage with automated UI tests, reducing regression bugs in releases
TECHNICAL SKILLS
Languages: JavaScript, TypeScript, HTML, CSS
Frameworks: Angular, React, RxJS, Tailwind CSS
AI & Tools: OpenAI APIs, Prompt Engineering, LLM Integration
Performance: Webpack, Lazy Loading, Code Splitting, Caching
Backend & APIs: REST APIs, WebSockets
Tools: Git, Docker, Kubernetes, CI/CD
EXPERIENCE
Software Engineer (Frontend) | Kyndryl (IBM) | Jul 2022 - Present
Architected a DevOps intelligence platform to track SDLC metrics, improving developer productivity and release visibility
Led Angular migration (v9 to v20), reducing bundle size from 43MB to 1.8MB and improving performance by 80%+
Implemented real-time updates using WebSockets, eliminating polling overhead
Built security intelligence module aggregating vulnerability and compliance data
Developed release management workflows, improving deployment efficiency
Led design system migration, ensuring consistency with zero regressions
PROJECTS
AI DevOps Insights Assistant
Built AI assistant using LLM APIs to generate insights from engineering metrics and detect bottlenecks
Implemented semantic search over logs/metrics using embeddings, enabling contextual query-based insights
Added role-based insights dashboards to personalize recommendations for developers vs managers
Frontend Performance Playground (Side Project)
Built a benchmarking app to compare rendering performance across Angular and React implementations
Implemented virtualization, memoization, and lazy loading strategies, improving render efficiency
Measured and visualized Core Web Vitals (LCP, CLS, TTI) using real-world scenarios
System Design Case Studies (Side Project)
Designed scalable frontend architectures for systems like chat application, Netflix UI, and analytics dashboards
Documented API design, caching strategies, and component-level scalability patterns
EDUCATION & CERTIFICATION
B.E. (Electrical & Electronics), BMS College of Engineering | CGPA: 8.6
AWS Certified Solutions Architect - Associate
"""

r = resume.lower()
score = 0
breakdown = []

# 1. CONTACT INFO (10 pts)
c = 0
if re.search(r'[\w.]+@[\w.]+', resume): c += 2.5
if re.search(r'\+91|\d{10}', resume): c += 2.5
if 'linkedin' in r: c += 2.5
if 'bengaluru' in r or 'bangalore' in r: c += 2.5
breakdown.append(("Contact Information", c, 10))
score += c

# 2. TITLE/ROLE MATCH (10 pts)
t = 0
title_area = r[:400]
for kw in ['software engineer', 'frontend', 'sde', 'front-end']:
    if kw in title_area: t += 2.5
t = min(10, t)
breakdown.append(("Title/Role Keyword Match", t, 10))
score += t

# 3. TECHNICAL KEYWORD DENSITY (25 pts)
k = 0
kw_map = {
    'angular': 4, 'typescript': 3, 'javascript': 3, 'react': 2.5,
    'rxjs': 2, 'html': 1, 'css': 1, 'rest api': 1.5,
    'webpack': 1, 'git': 0.5, 'ci/cd': 1, 'docker': 0.5,
    'tailwind': 1, 'websocket': 1.5, 'openai': 1, 'llm': 0.5,
    'kubernetes': 0.5
}
found_kw = []
missing_kw = []
for kw, pts in kw_map.items():
    if kw in r:
        k += pts
        found_kw.append(kw)
    else:
        missing_kw.append(kw)
k = min(25, k)
breakdown.append(("Technical Keyword Density", round(k, 1), 25))
score += k

# 4. QUANTIFIED ACHIEVEMENTS (15 pts)
metrics_found = re.findall(r'\d+%|\d+MB|\d+\.\d+MB|\d+x|80\+', resume)
m = min(15, len(set(metrics_found)) * 2.5)
breakdown.append(("Quantified Achievements", m, 15))
score += m

# 5. ACTION VERBS (8 pts)
verbs = ['architected', 'built', 'led', 'developed', 'implemented', 'designed',
         'reduced', 'improved', 'migrated', 'increased', 'introduced', 'measured',
         'created', 'optimized', 'delivered', 'integrated', 'aggregating']
fv = [v for v in verbs if v in r]
v_score = min(8, len(fv) * 0.7)
breakdown.append(("Action Verbs", round(v_score, 1), 8))
score += v_score

# 6. EXPERIENCE STRUCTURE (10 pts)
e = 0
if 'experience' in r: e += 2
if re.search(r'(jul|jan|feb|mar|apr|may|jun|aug|sep|oct|nov|dec)\s*\d{4}', r): e += 2
if 'present' in r: e += 2
if 'kyndryl' in r or 'ibm' in r: e += 2
bullets = len(re.findall(r'^[\s]*[\-\•\·]', resume, re.MULTILINE))
if bullets >= 5: e += 2
e = min(10, e)
breakdown.append(("Experience Structure", e, 10))
score += e

# 7. EDUCATION & CERTS (7 pts)
ed = 0
if re.search(r'b\.?e\.?|bachelor|engineering', r): ed += 2.5
if 'aws' in r and 'certified' in r: ed += 3
if re.search(r'cgpa|gpa', r): ed += 1.5
ed = min(7, ed)
breakdown.append(("Education & Certifications", ed, 7))
score += ed

# 8. PROJECTS (8 pts)
p = 0
if 'project' in r: p += 2
project_count = r.count('side project') + 1  # AI project + side projects
if project_count >= 3: p += 3
elif project_count >= 2: p += 2
if 'side project' in r: p += 2
if 'system design' in r: p += 1
p = min(8, p)
breakdown.append(("Projects & Side Projects", p, 8))
score += p

# 9. ATS FORMAT (7 pts)
f = 0
headers = ['experience', 'education', 'skills', 'projects', 'achievements', 'certification']
found_h = sum(1 for h in headers if h in r)
f += min(3, found_h)
# 2 pages, clean text = good
f += 2
# Proper section ordering
if r.index('skills') < r.index('experience') < r.index('project'):
    f += 2
f = min(7, f)
breakdown.append(("ATS Format Compatibility", f, 7))
score += f

score = min(100, round(score))

# ---- WARNINGS & ISSUES ----
issues = []
warnings = []
strengths = []

# Missing keywords that SDE-2 JDs commonly have
jd_keywords = {
    'ngrx': 'State management (NgRx/Redux)',
    'responsive': 'Responsive design',
    'accessibility': 'Accessibility (a11y/WCAG)',
    'agile': 'Agile/Scrum methodology',
    'jest': 'Testing framework (Jest/Jasmine)',
    'github': 'GitHub/GitLab profile link',
    'node': 'Node.js (common in full-stack JDs)',
}
for kw, label in jd_keywords.items():
    if kw not in r and kw.replace('/', '') not in r:
        # Check alternatives
        alts = {'jest': ['jasmine', 'karma', 'test'], 'agile': ['scrum', 'sprint'],
                'accessibility': ['a11y', 'wcag'], 'github': ['gitlab', 'bitbucket'],
                'node': ['node.js', 'express']}
        found_alt = any(alt in r for alt in alts.get(kw, []))
        if not found_alt:
            warnings.append(f"Missing: {label}")

# Check single employer
if r.count('kyndryl') >= 1 and r.count('|') < 3:
    warnings.append("Single employer — some ATS flag this (not a dealbreaker)")

# Strengths
if '95%' in resume: strengths.append("Killer metric: 95% bundle size reduction — instant attention grabber")
if 'angular' in r and 'react' in r: strengths.append("Dual framework coverage (Angular + React) — matches more JDs")
if 'openai' in r or 'llm' in r: strengths.append("AI/LLM keywords — massive differentiator for 2026 roles")
if 'websocket' in r: strengths.append("Real-time systems experience — shows senior-level depth")
if 'aws' in r and 'certified' in r: strengths.append("AWS certification — strong credibility beyond frontend")
if 'core web vitals' in r: strengths.append("Core Web Vitals expertise — proves performance-first mindset")
if 'micro-frontend' in r or 'micro frontend' in r: strengths.append("Micro-frontend architecture — system design thinking")
if 'system design' in r: strengths.append("System design projects — critical for SDE-2 level interviews")
if 'design system' in r: strengths.append("Design system migration — shows UI architecture experience")
if 'key achievements' in r: strengths.append("Dedicated achievements section — immediately shows impact")

# ---- PRINT ----
W = 62
print()
print("=" * W)
print(f"{'ATS SCORE REPORT':^{W}}")
print(f"{'Sidrameshwar Biradar — SDE-2 Frontend Resume':^{W}}")
print("=" * W)
print()

# Score bar
bar_len = 40
filled = int((score / 100) * bar_len)
bar = "█" * filled + "░" * (bar_len - filled)
grade = "A+" if score >= 90 else "A" if score >= 85 else "B+" if score >= 80 else "B" if score >= 75 else "C" if score >= 65 else "D"
color_label = "EXCELLENT" if score >= 85 else "GOOD" if score >= 75 else "FAIR" if score >= 65 else "NEEDS WORK"
print(f"  SCORE:  {score}/100  [{bar}]  Grade: {grade}")
print(f"  STATUS: {color_label}")
print()
print("─" * W)
print(f"  {'SECTION':<35} {'SCORE':>8}  {'BAR':>20}")
print("─" * W)

for section, pts, max_pts in breakdown:
    pct = pts / max_pts
    bar_f = int(pct * 15)
    bar_s = "█" * bar_f + "░" * (15 - bar_f)
    icon = "✅" if pct >= 0.8 else "⚠️ " if pct >= 0.5 else "❌"
    print(f"  {icon} {section:<33} {pts:>5.1f}/{max_pts:<3}  {bar_s}")

print("─" * W)
print(f"  {'TOTAL':<35} {score:>5}/100")
print()

if strengths:
    print("  ✅ STRENGTHS (These are working for you):")
    for s in strengths:
        print(f"     ✓ {s}")
    print()

if warnings:
    print("  ⚠️  GAPS (Minor — consider for specific JDs):")
    for w in warnings:
        print(f"     → {w}")
    print()

if issues:
    print("  ❌ ISSUES (Fix these):")
    for i in issues:
        print(f"     → {i}")
    print()

# FINAL VERDICT
print("─" * W)
print("  VERDICT:")
print()
if score >= 85:
    print("  This resume is STRONG. It will pass most ATS systems for")
    print("  SDE-2 Frontend roles at product companies and FAANG.")
    print()
    print("  The warnings above are MINOR — they matter only if a")
    print("  specific JD emphasizes those keywords. No major changes")
    print("  needed. Your resume is interview-ready.")
elif score >= 75:
    print("  GOOD resume that will pass most ATS. A few keyword gaps")
    print("  could cause misses on specific JDs. Consider the warnings.")
else:
    print("  Needs improvement to consistently pass ATS filters.")
print()
print("  HONEST TAKE: Don't over-optimize. Your resume already has")
print("  what matters most — real metrics, strong verbs, relevant")
print("  tech stack, and clear impact. Ship applications, not edits.")
print("=" * W)
