import { JsonPipe } from '@angular/common';
import { HttpErrorResponse } from '@angular/common/http';
import { Component, DestroyRef, OnInit, inject, signal } from '@angular/core';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';

import { AppConfigService } from '../../core/app-config';
import { About, Health } from '../../core/api.models';
import { ApiService, errorMessage } from '../../core/api.service';
import { StatusBadge } from '../../shared/status-badge';

/** The reviewer version, the API's configuration and health, and this UI's own settings. */
@Component({
  selector: 'app-about-page',
  imports: [JsonPipe, StatusBadge],
  templateUrl: './about-page.html',
})
export class AboutPage implements OnInit {
  private readonly api = inject(ApiService);
  private readonly destroyRef = inject(DestroyRef);
  protected readonly config = inject(AppConfigService);

  readonly about = signal<About | null>(null);
  readonly health = signal<Health | null>(null);
  readonly aboutError = signal<string | null>(null);
  readonly healthError = signal<string | null>(null);

  ngOnInit(): void {
    this.refresh();
  }

  refresh(): void {
    this.api.about().pipe(takeUntilDestroyed(this.destroyRef)).subscribe({
      next: (a) => {
        this.about.set(a);
        this.aboutError.set(null);
      },
      error: (e) => this.aboutError.set(errorMessage(e)),
    });
    this.api.health().pipe(takeUntilDestroyed(this.destroyRef)).subscribe({
      next: (h) => {
        this.health.set(h);
        this.healthError.set(null);
      },
      error: (e: unknown) => {
        // An unhealthy API answers 503 with the same body.
        const body = e instanceof HttpErrorResponse ? (e.error as Health | null) : null;
        if (body && typeof body === 'object' && 'status' in body) {
          this.health.set(body);
          this.healthError.set(null);
        } else {
          this.health.set(null);
          this.healthError.set(errorMessage(e));
        }
      },
    });
  }

  protected entries(record: Record<string, unknown> | null | undefined): { key: string; value: unknown }[] {
    return Object.entries(record ?? {}).map(([key, value]) => ({ key, value }));
  }
}
