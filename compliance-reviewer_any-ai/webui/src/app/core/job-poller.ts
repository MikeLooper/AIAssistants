import { Observable, exhaustMap, takeWhile, timer } from 'rxjs';

import { JobDetail, isFinished } from './api.models';

/** Fetches a job now and then every `intervalMs`, emitting each state. Completes after the first finished
 * state (completed, failed or cancelled), which is emitted too. A slow request is never overlapped. */
export function pollJob(fetchJob: () => Observable<JobDetail>, intervalMs: number): Observable<JobDetail> {
  return timer(0, intervalMs).pipe(
    exhaustMap(() => fetchJob()),
    takeWhile((job) => !isFinished(job.status), true),
  );
}
