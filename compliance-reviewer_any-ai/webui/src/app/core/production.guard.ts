import { inject } from '@angular/core';
import { CanMatchFn, Router } from '@angular/router';

import { AppConfigService } from './app-config';

/** Keeps the tester routes out of reach when the environment is production. */
export const notInProductionGuard: CanMatchFn = () => {
  const config = inject(AppConfigService);
  return config.isProduction() ? inject(Router).parseUrl('/review') : true;
};
