import { HttpClient, HttpErrorResponse, HttpEvent, HttpEventType, HttpParams } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';
import { Observable, filter, map } from 'rxjs';

import { AppConfigService } from './app-config';
import {
  About, Health, JobDetail, JobKind, JobSummary, ReviewOptions, TesterInfo, TesterRunOptions,
} from './api.models';

export type UploadEvent =
  | { type: 'progress'; loaded: number; total: number | null }
  | { type: 'done'; job: JobDetail };

/** Turns an HTTP error into one readable sentence (FastAPI puts the reason in `detail`). */
export function errorMessage(error: unknown): string {
  if (error instanceof HttpErrorResponse) {
    if (error.status === 0) {
      return 'The API could not be reached. Check that comp-review-api is running and that apiBaseUrl in config.json is right.';
    }
    const detail = (error.error as { detail?: unknown } | null)?.detail;
    if (typeof detail === 'string') {
      return `${detail} (HTTP ${error.status})`;
    }
    if (Array.isArray(detail)) {
      const parts = detail.map((d: { loc?: unknown[]; msg?: string }) =>
        `${(d.loc ?? []).slice(1).join('.') || 'request'}: ${d.msg ?? 'invalid'}`);
      return `${parts.join('; ')} (HTTP ${error.status})`;
    }
    return `${error.statusText || 'Request failed'} (HTTP ${error.status})`;
  }
  return error instanceof Error ? error.message : String(error);
}

@Injectable({ providedIn: 'root' })
export class ApiService {
  private readonly http = inject(HttpClient);
  private readonly config = inject(AppConfigService);

  private url(path: string): string {
    return `${this.config.apiBaseUrl()}${path}`;
  }

  about(): Observable<About> {
    return this.http.get<About>(this.url('/api/about'));
  }

  health(): Observable<Health> {
    return this.http.get<Health>(this.url('/api/health'));
  }

  startReview(zip: Blob, fileName: string, options: ReviewOptions): Observable<UploadEvent> {
    const form = new FormData();
    form.append('file', zip, fileName);
    form.append('tool', options.tool);
    form.append('subjects', options.subjects || 'all');
    form.append('advanced', String(!!options.advanced));
    if (options.model?.trim()) {
      form.append('model', options.model.trim());
    }
    if (options.advanced && options.analyzers?.trim()) {
      form.append('analyzers', options.analyzers.trim());
    }
    if (options.timeoutMin) {
      form.append('timeoutMin', String(options.timeoutMin));
    }
    return this.http
      .post<JobDetail>(this.url('/api/reviews'), form, { reportProgress: true, observe: 'events' })
      .pipe(
        map((event: HttpEvent<JobDetail>): UploadEvent | null => {
          if (event.type === HttpEventType.UploadProgress) {
            return { type: 'progress', loaded: event.loaded, total: event.total ?? null };
          }
          if (event.type === HttpEventType.Response && event.body) {
            return { type: 'done', job: event.body };
          }
          return null;
        }),
        filter((e): e is UploadEvent => e !== null),
      );
  }

  listJobs(kind?: JobKind): Observable<JobSummary[]> {
    const params = kind ? new HttpParams().set('kind', kind) : undefined;
    return this.http.get<JobSummary[]>(this.url('/api/jobs'), { params });
  }

  getJob(id: string, logLines = 300): Observable<JobDetail> {
    return this.http.get<JobDetail>(this.url(`/api/jobs/${encodeURIComponent(id)}`), {
      params: new HttpParams().set('logLines', logLines),
    });
  }

  getReport(id: string): Observable<string> {
    return this.http.get(this.url(`/api/jobs/${encodeURIComponent(id)}/report`), { responseType: 'text' });
  }

  cancelJob(id: string): Observable<JobDetail> {
    return this.http.post<JobDetail>(this.url(`/api/jobs/${encodeURIComponent(id)}/cancel`), null);
  }

  deleteJob(id: string): Observable<void> {
    return this.http.delete<void>(this.url(`/api/jobs/${encodeURIComponent(id)}`));
  }

  listTesters(): Observable<TesterInfo[]> {
    return this.http.get<TesterInfo[]>(this.url('/api/testers'));
  }

  runTester(name: string, options: TesterRunOptions): Observable<JobDetail> {
    const body = {
      tool: options.tool,
      model: options.model?.trim() || null,
      minFound: options.minFound,
      noBuild: options.noBuild,
      timeoutMin: options.timeoutMin || null,
    };
    return this.http.post<JobDetail>(this.url(`/api/testers/${encodeURIComponent(name)}`), body);
  }
}
