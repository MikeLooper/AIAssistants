import { provideHttpClient } from '@angular/common/http';
import { provideHttpClientTesting } from '@angular/common/http/testing';
import { EnvironmentProviders, Provider } from '@angular/core';
import { TestBed } from '@angular/core/testing';
import { provideRouter } from '@angular/router';

import { About, JobDetail } from '../core/api.models';
import { AppConfig, AppConfigService } from '../core/app-config';

export const API = 'http://api.test';

/** HTTP testing, an empty router, and a config pointing at API with a long poll interval. */
export function testProviders(extra: (Provider | EnvironmentProviders)[] = []): (Provider | EnvironmentProviders)[] {
  return [provideHttpClient(), provideHttpClientTesting(), provideRouter([]), ...extra];
}

export function configure(config: Partial<AppConfig> = {}): AppConfigService {
  const service = TestBed.inject(AppConfigService);
  service.set({ apiBaseUrl: API, pollIntervalMs: 600_000, ...config });
  return service;
}

/** Lets pending timers (RxJS timer(0)) and promises run. */
export function flushAsync(ms = 0): Promise<void> {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

export function aboutFixture(overrides: Partial<About> = {}): About {
  return {
    name: 'comp-review-api',
    reviewerVersion: '1.0.0',
    environment: 'development',
    pythonVersion: '3.14.6',
    tools: [
      { name: 'claude', found: true, path: '/bin/claude' },
      { name: 'copilot', found: false, path: null },
    ],
    subjects: ['review-maintainability', 'review-testing'],
    configuration: {
      Environment: 'development',
      DefaultModel: 'claude-sonnet-5-5',
      AvailableModels: { claude: ['claude-opus-5-5', 'claude-sonnet-5-5'], copilot: ['gpt-5', 'claude-sonnet-5-5'] },
    },
    ...overrides,
  };
}

export function jobFixture(overrides: Partial<JobDetail> = {}): JobDetail {
  return {
    id: 'job1',
    kind: 'review',
    name: 'myapp',
    status: 'running',
    createdAt: '2026-11-16T12:00:00Z',
    startedAt: '2026-11-16T12:00:01Z',
    finishedAt: null,
    durationSeconds: 65,
    error: null,
    overallScore: null,
    overallBand: null,
    verdict: null,
    options: { tool: 'claude', model: 'claude-sonnet-5-5', subjects: 'all', fileName: 'myapp.zip' },
    exitCode: null,
    log: ['Compliance review of myapp', '  [0m 15s] step 1/20 done: 00-init'],
    logLineCount: 2,
    result: null,
    ...overrides,
  };
}

/** A File as `<input webkitdirectory>` gives it, with its relative path. */
export function dirFile(path: string, content = 'x'): File {
  const file = new File([content], path.split('/').pop()!);
  Object.defineProperty(file, 'webkitRelativePath', { value: path });
  return file;
}
