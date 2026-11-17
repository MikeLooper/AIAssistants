import { HttpTestingController } from '@angular/common/http/testing';
import { ComponentFixture, TestBed } from '@angular/core/testing';

import { API, aboutFixture, configure, testProviders } from '../../testing/helpers';
import { AboutPage } from './about-page';

describe('AboutPage', () => {
  let fixture: ComponentFixture<AboutPage>;
  let http: HttpTestingController;

  beforeEach(() => {
    TestBed.configureTestingModule({ providers: testProviders() });
    configure();
    http = TestBed.inject(HttpTestingController);
    fixture = TestBed.createComponent(AboutPage);
    fixture.detectChanges();
  });

  afterEach(() => http.verify());

  const el = () => fixture.nativeElement as HTMLElement;

  it('shows the reviewer version, configuration, health and UI settings', async () => {
    http.expectOne(`${API}/api/about`).flush(aboutFixture());
    http.expectOne(`${API}/api/health`).flush({ status: 'degraded', checks: { reviewerScript: true, aiTool: false },
                                                 details: { aiTool: 'no CLI on PATH' } });
    await fixture.whenStable();
    expect(el().querySelector('[data-testid="reviewer-version"]')!.textContent).toBe('1.0.0');
    expect(el().textContent).toContain('claude: found (/bin/claude)');
    expect(el().textContent).toContain('copilot: not found on PATH');
    expect(el().textContent).toContain('"DefaultModel": "claude-sonnet-5-5"');
    expect(el().textContent).toContain('aiTool');
    expect(el().textContent).toContain('failing — no CLI on PATH');
    expect(el().textContent).toContain(API);
  });

  it('shows the body of a 503 health response', async () => {
    http.expectOne(`${API}/api/about`).flush(aboutFixture({ reviewerVersion: null }));
    http.expectOne(`${API}/api/health`).flush({ status: 'unhealthy', checks: { reviewerScript: false }, details: {} },
                                              { status: 503, statusText: 'Service Unavailable' });
    await fixture.whenStable();
    expect(fixture.componentInstance.health()!.status).toBe('unhealthy');
    expect(el().querySelector('[data-testid="reviewer-version"]')!.textContent).toBe('unknown');
  });

  it('shows errors when the API is unreachable, and refreshes', async () => {
    http.expectOne(`${API}/api/about`).error(new ProgressEvent('error'));
    http.expectOne(`${API}/api/health`).error(new ProgressEvent('error'));
    await fixture.whenStable();
    expect(fixture.componentInstance.aboutError()).toContain('could not be reached');
    expect(fixture.componentInstance.healthError()).toContain('could not be reached');
    expect(el().querySelectorAll('.alert-error').length).toBe(2);

    el().querySelector<HTMLButtonElement>('button')!.click();
    http.expectOne(`${API}/api/about`).flush(aboutFixture());
    http.expectOne(`${API}/api/health`).flush({ status: 'healthy', checks: {}, details: {} });
    expect(fixture.componentInstance.aboutError()).toBeNull();
    expect(fixture.componentInstance.healthError()).toBeNull();
  });

  it('shows the config load error', async () => {
    http.expectOne(`${API}/api/about`).flush(aboutFixture());
    http.expectOne(`${API}/api/health`).flush({ status: 'healthy', checks: {}, details: {} });
    await fixture.componentInstance['config'].load('missing.json', (async () => {
      throw new Error('404');
    }) as unknown as typeof fetch);
    await fixture.whenStable();
    expect(el().querySelector('.alert-warning')!.textContent).toContain('missing.json');
  });
});
