import { Component, input } from '@angular/core';

/** A coloured pill for a job status, verdict or health state. */
@Component({
  selector: 'app-status-badge',
  template: `<span class="badge" [class]="'badge badge-' + value()">{{ value() }}</span>`,
})
export class StatusBadge {
  readonly value = input.required<string>();
}
