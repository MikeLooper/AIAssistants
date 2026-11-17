import { Component, signal } from '@angular/core';
import { TestBed } from '@angular/core/testing';

import { About, Tool } from '../core/api.models';
import { aboutFixture } from '../testing/helpers';
import { MarkdownView, renderMarkdown } from './markdown-view';
import { StatusBadge } from './status-badge';
import { ToolModelPicker, suggestedModels } from './tool-model-picker';

describe('renderMarkdown / MarkdownView', () => {
  it('renders GitHub-flavoured Markdown', () => {
    const html = renderMarkdown('# Title\n\n| a | b |\n|---|---|\n| 1 | 2 |\n');
    expect(html).toContain('<h1>Title</h1>');
    expect(html).toContain('<table>');
    expect(renderMarkdown(null)).toBe('');
  });

  it('binds sanitized HTML', async () => {
    const fixture = TestBed.createComponent(MarkdownView);
    fixture.componentRef.setInput('markdown', '**bold** <script>alert(1)</script><img src=x onerror="alert(1)">');
    await fixture.whenStable();
    const el = fixture.nativeElement as HTMLElement;
    expect(el.querySelector('strong')?.textContent).toBe('bold');
    expect(el.querySelector('script')).toBeNull();
    expect(el.querySelector('img')?.getAttribute('onerror')).toBeNull();
  });
});

describe('StatusBadge', () => {
  it('shows the value with a matching class', async () => {
    const fixture = TestBed.createComponent(StatusBadge);
    fixture.componentRef.setInput('value', 'completed');
    await fixture.whenStable();
    const span = (fixture.nativeElement as HTMLElement).querySelector('span')!;
    expect(span.textContent).toBe('completed');
    expect(span.className).toContain('badge-completed');
  });
});

describe('suggestedModels', () => {
  it('lists the tool’s models, or every tool’s for auto, without duplicates', () => {
    const about = aboutFixture();
    expect(suggestedModels(about, 'claude')).toEqual(['claude-opus-5-5', 'claude-sonnet-5-5']);
    expect(suggestedModels(about, 'auto')).toEqual(['claude-opus-5-5', 'claude-sonnet-5-5', 'gpt-5']);
    expect(suggestedModels(null, 'copilot')).toEqual([]);
    expect(suggestedModels(aboutFixture({ configuration: {} }), 'claude')).toEqual([]);
  });
});

@Component({
  imports: [ToolModelPicker],
  template: `<app-tool-model-picker [about]="about()" [(tool)]="tool" [(modelName)]="model" />`,
})
class PickerHost {
  readonly about = signal<About | null>(aboutFixture());
  readonly tool = signal<Tool>('auto');
  readonly model = signal('');
}

describe('ToolModelPicker', () => {
  it('two-way binds the tool and model and suggests models', async () => {
    const fixture = TestBed.createComponent(PickerHost);
    await fixture.whenStable();
    const el = fixture.nativeElement as HTMLElement;
    const select = el.querySelector('select')!;
    const options = Array.from(select.options).map((o) => o.textContent!.trim());
    expect(options).toEqual(['auto (API default)', 'claude', 'copilot (not found on the API host)']);
    expect(el.querySelector('input')!.placeholder).toBe('default: claude-sonnet-5-5');

    select.value = 'copilot';
    select.dispatchEvent(new Event('change'));
    const input = el.querySelector('input')!;
    input.value = 'gpt-5';
    input.dispatchEvent(new Event('input'));
    await fixture.whenStable();
    expect(fixture.componentInstance.tool()).toBe('copilot');
    expect(fixture.componentInstance.model()).toBe('gpt-5');
    const datalist = Array.from(el.querySelectorAll('datalist option')).map((o) => o.getAttribute('value'));
    expect(datalist).toEqual(['gpt-5', 'claude-sonnet-5-5']);
  });

  it('describes the tool default when no DefaultModel is set', async () => {
    const fixture = TestBed.createComponent(PickerHost);
    fixture.componentInstance.about.set(null);
    await fixture.whenStable();
    expect((fixture.nativeElement as HTMLElement).querySelector('input')!.placeholder)
      .toBe("default: the tool's own");
  });
});
