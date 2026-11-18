import { HttpTestingController } from '@angular/common/http/testing';
import { ComponentFixture, TestBed } from '@angular/core/testing';
import { Router } from '@angular/router';

import { JobDetail } from '../../core/api.models';
import { API, configure, flushAsync, jobFixture, testProviders } from '../../testing/helpers';
import { JobDetailPage } from './job-detail-page';
import { JobsPage } from './jobs-page';

describe('JobsPage', () => {
  let http: HttpTestingController;

  beforeEach(() => {
    TestBed.configureTestingModule({ providers: testProviders() });
    http = TestBed.inject(HttpTestingController);
  });

  afterEach(() => http.verify());

  it('lists every job in development', async () => {
    configure();
    const fixture = TestBed.createComponent(JobsPage);
    fixture.detectChanges();
    await flushAsync();
    http.expectOne(`${API}/api/jobs`).flush([
      jobFixture({ id: 'a', name: 'myapp', status: 'completed', overallScore: 87, overallBand: 'Good' }),
      jobFixture({ id: 'b', kind: 'test', name: 'api-java', verdict: 'pass', status: 'completed' }),
    ]);
    await fixture.whenStable();
    const rows = (fixture.nativeElement as HTMLElement).querySelectorAll('tbody tr');
    expect(rows.length).toBe(2);
    expect(rows[0].textContent).toContain('87 (Good)');
    expect(rows[0].querySelector('a')!.getAttribute('href')).toBe('/jobs/a');
    expect(rows[1].textContent).toContain('pass');
  });

  it('lists only reviews in production, and shows the empty state', async () => {
    configure({ environment: 'production' });
    const fixture = TestBed.createComponent(JobsPage);
    fixture.detectChanges();
    await flushAsync();
    http.expectOne(`${API}/api/jobs?kind=review`).flush([]);
    await fixture.whenStable();
    expect((fixture.nativeElement as HTMLElement).textContent).toContain('No jobs yet.');
  });

  it('shows an error and keeps polling', async () => {
    configure({ pollIntervalMs: 300 });
    const fixture = TestBed.createComponent(JobsPage);
    fixture.detectChanges();
    await flushAsync();
    http.expectOne(`${API}/api/jobs`).flush({}, { status: 500, statusText: 'Server Error' });
    expect(fixture.componentInstance.error()).toBe('Server Error (HTTP 500)');
    await flushAsync(350);
    http.expectOne(`${API}/api/jobs`).flush([]);
    expect(fixture.componentInstance.error()).toBeNull();
    fixture.destroy();
  });
});

