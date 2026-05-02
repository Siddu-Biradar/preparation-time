"""
Add curated 'Top Resources' block to each of the 27 phases in complete-roadmap.html.
Only canonical, well-known URLs (official docs, MDN, web.dev, major YouTube channels, top blogs).
"""
import re
from pathlib import Path

FILE = Path(__file__).parent / "complete-roadmap.html"

# Resources: each phase -> list of (emoji, label, url)
# Categories: 📘 Docs, 🎥 Video/Course, ✍️ Blog/Article, 🎯 Interview
RESOURCES = {
    1: [  # Fundamentals
        ("📘", "MDN — How the web works", "https://developer.mozilla.org/en-US/docs/Learn/Getting_started_with_the_web/How_the_Web_works"),
        ("📘", "MDN — HTTP basics", "https://developer.mozilla.org/en-US/docs/Web/HTTP/Basics_of_HTTP"),
        ("🎥", "High Performance Browser Networking (book, free)", "https://hpbn.co/"),
        ("🎥", "Fireship — HTTP Crash Course", "https://www.youtube.com/watch?v=iYM2zFP3Zn0"),
        ("✍️", "How Browsers Work — Tali Garsiel", "https://web.dev/articles/howbrowserswork"),
        ("🎯", "roadmap.sh — Frontend", "https://roadmap.sh/frontend"),
    ],
    2: [  # HTML5
        ("📘", "MDN — HTML", "https://developer.mozilla.org/en-US/docs/Web/HTML"),
        ("📘", "MDN — HTML Forms", "https://developer.mozilla.org/en-US/docs/Learn/Forms"),
        ("✍️", "HTML5 Doctor — Semantic elements", "http://html5doctor.com/"),
        ("✍️", "web.dev — Learn HTML", "https://web.dev/learn/html"),
        ("🎥", "Kevin Powell — YouTube", "https://www.youtube.com/@KevinPowell"),
        ("🎯", "Frontend Interview Handbook — HTML", "https://www.frontendinterviewhandbook.com/"),
    ],
    3: [  # CSS3
        ("📘", "MDN — CSS", "https://developer.mozilla.org/en-US/docs/Web/CSS"),
        ("📘", "web.dev — Learn CSS", "https://web.dev/learn/css"),
        ("✍️", "CSS Tricks — Flexbox Guide", "https://css-tricks.com/snippets/css/a-guide-to-flexbox/"),
        ("✍️", "CSS Tricks — Grid Guide", "https://css-tricks.com/snippets/css/complete-guide-grid/"),
        ("✍️", "Josh Comeau — CSS for JS Devs", "https://www.joshwcomeau.com/css/"),
        ("🎥", "Kevin Powell — CSS Channel", "https://www.youtube.com/@KevinPowell"),
        ("📘", "Tailwind CSS Docs", "https://tailwindcss.com/docs"),
        ("📘", "Sass Docs", "https://sass-lang.com/documentation/"),
    ],
    4: [  # JavaScript
        ("📘", "javascript.info (The Modern JS Tutorial)", "https://javascript.info/"),
        ("📘", "MDN — JavaScript Guide", "https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide"),
        ("✍️", "You Don't Know JS (book series)", "https://github.com/getify/You-Dont-Know-JS"),
        ("🎥", "Philip Roberts — What the heck is the event loop?", "https://www.youtube.com/watch?v=8aGhZQkoFbQ"),
        ("🎥", "Jake Archibald — In the Loop (microtasks)", "https://www.youtube.com/watch?v=cCOL7MC4Pl0"),
        ("🎥", "Akshay Saini — Namaste JavaScript", "https://www.youtube.com/playlist?list=PLlasXeu85E9cQ32gLCvAvr9vNaUccPVNP"),
        ("✍️", "2ality by Axel Rauschmayer", "https://2ality.com/"),
        ("🎯", "BigFrontend.dev — JS coding challenges", "https://bigfrontend.dev/"),
        ("🎯", "GreatFrontEnd — JS Interview", "https://www.greatfrontend.com/"),
    ],
    5: [  # TypeScript
        ("📘", "TypeScript Handbook (official)", "https://www.typescriptlang.org/docs/handbook/intro.html"),
        ("📘", "Type Challenges", "https://github.com/type-challenges/type-challenges"),
        ("✍️", "Matt Pocock — Total TypeScript (tips)", "https://www.totaltypescript.com/tips"),
        ("🎥", "Matt Pocock — YouTube", "https://www.youtube.com/@mattpocockuk"),
        ("✍️", "TypeScript Deep Dive — Basarat", "https://basarat.gitbook.io/typescript/"),
        ("🎯", "Type Challenges interview set", "https://tsch.js.org/"),
    ],
    6: [  # Git
        ("📘", "Pro Git (book, free)", "https://git-scm.com/book/en/v2"),
        ("📘", "GitHub Docs", "https://docs.github.com/"),
        ("✍️", "Atlassian Git Tutorials", "https://www.atlassian.com/git/tutorials"),
        ("✍️", "Oh Shit, Git!?!", "https://ohshitgit.com/"),
        ("🎥", "The Net Ninja — Git & GitHub", "https://www.youtube.com/playlist?list=PL4cUxeGkcC9goXbgTDQ0n_4TBzOO0ocPR"),
        ("🎯", "Learn Git Branching (interactive)", "https://learngitbranching.js.org/"),
    ],
    7: [  # React
        ("📘", "React Docs (react.dev)", "https://react.dev/learn"),
        ("✍️", "Dan Abramov — overreacted.io", "https://overreacted.io/"),
        ("✍️", "Kent C. Dodds Blog", "https://kentcdodds.com/blog"),
        ("✍️", "Josh Comeau — React articles", "https://www.joshwcomeau.com/react/"),
        ("🎥", "Jack Herrington — YouTube", "https://www.youtube.com/@jherr"),
        ("🎥", "Theo - t3.gg", "https://www.youtube.com/@t3dotgg"),
        ("📘", "Epic React (Kent C. Dodds)", "https://www.epicreact.dev/"),
        ("🎯", "React Interview Questions — sudheerj", "https://github.com/sudheerj/reactjs-interview-questions"),
    ],
    8: [  # Angular
        ("📘", "Angular Docs (angular.dev)", "https://angular.dev/"),
        ("📘", "Angular CLI", "https://angular.dev/tools/cli"),
        ("📘", "NgRx Docs", "https://ngrx.io/"),
        ("✍️", "Angular University Blog", "https://blog.angular-university.io/"),
        ("🎥", "Joshua Morony — Modern Angular", "https://www.youtube.com/@JoshuaMorony"),
        ("🎥", "Decoded Frontend", "https://www.youtube.com/@DecodedFrontend"),
        ("✍️", "RxJS Docs", "https://rxjs.dev/"),
        ("🎯", "Angular Interview Questions — sudheerj", "https://github.com/sudheerj/angular-interview-questions"),
    ],
    9: [  # Next.js
        ("📘", "Next.js Docs", "https://nextjs.org/docs"),
        ("📘", "Next.js Learn (official course)", "https://nextjs.org/learn"),
        ("🎥", "Vercel — YouTube", "https://www.youtube.com/@VercelHQ"),
        ("🎥", "Lee Robinson — Next.js videos", "https://www.youtube.com/@leerob"),
        ("✍️", "Josh W Comeau — Next.js articles", "https://www.joshwcomeau.com/"),
        ("📘", "App Router Playbook — Lee Robinson", "https://leerob.io/"),
    ],
    10: [  # State Management
        ("📘", "Redux Toolkit Docs", "https://redux-toolkit.js.org/"),
        ("📘", "Zustand Docs", "https://zustand.docs.pmnd.rs/"),
        ("📘", "TanStack Query Docs", "https://tanstack.com/query/latest"),
        ("📘", "Apollo Client Docs", "https://www.apollographql.com/docs/react/"),
        ("✍️", "TkDodo's Blog (React Query author)", "https://tkdodo.eu/blog/"),
        ("🎥", "Jack Herrington — State management videos", "https://www.youtube.com/@jherr"),
        ("📘", "NgRx Docs", "https://ngrx.io/"),
    ],
    11: [  # Testing
        ("📘", "Testing Library Docs", "https://testing-library.com/"),
        ("📘", "Jest Docs", "https://jestjs.io/"),
        ("📘", "Playwright Docs", "https://playwright.dev/"),
        ("📘", "Cypress Docs", "https://docs.cypress.io/"),
        ("✍️", "Kent C. Dodds — Testing Trophy", "https://kentcdodds.com/blog/the-testing-trophy-and-testing-classifications"),
        ("📘", "Epic Testing (Kent C. Dodds)", "https://www.epicweb.dev/"),
        ("📘", "Storybook Docs", "https://storybook.js.org/docs"),
        ("📘", "MSW (Mock Service Worker)", "https://mswjs.io/"),
    ],
    12: [  # Performance
        ("📘", "web.dev — Core Web Vitals", "https://web.dev/articles/vitals"),
        ("📘", "web.dev — Performance", "https://web.dev/explore/learn-core-web-vitals"),
        ("✍️", "Addy Osmani — Web Performance", "https://addyosmani.com/blog/"),
        ("🎥", "Chrome for Developers — YouTube", "https://www.youtube.com/@ChromeDevs"),
        ("📘", "Lighthouse Docs", "https://developer.chrome.com/docs/lighthouse/overview"),
        ("✍️", "Patterns.dev (Addy Osmani & Lydia Hallie)", "https://www.patterns.dev/"),
        ("📘", "Web Performance Calendar", "https://calendar.perfplanet.com/"),
    ],
    13: [  # Accessibility
        ("📘", "WCAG 2.1 Guidelines", "https://www.w3.org/WAI/WCAG21/quickref/"),
        ("📘", "MDN — Accessibility", "https://developer.mozilla.org/en-US/docs/Web/Accessibility"),
        ("📘", "web.dev — Learn Accessibility", "https://web.dev/learn/accessibility"),
        ("✍️", "Deque — axe-core & patterns", "https://www.deque.com/blog/"),
        ("✍️", "Inclusive Components — Heydon Pickering", "https://inclusive-components.design/"),
        ("📘", "A11y Project Checklist", "https://www.a11yproject.com/checklist/"),
        ("📘", "ARIA Authoring Practices Guide", "https://www.w3.org/WAI/ARIA/apg/"),
    ],
    14: [  # DevOps
        ("📘", "Docker Docs", "https://docs.docker.com/"),
        ("📘", "Kubernetes Docs", "https://kubernetes.io/docs/home/"),
        ("📘", "GitHub Actions Docs", "https://docs.github.com/en/actions"),
        ("🎥", "TechWorld with Nana — DevOps", "https://www.youtube.com/@TechWorldwithNana"),
        ("🎥", "Fireship — Docker / K8s videos", "https://www.youtube.com/@Fireship"),
        ("📘", "AWS Free Tier & Workshops", "https://aws.amazon.com/getting-started/"),
        ("📘", "Sentry Docs", "https://docs.sentry.io/"),
        ("📘", "Datadog Learning Center", "https://learn.datadoghq.com/"),
    ],
    15: [  # AI/ML
        ("📘", "OpenAI API Docs", "https://platform.openai.com/docs"),
        ("📘", "Vercel AI SDK Docs", "https://sdk.vercel.ai/docs"),
        ("📘", "LangChain.js Docs", "https://js.langchain.com/docs/"),
        ("📘", "Anthropic API Docs", "https://docs.anthropic.com/"),
        ("✍️", "Simon Willison's Blog (LLMs)", "https://simonwillison.net/"),
        ("🎥", "Andrej Karpathy — YouTube", "https://www.youtube.com/@AndrejKarpathy"),
        ("📘", "Pinecone Learning Center", "https://www.pinecone.io/learn/"),
        ("📘", "Hugging Face Learn", "https://huggingface.co/learn"),
    ],
    16: [  # Projects
        ("📘", "System Design Primer", "https://github.com/donnemartin/system-design-primer"),
        ("📘", "Realworld Example Apps", "https://github.com/gothinkster/realworld"),
        ("✍️", "How to build a portfolio — Josh W Comeau", "https://www.joshwcomeau.com/blog/how-i-built-my-blog/"),
        ("🎥", "Fireship — Build along videos", "https://www.youtube.com/@Fireship"),
        ("🎥", "Theo - t3.gg — Real projects", "https://www.youtube.com/@t3dotgg"),
    ],
    17: [  # DSA
        ("🎯", "NeetCode — Roadmap & solutions", "https://neetcode.io/"),
        ("🎯", "LeetCode", "https://leetcode.com/"),
        ("🎯", "BigFrontend.dev — FE DSA", "https://bigfrontend.dev/"),
        ("🎥", "NeetCode — YouTube", "https://www.youtube.com/@NeetCode"),
        ("📘", "AlgoExpert / Grokking", "https://www.algoexpert.io/"),
        ("✍️", "Cracking the Coding Interview (book)", "https://www.crackingthecodinginterview.com/"),
        ("🎯", "Frontend Interview Handbook", "https://www.frontendinterviewhandbook.com/"),
    ],
    18: [  # System Design
        ("📘", "System Design Primer", "https://github.com/donnemartin/system-design-primer"),
        ("🎥", "ByteByteGo — YouTube", "https://www.youtube.com/@ByteByteGo"),
        ("📘", "Frontend System Design — GreatFrontEnd", "https://www.greatfrontend.com/system-design"),
        ("✍️", "Designing Data-Intensive Applications (book)", "https://dataintensive.net/"),
        ("🎯", "Hello Interview — System Design", "https://www.hellointerview.com/"),
        ("🎥", "Exponent — YouTube", "https://www.youtube.com/@tryexponent"),
        ("✍️", "High Scalability Blog", "http://highscalability.com/"),
    ],
    19: [  # Security
        ("📘", "OWASP Top 10", "https://owasp.org/www-project-top-ten/"),
        ("📘", "OWASP Cheat Sheet Series", "https://cheatsheetseries.owasp.org/"),
        ("📘", "MDN — Web Security", "https://developer.mozilla.org/en-US/docs/Web/Security"),
        ("📘", "PortSwigger Web Security Academy (free)", "https://portswigger.net/web-security"),
        ("✍️", "Content Security Policy — web.dev", "https://web.dev/articles/csp"),
        ("🎥", "LiveOverflow — Security videos", "https://www.youtube.com/@LiveOverflow"),
    ],
    20: [  # Node.js
        ("📘", "Node.js Docs", "https://nodejs.org/en/docs/"),
        ("📘", "Express.js Docs", "https://expressjs.com/"),
        ("📘", "NestJS Docs", "https://docs.nestjs.com/"),
        ("📘", "Fastify Docs", "https://fastify.dev/"),
        ("📘", "Bun Docs", "https://bun.sh/docs"),
        ("📘", "Deno Docs", "https://docs.deno.com/"),
        ("🎥", "The Net Ninja — Node.js", "https://www.youtube.com/@NetNinja"),
    ],
    21: [  # Vue
        ("📘", "Vue.js Docs", "https://vuejs.org/guide/introduction.html"),
        ("📘", "Pinia Docs", "https://pinia.vuejs.org/"),
        ("📘", "Nuxt Docs", "https://nuxt.com/docs"),
        ("📘", "Vue Mastery", "https://www.vuemastery.com/"),
        ("🎥", "The Net Ninja — Vue 3", "https://www.youtube.com/@NetNinja"),
    ],
    22: [  # Soft Skills
        ("✍️", "The Staff Engineer's Path (book)", "https://www.oreilly.com/library/view/the-staff-engineers/9781098118723/"),
        ("✍️", "StaffEng.com — Stories", "https://staffeng.com/"),
        ("✍️", "Will Larson — Irrational Exuberance", "https://lethain.com/"),
        ("✍️", "Google re:Work — Management guides", "https://rework.withgoogle.com/"),
        ("🎯", "Exponent — Behavioral interview", "https://www.tryexponent.com/"),
        ("✍️", "Julia Evans — Zines (writing/docs)", "https://jvns.ca/"),
    ],
    23: [  # Architect Toolkit
        ("📘", "AST Explorer", "https://astexplorer.net/"),
        ("📘", "Babel Plugin Handbook", "https://github.com/jamiebuilds/babel-handbook"),
        ("📘", "Vite Plugin Docs", "https://vite.dev/guide/api-plugin"),
        ("📘", "Webpack Concepts", "https://webpack.js.org/concepts/"),
        ("📘", "XState Docs", "https://stately.ai/docs"),
        ("📘", "WebAssembly (Rust & WASM book)", "https://rustwasm.github.io/docs/book/"),
        ("📘", "React Native Docs", "https://reactnative.dev/docs/getting-started"),
        ("📘", "Tauri Docs", "https://tauri.app/start/"),
        ("📘", "Turborepo Docs", "https://turbo.build/repo/docs"),
        ("✍️", "Martin Fowler — Architecture articles", "https://martinfowler.com/architecture/"),
    ],
    24: [  # AI Agents
        ("📘", "LangChain.js Docs", "https://js.langchain.com/docs/"),
        ("📘", "Vercel AI SDK", "https://sdk.vercel.ai/docs"),
        ("📘", "LlamaIndex Docs", "https://docs.llamaindex.ai/"),
        ("📘", "Ollama Docs", "https://ollama.com/"),
        ("📘", "Anthropic MCP (Model Context Protocol)", "https://modelcontextprotocol.io/"),
        ("📘", "Hugging Face Agents Course", "https://huggingface.co/learn/agents-course/"),
        ("✍️", "Lilian Weng — LLM Agents essay", "https://lilianweng.github.io/posts/2023-06-23-agent/"),
        ("📘", "Langfuse Docs (observability)", "https://langfuse.com/docs"),
        ("📘", "Transformers.js (in-browser ML)", "https://huggingface.co/docs/transformers.js"),
    ],
    25: [  # Backend Deep Dive
        ("📘", "Prisma Docs", "https://www.prisma.io/docs"),
        ("📘", "Drizzle ORM Docs", "https://orm.drizzle.team/docs/overview"),
        ("📘", "Redis Docs", "https://redis.io/docs/"),
        ("📘", "BullMQ Docs", "https://docs.bullmq.io/"),
        ("📘", "Apollo Server Docs", "https://www.apollographql.com/docs/apollo-server/"),
        ("📘", "tRPC Docs", "https://trpc.io/docs"),
        ("📘", "Kafka Intro (Confluent)", "https://developer.confluent.io/learn-kafka/"),
        ("✍️", "microservices.io (Chris Richardson)", "https://microservices.io/"),
        ("✍️", "Martin Fowler — Microservices", "https://martinfowler.com/microservices/"),
    ],
    26: [  # Cloud & IaC
        ("📘", "AWS Well-Architected Framework", "https://aws.amazon.com/architecture/well-architected/"),
        ("📘", "AWS Docs", "https://docs.aws.amazon.com/"),
        ("📘", "Terraform Docs", "https://developer.hashicorp.com/terraform/docs"),
        ("📘", "AWS CDK Docs", "https://docs.aws.amazon.com/cdk/"),
        ("📘", "Pulumi Docs", "https://www.pulumi.com/docs/"),
        ("📘", "SST Docs", "https://sst.dev/docs/"),
        ("📘", "k6 Docs", "https://grafana.com/docs/k6/latest/"),
        ("🎥", "AWS — YouTube", "https://www.youtube.com/@amazonwebservices"),
        ("🎥", "TechWorld with Nana — Cloud/DevOps", "https://www.youtube.com/@TechWorldwithNana"),
        ("✍️", "AWS Architecture Blog", "https://aws.amazon.com/blogs/architecture/"),
    ],
    27: [  # DB & Observability
        ("📘", "PostgreSQL Docs", "https://www.postgresql.org/docs/"),
        ("✍️", "Use The Index, Luke! (SQL indexing)", "https://use-the-index-luke.com/"),
        ("✍️", "Crunchy Data — Postgres blog", "https://www.crunchydata.com/blog"),
        ("📘", "MongoDB University (free courses)", "https://learn.mongodb.com/"),
        ("📘", "OpenTelemetry Docs", "https://opentelemetry.io/docs/"),
        ("📘", "Prometheus Docs", "https://prometheus.io/docs/introduction/overview/"),
        ("📘", "Grafana Docs", "https://grafana.com/docs/"),
        ("📘", "Go by Example", "https://gobyexample.com/"),
        ("📘", "The Go Tour", "https://go.dev/tour/welcome/1"),
        ("✍️", "Honeycomb — Observability guides", "https://www.honeycomb.io/blog"),
        ("📘", "Debezium (CDC)", "https://debezium.io/documentation/"),
    ],
}


