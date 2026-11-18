import { DatePipe } from '@angular/common';
import {
  Component, DestroyRef, ElementRef, afterRenderEffect, computed, inject, input, signal, viewChild,
} from '@angular/core';
import { takeUntilDestroyed, toObservable } from '@angular/core/rxjs-interop';
import { Router, RouterLink } from '@angular/router';
import { catchError, EMPTY, switchMap, tap } from 'rxjs';

import { AppConfigService } from '../../core/app-config';
import { JobDetail, isFinished } from '../../core/api.models';
import { ApiService, errorMessage } from '../../core/api.service';
import { downloadText, formatDuration, formatUsd } from '../../core/format';
import { pollJob } from '../../core/job-poller';
import { MarkdownView } from '../../shared/markdown-view';
import { StatusBadge } from '../../shared/status-badge';

/** One job: live status and console output while it runs; the report (and test result) when it ends. */
@Component({
  selector: 'app-job-detail-page',
  imports: [RouterLink, DatePipe, MarkdownView, StatusBadge],
  templateUrl: './job-detail-page.html',
})
export class JobDetailPage {
  private readonly api = inject(ApiService);
  private readonly config = inject(AppConfigService);
  private readonly router = inject(Router);
  private readonly destroyRef = inject(DestroyRef);

  /** The job ID, bound from the route. */
  readonly id = input.required<string>();

  readonly job = signal<JobDetail | null>(null);
  readonly error = signal<string | null>(null);
  readonly actionError = signal<string | null>(null);
  readonly showRaw = signal(false);
  readonly showLog = signal(true);

  protected readonly formatDuration = formatDuration;
  private readonly logBox = viewChild<ElementRef<HTMLElement>>('logBox');

  readonly finished = computed(() => {
    const job = this.job();
    return !!job && isFinished(job.status);
  });
  readonly report = computed(() => this.job()?.result?.report ?? null);
  readonly testResult = computed(() => this.job()?.result?.testResultMarkdown ?? null);
  readonly cost = computed(() => {
    const r = this.job()?.result;
    const usage = (r?.summary as { usage?: { costUsd?: unknown } } | null | undefined)?.usage;
    return formatUsd(usage?.costUsd ?? (r?.testResult as { costUsd?: unknown } | null | undefined)?.costUsd);
  });
  readonly optionRows = computed(() =>
    Object.entries(this.job()?.options ?? {})
      .filter(([, v]) => v !== null && v !== undefined && v !== '')
      .map(([k, v]) => ({ key: k, value: String(v) })));

  constructor() {
    toObservable(this.id)
      .pipe(
        tap(() => {
          this.job.set(null);
          this.error.set(null);
        }),
        switchMap((id) => pollJob(() => this.api.getJob(id), this.config.config().pollIntervalMs).pipe(
          catchError((e) => {
            this.error.set(errorMessage(e));
            return EMPTY;
          }),
        )),
        takeUntilDestroyed(this.destroyRef),
      )
      .subscribe((job) => {
        this.job.set(job);
        if (isFinished(job.status)) {
          this.showLog.set(job.status !== 'completed');
        }
      });

    // Keep the console view scrolled to the newest line while the job runs.
    afterRenderEffect(() => {
      this.job();
      const box = this.logBox()?.nativeElement;
      if (box && !this.finished()) {
        box.scrollTop = box.scrollHeight;
      }
    });
  }

  cancel(): void {
    this.actionError.set(null);
    this.api.cancelJob(this.id()).pipe(takeUntilDestroyed(this.destroyRef)).subscribe({
      next: (job) => this.job.set(job),
      error: (e) => this.actionError.set(errorMessage(e)),
    });
  }

  remove(): void {
    this.actionError.set(null);
    this.api.deleteJob(this.id()).pipe(takeUntilDestroyed(this.destroyRef)).subscribe({
      next: () => void this.router.navigate(['/jobs']),
      error: (e) => this.actionError.set(errorMessage(e)),
    });
  }

  downloadReport(): void {
    const job = this.job();
    const report = this.report();
    if (job && report) {
      downloadText(report, `${job.name}-compliance-review.md`);
    }
  }

  downloadTestResult(): void {
    const job = this.job();
    const md = this.testResult();
    if (job && md) {
      downloadText(md, `${job.name}-test-result.md`);
    }
  }
}
