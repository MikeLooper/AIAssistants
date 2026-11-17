import { HttpTestingController } from '@angular/common/http/testing';
import { TestBed } from '@angular/core/testing';
import { Router, provideRouter } from '@angular/router';
import { RouterTestingHarness } from '@angular/router/testing';

import { App } from './app';
import { routes } from './app.routes';
import { API, configure, flushAsync, testProviders } from './testing/helpers';

async function createApp() {
  const fixture = TestBed.createComponent(App);
  fixture.detectChanges();
  await flushAsync();
  return fixture;
}

describe('App shell', () => {
  let http: HttpTestingController;

  beforeEach(() => {
    TestBed.configureTestingModule({ providers: testProviders() });
    http = TestBed.inject(HttpTestingController);
  });

  it('shows the Testers link and the environment in development', async () => {
    configure({ environment: 'development' });
    const fixture = await createApp();
    http.expectOne(`${API}/api/health`).flush({ status: 'healthy', checks: {}, details: {} });
    await fixture.whenStable();
    const el = fixture.nativeElement as HTMLElement;
    expect(el.querySelector('[data-testid="nav-testers"]')).not.toBeNull();
    expect(el.querySelector('[data-testid="environment"]')!.textContent).toBe('development');
    expect(el.querySelector('.api-state')!.className).toContain('api-healthy');
  });

  it('hides the Testers link in production', async () => {
    configure({ environment: 'production' });
    const fixture = await createApp();
    http.expectOne(`${API}/api/health`).flush({ status: 'degraded', checks: {}, details: {} });
    await fixture.whenStable();
    const el = fixture.nativeElement as HTMLElement;
    expect(el.querySelector('[data-testid="nav-testers"]')).toBeNull();
    expect(el.querySelector('[data-testid="environment"]')!.textContent).toBe('production');
    expect(fixture.componentInstance.apiState()).toBe('degraded');
  });

  it('reads the state from a 503 body, else reports the API unreachable', async () => {
    configure();
    const fixture = await createApp();
    http.expectOne(`${API}/api/health`).flush({ status: 'unhealthy' }, { status: 503, statusText: 'Unavailable' });
    expect(fixture.componentInstance.apiState()).toBe('unhealthy');
    fixture.destroy();

    const second = await createApp();
    http.expectOne(`${API}/api/health`).error(new ProgressEvent('error'));
    expect(second.componentInstance.apiState()).toBe('unreachable');
  });
});

describe('routes', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({ providers: [...testProviders(), provideRouter(routes)] });
  });

  it('opens the testers page in development', async () => {
    configure({ environment: 'development' });
    const harness = await RouterTestingHarness.create();
    await harness.navigateByUrl('/testers');
    expect(TestBed.inject(Router).url).toBe('/testers');
  });

  it('redirects the testers page to the review page in production', async () => {
    configure({ environment: 'production' });
    const harness = await RouterTestingHarness.create();
    await harness.navigateByUrl('/testers');
    expect(TestBed.inject(Router).url).toBe('/review');
  });

  it('redirects unknown and empty paths to the review page', async () => {
    configure();
    const harness = await RouterTestingHarness.create();
    await harness.navigateByUrl('/nowhere');
    expect(TestBed.inject(Router).url).toBe('/review');
    await harness.navigateByUrl('/');
    expect(TestBed.inject(Router).url).toBe('/review');
  });
});
