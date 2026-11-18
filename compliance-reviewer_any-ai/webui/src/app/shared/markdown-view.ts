import { Component, computed, input } from '@angular/core';
import { marked } from 'marked';

/** Markdown to HTML (GitHub-flavoured). Angular sanitizes the HTML when it is bound to [innerHTML]. */
export function renderMarkdown(markdown: string | null | undefined): string {
  return markdown ? (marked.parse(markdown, { async: false, gfm: true }) as string) : '';
}

@Component({
  selector: 'app-markdown-view',
  template: `<div class="markdown" [innerHTML]="html()"></div>`,
})
export class MarkdownView {
  readonly markdown = input<string | null | undefined>('');
  protected readonly html = computed(() => renderMarkdown(this.markdown()));
}
