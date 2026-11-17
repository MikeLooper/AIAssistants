import { TestBed } from '@angular/core/testing';
import { Router, UrlTree } from '@angular/router';
import { Observable, of, toArray, firstValueFrom } from 'rxjs';

import { configure, jobFixture, testProviders } from '../testing/helpers';
import { JobDetail, JobStatus, isFinished } from './api.models';
import { downloadText, formatDuration, formatUsd } from './format';
import { pollJob } from './job-poller';
import { notInProductionGuard } from './production.guard';

describe('isFinished', () => {
  it('is true only for completed, failed and cancelled', () => {
    const states: JobStatus[] = ['queued', 'running', 'completed', 'failed', 'cancelled'];
    expect(states.map(isFinished)).toEqual([false, false, true, true, true]);
  });
});

describe('pollJob', () => {
  it('polls until the job finishes and emits the finished state', async () => {
    const states: JobStatus[] = ['queued', 'running', 'running', 'completed', 'running'];
    let calls = 0;
    const fetchJob = (): Observable<JobDetail> => of(jobFixture({ status: states[calls++] }));
    const seen = await firstValueFrom(pollJob(fetchJob, 1).pipe(toArray()));
    expect(seen.map((j) => j.status)).toEqual(['queued', 'running', 'running', 'completed']);
    expect(calls).toBe(4);
  });

  it('propagates errors', async () => {
    const failing = () => new Observable<JobDetail>((s) => s.error(new Error('404')));
    await expect(firstValueFrom(pollJob(failing, 1))).rejects.toThrow('404');
  });
});

describe('notInProductionGuard', () => {
  beforeEach(() => TestBed.configureTestingModule({ providers: testProviders() }));

  const run = () => TestBed.runInInjectionContext(() => notInProductionGuard({}, [], {} as never));

  it('allows the route in development', () => {
    configure({ environment: 'development' });
    expect(run()).toBe(true);
  });

  it('redirects to /review in production', () => {
    configure({ environment: 'production' });
    const result = run() as UrlTree;
    expect(TestBed.inject(Router).serializeUrl(result)).toBe('/review');
  });
});

describe('format helpers', () => {
  it('formatDuration', () => {
    expect(formatDuration(null)).toBe('—');
    expect(formatDuration(undefined)).toBe('—');
    expect(formatDuration(Number.NaN)).toBe('—');
    expect(formatDuration(12.4)).toBe('12s');
    expect(formatDuration(65)).toBe('1m 05s');
    expect(formatDuration(3723)).toBe('1h 02m 03s');
    expect(formatDuration(-5)).toBe('0s');
  });

  it('formatUsd', () => {
    expect(formatUsd(1.5)).toBe('$1.50');
    expect(formatUsd(null)).toBe('—');
    expect(formatUsd('3')).toBe('—');
  });

  it('downloadText clicks a temporary link', () => {
    const create = vi.fn(() => 'blob:x');
    const revoke = vi.fn();
    Object.assign(URL, { createObjectURL: create, revokeObjectURL: revoke });
    const click = vi.spyOn(HTMLAnchorElement.prototype, 'click').mockImplementation(() => undefined);
    downloadText('# hi', 'r.md');
    expect(create).toHaveBeenCalled();
    expect(click).toHaveBeenCalled();
    expect(revoke).toHaveBeenCalledWith('blob:x');
    click.mockRestore();
  });
});
