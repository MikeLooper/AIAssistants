import { Injectable, computed, signal } from '@angular/core';

export type Environment = 'development' | 'production';

/** Runtime settings, read from /config.json when the app starts (edit that file; no rebuild needed). */
export interface AppConfig {
  /** `production` hides the tester pages and the tester jobs. */
  environment: Environment;
  /** Base URL of comp-review-api, without a trailing slash. */
  apiBaseUrl: string;
  /** How often running jobs are polled, in milliseconds. */
  pollIntervalMs: number;
}

export const DEFAULT_CONFIG: AppConfig = {
  environment: 'development',
  apiBaseUrl: 'http://localhost:12001',
  pollIntervalMs: 3000,
};

/** Validates a raw config object; unknown or invalid values fall back to the defaults. */
export function normalizeConfig(raw: unknown): AppConfig {
  const value = (raw && typeof raw === 'object' ? raw : {}) as Record<string, unknown>;
  const env = String(value['environment'] ?? DEFAULT_CONFIG.environment).trim().toLowerCase();
  const apiBaseUrl = String(value['apiBaseUrl'] ?? DEFAULT_CONFIG.apiBaseUrl).trim().replace(/\/+$/, '');
  const poll = Number(value['pollIntervalMs']);
  return {
    environment: env === 'production' ? 'production' : 'development',
    apiBaseUrl: apiBaseUrl || DEFAULT_CONFIG.apiBaseUrl,
    pollIntervalMs: Number.isFinite(poll) && poll >= 250 ? poll : DEFAULT_CONFIG.pollIntervalMs,
  };
}

@Injectable({ providedIn: 'root' })
export class AppConfigService {
  private readonly state = signal<AppConfig>(DEFAULT_CONFIG);
  private readonly loadError = signal<string | null>(null);

  readonly config = this.state.asReadonly();
  readonly error = this.loadError.asReadonly();
  readonly environment = computed(() => this.state().environment);
  readonly isProduction = computed(() => this.state().environment === 'production');
  readonly apiBaseUrl = computed(() => this.state().apiBaseUrl);

  /** Loads config.json. A missing or broken file leaves the defaults in place and records the error. */
  async load(url = 'config.json', fetchFn: typeof fetch = (...args) => fetch(...args)): Promise<AppConfig> {
    try {
      const response = await fetchFn(url, { cache: 'no-store' });
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
      }
      this.state.set(normalizeConfig(await response.json()));
    } catch (e) {
      this.loadError.set(`Could not load ${url} (${e instanceof Error ? e.message : e}); using defaults.`);
      this.state.set(DEFAULT_CONFIG);
    }
    return this.state();
  }

  /** Replaces the config (used by tests). */
  set(config: Partial<AppConfig>): void {
    this.state.set(normalizeConfig({ ...this.state(), ...config }));
  }
}
