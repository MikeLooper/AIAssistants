import { Routes } from '@angular/router';

import { notInProductionGuard } from './core/production.guard';
import { AboutPage } from './features/about/about-page';
import { JobDetailPage } from './features/jobs/job-detail-page';
import { JobsPage } from './features/jobs/jobs-page';
import { ReviewPage } from './features/review/review-page';
import { TestersPage } from './features/testers/testers-page';

export const routes: Routes = [
  { path: '', pathMatch: 'full', redirectTo: 'review' },
  { path: 'review', component: ReviewPage, title: 'Review · Compliance Reviewer' },
  { path: 'testers', component: TestersPage, canMatch: [notInProductionGuard], title: 'Testers · Compliance Reviewer' },
  { path: 'jobs', component: JobsPage, title: 'Jobs · Compliance Reviewer' },
  { path: 'jobs/:id', component: JobDetailPage, title: 'Job · Compliance Reviewer' },
  { path: 'about', component: AboutPage, title: 'About · Compliance Reviewer' },
  { path: '**', redirectTo: 'review' },
];
