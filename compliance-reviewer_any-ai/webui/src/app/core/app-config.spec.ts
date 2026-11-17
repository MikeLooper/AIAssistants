import { TestBed } from '@angular/core/testing';

import { AppConfigService, DEFAULT_CONFIG, normalizeConfig } from './app-config';

function response(body: unknown, ok = true, status = 200): Response {
  return { ok, status, json: async () => body } as Response;
}

describe('normalizeConfig', () => {
  it('keeps valid values and trims the API URL', () => {
    expect(normalizeConfig({ environment: ' Production ', apiBaseUrl: 'http://h:1/ ', pollIntervalMs: 500 }))
      .toEqual({ environment: 'production', apiBaseUrl: 'http://h:1', pollIntervalMs: 500 });
  });

  it('falls back to defaults for missing or invalid values', () => {
    expect(normalizeConfig(null)).toEqual(DEFAULT_CONFIG);
    expect(normalizeConfig({ environment: 'staging', apiBaseUrl: '  ', pollIntervalMs: 10 })).toEqual(DEFAULT_CONFIG);
    expect(normalizeConfig({ pollIntervalMs: 'abc' }).pollIntervalMs).toBe(DEFAULT_CONFIG.pollIntervalMs);
  });
});

describe('AppConfigService', () => {
  let service: AppConfigService;

  beforeEach(() => {
    service = TestBed.inject(AppConfigService);
  });

  it('starts with the defaults', () => {
    expect(service.config()).toEqual(DEFAULT_CONFIG);
    expect(service.isProduction()).toBe(false);
    expect(service.error()).toBeNull();
  });

  it('loads config.json', async () => {
    const fetchFn = vi.fn(async () => response({ environment: 'production', apiBaseUrl: 'http://x' }));
    const config = await service.load('config.json', fetchFn as unknown as typeof fetch);
    expect(fetchFn).toHaveBeenCalledWith('config.json', { cache: 'no-store' });
    expect(config.environment).toBe('production');
    expect(service.isProduction()).toBe(true);
    expect(service.environment()).toBe('production');
    expect(service.apiBaseUrl()).toBe('http://x');
  });

  it('keeps the defaults and records an error when the file is missing', async () => {
    await service.load('config.json', (async () => response({}, false, 404)) as unknown as typeof fetch);
    expect(service.config()).toEqual(DEFAULT_CONFIG);
    expect(service.error()).toContain('HTTP 404');
  });

  it('keeps the defaults when fetching throws', async () => {
    await service.load('c.json', (async () => { throw new Error('offline'); }) as unknown as typeof fetch);
    expect(service.error()).toContain('offline');
  });

  it('set() merges and normalizes', () => {
    service.set({ environment: 'production' });
    expect(service.isProduction()).toBe(true);
    expect(service.apiBaseUrl()).toBe(DEFAULT_CONFIG.apiBaseUrl);
  });
});
