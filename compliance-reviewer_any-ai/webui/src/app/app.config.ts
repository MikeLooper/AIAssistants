import { provideHttpClient } from '@angular/common/http';
import {
  ApplicationConfig, inject, provideAppInitializer, provideBrowserGlobalErrorListeners,
} from '@angular/core';
import { provideRouter, withComponentInputBinding } from '@angular/router';

import { routes } from './app.routes';
import { AppConfigService } from './core/app-config';

export const appConfig: ApplicationConfig = {
  providers: [
    provideBrowserGlobalErrorListeners(),
    // The XHR backend (the default) is kept on purpose: the fetch backend can't report upload progress.
    provideHttpClient(),
    provideRouter(routes, withComponentInputBinding()),
    // Read config.json (environment, API URL) before the first route is matched.
    provideAppInitializer(() => inject(AppConfigService).load()),
  ],
};