def build_block(phase_num: int) -> str:
    items = RESOURCES[phase_num]
    links = "\n".join(
        f'        <a href="{url}" target="_blank" rel="noopener noreferrer">{emoji} {label}</a>'
        for emoji, label, url in items
    )
    return f"""
  <div class="resources" style="margin-top: 24px;">
    <h5>💎 Top Resources for Phase {phase_num} (E2E + Interviews)</h5>
    <div>
{links}
    </div>
  </div>
"""


def main():
    html = FILE.read_text(encoding="utf-8")

    # Safety: do not re-add if resources already inserted
    if "Top Resources for Phase 1" in html:
        print("⚠️  Resources blocks already present — aborting to avoid duplicates.")
        return

    # For each phase, find `<div class="phase" id="phaseN">` block,
    # locate its matching closing </div> (the one that closes the phase div),
    # and insert the resources block right before it.
    for phase_num in range(1, 28):
        pattern = f'<div class="phase" id="phase{phase_num}">'
        start = html.find(pattern)
        if start == -1:
            print(f"❌ Phase {phase_num} not found")
            continue

        # Walk forward counting div open/close to find matching close
        depth = 0
        i = start
        close_pos = -1
        while i < len(html):
            # Check for <div (possibly with attributes)
            if html.startswith("<div", i) and (len(html) > i + 4 and html[i + 4] in " >"):
                depth += 1
                i += 4
            elif html.startswith("</div>", i):
                depth -= 1
                if depth == 0:
                    close_pos = i
                    break
                i += 6
            else:
                i += 1

        if close_pos == -1:
            print(f"❌ Could not find closing </div> for phase {phase_num}")
            continue

        block = build_block(phase_num)
        html = html[:close_pos] + block + html[close_pos:]
        print(f"✅ Phase {phase_num}: inserted {len(RESOURCES[phase_num])} resources")

    FILE.write_text(html, encoding="utf-8")
    print(f"\n✨ Done. File size: {len(html):,} chars")


if __name__ == "__main__":
    main()
