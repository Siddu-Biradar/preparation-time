SECTIONS = r"""

<!-- ═══════════════════════════════════════════════════════════════════
     SECURITY — 3 SUB-SECTIONS
     ═══════════════════════════════════════════════════════════════════ -->

<h2 id="sec-vulnerabilities" class="section-break">55. Common Vulnerabilities</h2>
<p class="small"><strong>Checklist:</strong> XSS (reflected, stored, DOM-based) · CSRF · SQL injection (API context) · clickjacking · MITM attacks</p>

<h3>XSS (Cross-Site Scripting)</h3>
<table>
<thead><tr><th>Type</th><th>How it works</th><th>Example</th></tr></thead>
<tbody>
<tr><td><strong>Reflected</strong></td><td>Malicious script in URL, reflected back in response</td><td><code>?search=&lt;script&gt;alert(1)&lt;/script&gt;</code></td></tr>
<tr><td><strong>Stored</strong></td><td>Script saved in DB, served to other users</td><td>Comment containing <code>&lt;img onerror="steal()"&gt;</code></td></tr>
<tr><td><strong>DOM-based</strong></td><td>Script modifies DOM via client-side JS (never hits server)</td><td><code>innerHTML = location.hash</code></td></tr>
</tbody>
</table>

<h3>CSRF (Cross-Site Request Forgery)</h3>
<p>Tricks an authenticated user into making unwanted requests. The attacker creates a form on their site that submits to YOUR API — the browser automatically sends cookies, so the request looks legitimate.</p>
<pre>// Attacker's page
&lt;form action="https://bank.com/transfer" method="POST" id="evil"&gt;
  &lt;input name="to" value="attacker"&gt;
  &lt;input name="amount" value="10000"&gt;
&lt;/form&gt;
&lt;script&gt;document.getElementById('evil').submit();&lt;/script&gt;
// Prevention: CSRF tokens, SameSite cookies, check Origin header</pre>

<h3>Clickjacking</h3>
<p>Loading your site in an invisible iframe and tricking users into clicking buttons. Prevention: <code>X-Frame-Options: DENY</code> or CSP <code>frame-ancestors 'none'</code>.</p>

<h2 id="sec-prevention" class="section-break">56. Prevention Techniques</h2>
<p class="small"><strong>Checklist:</strong> Input sanitization · output encoding · CSP · HTTPS · secure cookies · CORS · SRI · X-Frame-Options · X-Content-Type-Options</p>

<pre>// XSS Prevention
// 1. ALWAYS use textContent (not innerHTML) for user data
element.textContent = userInput;  // ✅ SAFE
element.innerHTML = userInput;    // ❌ DANGEROUS

// 2. Content Security Policy (CSP) — whitelists allowed resources
Content-Security-Policy:
  default-src 'self';
  script-src 'self' 'nonce-abc123';  // only scripts with this nonce
  style-src 'self' 'unsafe-inline';
  img-src 'self' data: https://cdn.example.com;
  connect-src 'self' https://api.example.com;
  frame-ancestors 'none';           // prevents clickjacking
  base-uri 'self';
  form-action 'self';

// 3. Subresource Integrity — verify CDN files
&lt;script src="https://cdn.example.com/lib.js"
        integrity="sha384-oqVuAfXRKap7fdgcCY5uykM6..."
        crossorigin="anonymous"&gt;&lt;/script&gt;

// 4. Security headers
X-Frame-Options: DENY                    // no iframing
X-Content-Type-Options: nosniff          // prevent MIME sniffing
X-XSS-Protection: 0                     // disable old XSS filter (CSP is better)
Strict-Transport-Security: max-age=31536000; includeSubDomains // force HTTPS
Referrer-Policy: strict-origin-when-cross-origin

// 5. CORS — server controls which origins can access your API
Access-Control-Allow-Origin: https://my-app.com  // NOT *
Access-Control-Allow-Methods: GET, POST, PUT, DELETE
Access-Control-Allow-Headers: Content-Type, Authorization
Access-Control-Allow-Credentials: true

// 6. Secure cookies
Set-Cookie: session=abc123;
  HttpOnly;                    // not accessible from JavaScript
  Secure;                      // only sent over HTTPS
  SameSite=Strict;             // not sent with cross-site requests
  Max-Age=86400;               // expires in 24 hours
  Path=/;                      // applies to entire site</pre>

<h2 id="sec-auth" class="section-break">57. Authentication &amp; Authorization</h2>
<p class="small"><strong>Checklist:</strong> JWT · OAuth 2.0 · token storage · refresh token rotation · session management · password hashing · MFA</p>

<pre>// JWT structure: header.payload.signature
// header: { "alg": "HS256", "typ": "JWT" }
// payload: { "sub": "user123", "name": "Sid", "iat": 1710000000, "exp": 1710003600 }
// signature: HMACSHA256(base64(header) + "." + base64(payload), secret)

// Token refresh pattern
class AuthService {
  private refreshing = false;
  private refreshQueue: Function[] = [];

  async fetchWithAuth(url: string, options?: RequestInit): Promise<Response> {
    let token = this.getAccessToken();
    let response = await fetch(url, {
      ...options,
      headers: { ...options?.headers, Authorization: `Bearer ${token}` }
    });

    if (response.status === 401) {
      token = await this.refreshToken();
      response = await fetch(url, {
        ...options,
        headers: { ...options?.headers, Authorization: `Bearer ${token}` }
      });
    }
    return response;
  }

  private async refreshToken(): Promise<string> {
    if (this.refreshing) {
      return new Promise(resolve => this.refreshQueue.push(resolve));
    }
    this.refreshing = true;
    const res = await fetch('/api/auth/refresh', {
      method: 'POST',
      credentials: 'include' // send HttpOnly refresh token cookie
    });
    const { accessToken } = await res.json();
    this.setAccessToken(accessToken);
    this.refreshQueue.forEach(cb => cb(accessToken));
    this.refreshQueue = [];
    this.refreshing = false;
    return accessToken;
  }
}

// OAuth 2.0 Authorization Code Flow (with PKCE for SPAs)
// 1. App generates code_verifier + code_challenge
// 2. Redirect user to authorization server with code_challenge
// 3. User logs in, server redirects back with authorization code
// 4. App exchanges code + code_verifier for tokens
// 5. PKCE prevents authorization code interception attacks</pre>

<div class="interview-q">
<h4>🎯 Interview Questions — Security</h4>
<p><strong>Q: How do you prevent XSS in a frontend application?</strong></p>
<p><strong>A:</strong> (1) Never use <code>innerHTML</code> with user input — use <code>textContent</code>. (2) Implement Content Security Policy (CSP). (3) Sanitize HTML if you must render it (DOMPurify library). (4) Use frameworks' built-in escaping (Angular sanitizes by default). (5) Use HttpOnly cookies for tokens. (6) Validate and encode on both client and server.</p>

<p><strong>Q: Where should you store tokens in a SPA?</strong></p>
<p><strong>A:</strong> <strong>Access token:</strong> In memory (JS variable) — short-lived, lost on refresh. <strong>Refresh token:</strong> In HttpOnly, Secure, SameSite=Strict cookie — not accessible from JS (immune to XSS). Avoid localStorage for sensitive tokens. This pattern gives security (HttpOnly cookie) + SPA convenience (in-memory access token).</p>
</div>

<!-- ═══════════════════════════════════════════════════════════════════
     NETWORKING & APIs — 5 SUB-SECTIONS
     ═══════════════════════════════════════════════════════════════════ -->

<h2 id="net-http" class="section-break">58. HTTP Basics</h2>
<p class="small"><strong>Checklist:</strong> HTTP methods · status codes · request/response headers · Content-Type · Accept · Cache-Control · CORS headers</p>

<table>
<thead><tr><th>Method</th><th>Use</th><th>Idempotent?</th><th>Body?</th></tr></thead>
<tbody>
<tr><td><code>GET</code></td><td>Read data</td><td>Yes</td><td>No</td></tr>
<tr><td><code>POST</code></td><td>Create resource</td><td>No</td><td>Yes</td></tr>
<tr><td><code>PUT</code></td><td>Replace entire resource</td><td>Yes</td><td>Yes</td></tr>
<tr><td><code>PATCH</code></td><td>Partial update</td><td>No</td><td>Yes</td></tr>
<tr><td><code>DELETE</code></td><td>Remove resource</td><td>Yes</td><td>Optional</td></tr>
</tbody>
</table>

<h3>Status Codes to Know</h3>
<pre>// 2xx — Success
200 OK                    // successful request
201 Created               // resource created (POST)
204 No Content            // success, no body (DELETE)

// 3xx — Redirection
301 Moved Permanently     // SEO redirect (permanent)
302 Found                 // temporary redirect
304 Not Modified          // use cached version (ETag/If-Modified-Since)

// 4xx — Client Errors
400 Bad Request           // malformed request / validation error
401 Unauthorized          // not authenticated (need to login)
403 Forbidden             // authenticated but no permission
404 Not Found             // resource doesn't exist
409 Conflict              // resource conflict (e.g., duplicate)
422 Unprocessable Entity  // validation failed (semantic error)
429 Too Many Requests     // rate limited

// 5xx — Server Errors
500 Internal Server Error // generic server failure
502 Bad Gateway           // upstream server error
503 Service Unavailable   // server overloaded / maintenance
504 Gateway Timeout       // upstream server timeout</pre>

<h2 id="net-rest" class="section-break">59. REST API Design</h2>
<p class="small"><strong>Checklist:</strong> Resource naming · endpoint structure · versioning · HATEOAS · idempotency · pagination (offset/cursor) · filtering/sorting · rate limiting</p>

<pre>// RESTful URL conventions
GET    /api/v1/users           // list all users
GET    /api/v1/users/42        // get user by ID
POST   /api/v1/users           // create user
PUT    /api/v1/users/42        // replace user 42
PATCH  /api/v1/users/42        // partial update user 42
DELETE /api/v1/users/42        // delete user 42
GET    /api/v1/users/42/orders // user's orders (sub-resource)

// Pagination — cursor-based (better for real-time data)
GET /api/v1/products?cursor=eyJpZCI6NDJ9&limit=20
Response: {
  "data": [...],
  "pagination": {
    "next_cursor": "eyJpZCI6NjJ9",
    "has_more": true
  }
}

// Filtering + sorting
GET /api/v1/products?category=electronics&price_min=100&sort=-price&fields=name,price

// Rate limiting headers
X-RateLimit-Limit: 100       // max requests per window
X-RateLimit-Remaining: 42    // remaining in current window
X-RateLimit-Reset: 1710000060 // when window resets (Unix timestamp)
Retry-After: 30               // when rate limited (429)</pre>

<h2 id="net-graphql" class="section-break">60. GraphQL</h2>
<p class="small"><strong>Checklist:</strong> Queries · mutations · fragments · variables · aliases · schema · resolvers · Apollo Client · over-fetching/under-fetching</p>

<pre>// Query — fetch exactly what you need (no over-fetching)
query GetUserWithOrders($userId: ID!) {
  user(id: $userId) {
    name
    email
    orders(limit: 5) {
      id
      total
      status
      items {
        name
        quantity
      }
    }
  }
}

// Mutation — modify data
mutation CreateOrder($input: OrderInput!) {
  createOrder(input: $input) {
    id
    total
    status
  }
}

// Fragments — reusable field sets
fragment UserFields on User {
  id
  name
  email
  avatar
}
query { users { ...UserFields } }

// GraphQL vs REST trade-offs
// ✅ GraphQL: single endpoint, no over-fetching, typed schema, self-documenting
// ❌ GraphQL: complexity, caching harder, potential N+1 queries, learning curve
// ✅ REST: simple, cacheable (HTTP), well-understood, tools ecosystem
// ❌ REST: over-fetching, multiple endpoints, versioning complexity</pre>

<h2 id="net-data-fetching" class="section-break">61. Data Fetching</h2>
<p class="small"><strong>Checklist:</strong> Fetch API · Axios · AbortController · retry logic · error handling · loading states · optimistic updates · polling vs WebSocket vs SSE · request deduplication</p>

<pre>// Fetch with AbortController — cancel on unmount
const controller = new AbortController();
try {
  const response = await fetch('/api/data', {
    signal: controller.signal,
    headers: { 'Content-Type': 'application/json' }
  });
  if (!response.ok) throw new Error(`HTTP ${response.status}`);
  const data = await response.json();
} catch (error) {
  if (error.name === 'AbortError') return; // intentional cancel
  throw error;
}
// Cleanup: controller.abort();

// Retry with exponential backoff
async function fetchWithRetry(url, maxRetries = 3) {
  for (let attempt = 0; attempt < maxRetries; attempt++) {
    try {
      const res = await fetch(url);
      if (res.ok) return await res.json();
      if (res.status < 500) throw new Error(`Client error ${res.status}`);
    } catch (error) {
      if (attempt === maxRetries - 1) throw error;
      const delay = Math.min(1000 * Math.pow(2, attempt), 10000);
      await new Promise(r => setTimeout(r, delay + Math.random() * 1000));
    }
  }
}

// Optimistic update pattern
function addTodo(newTodo) {
  const tempId = crypto.randomUUID();
  // 1. Update UI instantly
  todos.update(list => [...list, { ...newTodo, id: tempId, status: 'pending' }]);
  // 2. Send to server
  api.createTodo(newTodo).then(
    saved => todos.update(list => list.map(t => t.id === tempId ? saved : t)),
    error => {
      todos.update(list => list.filter(t => t.id !== tempId)); // rollback
      showError('Failed to add todo');
    }
  );
}

// Polling vs WebSocket vs SSE
// Polling:    Simple, works everywhere, wasteful if no updates
// WebSocket:  Full-duplex, low latency, complex connection management
// SSE:        Server → client only, auto-reconnect, simpler than WebSocket</pre>

<h2 id="net-websockets" class="section-break">62. WebSockets</h2>
<p class="small"><strong>Checklist:</strong> Connection establishment · message sending/receiving · Socket.io · reconnection strategies · heartbeat/ping-pong</p>

<pre>// Native WebSocket
const ws = new WebSocket('wss://api.example.com/ws');

ws.addEventListener('open', () => {
  console.log('Connected');
  ws.send(JSON.stringify({ type: 'subscribe', channel: 'prices' }));
});

ws.addEventListener('message', (event) => {
  const data = JSON.parse(event.data);
  updatePriceDisplay(data);
});

ws.addEventListener('close', (event) => {
  console.log(`Disconnected: ${event.code} ${event.reason}`);
  if (event.code !== 1000) reconnect(); // abnormal close → reconnect
});

ws.addEventListener('error', () => { ws.close(); });

// Reconnection with exponential backoff
class ReconnectingWebSocket {
  private ws: WebSocket;
  private retryCount = 0;
  private maxRetries = 10;

  connect() {
    this.ws = new WebSocket(this.url);
    this.ws.onopen = () => { this.retryCount = 0; this.startHeartbeat(); };
    this.ws.onclose = (e) => {
      if (e.code !== 1000 && this.retryCount < this.maxRetries) {
        const delay = Math.min(1000 * Math.pow(2, this.retryCount++), 30000);
        setTimeout(() => this.connect(), delay);
      }
    };
  }

  // Heartbeat — detect broken connections
  private startHeartbeat() {
    setInterval(() => {
      if (this.ws.readyState === WebSocket.OPEN) {
        this.ws.send(JSON.stringify({ type: 'ping' }));
      }
    }, 30000);
  }
}</pre>

<!-- ═══════════════════════════════════════════════════════════════════
     STATE MANAGEMENT + TESTING — 5 SUB-SECTIONS
     ═══════════════════════════════════════════════════════════════════ -->

<h2 id="state-management" class="section-break">63. State Management Patterns</h2>
<p class="small"><strong>Checklist:</strong> Store/actions/reducers · middleware · selectors · State types (server/client/local/global/URL/derived) · data fetching libraries · caching strategies · stale-while-revalidate</p>

<h3>State Types</h3>
<table>
<thead><tr><th>Type</th><th>Where it lives</th><th>Example</th></tr></thead>
<tbody>
<tr><td><strong>Server state</strong></td><td>Remote, cached locally</td><td>User profile, product list, orders</td></tr>
<tr><td><strong>Client state</strong></td><td>Only in browser</td><td>UI toggles, theme, form input</td></tr>
<tr><td><strong>Local state</strong></td><td>Single component</td><td>Dropdown open/closed, form fields</td></tr>
<tr><td><strong>Global state</strong></td><td>Shared across app</td><td>Auth user, cart, notifications</td></tr>
<tr><td><strong>URL state</strong></td><td>In the URL</td><td>Filters, pagination, search query</td></tr>
<tr><td><strong>Derived state</strong></td><td>Computed from other state</td><td>Total price (items × quantities), filtered lists</td></tr>
</tbody>
</table>

<pre>// Redux pattern (framework-agnostic concept)
// Action → Reducer → New State → View updates

// 1. Action — describes WHAT happened
const addItem = (product) => ({ type: 'cart/addItem', payload: product });

// 2. Reducer — describes HOW state changes (pure function!)
function cartReducer(state = { items: [] }, action) {
  switch (action.type) {
    case 'cart/addItem':
      return { ...state, items: [...state.items, action.payload] };
    case 'cart/removeItem':
      return { ...state, items: state.items.filter(i => i.id !== action.payload) };
    default:
      return state;
  }
}

// 3. Selector — derives data from state (memoized for performance)
const selectCartTotal = (state) =>
  state.cart.items.reduce((sum, item) => sum + item.price * item.quantity, 0);

// Angular equivalent: NgRx / signals
// signals are Angular's built-in state management (Angular 16+)
const count = signal(0);
const doubled = computed(() => count() * 2); // derived state
count.set(5);     // doubled() === 10</pre>

<h2 id="test-unit" class="section-break">64. Unit Testing</h2>
<p class="small"><strong>Checklist:</strong> Jest test runner · describe/it/test · assertions &amp; matchers · setup/teardown · mocking (jest.fn, jest.mock) · spies · timer mocks · coverage</p>

<pre>// Test structure
describe('CartService', () => {
  let service: CartService;

  beforeEach(() => {
    service = new CartService();  // fresh instance for each test
  });

  afterEach(() => {
    jest.restoreAllMocks();       // cleanup mocks
  });

  describe('addItem', () => {
    it('should add item to cart', () => {
      const item = { id: '1', name: 'Laptop', price: 1200, quantity: 1 };
      service.addItem(item);
      expect(service.getItems()).toHaveLength(1);
      expect(service.getItems()[0]).toEqual(item);
    });

    it('should increment quantity for duplicate items', () => {
      const item = { id: '1', name: 'Laptop', price: 1200, quantity: 1 };
      service.addItem(item);
      service.addItem(item);
      expect(service.getItems()).toHaveLength(1);
      expect(service.getItems()[0].quantity).toBe(2);
    });

    it('should throw for invalid price', () => {
      expect(() => service.addItem({ id: '1', price: -10 }))
        .toThrow('Price must be positive');
    });
  });

  describe('getTotal', () => {
    it('should calculate total with tax', () => {
      service.addItem({ id: '1', price: 100, quantity: 2 });
      service.addItem({ id: '2', price: 50, quantity: 1 });
      expect(service.getTotal(0.1)).toBe(275); // (200 + 50) * 1.1
    });
  });
});

// Mocking
jest.mock('./api', () => ({
  fetchUser: jest.fn()
}));
import { fetchUser } from './api';

test('handles API errors gracefully', async () => {
  (fetchUser as jest.Mock).mockRejectedValue(new Error('Network error'));
  const result = await getUserSafe('123');
  expect(result).toBeNull();
  expect(fetchUser).toHaveBeenCalledWith('123');
});

// Timer mocking
jest.useFakeTimers();
test('debounce waits before calling', () => {
  const fn = jest.fn();
  const debounced = debounce(fn, 300);
  debounced(); debounced(); debounced();
  expect(fn).not.toHaveBeenCalled();
  jest.advanceTimersByTime(300);
  expect(fn).toHaveBeenCalledTimes(1);
});</pre>

<h2 id="test-integration" class="section-break">65. Integration Testing</h2>
<p class="small"><strong>Checklist:</strong> Testing component interactions · multi-component flows · API integration tests · testing with real dependencies</p>

<pre>// Integration test — multiple components working together
describe('Checkout Flow', () => {
  it('should complete purchase flow', async () => {
    // Setup: mock API but test real component interaction
    server.use(
      rest.get('/api/products/:id', (req, res, ctx) =>
        res(ctx.json({ id: req.params.id, name: 'Laptop', price: 1200 }))
      ),
      rest.post('/api/orders', (req, res, ctx) =>
        res(ctx.json({ id: 'order-1', status: 'created' }))
      )
    );

    // Render full checkout page (multiple child components)
    render(&lt;CheckoutPage /&gt;);

    // Wait for product to load
    await screen.findByText('Laptop');

    // Fill shipping form
    await userEvent.type(screen.getByLabelText('Street'), '123 Main St');
    await userEvent.type(screen.getByLabelText('City'), 'Bengaluru');

    // Fill payment
    await userEvent.type(screen.getByLabelText('Card Number'), '4242424242424242');

    // Submit
    await userEvent.click(screen.getByRole('button', { name: /place order/i }));

    // Verify success
    await screen.findByText('Order placed successfully');
  });
});</pre>

<h2 id="test-e2e" class="section-break">66. E2E Testing (0 → Advanced)</h2>
<p class="small"><strong>Checklist:</strong> Cypress · Playwright · selectors/locators · network mocking · screenshots/video · parallel execution · page object model</p>

<h3>66.1 Playwright — Modern E2E Framework</h3>
<pre>// playwright.config.ts
import { defineConfig } from '@playwright/test';
export default defineConfig({
  testDir: './e2e',
  use: {
    baseURL: 'http://localhost:4200',
    screenshot: 'only-on-failure',
    video: 'retain-on-failure',
    trace: 'on-first-retry'
  },
  projects: [
    { name: 'chromium', use: { browserName: 'chromium' } },
    { name: 'firefox', use: { browserName: 'firefox' } },
    { name: 'webkit', use: { browserName: 'webkit' } }
  ],
  webServer: {
    command: 'ng serve',
    port: 4200,
    reuseExistingServer: !process.env.CI
  }
});

// Basic test
import { test, expect } from '@playwright/test';

test('user can search for products', async ({ page }) => {
  await page.goto('/products');
  await page.getByPlaceholder('Search products').fill('laptop');
  await page.getByRole('button', { name: 'Search' }).click();
  await expect(page.getByTestId('results-count')).toHaveText('5 results');
  await expect(page.getByRole('listitem')).toHaveCount(5);
});</pre>

<h3>66.2 Page Object Model — Scalable E2E</h3>
<pre>// pages/login.page.ts
class LoginPage {
  constructor(private page: Page) {}

  get emailInput() { return this.page.getByLabel('Email'); }
  get passwordInput() { return this.page.getByLabel('Password'); }
  get submitButton() { return this.page.getByRole('button', { name: 'Login' }); }
  get errorMessage() { return this.page.getByTestId('error-message'); }

  async goto() { await this.page.goto('/login'); }

  async login(email: string, password: string) {
    await this.emailInput.fill(email);
    await this.passwordInput.fill(password);
    await this.submitButton.click();
  }
}

// Using the page object
test('login with valid credentials', async ({ page }) => {
  const loginPage = new LoginPage(page);
  await loginPage.goto();
  await loginPage.login('user@example.com', 'password123');
  await expect(page).toHaveURL('/dashboard');
});

test('shows error for invalid credentials', async ({ page }) => {
  const loginPage = new LoginPage(page);
  await loginPage.goto();
  await loginPage.login('user@example.com', 'wrong');
  await expect(loginPage.errorMessage).toBeVisible();
  await expect(loginPage.errorMessage).toHaveText('Invalid credentials');
});</pre>

<h3>66.3 Network Mocking in E2E</h3>
<pre>// Playwright — intercept API calls
test('shows empty state when no products', async ({ page }) => {
  await page.route('/api/products', route =>
    route.fulfill({ status: 200, body: JSON.stringify([]) })
  );
  await page.goto('/products');
  await expect(page.getByText('No products found')).toBeVisible();
});

// Cypress equivalent
cy.intercept('GET', '/api/products', { body: [] }).as('getProducts');
cy.visit('/products');
cy.wait('@getProducts');
cy.contains('No products found').should('be.visible');</pre>

<h3>66.4 Advanced E2E Patterns</h3>
<pre>// Visual regression testing
test('homepage matches snapshot', async ({ page }) => {
  await page.goto('/');
  await expect(page).toHaveScreenshot('homepage.png', { maxDiffPixels: 100 });
});

// Testing accessibility
test('page should be accessible', async ({ page }) => {
  await page.goto('/');
  const violations = await new AxeBuilder({ page }).analyze();
  expect(violations.violations).toHaveLength(0);
});

// Testing with authentication state
test.describe('authenticated user', () => {
  test.use({
    storageState: 'e2e/.auth/user.json' // pre-saved login state
  });

  test('can access dashboard', async ({ page }) => {
    await page.goto('/dashboard');
    await expect(page.getByText('Welcome, Sid')).toBeVisible();
  });
});

// Parallel execution best practices
// - Each test should be independent (no shared state)
// - Use unique test data (UUIDs) to avoid conflicts
// - Use test fixtures for common setup
// - Keep tests fast: mock external services</pre>

<h2 id="test-tdd" class="section-break">67. Test-Driven Development</h2>
<p class="small"><strong>Checklist:</strong> Red-Green-Refactor cycle · writing tests first · benefits &amp; trade-offs</p>

<pre>// TDD: Red → Green → Refactor

// Step 1: RED — Write a failing test
test('isValidEmail returns true for valid emails', () => {
  expect(isValidEmail('user@example.com')).toBe(true);
  expect(isValidEmail('a.b@c.co')).toBe(true);
});
test('isValidEmail returns false for invalid emails', () => {
  expect(isValidEmail('invalid')).toBe(false);
  expect(isValidEmail('@no-local.com')).toBe(false);
  expect(isValidEmail('no-domain@')).toBe(false);
  expect(isValidEmail('')).toBe(false);
});
// Tests fail because isValidEmail doesn't exist yet!

// Step 2: GREEN — Write minimal code to pass
function isValidEmail(email) {
  return /^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email);
}
// Tests pass!

// Step 3: REFACTOR — improve without changing behavior
function isValidEmail(email: string): boolean {
  if (!email || typeof email !== 'string') return false;
  return /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/.test(email);
}
// Tests still pass → refactoring is safe

// TDD benefits:
// ✅ Forces you to think about API design before implementation
// ✅ High test coverage by default
// ✅ Confidence when refactoring
// ✅ Tests serve as documentation
// ❌ Slower initial development
// ❌ Can lead to over-testing implementation details</pre>

<div class="interview-q">
<h4>🎯 Interview Questions — Testing</h4>
<p><strong>Q: What's the testing pyramid?</strong></p>
<p><strong>A:</strong> Bottom: <strong>Unit tests</strong> (many, fast, cheap — test individual functions/classes). Middle: <strong>Integration tests</strong> (fewer, test component interactions). Top: <strong>E2E tests</strong> (fewest, slow, expensive — test full user flows). Most tests should be unit tests; E2E for critical paths only.</p>

<p><strong>Q: What makes a good unit test?</strong></p>
<p><strong>A:</strong> (1) <strong>Fast</strong> — runs in milliseconds. (2) <strong>Isolated</strong> — no external dependencies (mock them). (3) <strong>Deterministic</strong> — same result every time. (4) <strong>Self-validating</strong> — pass or fail, no manual inspection. (5) <strong>Thorough</strong> — covers happy path, edge cases, and error cases. (6) <strong>Readable</strong> — test name describes the behavior being tested.</p>
</div>
"""
