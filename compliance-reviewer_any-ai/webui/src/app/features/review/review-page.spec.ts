import { HttpEventType } from '@angular/common/http';
import { HttpTestingController } from '@angular/common/http/testing';
import { ComponentFixture, TestBed } from '@angular/core/testing';
import { Router } from '@angular/router';
import { strFromU8, unzipSync } from 'fflate';

import { API, aboutFixture, configure, dirFile, flushAsync, jobFixture, testProviders } from '../../testing/helpers';
import { ReviewPage } from './review-page';

describe('ReviewPage', () => {
  let fixture: ComponentFixture<ReviewPage>;
  let page: ReviewPage;
  let http: HttpTestingController;
  let navigate: ReturnType<typeof vi.spyOn>;

  beforeEach(async () => {
    TestBed.configureTestingModule({ providers: testProviders() });
    configure();
    http = TestBed.inject(HttpTestingController);
    navigate = vi.spyOn(TestBed.inject(Router), 'navigate').mockResolvedValue(true);
    fixture = TestBed.createComponent(ReviewPage);
    page = fixture.componentInstance;
    fixture.detectChanges();
    http.expectOne(`${API}/api/about`).flush(aboutFixture());
    await fixture.whenStable();
  });

  afterEach(() => http.verify());

  const el = () => fixture.nativeElement as HTMLElement;

  function pickZip(name = 'myapp.zip', content = 'PK') {
    const input = el().querySelector<HTMLInputElement>('input[name="zip"]')!;
    Object.defineProperty(input, 'files', { value: [new File([content], name)], configurable: true });
    input.dispatchEvent(new Event('change'));
  }

  it('loads the subjects and requires a source', () => {
    expect(page.about()?.subjects.length).toBe(2);
    expect(page.validationError()).toBe('Choose a zip file.');
    expect(el().querySelector<HTMLButtonElement>('button[type="submit"]')!.disabled).toBe(true);
  });

  it('shows an error when the API settings cannot be loaded', async () => {
    const f = TestBed.createComponent(ReviewPage);
    f.detectChanges();
    http.expectOne(`${API}/api/about`).flush({ detail: 'down' }, { status: 500, statusText: 'x' });
    await f.whenStable();
    expect(f.componentInstance.aboutError()).toBe('down (HTTP 500)');
    expect((f.nativeElement as HTMLElement).querySelector('.alert-warning')!.textContent).toContain('down');
  });

  it('validates the zip name, subjects and time limit', async () => {
    pickZip('notes.txt');
    expect(page.validationError()).toBe('The file must be a .zip archive.');
    pickZip();
    expect(page.validationError()).toBeNull();
    page.subjectsMode.set('selected');
    expect(page.validationError()).toBe('Pick at least one subject.');
    page.toggleSubject('review-testing', true);
    page.toggleSubject('review-maintainability', true);
    page.toggleSubject('review-maintainability', false);
    expect(page.subjectsValue()).toBe('review-testing');
    expect(page.validationError()).toBeNull();
    page.timeoutMin.set(0);
    expect(page.validationError()).toBe('The time limit must be greater than 0.');
    page.timeoutMin.set(null);
    await fixture.whenStable();
    expect(el().querySelector('[data-testid="zip-summary"]')!.textContent).toContain('myapp.zip');
    expect(el().querySelectorAll('.subject-grid input').length).toBe(2);
  });

  it('uploads the picked zip with the chosen options and opens the job', async () => {
    pickZip();
    page.tool.set('claude');
    page.model.set('claude-opus-5-5');
    page.advanced.set(true);
    page.analyzers.set('pip-audit');
    page.timeoutMin.set(20);
    await page.submit();
    expect(page.phase()).toBe('uploading');

    const req = http.expectOne(`${API}/api/reviews`);
    const form = req.request.body as FormData;
    expect((form.get('file') as File).name).toBe('myapp.zip');
    expect(form.get('tool')).toBe('claude');
    expect(form.get('model')).toBe('claude-opus-5-5');
    expect(form.get('subjects')).toBe('all');
    expect(form.get('advanced')).toBe('true');
    expect(form.get('analyzers')).toBe('pip-audit');
    expect(form.get('timeoutMin')).toBe('20');

    req.event({ type: HttpEventType.UploadProgress, loaded: 1, total: 4 });
    expect(page.uploadPercent()).toBe(25);
    req.event({ type: HttpEventType.UploadProgress, loaded: 1 });
    expect(page.uploadPercent()).toBeNull();
    req.flush(jobFixture({ id: 'abc' }));
    expect(page.phase()).toBe('idle');
    expect(navigate).toHaveBeenCalledWith(['/jobs', 'abc']);
  });

  it('zips a picked directory in the browser, leaving out build output', async () => {
    page.sourceType.set('directory');
    await fixture.whenStable();
    expect(page.validationError()).toBe('Choose a directory.');
    const input = el().querySelector<HTMLInputElement>('input[name="directory"]')!;
    const files = [dirFile('proj/src/a.py', 'print(1)'), dirFile('proj/bin/x.dll'), dirFile('proj/README.md', '#')];
    Object.defineProperty(input, 'files', { value: files });
    input.dispatchEvent(new Event('change'));
    await fixture.whenStable();
    expect(page.selection()!.files.length).toBe(2);
    expect(el().querySelector('[data-testid="directory-summary"]')!.textContent).toContain('1 left out');

    page.skipBuildOutput.set(false);
    expect(page.selection()!.files.length).toBe(3);
    page.skipBuildOutput.set(true);

    await page.submit();
    const req = http.expectOne(`${API}/api/reviews`);
    const file = (req.request.body as FormData).get('file') as File;
    expect(file.name).toBe('proj.zip');
    const entries = unzipSync(new Uint8Array(await file.arrayBuffer()));
    expect(Object.keys(entries).sort()).toEqual(['proj/README.md', 'proj/src/a.py']);
    expect(strFromU8(entries['proj/src/a.py'])).toBe('print(1)');
    req.flush(jobFixture({ id: 'dir1' }));
    expect(navigate).toHaveBeenCalledWith(['/jobs', 'dir1']);
  });

  it('rejects a directory with no files left to upload', async () => {
    page.sourceType.set('directory');
    page.directoryFiles.set([dirFile('proj/node_modules/a.js')]);
    expect(page.validationError()).toBe('The directory has no files to upload.');
    await page.submit();
    http.expectNone(`${API}/api/reviews`);
  });

  it('reports a zipping failure', async () => {
    page.sourceType.set('directory');
    page.directoryFiles.set([dirFile('proj/a.py')]);
    vi.spyOn(page, 'buildArchive').mockRejectedValue(new Error('out of memory'));
    await page.submit();
    expect(page.error()).toBe('Could not zip the directory: out of memory');
    expect(page.phase()).toBe('idle');
  });

  it('shows the API error when the upload is refused', async () => {
    pickZip();
    await page.submit();
    http.expectOne(`${API}/api/reviews`).flush({ detail: 'the archive holds no files' },
                                                { status: 400, statusText: 'Bad Request' });
    await fixture.whenStable();
    expect(page.error()).toBe('the archive holds no files (HTTP 400)');
    expect(page.phase()).toBe('idle');
    expect(el().querySelector('.alert-error')!.textContent).toContain('no files');
    expect(navigate).not.toHaveBeenCalled();
  });

  it('does nothing when submitted while invalid or busy', async () => {
    await page.submit();
    pickZip();
    page.phase.set('uploading');
    await page.submit();
    http.expectNone(`${API}/api/reviews`);
  });

  it('wires the form controls to its state', async () => {
    const check = (name: string, value: boolean) => {
      const box = el().querySelector<HTMLInputElement>(`input[name="${name}"]`)!;
      box.checked = value;
      box.dispatchEvent(new Event('change'));
    };
    check('advanced', true);
    await fixture.whenStable();
    const analyzers = el().querySelector<HTMLInputElement>('input[name="analyzers"]')!;
    analyzers.value = 'pip-audit';
    analyzers.dispatchEvent(new Event('input'));
    const timeout = el().querySelector<HTMLInputElement>('input[name="timeoutMin"]')!;
    timeout.value = '12';
    timeout.dispatchEvent(new Event('input'));
    expect(page.advanced()).toBe(true);
    expect(page.analyzers()).toBe('pip-audit');
    expect(page.timeoutMin()).toBe(12);
    timeout.value = '';
    timeout.dispatchEvent(new Event('input'));
    expect(page.timeoutMin()).toBeNull();

    const radios = el().querySelectorAll<HTMLInputElement>('input[name="sourceType"]');
    radios[1].dispatchEvent(new Event('change'));
    await fixture.whenStable();
    expect(page.sourceType()).toBe('directory');
    check('skipBuildOutput', false);
    expect(page.skipBuildOutput()).toBe(false);
    radios[0].dispatchEvent(new Event('change'));
    expect(page.sourceType()).toBe('zip');

    const modes = el().querySelectorAll<HTMLInputElement>('input[name="subjectsMode"]');
    modes[1].dispatchEvent(new Event('change'));
    await fixture.whenStable();
    const subject = el().querySelector<HTMLInputElement>('.subject-grid input')!;
    subject.checked = true;
    subject.dispatchEvent(new Event('change'));
    expect(page.subjectsValue()).toBe('review-maintainability');
    modes[0].dispatchEvent(new Event('change'));
    expect(page.subjectsValue()).toBe('all');
  });

  it('labels the button with the current phase', async () => {
    const button = () => el().querySelector<HTMLButtonElement>('button[type="submit"]')!.textContent!.trim();
    expect(button()).toBe('Start review');
    page.phase.set('zipping');
    await fixture.whenStable();
    expect(button()).toBe('Zipping…');
    page.phase.set('uploading');
    page.uploadPercent.set(40);
    await fixture.whenStable();
    expect(button()).toBe('Uploading 40%');
    page.uploadPercent.set(null);
    await fixture.whenStable();
    expect(button()).toBe('Uploading…');
    await flushAsync();
  });
});
