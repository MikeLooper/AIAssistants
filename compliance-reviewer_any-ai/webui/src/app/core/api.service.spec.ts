import { HttpErrorResponse, HttpEventType } from '@angular/common/http';
import { HttpTestingController } from '@angular/common/http/testing';
import { TestBed } from '@angular/core/testing';

import { API, configure, jobFixture, testProviders } from '../testing/helpers';
import { ApiService, UploadEvent, errorMessage } from './api.service';

describe('ApiService', () => {
  let api: ApiService;
  let http: HttpTestingController;

  beforeEach(() => {
    TestBed.configureTestingModule({ providers: testProviders() });
    configure();
    api = TestBed.inject(ApiService);
    http = TestBed.inject(HttpTestingController);
  });

  afterEach(() => http.verify());

  it('gets about and health from the configured base URL', () => {
    api.about().subscribe();
    api.health().subscribe();
    http.expectOne(`${API}/api/about`).flush({});
    http.expectOne(`${API}/api/health`).flush({});
  });

  it('uploads a review as multipart form data and reports progress', () => {
    const events: UploadEvent[] = [];
    const zip = new Blob(['zip'], { type: 'application/zip' });
    api.startReview(zip, 'myapp.zip', {
      tool: 'claude', model: ' claude-opus-5-5 ', subjects: 'review-testing', advanced: true, analyzers: 'pip-audit',
      timeoutMin: 15,
    }).subscribe((e) => events.push(e));

    const req = http.expectOne(`${API}/api/reviews`);
    expect(req.request.method).toBe('POST');
    const form = req.request.body as FormData;
    expect((form.get('file') as File).name).toBe('myapp.zip');
    expect(form.get('tool')).toBe('claude');
    expect(form.get('model')).toBe('claude-opus-5-5');
    expect(form.get('subjects')).toBe('review-testing');
    expect(form.get('advanced')).toBe('true');
    expect(form.get('analyzers')).toBe('pip-audit');
    expect(form.get('timeoutMin')).toBe('15');

    req.event({ type: HttpEventType.UploadProgress, loaded: 5, total: 10 });
    req.event({ type: HttpEventType.Sent });
    req.flush(jobFixture());
    expect(events[0]).toEqual({ type: 'progress', loaded: 5, total: 10 });
    expect(events[1]).toEqual({ type: 'done', job: jobFixture() });
    expect(events.length).toBe(2);
  });

  it('leaves out blank optional review fields', () => {
    api.startReview(new Blob(['z']), 'a.zip', { tool: 'auto', model: ' ', subjects: '', advanced: false,
                                                 analyzers: 'pip-audit', timeoutMin: null }).subscribe();
    const form = http.expectOne(`${API}/api/reviews`).request.body as FormData;
    expect(form.get('model')).toBeNull();
    expect(form.get('analyzers')).toBeNull();
    expect(form.get('timeoutMin')).toBeNull();
    expect(form.get('subjects')).toBe('all');
    expect(form.get('advanced')).toBe('false');
  });

  it('progress without a total reports null', () => {
    const events: UploadEvent[] = [];
    api.startReview(new Blob(['z']), 'a.zip', { tool: 'auto', subjects: 'all', advanced: false })
      .subscribe((e) => events.push(e));
    const req = http.expectOne(`${API}/api/reviews`);
    req.event({ type: HttpEventType.UploadProgress, loaded: 5 });
    req.flush(jobFixture());
    expect(events[0]).toEqual({ type: 'progress', loaded: 5, total: null });
  });

  it('job endpoints', () => {
    api.listJobs().subscribe();
    http.expectOne(`${API}/api/jobs`).flush([]);
    api.listJobs('review').subscribe();
    http.expectOne(`${API}/api/jobs?kind=review`).flush([]);
    api.getJob('a/b', 50).subscribe();
    http.expectOne(`${API}/api/jobs/a%2Fb?logLines=50`).flush(jobFixture());
    let report = '';
    api.getReport('j1').subscribe((r) => (report = r));
    http.expectOne(`${API}/api/jobs/j1/report`).flush('# Report');
    expect(report).toBe('# Report');
    api.cancelJob('j1').subscribe();
    expect(http.expectOne(`${API}/api/jobs/j1/cancel`).request.method).toBe('POST');
    api.deleteJob('j1').subscribe();
    expect(http.expectOne(`${API}/api/jobs/j1`).request.method).toBe('DELETE');
  });

  it('tester endpoints', () => {
    api.listTesters().subscribe();
    http.expectOne(`${API}/api/testers`).flush([]);
    api.runTester('api-dotnet', { tool: 'copilot', model: ' ', minFound: 80, noBuild: true, timeoutMin: null })
      .subscribe();
    const req = http.expectOne(`${API}/api/testers/api-dotnet`);
    expect(req.request.method).toBe('POST');
    expect(req.request.body).toEqual({ tool: 'copilot', model: null, minFound: 80, noBuild: true, timeoutMin: null });
  });
});

describe('errorMessage', () => {
  it('explains an unreachable API', () => {
    expect(errorMessage(new HttpErrorResponse({ status: 0 }))).toContain('could not be reached');
  });

  it('uses a FastAPI detail string', () => {
    expect(errorMessage(new HttpErrorResponse({ status: 400, error: { detail: 'bad zip' } }))).toBe('bad zip (HTTP 400)');
  });

  it('joins FastAPI validation errors', () => {
    const error = { detail: [{ loc: ['body', 'minFound'], msg: 'too big' }, { msg: 'nope' }] };
    expect(errorMessage(new HttpErrorResponse({ status: 422, error })))
      .toBe('minFound: too big; request: nope (HTTP 422)');
  });

  it('falls back to the status text, then to Error and plain values', () => {
    expect(errorMessage(new HttpErrorResponse({ status: 500, statusText: 'Server Error' })))
      .toBe('Server Error (HTTP 500)');
    expect(errorMessage(new HttpErrorResponse({ status: 502, statusText: '' }))).toBe('Unknown Error (HTTP 502)');
    expect(errorMessage(new Error('boom'))).toBe('boom');
    expect(errorMessage('plain')).toBe('plain');
  });
});
