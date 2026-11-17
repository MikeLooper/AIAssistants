import { DatePipe } from '@angular/common';
import { Component, DestroyRef, OnInit, inject, signal } from '@angular/core';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { RouterLink } from '@angular/router';
import { EMPTY, catchError, exhaustMap, timer } from 'rxjs';

import { AppConfigService } from '../../core/app-config';
import { JobSummary } from '../../core/api.models';
import { ApiService, errorMessage } from '../../core/api.service';
import { formatDuration } from '../../core/format';
import { StatusBadge } from '../../shared/status-badge';

/** The jobs the API holds, newest first, refreshed every poll interval. */
@Component({
  selector: 'app-jobs-page',
  imports: [RouterLink, DatePipe, StatusBadge],
  templateUrl: './jobs-page.html',
})
export class JobsPage implements OnInit {
  private readonly api = inject(ApiService);
  private readonly config = inject(AppConfigService);
  private readonly destroyRef = inject(DestroyRef);

  protected readonly formatDuration = formatDuration;
  readonly jobs = signal<JobSummary[]>([]);
  readonly loaded = signal(false);
  readonly error = signal<string | null>(null);

  ngOnInit(): void {
    // In production the tester jobs are hidden along with the tester pages.
    const kind = this.config.isProduction() ? 'review' : undefined;
    timer(0, this.config.config().pollIntervalMs)
      .pipe(
        exhaustMap(() => this.api.listJobs(kind).pipe(
          catchError((e) => {
            this.error.set(errorMessage(e)); // keep polling: the API may come back
            this.loaded.set(true);
            return EMPTY;
          }),
        )),
        takeUntilDestroyed(this.destroyRef),
      )
      .subscribe((jobs) => {
        this.jobs.set(jobs);
        this.loaded.set(true);
        this.error.set(null);
      });
  }
}
