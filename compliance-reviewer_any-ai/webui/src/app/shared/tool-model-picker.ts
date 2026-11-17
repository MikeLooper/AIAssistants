import { Component, computed, input, model } from '@angular/core';

import { About, Tool } from '../core/api.models';

export const TOOLS: readonly Tool[] = ['auto', 'claude', 'copilot'];

/** Model names to suggest for a tool, from the API's AvailableModels setting ("auto": every tool's). */
export function suggestedModels(about: About | null, tool: Tool): string[] {
  const available = (about?.configuration?.['AvailableModels'] ?? {}) as Record<string, string[]>;
  const lists = tool === 'auto' ? Object.values(available) : [available[tool] ?? []];
  return [...new Set(lists.flat().filter((m) => typeof m === 'string' && m.trim()))];
}

/** Picks the AI tool and model that run the reviewer. The model is free text with suggestions;
 * blank means the API's DefaultModel, else the tool's own default. */
@Component({
  selector: 'app-tool-model-picker',
  template: `
    <label class="field">
      <span>AI tool</span>
      <select name="tool" [value]="tool()" (change)="tool.set($any($event.target).value)">
        @for (t of tools; track t) {
          <option [value]="t">{{ t === 'auto' ? 'auto (API default)' : t }}{{ toolMissing(t) ? ' (not found on the API host)' : '' }}</option>
        }
      </select>
    </label>
    <label class="field">
      <span>Model</span>
      <input name="model" [attr.list]="listId" [value]="modelName()" placeholder="{{ placeholder() }}"
             (input)="modelName.set($any($event.target).value)" autocomplete="off" />
      <datalist [id]="listId">
        @for (m of suggestions(); track m) {
          <option [value]="m"></option>
        }
      </datalist>
    </label>
  `,
  host: { class: 'field-row' },
})
export class ToolModelPicker {
  private static nextId = 0;

  readonly about = input<About | null>(null);
  readonly tool = model<Tool>('auto');
  readonly modelName = model<string>('');

  protected readonly tools = TOOLS;
  protected readonly listId = `models-${ToolModelPicker.nextId++}`;
  protected readonly suggestions = computed(() => suggestedModels(this.about(), this.tool()));
  protected readonly placeholder = computed(() => {
    const def = this.about()?.configuration?.['DefaultModel'];
    return typeof def === 'string' && def ? `default: ${def}` : "default: the tool's own";
  });

  protected toolMissing(tool: Tool): boolean {
    const info = this.about()?.tools?.find((t) => t.name === tool);
    return !!info && !info.found;
  }
}
