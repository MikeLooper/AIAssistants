import { HttpErrorResponse } from '@angular/common/http';
import { Component, DestroyRef, OnInit, inject, signal } from '@angular/core';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { RouterLink, RouterLinkActive, RouterOutlet } from '@angular/router';
import { catchError, exhaustMap, map, of, timer } from 'rxjs';

import { AppConfigService } from './core/app-config';
import { Health } from './core/api.models';
import { ApiService } from './core/api.service';

export const HEALTH_POLL_MS = 60_000;
export type ApiState = Health['status'] | 'unreachable' | 'checking';

@Component({
  selector: 'app-root',
  imports: [RouterOutlet, RouterLink, RouterLinkActive],
  templateUrl: './app.html',
})
export class App implements OnInit {
  private readonly api = inject(ApiService);
  private readonly destroyRef = inject(DestroyRef);
  protected readonly config = inject(AppConfigService);

  readonly apiState = signal<ApiState>('checking');

  ngOnInit(): void {
    timer(0, HEALTH_POLL_MS)
      .pipe(
        exhaustMap(() => this.api.health().pipe(
          map((h): ApiState => h.status),
          catchError((e: unknown) => {
            const body = e instanceof HttpErrorResponse ? (e.error as Partial<Health> | null) : null;
            return of<ApiState>(body?.status ?? 'unreachable');
          }),
        )),
        takeUntilDestroyed(this.destroyRef),
      )
      .subscribe((state) => this.apiState.set(state));
  }
}