describe('JobDetailPage', () => {
  let fixture: ComponentFixture<JobDetailPage>;
  let page: JobDetailPage;
  let http: HttpTestingController;
  let navigate: ReturnType<typeof vi.spyOn>;

  async function create(pollIntervalMs = 600_000) {
    configure({ pollIntervalMs });
    fixture = TestBed.createComponent(JobDetailPage);
    page = fixture.componentInstance;
    fixture.componentRef.setInput('id', 'job1');
    fixture.detectChanges();
    await flushAsync();
  }

  function flushJob(job: Partial<JobDetail>) {
    http.expectOne((r) => r.url === `${API}/api/jobs/job1`).flush(jobFixture(job));
  }

  beforeEach(() => {
    TestBed.configureTestingModule({ providers: testProviders() });
    http = TestBed.inject(HttpTestingController);
    navigate = vi.spyOn(TestBed.inject(Router), 'navigate').mockResolvedValue(true);
  });

  afterEach(() => http.verify());

  const el = () => fixture.nativeElement as HTMLElement;

  it('shows a running job with its console output and a cancel button', async () => {
    await create();
    flushJob({ status: 'running' });
    await fixture.whenStable();
    expect(el().querySelector('h1')!.textContent).toContain('Review: myapp');
    expect(el().querySelector('pre.log')!.textContent).toContain('00-init');
    expect(el().textContent).toContain('Cancel job');
    expect(page.finished()).toBe(false);
    expect(page.optionRows().map((r) => r.key)).toEqual(['tool', 'model', 'subjects', 'fileName']);
  });

  it('polls until the review completes, then shows the report', async () => {
    await create(250);
    flushJob({ status: 'queued' });
    await fixture.whenStable();
    expect(el().textContent).toContain('Waiting for a free slot');
    await flushAsync(300);
    flushJob({
      status: 'completed', overallScore: 87, overallBand: 'Good', durationSeconds: 125,
      result: { report: '# Compliance report\n\n| Subject | Score |\n|---|---|\n| Testing | 80 |', runId: 'run-1',
                summary: { usage: { costUsd: 2.25 } } },
    });
    await fixture.whenStable();
    expect(el().querySelector('.markdown h1')!.textContent).toBe('Compliance report');
    expect(el().querySelector('.markdown table')).not.toBeNull();
    expect(page.cost()).toBe('$2.25');
    expect(el().textContent).toContain('2m 05s');
    expect(el().textContent).toContain('run-1');
    expect(page.showLog()).toBe(false); // collapsed after a successful run
    await flushAsync(300);
    http.expectNone((r) => r.url === `${API}/api/jobs/job1`); // polling stopped

    page.showRaw.set(true);
    await fixture.whenStable();
    expect(el().querySelector('pre.raw')!.textContent).toContain('| Testing | 80 |');
  });

  it('shows the test result and the report for a tester job', async () => {
    await create();
    flushJob({
      kind: 'test', name: 'api-java', status: 'completed', verdict: 'fail',
      result: { testResultMarkdown: '# apis-java — FAIL', report: '# Report', testResult: { costUsd: 3 } },
    });
    await fixture.whenStable();
    expect(el().querySelector('h1')!.textContent).toContain('Tester: api-java');
    const headings = Array.from(el().querySelectorAll('section h2')).map((h) => h.textContent!.trim());
    expect(headings.slice(0, 2)).toEqual(['Test result', 'Compliance report']);
    expect(el().textContent).toContain('apis-java — FAIL');
    expect(page.cost()).toBe('$3.00');
  });

  it('shows a failed job’s error and keeps the console open', async () => {
    await create();
    flushJob({ status: 'failed', error: 'step 01: inventory failed', result: { report: null } });
    await fixture.whenStable();
    expect(el().querySelector('.alert-error')!.textContent).toContain('inventory failed');
    expect(page.showLog()).toBe(true);
    expect(page.cost()).toBe('—');
  });

  it('notes a completed job without a report', async () => {
    await create();
    flushJob({ status: 'completed', result: {} });
    await fixture.whenStable();
    expect(el().textContent).toContain('finished without a report');
  });

  it('reports a missing job', async () => {
    await create();
    http.expectOne((r) => r.url === `${API}/api/jobs/job1`).flush({ detail: 'job job1 not found' },
                                                                 { status: 404, statusText: 'Not Found' });
    await fixture.whenStable();
    expect(el().querySelector('.alert-error')!.textContent).toContain('not found');
  });

  it('cancels a job', async () => {
    await create();
    flushJob({ status: 'running' });
    page.cancel();
    http.expectOne(`${API}/api/jobs/job1/cancel`).flush(jobFixture({ status: 'cancelled' }));
    expect(page.job()!.status).toBe('cancelled');
    page.cancel();
    http.expectOne(`${API}/api/jobs/job1/cancel`).flush({ detail: 'x' }, { status: 500, statusText: 'x' });
    expect(page.actionError()).toBe('x (HTTP 500)');
  });

  it('deletes a finished job and returns to the list', async () => {
    await create();
    flushJob({ status: 'completed' });
    page.remove();
    http.expectOne(`${API}/api/jobs/job1`).flush({ detail: 'still running' }, { status: 409, statusText: 'Conflict' });
    expect(page.actionError()).toContain('still running');
    page.remove();
    http.expectOne(`${API}/api/jobs/job1`).flush(null, { status: 204, statusText: 'No Content' });
    expect(navigate).toHaveBeenCalledWith(['/jobs']);
  });

  it('downloads the report and the test result', async () => {
    const create_ = vi.fn(() => 'blob:x');
    Object.assign(URL, { createObjectURL: create_, revokeObjectURL: vi.fn() });
    const click = vi.spyOn(HTMLAnchorElement.prototype, 'click').mockImplementation(() => undefined);
    await create();
    page.downloadReport(); // no job yet: nothing happens
    expect(click).not.toHaveBeenCalled();
    flushJob({ status: 'completed', result: { report: '# R', testResultMarkdown: '# T' } });
    page.downloadReport();
    page.downloadTestResult();
    expect(click).toHaveBeenCalledTimes(2);
    click.mockRestore();
  });

  it('toggles the console', async () => {
    await create();
    flushJob({ status: 'running', log: [] });
    await fixture.whenStable();
    expect(el().querySelector('pre.log')!.textContent).toBe('No output yet.');
    page.showLog.set(false);
    await fixture.whenStable();
    expect(el().querySelector('pre.log')).toBeNull();
  });
});
