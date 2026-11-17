import { Component, DestroyRef, OnInit, computed, inject, signal } from '@angular/core';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { Router } from '@angular/router';
import { catchError, forkJoin, map, of } from 'rxjs';

import { About, TesterInfo, TesterRunOptions, Tool } from '../../core/api.models';
import { ApiService, errorMessage } from '../../core/api.service';
import { ToolModelPicker } from '../../shared/tool-model-picker';

@Component({
  selector: 'app-testers-page',
  imports: [ToolModelPicker],
  templateUrl: './testers-page.html',
})
export class TestersPage implements OnInit {
  private readonly api = inject(ApiService);
  private readonly router = inject(Router);
  private readonly destroyRef = inject(DestroyRef);

  readonly about = signal<About | null>(null);
  readonly testers = signal<TesterInfo[]>([]);
  readonly loading = signal(true);
  readonly selected = signal<ReadonlySet<string>>(new Set());
  readonly tool = signal<Tool>('auto');
  readonly model = signal('');
  readonly minFound = signal(90);
  readonly noBuild = signal(false);
  readonly timeoutMin = signal<number | null>(null);
  readonly starting = signal(false);
  readonly error = signal<string | null>(null);

  readonly allSelected = computed(() => this.testers().length > 0 && this.selected().size === this.testers().length);
  readonly optionsError = computed(() => {
    const min = this.minFound();
    if (!(min >= 0 && min <= 100)) return 'Required share of flaws must be between 0 and 100.';
    const t = this.timeoutMin();
    if (t !== null && !(t > 0)) return 'The time limit must be greater than 0.';
    return null;
  });

  ngOnInit(): void {
    this.api.about().pipe(takeUntilDestroyed(this.destroyRef)).subscribe({
      next: (a) => this.about.set(a),
      error: () => undefined, // the picker works without suggestions
    });
    this.api.listTesters().pipe(takeUntilDestroyed(this.destroyRef)).subscribe({
      next: (t) => {
        this.testers.set(t);
        this.loading.set(false);
      },
      error: (e) => {
        this.error.set(errorMessage(e));
        this.loading.set(false);
      },
    });
  }

  options(): TesterRunOptions {
    return {
      tool: this.tool(),
      model: this.model(),
      minFound: this.minFound(),
      noBuild: this.noBuild(),
      timeoutMin: this.timeoutMin(),
    };
  }

  toggle(name: string, checked: boolean): void {
    const next = new Set(this.selected());
    if (checked) {
      next.add(name);
    } else {
      next.delete(name);
    }
    this.selected.set(next);
  }

  toggleAll(checked: boolean): void {
    this.selected.set(new Set(checked ? this.testers().map((t) => t.name) : []));
  }

  /** Starts one tester and opens its job. */
  run(name: string): void {
    if (this.starting() || this.optionsError()) return;
    this.starting.set(true);
    this.error.set(null);
    this.api.runTester(name, this.options()).pipe(takeUntilDestroyed(this.destroyRef)).subscribe({
      next: (job) => {
        this.starting.set(false);
        void this.router.navigate(['/jobs', job.id]);
      },
      error: (e) => {
        this.starting.set(false);
        this.error.set(errorMessage(e));
      },
    });
  }

  /** Starts every selected tester (the API queues them) and opens the job list. */
  runSelected(): void {
    const names = this.testers().map((t) => t.name).filter((n) => this.selected().has(n));
    if (!names.length || this.starting() || this.optionsError()) return;
    this.starting.set(true);
    this.error.set(null);
    const opts = this.options();
    forkJoin(names.map((n) => this.api.runTester(n, opts).pipe(
      map(() => null),
      catchError((e) => of(`${n}: ${errorMessage(e)}`)),
    ))).pipe(takeUntilDestroyed(this.destroyRef)).subscribe((errors) => {
      this.starting.set(false);
      const failed = errors.filter((e): e is string => !!e);
      if (failed.length) {
        this.error.set(failed.join('\n'));
      }
      if (failed.length < names.length) {
        void this.router.navigate(['/jobs']);
      }
    });
  }

  protected numberOrNull(value: string): number | null {
    return value.trim() === '' ? null : Number(value);
  }
}
