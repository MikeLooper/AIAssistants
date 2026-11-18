import { Component, DestroyRef, OnInit, computed, inject, signal } from '@angular/core';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { Router } from '@angular/router';

import { About, Tool } from '../../core/api.models';
import { ApiService, errorMessage } from '../../core/api.service';
import {
  DEFAULT_SKIPPED_FOLDERS, DirectorySelection, formatBytes, selectDirectoryFiles, zipSelection,
} from '../../core/zip';
import { ToolModelPicker } from '../../shared/tool-model-picker';

export type SourceType = 'zip' | 'directory';
export type Phase = 'idle' | 'zipping' | 'uploading';

@Component({
  selector: 'app-review-page',
  imports: [ToolModelPicker],
  templateUrl: './review-page.html',
})
export class ReviewPage implements OnInit {
  private readonly api = inject(ApiService);
  private readonly router = inject(Router);
  private readonly destroyRef = inject(DestroyRef);

  protected readonly skippedFolders = DEFAULT_SKIPPED_FOLDERS;
  protected readonly formatBytes = formatBytes;

  readonly about = signal<About | null>(null);
  readonly aboutError = signal<string | null>(null);

  readonly sourceType = signal<SourceType>('zip');
  readonly zipFile = signal<File | null>(null);
  readonly directoryFiles = signal<File[]>([]);
  readonly skipBuildOutput = signal(true);

  readonly tool = signal<Tool>('auto');
  readonly model = signal('');
  readonly subjectsMode = signal<'all' | 'selected'>('all');
  readonly selectedSubjects = signal<ReadonlySet<string>>(new Set());
  readonly advanced = signal(false);
  readonly analyzers = signal('auto');
  readonly timeoutMin = signal<number | null>(null);

  readonly phase = signal<Phase>('idle');
  readonly uploadPercent = signal<number | null>(null);
  readonly error = signal<string | null>(null);

  readonly selection = computed<DirectorySelection | null>(() => {
    const files = this.directoryFiles();
    return files.length ? selectDirectoryFiles(files, this.skipBuildOutput() ? DEFAULT_SKIPPED_FOLDERS : []) : null;
  });

  readonly subjectsValue = computed(() =>
    this.subjectsMode() === 'all' ? 'all' : [...this.selectedSubjects()].sort().join(','));

  readonly validationError = computed<string | null>(() => {
    if (this.sourceType() === 'zip') {
      const zip = this.zipFile();
      if (!zip) return 'Choose a zip file.';
      if (!zip.name.toLowerCase().endsWith('.zip')) return 'The file must be a .zip archive.';
    } else {
      const sel = this.selection();
      if (!sel) return 'Choose a directory.';
      if (!sel.files.length) return 'The directory has no files to upload.';
    }
    if (this.subjectsMode() === 'selected' && !this.selectedSubjects().size) return 'Pick at least one subject.';
    const t = this.timeoutMin();
    if (t !== null && !(t > 0)) return 'The time limit must be greater than 0.';
    return null;
  });

  readonly busy = computed(() => this.phase() !== 'idle');

  ngOnInit(): void {
    this.api.about().pipe(takeUntilDestroyed(this.destroyRef)).subscribe({
      next: (about) => this.about.set(about),
      error: (e) => this.aboutError.set(errorMessage(e)),
    });
  }

  onZipPicked(event: Event): void {
    const input = event.target as HTMLInputElement;
    this.zipFile.set(input.files?.[0] ?? null);
    this.error.set(null);
  }

  onDirectoryPicked(event: Event): void {
    const input = event.target as HTMLInputElement;
    this.directoryFiles.set(Array.from(input.files ?? []));
    this.error.set(null);
  }

  toggleSubject(subject: string, checked: boolean): void {
    const next = new Set(this.selectedSubjects());
    if (checked) {
      next.add(subject);
    } else {
      next.delete(subject);
    }
    this.selectedSubjects.set(next);
  }

  /** Builds the archive to upload: the picked zip as-is, or the picked directory zipped in the browser. */
  async buildArchive(): Promise<{ blob: Blob; fileName: string }> {
    if (this.sourceType() === 'zip') {
      const zip = this.zipFile()!;
      return { blob: zip, fileName: zip.name };
    }
    const sel = this.selection()!;
    this.phase.set('zipping');
    return { blob: await zipSelection(sel), fileName: `${sel.rootName}.zip` };
  }

  async submit(): Promise<void> {
    if (this.validationError() || this.busy()) return;
    this.error.set(null);
    let archive: { blob: Blob; fileName: string };
    try {
      archive = await this.buildArchive();
    } catch (e) {
      this.error.set(`Could not zip the directory: ${errorMessage(e)}`);
      this.phase.set('idle');
      return;
    }
    this.phase.set('uploading');
    this.uploadPercent.set(0);
    this.api
      .startReview(archive.blob, archive.fileName, {
        tool: this.tool(),
        model: this.model(),
        subjects: this.subjectsValue(),
        advanced: this.advanced(),
        analyzers: this.analyzers(),
        timeoutMin: this.timeoutMin(),
      })
      .pipe(takeUntilDestroyed(this.destroyRef))
      .subscribe({
        next: (event) => {
          if (event.type === 'progress') {
            this.uploadPercent.set(event.total ? Math.round((100 * event.loaded) / event.total) : null);
          } else {
            this.phase.set('idle');
            void this.router.navigate(['/jobs', event.job.id]);
          }
        },
        error: (e) => {
          this.error.set(errorMessage(e));
          this.phase.set('idle');
          this.uploadPercent.set(null);
        },
      });
  }

  protected numberOrNull(value: string): number | null {
    return value.trim() === '' ? null : Number(value);
  }
}
