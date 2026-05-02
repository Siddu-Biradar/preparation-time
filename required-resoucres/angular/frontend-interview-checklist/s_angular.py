SECTIONS = r"""

<!-- ═══════════════════════════════════════════════════════════════════
     ANGULAR DEEP DIVE — 15 SUB-SECTIONS (106 – 120)
     Everything an SDE-3 Angular candidate MUST know
     ═══════════════════════════════════════════════════════════════════ -->

<h2 id="ng-change-detection" class="section-break">106. Angular Change Detection</h2>
<p class="small"><strong>Checklist:</strong> Zone.js · Default vs OnPush · markForCheck · detectChanges · async pipe · Signals · runOutsideAngular · ApplicationRef.tick</p>

<h3>106.1 How Zone.js Works</h3>
<pre>// Zone.js monkey-patches ALL async APIs:
// setTimeout, setInterval, Promise.then, addEventListener,
// XMLHttpRequest, fetch, requestAnimationFrame, MutationObserver

// When any async callback fires:
// 1. Zone.js intercepts it
// 2. Notifies Angular via NgZone
// 3. Angular runs change detection on the ENTIRE component tree

// This means EVERY click, timer, HTTP response triggers full tree check!
// For large apps this is a huge performance bottleneck.</pre>

<h3>106.2 Default vs OnPush Strategy</h3>
<pre>// DEFAULT — checks component on EVERY change detection cycle
@Component({
  changeDetection: ChangeDetectionStrategy.Default // ← default
})

// OnPush — only checks when:
// 1. @Input() reference changes (not mutation!)
// 2. Event handler fires within the component
// 3. Async pipe emits a new value
// 4. markForCheck() is called manually
@Component({
  changeDetection: ChangeDetectionStrategy.OnPush  // ← use this!
})
export class ProductListComponent {
  @Input() products: Product[] = [];

  // ❌ This WON'T trigger change detection with OnPush:
  addProductWrong(p: Product) {
    this.products.push(p); // mutation, same reference!
  }

  // ✅ This WILL trigger change detection:
  addProductRight(p: Product) {
    this.products = [...this.products, p]; // new reference!
  }
}

// Rule: With OnPush, ALWAYS treat data as immutable
// Arrays: use spread [...arr, newItem], filter(), map()
// Objects: use spread { ...obj, key: newValue }</pre>

<h3>106.3 Manual Change Detection Controls</h3>
<pre>@Component({
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class DashboardComponent {
  data: any;

  constructor(
    private cdr: ChangeDetectorRef,
    private ngZone: NgZone,
    private ws: WebSocketService
  ) {}

  ngOnInit() {
    // markForCheck — marks this component + ancestors dirty
    // (checked on next CD cycle)
    this.ws.messages$.subscribe(msg => {
      this.data = msg;
      this.cdr.markForCheck(); // ← tell Angular to check this component
    });

    // detectChanges — runs CD immediately on this component + children
    // Use sparingly! Usually markForCheck is better.
    // this.cdr.detectChanges();

    // detach — remove component from CD tree entirely
    // reattach — add back to CD tree
    this.cdr.detach(); // component won't be checked anymore
    setInterval(() => {
      this.cdr.detectChanges(); // manually check every 5s
    }, 5000);
  }

  // runOutsideAngular — skip Zone.js for perf-heavy work
  startAnimation() {
    this.ngZone.runOutsideAngular(() => {
      // This won't trigger change detection!
      requestAnimationFrame(function animate() {
        // do animation work
        requestAnimationFrame(animate);
      });
    });

    // When you need to come back to Angular zone:
    this.ngZone.run(() => {
      this.status = 'Animation complete';
    });
  }
}</pre>

<h3>106.4 Angular Signals (Angular 16+)</h3>
<pre>import { signal, computed, effect } from '@angular/core';

// Signal — reactive primitive, replaces Zone.js for CD
const count = signal(0);
count();          // read: 0
count.set(5);     // write: 5
count.update(v => v + 1); // update based on previous: 6

// Computed — derived signal (lazy, memoized)
const doubled = computed(() => count() * 2); // 12
// Only recalculates when count changes

// Effect — side effect that auto-tracks dependencies
effect(() => {
  console.log(`Count is now: ${count()}`);
  // Re-runs whenever count changes
  // Auto-cleanup on component destroy
});

// Signals in components
@Component({
  template: `
    &lt;p&gt;Count: {{ count() }}&lt;/p&gt;
    &lt;p&gt;Double: {{ doubled() }}&lt;/p&gt;
    &lt;button (click)="increment()"&gt;+1&lt;/button&gt;
  `,
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class CounterComponent {
  count = signal(0);
  doubled = computed(() => this.count() * 2);

  increment() { this.count.update(v => v + 1); }
}

// Signal vs Observable
// Signal:     synchronous, always has a value, simpler API
// Observable: async streams, can be empty, operators for complex flows
// Use Signals for: UI state, computed values, simple reactivity
// Use RxJS for: HTTP, WebSocket, complex async flows, operators</pre>

<div class="interview-q">
<h4>🎯 Interview Questions — Change Detection</h4>
<p><strong>Q: Your app with 500 components is sluggish. How do you diagnose and fix?</strong></p>
<p><strong>A:</strong> (1) Use Angular DevTools Profiler to see which components re-render and how long. (2) Switch all components to <code>OnPush</code> change detection. (3) Use <code>async</code> pipe for observables (auto-marks for check). (4) Use <code>trackBy</code> for <code>*ngFor</code>. (5) Memoize expensive computations with pure pipes or <code>computed()</code> signals. (6) Use <code>runOutsideAngular</code> for animations/timers that don't affect the UI. (7) Lazy-load feature modules. (8) Use virtual scrolling for long lists.</p>

<p><strong>Q: What's the difference between markForCheck and detectChanges?</strong></p>
<p><strong>A:</strong> <code>markForCheck()</code> marks the component and all ancestors as dirty — they'll be checked on the <em>next</em> CD cycle. It's safe and non-disruptive. <code>detectChanges()</code> runs CD <em>immediately</em> on the component and its children, bypassing the normal cycle. It can cause performance issues if overused and can lead to "Expression has changed after it was checked" errors.</p>
</div>

<h2 id="ng-di" class="section-break">107. Angular Dependency Injection</h2>
<p class="small"><strong>Checklist:</strong> Providers · injection tokens · providedIn · hierarchical injectors · useClass/useValue/useFactory/useExisting · forRoot/forChild · tree-shakable providers · inject() function</p>

<pre>// Provider strategies
@Injectable({
  providedIn: 'root'  // tree-shakable singleton (recommended!)
})
export class AuthService { }

// providedIn options:
// 'root'    — app-wide singleton
// 'any'     — unique instance per lazy-loaded module
// 'platform' — shared across all apps on the page (micro-frontends)
// SomeModule — singleton within that module's injector

// Provider types
providers: [
  // useClass — create instance of different class
  { provide: LoggerService, useClass: BetterLoggerService },

  // useValue — provide a static value
  { provide: API_URL, useValue: 'https://api.example.com' },

  // useFactory — compute at runtime
  {
    provide: DataService,
    useFactory: (http: HttpClient, config: ConfigService) => {
      return config.useMock
        ? new MockDataService()
        : new RealDataService(http);
    },
    deps: [HttpClient, ConfigService]
  },

  // useExisting — alias to another provider
  { provide: AbstractLogger, useExisting: ConsoleLoggerService }
]

// InjectionToken — type-safe tokens for non-class dependencies
export const API_CONFIG = new InjectionToken&lt;ApiConfig&gt;('api.config', {
  providedIn: 'root',
  factory: () => ({ baseUrl: '/api', timeout: 5000 })
});

// inject() function (Angular 14+) — replaces constructor injection
@Component({ ... })
export class UserComponent {
  private http = inject(HttpClient);
  private config = inject(API_CONFIG);
  private router = inject(Router);
  private user = inject(UserService, { optional: true }); // nullable

  // No constructor needed!
}

// Hierarchical injectors — child overrides parent
@Component({
  providers: [{ provide: LoggerService, useClass: VerboseLogger }]
  // This component and its children get VerboseLogger
  // Rest of the app still uses default LoggerService
})</pre>

<h2 id="ng-lifecycle" class="section-break">108. Angular Lifecycle Hooks</h2>
<p class="small"><strong>Checklist:</strong> constructor · ngOnChanges · ngOnInit · ngDoCheck · ngAfterContentInit/Checked · ngAfterViewInit/Checked · ngOnDestroy · execution order · parent-child order</p>

<pre>@Component({ ... })
export class LifecycleComponent implements
  OnChanges, OnInit, DoCheck,
  AfterContentInit, AfterContentChecked,
  AfterViewInit, AfterViewChecked, OnDestroy {

  @Input() data: any;

  // 1. constructor — DI happens here, inputs NOT available yet
  constructor() { }

  // 2. ngOnChanges — called BEFORE ngOnInit and every @Input change
  //    Only for @Input() properties. Receives SimpleChanges object.
  ngOnChanges(changes: SimpleChanges) {
    if (changes['data'] &amp;&amp; !changes['data'].firstChange) {
      console.log('data changed:', changes['data'].previousValue,
                  '→', changes['data'].currentValue);
    }
  }

  // 3. ngOnInit — component initialized. Inputs ARE available.
  //    Called ONCE. Best place for initialization logic.
  ngOnInit() {
    this.loadData();  // ✅ Do API calls here, not in constructor
  }

  // 4. ngDoCheck — custom change detection. Called EVERY CD cycle!
  //    Use sparingly — runs very frequently.
  ngDoCheck() { }

  // 5. ngAfterContentInit — projected content (ng-content) initialized
  //    Called ONCE after first ngDoCheck
  ngAfterContentInit() { }

  // 6. ngAfterContentChecked — after every check of projected content
  ngAfterContentChecked() { }

  // 7. ngAfterViewInit — view (template + child views) initialized
  //    @ViewChild is available here, NOT in ngOnInit!
  @ViewChild('chart') chartRef: ElementRef;
  ngAfterViewInit() {
    this.initChart(this.chartRef.nativeElement);  // ✅ safe here
  }

  // 8. ngAfterViewChecked — after every check of the view
  ngAfterViewChecked() { }

  // 9. ngOnDestroy — cleanup! Unsubscribe, detach listeners
  private destroy$ = new Subject&lt;void&gt;();
  ngOnDestroy() {
    this.destroy$.next();
    this.destroy$.complete();
  }
}

// Execution order (parent P, child C):
// P.constructor → P.ngOnChanges → P.ngOnInit → P.ngDoCheck
// → C.constructor → C.ngOnChanges → C.ngOnInit → C.ngDoCheck
// → C.ngAfterContentInit → C.ngAfterContentChecked
// → C.ngAfterViewInit → C.ngAfterViewChecked
// → P.ngAfterContentInit → P.ngAfterContentChecked
// → P.ngAfterViewInit → P.ngAfterViewChecked</pre>

<h2 id="ng-rxjs" class="section-break">109. RxJS Deep Dive (Operators)</h2>
<p class="small"><strong>Checklist:</strong> Observables · Subjects · switchMap · mergeMap · concatMap · exhaustMap · combineLatest · forkJoin · takeUntil · shareReplay · debounceTime · distinctUntilChanged · catchError · retry · tap · BehaviorSubject · ReplaySubject</p>

<h3>109.1 Observable vs Promise</h3>
<pre>// Observable: lazy, cancellable, multiple values, operators
// Promise: eager, not cancellable, single value

const obs$ = new Observable(subscriber => {
  subscriber.next(1);
  subscriber.next(2);
  setTimeout(() => subscriber.next(3), 1000);
  // subscriber.complete();
  // subscriber.error(new Error('fail'));
});

const sub = obs$.subscribe({
  next: val => console.log(val),
  error: err => console.error(err),
  complete: () => console.log('done')
});

sub.unsubscribe(); // ← cancel! Promises can't do this</pre>

<h3>109.2 Subjects — Observable + Observer</h3>
<pre>// Subject — multicast, no initial value
const subject = new Subject&lt;number&gt;();
subject.subscribe(v => console.log('A:', v));
subject.next(1); // A: 1
subject.subscribe(v => console.log('B:', v));
subject.next(2); // A: 2, B: 2  (B missed value 1!)

// BehaviorSubject — has initial value, emits last value to new subscribers
const behavior$ = new BehaviorSubject&lt;string&gt;('initial');
behavior$.subscribe(v => console.log('A:', v)); // A: initial
behavior$.next('hello');                         // A: hello
behavior$.subscribe(v => console.log('B:', v)); // B: hello (gets last value!)
behavior$.getValue(); // 'hello' — synchronous read

// ReplaySubject — replays N last values to new subscribers
const replay$ = new ReplaySubject&lt;number&gt;(3); // buffer last 3
replay$.next(1); replay$.next(2); replay$.next(3); replay$.next(4);
replay$.subscribe(v => console.log(v)); // 2, 3, 4

// AsyncSubject — only emits the LAST value, and only on complete()
const async$ = new AsyncSubject&lt;number&gt;();
async$.next(1); async$.next(2); async$.next(3);
async$.subscribe(v => console.log(v)); // nothing yet...
async$.complete(); // NOW logs: 3</pre>

<h3>109.3 Flattening Operators — THE Most Asked Topic</h3>
<pre>// switchMap — cancel previous, use latest only
// Use for: search/typeahead, route params, latest value
this.searchInput$.pipe(
  debounceTime(300),
  distinctUntilChanged(),
  switchMap(query => this.api.search(query))
  // If user types again before response, previous HTTP is CANCELLED
).subscribe(results => this.results = results);

// mergeMap (flatMap) — all run in parallel, no cancellation
// Use for: parallel independent requests, logging, analytics
this.items$.pipe(
  mergeMap(item => this.api.process(item), 3) // max 3 concurrent
).subscribe();

// concatMap — sequential, one at a time, preserves order
// Use for: ordered operations, file uploads one-by-one
this.files$.pipe(
  concatMap(file => this.api.upload(file))
  // Waits for each upload to complete before starting next
).subscribe();

// exhaustMap — ignore new emissions while current is running
// Use for: login button, form submit (prevent double-click!)
this.loginClick$.pipe(
  exhaustMap(() => this.auth.login(this.credentials))
  // Clicking again while login is in-flight does NOTHING
).subscribe();

// SUMMARY TABLE:
// switchMap  → cancel previous → typeahead, route params
// mergeMap   → all parallel    → parallel API calls
// concatMap  → one by one      → ordered operations
// exhaustMap → ignore new      → prevent double-submit</pre>

<h3>109.4 Combination Operators</h3>
<pre>// combineLatest — emit when ANY source emits (needs all to emit once first)
combineLatest([
  this.route.params,
  this.route.queryParams,
  this.store.select(selectFilters)
]).pipe(
  map(([params, query, filters]) => ({ ...params, ...query, ...filters }))
).subscribe(combined => this.loadData(combined));

// forkJoin — emit when ALL complete (like Promise.all)
forkJoin({
  user: this.api.getUser(id),
  orders: this.api.getOrders(id),
  settings: this.api.getSettings(id)
}).subscribe(({ user, orders, settings }) => {
  // All three responses available here
});
// ⚠️ If ANY fails, entire forkJoin fails! Use catchError inside each.

// withLatestFrom — get latest value of another observable
this.saveClick$.pipe(
  withLatestFrom(this.form.valueChanges),
  map(([click, formValue]) => formValue),
  exhaustMap(value => this.api.save(value))
).subscribe();

// merge — combine multiple into one (interleaved)
merge(this.ws.messages$, this.polling$, this.push$).subscribe();

// zip — pair values by index (nth from each source)
zip(names$, scores$).subscribe(([name, score]) => {});</pre>

<h3>109.5 Error Handling &amp; Retry</h3>
<pre>// catchError — handle errors, return fallback observable
this.api.getData().pipe(
  catchError(error => {
    this.logger.log(error);
    return of([]); // fallback: empty array
    // or: return EMPTY; (complete without emitting)
    // or: return throwError(() => new Error('Custom msg'));
  })
).subscribe();

// retry — retry N times
this.api.getData().pipe(
  retry(3),                     // retry up to 3 times
  catchError(err => of([]))     // after 3 failures, fallback
).subscribe();

// retryWhen with delay (exponential backoff)
this.api.getData().pipe(
  retry({
    count: 3,
    delay: (error, retryCount) => {
      const delay = Math.pow(2, retryCount) * 1000;
      console.log(`Retry ${retryCount} in ${delay}ms`);
      return timer(delay);
    }
  })
).subscribe();</pre>

<h3>109.6 Memory Leak Prevention</h3>
<pre>// ❌ BAD — manual subscribe without cleanup → MEMORY LEAK
ngOnInit() {
  this.userService.user$.subscribe(user => this.user = user);
  // This subscription lives FOREVER after component is destroyed!
}

// ✅ Method 1: takeUntil pattern
private destroy$ = new Subject&lt;void&gt;();
ngOnInit() {
  this.userService.user$.pipe(
    takeUntil(this.destroy$)
  ).subscribe(user => this.user = user);
}
ngOnDestroy() {
  this.destroy$.next();
  this.destroy$.complete();
}

// ✅ Method 2: async pipe (BEST — auto-subscribes + unsubscribes)
@Component({
  template: `
    &lt;div *ngIf="user$ | async as user"&gt;
      Welcome, {{ user.name }}
    &lt;/div&gt;
  `
})
export class UserComponent {
  user$ = this.userService.user$; // no subscribe needed!
}

// ✅ Method 3: takeUntilDestroyed (Angular 16+)
export class UserComponent {
  constructor() {
    this.userService.user$.pipe(
      takeUntilDestroyed()  // auto-unsubscribe on destroy!
    ).subscribe(user => this.user = user);
  }
}

// ✅ Method 4: DestroyRef (Angular 16+)
export class UserComponent {
  private destroyRef = inject(DestroyRef);

  ngOnInit() {
    const sub = this.data$.subscribe(d => this.data = d);
    this.destroyRef.onDestroy(() => sub.unsubscribe());
  }
}</pre>

<div class="interview-q">
<h4>🎯 Interview Questions — RxJS</h4>
<p><strong>Q: You have a search input. User types fast. How do you optimize API calls?</strong></p>
<p><strong>A:</strong> <code>searchInput.valueChanges.pipe(debounceTime(300), distinctUntilChanged(), filter(q => q.length >= 2), switchMap(q => api.search(q).pipe(catchError(() => of([])))))</code>. <code>debounceTime</code> waits for pause. <code>distinctUntilChanged</code> skips duplicate queries. <code>switchMap</code> cancels previous HTTP if new keystroke arrives. <code>catchError</code> inside switchMap prevents the outer observable from dying on error.</p>

<p><strong>Q: When would you use mergeMap over switchMap?</strong></p>
<p><strong>A:</strong> Use <code>mergeMap</code> when you need ALL results (parallel, order doesn't matter) — e.g., sending analytics events, processing a batch of items. Use <code>switchMap</code> when only the LATEST matters and older results are stale — e.g., typeahead search, route param changes. Use <code>concatMap</code> when order matters — e.g., sequential file uploads. Use <code>exhaustMap</code> to prevent duplicate work — e.g., login/submit buttons.</p>
</div>

<h2 id="ng-router" class="section-break">110. Angular Router</h2>
<p class="small"><strong>Checklist:</strong> Route config · lazy loading · guards (canActivate, canDeactivate, resolve, canMatch) · route params/query params · child/nested routes · router events · preloading strategies</p>

<pre>// Route configuration
const routes: Routes = [
  { path: '', redirectTo: 'dashboard', pathMatch: 'full' },

  // Eager route with guard
  {
    path: 'dashboard',
    component: DashboardComponent,
    canActivate: [authGuard],
    resolve: { stats: dashboardResolver }
  },

  // Lazy-loaded with functional guard (modern approach)
  {
    path: 'products',
    loadChildren: () => import('./products/routes').then(m => m.PRODUCT_ROUTES),
    canMatch: [() => inject(AuthService).isAuthenticated()]
  },

  // Lazy-load standalone component
  {
    path: 'profile',
    loadComponent: () => import('./profile.component').then(c => c.ProfileComponent)
  },

  // Nested routes
  {
    path: 'admin',
    component: AdminLayoutComponent,
    canActivate: [authGuard, roleGuard('admin')],
    children: [
      { path: '', redirectTo: 'users', pathMatch: 'full' },
      { path: 'users', component: UserManagementComponent },
      { path: 'users/:id', component: UserDetailComponent },
      { path: 'settings', component: AdminSettingsComponent }
    ]
  },

  // Wildcard — must be last!
  { path: '**', component: NotFoundComponent }
];

// Functional guards (Angular 15+) — replace class-based guards
export const authGuard: CanActivateFn = (route, state) => {
  const auth = inject(AuthService);
  const router = inject(Router);
  if (auth.isLoggedIn()) return true;
  return router.createUrlTree(['/login'], { queryParams: { returnUrl: state.url } });
};

// Role guard factory
export function roleGuard(requiredRole: string): CanActivateFn {
  return () => {
    const auth = inject(AuthService);
    return auth.hasRole(requiredRole) || inject(Router).createUrlTree(['/forbidden']);
  };
}

// Resolver — fetch data before route activates
export const dashboardResolver: ResolveFn&lt;DashboardStats&gt; = () => {
  return inject(DashboardService).getStats().pipe(
    catchError(() => {
      inject(Router).navigate(['/error']);
      return EMPTY;
    })
  );
};

// canDeactivate — warn on unsaved changes
export const unsavedChangesGuard: CanDeactivateFn&lt;{ hasUnsavedChanges: () => boolean }&gt; =
  (component) => {
    if (component.hasUnsavedChanges()) {
      return confirm('You have unsaved changes. Leave anyway?');
    }
    return true;
  };

// Preloading strategies
RouterModule.forRoot(routes, {
  preloadingStrategy: PreloadAllModules  // preload ALL lazy modules after initial load
  // Or: QuicklinkStrategy — preload only visible links (via quicklink library)
})</pre>

<h2 id="ng-forms" class="section-break">111. Angular Forms (Reactive vs Template)</h2>
<p class="small"><strong>Checklist:</strong> FormBuilder · FormGroup/FormControl/FormArray · validators · custom validators · async validators · dynamic forms · template-driven vs reactive · valueChanges · patchValue/setValue · strong typing</p>

<pre>// REACTIVE FORMS — recommended for complex forms

// Strongly-typed form (Angular 14+)
interface LoginForm {
  email: FormControl&lt;string&gt;;
  password: FormControl&lt;string&gt;;
  rememberMe: FormControl&lt;boolean&gt;;
}

@Component({
  template: `
    &lt;form [formGroup]="loginForm" (ngSubmit)="onSubmit()"&gt;
      &lt;input formControlName="email" /&gt;
      &lt;div *ngIf="loginForm.controls.email.errors?.['required']"&gt;
        Email is required
      &lt;/div&gt;
      &lt;div *ngIf="loginForm.controls.email.errors?.['email']"&gt;
        Invalid email format
      &lt;/div&gt;
      &lt;div *ngIf="loginForm.controls.email.errors?.['emailTaken']"&gt;
        Email already registered
      &lt;/div&gt;

      &lt;input formControlName="password" type="password" /&gt;
      &lt;label&gt;
        &lt;input formControlName="rememberMe" type="checkbox" /&gt;
        Remember me
      &lt;/label&gt;
      &lt;button [disabled]="loginForm.invalid"&gt;Login&lt;/button&gt;
    &lt;/form&gt;
  `
})
export class LoginComponent {
  loginForm = new FormGroup&lt;LoginForm&gt;({
    email: new FormControl('', {
      nonNullable: true,
      validators: [Validators.required, Validators.email],
      asyncValidators: [this.emailExistsValidator()]
    }),
    password: new FormControl('', {
      nonNullable: true,
      validators: [Validators.required, Validators.minLength(8)]
    }),
    rememberMe: new FormControl(false, { nonNullable: true })
  });

  // Custom sync validator
  static passwordStrength(control: AbstractControl): ValidationErrors | null {
    const value = control.value;
    const hasUpper = /[A-Z]/.test(value);
    const hasLower = /[a-z]/.test(value);
    const hasDigit = /\d/.test(value);
    const hasSpecial = /[!@#$%^&*]/.test(value);
    const valid = hasUpper &amp;&amp; hasLower &amp;&amp; hasDigit &amp;&amp; hasSpecial;
    return valid ? null : { weakPassword: true };
  }

  // Custom async validator — check if email exists on server
  emailExistsValidator(): AsyncValidatorFn {
    return (control: AbstractControl): Observable&lt;ValidationErrors | null&gt; => {
      return this.authService.checkEmail(control.value).pipe(
        map(exists => exists ? { emailTaken: true } : null),
        catchError(() => of(null))
      );
    };
  }

  // Cross-field validator (password confirmation)
  static passwordMatch(group: AbstractControl): ValidationErrors | null {
    const password = group.get('password')?.value;
    const confirm = group.get('confirmPassword')?.value;
    return password === confirm ? null : { passwordMismatch: true };
  }

  // FormArray — dynamic number of fields (e.g., add skills)
  skills = new FormArray&lt;FormControl&lt;string&gt;&gt;([]);
  addSkill() { this.skills.push(new FormControl('', { nonNullable: true })); }
  removeSkill(i: number) { this.skills.removeAt(i); }

  onSubmit() {
    if (this.loginForm.valid) {
      const value = this.loginForm.getRawValue(); // typed!
      // value.email: string, value.password: string, value.rememberMe: boolean
    }
  }
}</pre>

<h2 id="ng-http" class="section-break">112. Angular HTTP &amp; Interceptors</h2>
<p class="small"><strong>Checklist:</strong> HttpClient · typed responses · interceptors (class & functional) · error handling · caching · retry · request/response transformation · XSRF protection</p>

<pre>// HttpClient basics
@Injectable({ providedIn: 'root' })
export class ProductService {
  private url = '/api/products';

  constructor(private http: HttpClient) {}

  getAll(): Observable&lt;Product[]&gt; {
    return this.http.get&lt;Product[]&gt;(this.url);
  }

  getById(id: string): Observable&lt;Product&gt; {
    return this.http.get&lt;Product&gt;(`${this.url}/${id}`);
  }

  create(product: CreateProductDto): Observable&lt;Product&gt; {
    return this.http.post&lt;Product&gt;(this.url, product);
  }

  update(id: string, product: Partial&lt;Product&gt;): Observable&lt;Product&gt; {
    return this.http.patch&lt;Product&gt;(`${this.url}/${id}`, product);
  }

  delete(id: string): Observable&lt;void&gt; {
    return this.http.delete&lt;void&gt;(`${this.url}/${id}`);
  }

  search(params: SearchParams): Observable&lt;PaginatedResponse&lt;Product&gt;&gt; {
    return this.http.get&lt;PaginatedResponse&lt;Product&gt;&gt;(this.url, {
      params: new HttpParams()
        .set('query', params.query)
        .set('page', params.page.toString())
        .set('limit', params.limit.toString())
    });
  }
}

// Functional interceptor (Angular 15+) — MODERN APPROACH
export const authInterceptor: HttpInterceptorFn = (req, next) => {
  const auth = inject(AuthService);
  const token = auth.getToken();

  if (token) {
    req = req.clone({
      setHeaders: { Authorization: `Bearer ${token}` }
    });
  }
  return next(req);
};

// Error interceptor with refresh token
export const errorInterceptor: HttpInterceptorFn = (req, next) => {
  const auth = inject(AuthService);
  const router = inject(Router);

  return next(req).pipe(
    catchError((error: HttpErrorResponse) => {
      if (error.status === 401) {
        return auth.refreshToken().pipe(
          switchMap(newToken => {
            const cloned = req.clone({
              setHeaders: { Authorization: `Bearer ${newToken}` }
            });
            return next(cloned);
          }),
          catchError(() => {
            auth.logout();
            router.navigate(['/login']);
            return throwError(() => error);
          })
        );
      }
      return throwError(() => error);
    })
  );
};

// Loading interceptor
export const loadingInterceptor: HttpInterceptorFn = (req, next) => {
  const loading = inject(LoadingService);
  loading.show();
  return next(req).pipe(finalize(() => loading.hide()));
};

// Register interceptors
export const appConfig: ApplicationConfig = {
  providers: [
    provideHttpClient(
      withInterceptors([authInterceptor, errorInterceptor, loadingInterceptor])
    )
  ]
};</pre>

<h2 id="ng-standalone" class="section-break">113. Angular Standalone Components &amp; Modern APIs</h2>
<p class="small"><strong>Checklist:</strong> Standalone components · bootstrapping without NgModule · provideRouter · provideHttpClient · input/output/model signals · viewChild/contentChild signals · deferrable views · control flow (@if, @for, @switch)</p>

<pre>// Standalone component — no NgModule needed!
@Component({
  standalone: true,
  selector: 'app-product-card',
  imports: [CommonModule, RouterLink],  // import what you need
  template: `
    &lt;!-- New control flow (Angular 17+) --&gt;
    @if (product) {
      &lt;div class="card"&gt;
        &lt;h3&gt;{{ product.name }}&lt;/h3&gt;
        &lt;p&gt;{{ product.price | currency }}&lt;/p&gt;
        @switch (product.status) {
          @case ('active') { &lt;span class="badge green"&gt;Active&lt;/span&gt; }
          @case ('draft') { &lt;span class="badge gray"&gt;Draft&lt;/span&gt; }
          @default { &lt;span class="badge"&gt;Unknown&lt;/span&gt; }
        }
      &lt;/div&gt;
    } @else {
      &lt;p&gt;Loading...&lt;/p&gt;
    }
  `
})
export class ProductCardComponent {
  // Signal-based inputs (Angular 17.1+)
  product = input.required&lt;Product&gt;();
  highlighted = input(false);  // optional with default

  // Signal-based output
  addToCart = output&lt;Product&gt;();

  // model() — two-way binding signal (Angular 17.2+)
  quantity = model(1);
}

// Usage:
// &lt;app-product-card [product]="p" [(quantity)]="qty"
//   (addToCart)="onAdd($event)" /&gt;

// Deferrable views — lazy-load heavy components
@Component({
  template: `
    @defer (on viewport) {
      &lt;app-heavy-chart [data]="chartData" /&gt;
    } @placeholder {
      &lt;div class="skeleton"&gt;Loading chart...&lt;/div&gt;
    } @loading (minimum 500ms) {
      &lt;app-spinner /&gt;
    } @error {
      &lt;p&gt;Failed to load chart.&lt;/p&gt;
    }
  `
})
// Triggers: on viewport, on idle, on interaction, on hover, on timer(5s), when condition

// Bootstrapping without NgModule
// main.ts
bootstrapApplication(AppComponent, {
  providers: [
    provideRouter(routes, withPreloading(PreloadAllModules)),
    provideHttpClient(withInterceptors([authInterceptor])),
    provideAnimations(),
    { provide: ErrorHandler, useClass: GlobalErrorHandler }
  ]
});</pre>

<h2 id="ng-pipes" class="section-break">114. Angular Pipes &amp; Directives</h2>
<p class="small"><strong>Checklist:</strong> Built-in pipes · pure vs impure pipes · custom pipes · structural directives · attribute directives · host binding · host listener</p>

<pre>// PURE PIPE — only re-evaluates when input value OR reference changes
// Angular caches the result. Much better for performance.
@Pipe({ name: 'filterBy', standalone: true, pure: true })
export class FilterByPipe implements PipeTransform {
  transform(items: any[], field: string, value: string): any[] {
    if (!items || !value) return items;
    return items.filter(item =>
      item[field].toLowerCase().includes(value.toLowerCase())
    );
  }
}
// ✅ Use with OnPush + immutable data: products = [...products, newProduct]
// Usage: *ngFor="let p of products | filterBy:'name':searchTerm"

// IMPURE PIPE — re-evaluates on EVERY change detection cycle!
@Pipe({ name: 'filterBy', pure: false })
// ❌ Avoid! Runs dozens of times per second. Use computed() or component logic instead.

// CUSTOM DIRECTIVE — attribute directive
@Directive({
  selector: '[appTooltip]',
  standalone: true
})
export class TooltipDirective {
  @Input('appTooltip') text = '';
  private tooltipEl: HTMLElement | null = null;

  @HostListener('mouseenter')
  show() {
    this.tooltipEl = document.createElement('div');
    this.tooltipEl.className = 'tooltip';
    this.tooltipEl.textContent = this.text;
    document.body.appendChild(this.tooltipEl);
    // position near host element...
  }

  @HostListener('mouseleave')
  hide() {
    this.tooltipEl?.remove();
    this.tooltipEl = null;
  }
}

// STRUCTURAL DIRECTIVE — modifies DOM structure
@Directive({ selector: '[appRepeat]', standalone: true })
export class RepeatDirective {
  constructor(
    private templateRef: TemplateRef&lt;any&gt;,
    private viewContainer: ViewContainerRef
  ) {}

  @Input() set appRepeat(times: number) {
    this.viewContainer.clear();
    for (let i = 0; i &lt; times; i++) {
      this.viewContainer.createEmbeddedView(this.templateRef, { index: i });
    }
  }
}
// Usage: &lt;div *appRepeat="5"&gt;Repeated 5 times&lt;/div&gt;</pre>

<h2 id="ng-content-projection" class="section-break">115. Content Projection &amp; Templates</h2>
<p class="small"><strong>Checklist:</strong> ng-content · select attribute · multi-slot projection · ng-template · ng-container · ngTemplateOutlet · dynamic components</p>

<pre>// Single-slot content projection
@Component({
  selector: 'app-card',
  template: `
    &lt;div class="card"&gt;
      &lt;ng-content&gt;&lt;/ng-content&gt;
    &lt;/div&gt;
  `
})
// Usage: &lt;app-card&gt;Any content here!&lt;/app-card&gt;

// Multi-slot projection — powerful composition pattern!
@Component({
  selector: 'app-dialog',
  template: `
    &lt;div class="dialog"&gt;
      &lt;header&gt;&lt;ng-content select="[dialog-title]"&gt;&lt;/ng-content&gt;&lt;/header&gt;
      &lt;main&gt;&lt;ng-content&gt;&lt;/ng-content&gt;&lt;/main&gt;
      &lt;footer&gt;&lt;ng-content select="[dialog-actions]"&gt;&lt;/ng-content&gt;&lt;/footer&gt;
    &lt;/div&gt;
  `
})
// Usage:
// &lt;app-dialog&gt;
//   &lt;h2 dialog-title&gt;Confirm Delete&lt;/h2&gt;
//   &lt;p&gt;Are you sure you want to delete this item?&lt;/p&gt;
//   &lt;div dialog-actions&gt;
//     &lt;button (click)="cancel()"&gt;Cancel&lt;/button&gt;
//     &lt;button (click)="confirm()"&gt;Delete&lt;/button&gt;
//   &lt;/div&gt;
// &lt;/app-dialog&gt;

// ng-template + ngTemplateOutlet — render templates dynamically
@Component({
  template: `
    &lt;app-data-table [data]="users" [columns]="columns"&gt;
      &lt;!-- Custom cell template --&gt;
      &lt;ng-template #statusTpl let-row&gt;
        &lt;span [class]="'badge ' + row.status"&gt;{{ row.status }}&lt;/span&gt;
      &lt;/ng-template&gt;
      &lt;ng-template #actionsTpl let-row&gt;
        &lt;button (click)="edit(row)"&gt;Edit&lt;/button&gt;
        &lt;button (click)="delete(row)"&gt;Delete&lt;/button&gt;
      &lt;/ng-template&gt;
    &lt;/app-data-table&gt;
  `
})

// Dynamic component loading (Angular 13+)
@Component({
  template: `&lt;ng-container #host&gt;&lt;/ng-container&gt;`
})
export class DynamicLoaderComponent {
  @ViewChild('host', { read: ViewContainerRef }) host!: ViewContainerRef;

  async loadWidget(type: string) {
    this.host.clear();
    const component = await this.getComponent(type);
    const ref = this.host.createComponent(component);
    ref.instance.data = this.widgetData;
  }

  private async getComponent(type: string) {
    switch (type) {
      case 'chart': return (await import('./chart.component')).ChartComponent;
      case 'table': return (await import('./table.component')).TableComponent;
      default: throw new Error(`Unknown widget: ${type}`);
    }
  }
}</pre>

<h2 id="ng-performance" class="section-break">116. Angular Performance Optimization</h2>
<p class="small"><strong>Checklist:</strong> trackBy · OnPush · pure pipes · lazy loading · @defer · virtual scrolling · bundle size · source map analysis · tree shaking · zone-less Angular</p>

<pre>// PERFORMANCE CHECKLIST — apply all of these for production apps

// 1. trackBy for ngFor — prevents re-creating DOM elements
@for (product of products; track product.id) {
  &lt;app-product-card [product]="product" /&gt;
}
// Without trackBy: entire list re-renders on data change
// With trackBy: only changed items re-render

// 2. OnPush everywhere + immutable data patterns
// Already covered in section 106

// 3. Virtual scrolling for large lists
import { ScrollingModule } from '@angular/cdk/scrolling';

&lt;cdk-virtual-scroll-viewport itemSize="72" class="list-viewport"&gt;
  &lt;div *cdkVirtualFor="let item of items; trackBy: trackById"&gt;
    {{ item.name }}
  &lt;/div&gt;
&lt;/cdk-virtual-scroll-viewport&gt;
// Only renders visible items! 10,000 items? Only ~20 DOM nodes.

// 4. Lazy loading (already covered in routing)
// 5. @defer for heavy components (covered in section 113)

// 6. Bundle analysis
// ng build --stats-json
// npx webpack-bundle-analyzer dist/your-app/stats.json
// Look for: large dependencies, duplicate code, unused imports

// 7. Angular budgets in angular.json
"budgets": [
  { "type": "initial", "maximumWarning": "500kb", "maximumError": "1mb" },
  { "type": "anyComponentStyle", "maximumWarning": "4kb", "maximumError": "8kb" }
]

// 8. Preloading strategies
// PreloadAllModules — load all lazy chunks after initial load
// Custom: preload based on user role, viewport links, or prediction

// 9. Image optimization
&lt;img ngSrc="hero.jpg" width="800" height="400" priority /&gt;
// NgOptimizedImage: automatic lazy loading, srcset, priority hints

// 10. Zone-less Angular (bleeding edge)
bootstrapApplication(AppComponent, {
  providers: [provideExperimentalZonelessChangeDetection()]
});
// Requires all components to use Signals or manual CD</pre>

<div class="interview-q">
<h4>🎯 Interview Questions — Angular Performance</h4>
<p><strong>Q: Your Angular app takes 8 seconds to load. Walk me through your optimization approach.</strong></p>
<p><strong>A:</strong> (1) Measure: Lighthouse audit, performance.getEntries(), bundle analyzer. (2) <strong>Code splitting</strong>: lazy-load routes, @defer for below-fold components. (3) <strong>Bundle size</strong>: remove unused imports, replace moment.js with date-fns, tree-shake lodash. (4) <strong>Loading</strong>: preload critical fonts, preconnect to API, SSR for FCP. (5) <strong>Images</strong>: NgOptimizedImage, WebP/AVIF, responsive srcset. (6) <strong>Caching</strong>: service worker, HTTP cache headers, stale-while-revalidate. (7) <strong>Runtime</strong>: OnPush everywhere, virtual scroll for lists, trackBy. (8) Set budgets in CI to prevent regression.</p>
</div>

<h2 id="ng-testing" class="section-break">117. Angular Testing</h2>
<p class="small"><strong>Checklist:</strong> TestBed · ComponentFixture · provide mock services · fakeAsync/tick/flush · HttpClientTestingModule · RouterTestingModule · component harness · integration tests</p>

<pre>// Component test with TestBed
describe('ProductListComponent', () => {
  let component: ProductListComponent;
  let fixture: ComponentFixture&lt;ProductListComponent&gt;;
  let mockProductService: jasmine.SpyObj&lt;ProductService&gt;;

  beforeEach(async () => {
    mockProductService = jasmine.createSpyObj('ProductService', ['getAll', 'delete']);
    mockProductService.getAll.and.returnValue(of([
      { id: '1', name: 'Laptop', price: 1200 },
      { id: '2', name: 'Phone', price: 800 }
    ]));

    await TestBed.configureTestingModule({
      imports: [ProductListComponent],  // standalone component
      providers: [
        { provide: ProductService, useValue: mockProductService }
      ]
    }).compileComponents();

    fixture = TestBed.createComponent(ProductListComponent);
    component = fixture.componentInstance;
    fixture.detectChanges(); // triggers ngOnInit
  });

  it('should display products', () => {
    const cards = fixture.nativeElement.querySelectorAll('.product-card');
    expect(cards.length).toBe(2);
    expect(cards[0].textContent).toContain('Laptop');
  });

  it('should call delete and refresh list', fakeAsync(() => {
    mockProductService.delete.and.returnValue(of(void 0));
    mockProductService.getAll.and.returnValue(of([
      { id: '2', name: 'Phone', price: 800 }
    ]));

    component.deleteProduct('1');
    tick(); // resolve the observable

    expect(mockProductService.delete).toHaveBeenCalledWith('1');
    fixture.detectChanges();
    const cards = fixture.nativeElement.querySelectorAll('.product-card');
    expect(cards.length).toBe(1);
  }));
});

// HTTP testing
describe('ProductService', () => {
  let service: ProductService;
  let httpMock: HttpTestingController;

  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [
        ProductService,
        provideHttpClient(),
        provideHttpClientTesting()
      ]
    });
    service = TestBed.inject(ProductService);
    httpMock = TestBed.inject(HttpTestingController);
  });

  afterEach(() => httpMock.verify()); // no outstanding requests

  it('should fetch products', () => {
    const mockProducts = [{ id: '1', name: 'Laptop' }];
    service.getAll().subscribe(products => {
      expect(products).toEqual(mockProducts);
    });
    const req = httpMock.expectOne('/api/products');
    expect(req.request.method).toBe('GET');
    req.flush(mockProducts);
  });
});</pre>

<h2 id="ng-ngrx" class="section-break">118. State Management with NgRx</h2>
<p class="small"><strong>Checklist:</strong> Store · Actions · Reducers · Selectors · Effects · Entity adapter · Component Store · SignalStore</p>

<pre>// NgRx — Redux pattern for Angular

// 1. ACTIONS — describe events
export const ProductActions = createActionGroup({
  source: 'Products',
  events: {
    'Load Products': emptyProps(),
    'Load Products Success': props&lt;{ products: Product[] }&gt;(),
    'Load Products Failure': props&lt;{ error: string }&gt;(),
    'Delete Product': props&lt;{ id: string }&gt;(),
    'Delete Product Success': props&lt;{ id: string }&gt;(),
  }
});

// 2. REDUCER — how state changes
interface ProductState {
  products: Product[];
  loading: boolean;
  error: string | null;
}

const initialState: ProductState = { products: [], loading: false, error: null };

export const productReducer = createReducer(
  initialState,
  on(ProductActions.loadProducts, state => ({ ...state, loading: true, error: null })),
  on(ProductActions.loadProductsSuccess, (state, { products }) =>
    ({ ...state, products, loading: false })),
  on(ProductActions.loadProductsFailure, (state, { error }) =>
    ({ ...state, loading: false, error })),
  on(ProductActions.deleteProductSuccess, (state, { id }) =>
    ({ ...state, products: state.products.filter(p => p.id !== id) }))
);

// 3. SELECTORS — derive data from state (memoized!)
export const selectProductState = createFeatureSelector&lt;ProductState&gt;('products');
export const selectAllProducts = createSelector(selectProductState, s => s.products);
export const selectLoading = createSelector(selectProductState, s => s.loading);
export const selectExpensiveProducts = createSelector(
  selectAllProducts,
  products => products.filter(p => p.price > 1000)
);

// 4. EFFECTS — side effects (API calls)
@Injectable()
export class ProductEffects {
  loadProducts$ = createEffect(() =>
    this.actions$.pipe(
      ofType(ProductActions.loadProducts),
      exhaustMap(() =>
        this.productService.getAll().pipe(
          map(products => ProductActions.loadProductsSuccess({ products })),
          catchError(error =>
            of(ProductActions.loadProductsFailure({ error: error.message })))
        )
      )
    )
  );

  constructor(private actions$: Actions, private productService: ProductService) {}
}

// 5. COMPONENT — use store
@Component({
  template: `
    @if (loading$ | async) { &lt;app-spinner /&gt; }
    @for (product of products$ | async; track product.id) {
      &lt;app-product-card [product]="product" (delete)="onDelete($event)" /&gt;
    }
  `
})
export class ProductListComponent {
  products$ = this.store.select(selectAllProducts);
  loading$ = this.store.select(selectLoading);

  constructor(private store: Store) {
    this.store.dispatch(ProductActions.loadProducts());
  }

  onDelete(id: string) {
    this.store.dispatch(ProductActions.deleteProduct({ id }));
  }
}

// NgRx SignalStore (modern alternative) — simpler, signal-based
export const ProductStore = signalStore(
  withState({ products: [] as Product[], loading: false }),
  withComputed(({ products }) => ({
    expensiveProducts: computed(() => products().filter(p => p.price > 1000)),
    total: computed(() => products().length)
  })),
  withMethods((store, productService = inject(ProductService)) => ({
    async loadProducts() {
      patchState(store, { loading: true });
      const products = await firstValueFrom(productService.getAll());
      patchState(store, { products, loading: false });
    }
  }))
);</pre>

<h2 id="ng-patterns" class="section-break">119. Angular Best Practices &amp; Patterns</h2>
<p class="small"><strong>Checklist:</strong> Smart vs dumb components · service layer patterns · error handling strategy · environment configs · barrel exports · feature modules · shared modules</p>

<pre>// SMART vs DUMB components (Container vs Presentational)

// SMART (Container) — knows about services, state, business logic
@Component({
  template: `
    &lt;app-product-filters [categories]="categories"
      (filterChange)="onFilter($event)" /&gt;
    &lt;app-product-grid [products]="filteredProducts$ | async"
      (addToCart)="onAddToCart($event)" /&gt;
  `
})
export class ProductPageComponent {
  // Handles: data fetching, state management, business logic
  private store = inject(ProductStore);
  filteredProducts$ = this.store.filteredProducts$;
}

// DUMB (Presentational) — only @Input and @Output, no injected services
@Component({
  template: `
    @for (product of products; track product.id) {
      &lt;div class="card" (click)="addToCart.emit(product)"&gt;
        {{ product.name }} — {{ product.price | currency }}
      &lt;/div&gt;
    }
  `,
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class ProductGridComponent {
  @Input() products: Product[] = [];
  @Output() addToCart = new EventEmitter&lt;Product&gt;();
  // Easy to test, reusable, predictable
}

// SERVICE LAYER PATTERN
// API Service → Domain Service → Component
@Injectable({ providedIn: 'root' })
export class OrderApiService {
  // Only HTTP calls, no business logic
  getOrders = () => this.http.get&lt;Order[]&gt;('/api/orders');
}

@Injectable({ providedIn: 'root' })
export class OrderService {
  // Business logic, caching, transformation
  private cache = new Map&lt;string, Order&gt;();

  getOrderWithTotal(id: string): Observable&lt;OrderWithTotal&gt; {
    return this.api.getOrder(id).pipe(
      map(order => ({
        ...order,
        total: order.items.reduce((sum, i) => sum + i.price * i.quantity, 0),
        tax: this.calculateTax(order),
        status: this.mapStatus(order.rawStatus)
      })),
      tap(order => this.cache.set(id, order))
    );
  }
}

// ENVIRONMENT-BASED FEATURE FLAGS
@Injectable({ providedIn: 'root' })
export class FeatureFlagService {
  private flags = signal(environment.featureFlags);

  isEnabled(flag: string): boolean {
    return this.flags()[flag] ?? false;
  }
}

// Usage in template:
// @if (featureFlags.isEnabled('newCheckout')) {
//   &lt;app-new-checkout /&gt;
// } @else {
//   &lt;app-legacy-checkout /&gt;
// }</pre>

<h2 id="ng-common-mistakes" class="section-break">120. Common Angular Mistakes &amp; Fixes</h2>
<p class="small"><strong>Checklist:</strong> Memory leaks · ExpressionChangedAfterItHasBeenChecked · circular dependencies · over-subscribing · template performance · AOT issues</p>

<pre>// MISTAKE 1: Memory leaks from subscriptions
// ❌
ngOnInit() { this.dataService.data$.subscribe(d => this.data = d); }
// ✅
ngOnInit() {
  this.dataService.data$.pipe(takeUntilDestroyed()).subscribe(d => this.data = d);
}
// ✅ BEST: use async pipe in template
// {{ data$ | async }}

// MISTAKE 2: ExpressionChangedAfterItHasBeenChecked
// Happens when you change state DURING change detection
// ❌ Changing parent state in ngAfterViewInit of child
ngAfterViewInit() {
  this.parentService.title = 'New Title'; // ERROR in dev mode!
}
// ✅ Fix: defer the change
ngAfterViewInit() {
  setTimeout(() => this.parentService.title = 'New Title');
  // OR: this.cdr.detectChanges();
}

// MISTAKE 3: Not using trackBy with ngFor
// ❌ Entire list re-renders every time
&lt;div *ngFor="let item of items"&gt;{{ item.name }}&lt;/div&gt;
// ✅
&lt;div *ngFor="let item of items; trackBy: trackById"&gt;{{ item.name }}&lt;/div&gt;
trackById = (index: number, item: any) => item.id;
// ✅ Angular 17 @for:
// @for (item of items; track item.id) { ... }

// MISTAKE 4: Function calls in templates
// ❌ getFullName() called on EVERY change detection cycle!
&lt;p&gt;{{ getFullName() }}&lt;/p&gt;
// ✅ Use a pipe
&lt;p&gt;{{ user | fullName }}&lt;/p&gt;
// ✅ Or compute in component
fullName = computed(() => `${this.user().first} ${this.user().last}`);

// MISTAKE 5: Importing entire libraries
// ❌ Imports ALL of lodash (70KB gzipped!)
import _ from 'lodash';
// ✅ Import only what you need (2KB)
import debounce from 'lodash-es/debounce';
// ✅ Or use native
const unique = [...new Set(arr)]; // no lodash needed

// MISTAKE 6: Not handling HTTP errors
// ❌ Error kills the observable stream
this.api.getData().subscribe(data => this.data = data);
// ✅
this.api.getData().pipe(
  catchError(error => {
    this.errorService.handle(error);
    return of(fallbackData);
  })
).subscribe(data => this.data = data);

// MISTAKE 7: Circular dependencies
// Module A imports Module B, Module B imports Module A → ERROR
// ✅ Fix: extract shared code into a third module
// ✅ Fix: use injection tokens instead of direct imports</pre>

<div class="interview-q">
<h4>🎯 Interview Questions — Angular Architecture</h4>
<p><strong>Q: How would you migrate a large Angular app from Zone.js to Signals?</strong></p>
<p><strong>A:</strong> Gradual migration, not big-bang. (1) Start by adding <code>OnPush</code> to all components (prerequisite). (2) Replace simple component state with <code>signal()</code> and <code>computed()</code>. (3) Replace BehaviorSubjects in services with signals where appropriate. (4) Use <code>toSignal()</code> to convert observables to signals at boundaries. (5) Keep RxJS for complex async flows (HTTP, WebSocket, operators). (6) Test each module independently. (7) Eventually enable <code>provideExperimentalZonelessChangeDetection()</code> when all components are ready.</p>

<p><strong>Q: Explain your approach to structuring a large Angular enterprise application.</strong></p>
<p><strong>A:</strong> Feature-based folder structure. <strong>Core module</strong>: singleton services (auth, logging, interceptors) — imported once in root. <strong>Shared module</strong>: reusable components, pipes, directives — imported by feature modules. <strong>Feature modules</strong>: each has its own components, services, routes, state — lazy-loaded independently. Smart/dumb component split: containers handle logic, presentational components are pure @Input/@Output. API layer separated from business logic layer. NgRx (or SignalStore) per feature slice. Strict typing, no <code>any</code>. ESLint + Prettier + Husky enforced.</p>
</div>
"""
