import { HttpTestingController } from '@angular/common/http/testing';
import { ComponentFixture, TestBed } from '@angular/core/testing';
import { Router } from '@angular/router';

import { TesterInfo } from '../../core/api.models';
import { API, aboutFixture, configure, jobFixture, testProviders } from '../../testing/helpers';
import { TestersPage } from './testers-page';

const TESTERS: TesterInfo[] = [
  { name: 'api-dotnet', title: 'C# API', kind: 'apis', language: 'dotNET', script: 'test/logic/test_api_dotnet.py' },
  { name: 'ui-java', title: 'Java UI', kind: 'uis', language: 'java', script: 'test/logic/test_ui_java.py' },
];

describe('TestersPage', () => {
  let fixture: ComponentFixture<TestersPage>;
  let page: TestersPage;
  let http: HttpTestingController;
  let navigate: ReturnType<typeof vi.spyOn>;

  async function create(testers: TesterInfo[] | 'error' = TESTERS) {
    fixture = TestBed.createComponent(TestersPage);
    page = fixture.componentInstance;
    fixture.detectChanges();
    http.expectOne(`${API}/api/about`).flush(aboutFixture());
    const req = http.expectOne(`${API}/api/testers`);
    if (testers === 'error') {
      req.flush({ detail: 'nope' }, { status: 500, statusText: 'x' });
    } else {
      req.flush(testers);
    }
    await fixture.whenStable();
  }

  beforeEach(() => {
    TestBed.configureTestingModule({ providers: testProviders() });
    configure();
    http = TestBed.inject(HttpTestingController);
    navigate = vi.spyOn(TestBed.inject(Router), 'navigate').mockResolvedValue(true);
  });

  afterEach(() => http.verify());

  const el = () => fixture.nativeElement as HTMLElement;

  it('lists the testers', async () => {
    await create();
    const rows = el().querySelectorAll('tbody tr');
    expect(rows.length).toBe(2);
    expect(rows[0].textContent).toContain('C# API');
    expect(rows[0].textContent).toContain('test/logic/test_api_dotnet.py');
  });

  it('shows a load error and an empty state', async () => {
    await create('error');
    expect(page.error()).toBe('nope (HTTP 500)');
    expect(page.loading()).toBe(false);
    await create([]);
    expect(el().textContent).toContain('found no tester scripts');
  });

  it('keeps working without the about data', async () => {
    fixture = TestBed.createComponent(TestersPage);
    fixture.detectChanges();
    http.expectOne(`${API}/api/about`).error(new ProgressEvent('error'));
    http.expectOne(`${API}/api/testers`).flush(TESTERS);
    expect(fixture.componentInstance.about()).toBeNull();
    expect(fixture.componentInstance.testers().length).toBe(2);
  });

  it('runs one tester with the options and opens its job', async () => {
    await create();
    page.tool.set('claude');
    page.model.set('claude-opus-5-5');
    page.minFound.set(75);
    page.noBuild.set(true);
    page.timeoutMin.set(30);
    el().querySelector<HTMLButtonElement>('tbody tr button')!.click();
    const req = http.expectOne(`${API}/api/testers/api-dotnet`);
    expect(req.request.body).toEqual({ tool: 'claude', model: 'claude-opus-5-5', minFound: 75, noBuild: true,
                                       timeoutMin: 30 });
    expect(page.starting()).toBe(true);
    page.run('ui-java'); // ignored while starting
    req.flush(jobFixture({ id: 't1', kind: 'test' }));
    expect(navigate).toHaveBeenCalledWith(['/jobs', 't1']);
    expect(page.starting()).toBe(false);
  });

  it('shows a conflict when the tester is already running', async () => {
    await create();
    page.run('api-dotnet');
    http.expectOne(`${API}/api/testers/api-dotnet`).flush({ detail: 'already running' },
                                                           { status: 409, statusText: 'Conflict' });
    expect(page.error()).toBe('already running (HTTP 409)');
    expect(navigate).not.toHaveBeenCalled();
  });

  it('selects testers and runs the selection, reporting partial failures', async () => {
    await create();
    page.toggleAll(true);
    expect(page.allSelected()).toBe(true);
    page.toggle('ui-java', false);
    expect(page.allSelected()).toBe(false);
    page.toggle('ui-java', true);
    page.runSelected();
    http.expectOne(`${API}/api/testers/api-dotnet`).flush(jobFixture());
    http.expectOne(`${API}/api/testers/ui-java`).flush({ detail: 'busy' }, { status: 409, statusText: 'Conflict' });
    expect(page.error()).toBe('ui-java: busy (HTTP 409)');
    expect(navigate).toHaveBeenCalledWith(['/jobs']);
  });

  it('stays on the page when every selected tester fails', async () => {
    await create();
    page.toggle('ui-java', true);
    page.runSelected();
    http.expectOne(`${API}/api/testers/ui-java`).flush({ detail: 'busy' }, { status: 409, statusText: 'Conflict' });
    expect(navigate).not.toHaveBeenCalled();
    page.toggleAll(false);
    page.runSelected(); // nothing selected
    http.expectNone(`${API}/api/testers/ui-java`);
  });

  it('validates the options and blocks runs while invalid', async () => {
    await create();
    page.minFound.set(150);
    expect(page.optionsError()).toContain('between 0 and 100');
    page.run('api-dotnet');
    http.expectNone(`${API}/api/testers/api-dotnet`);
    page.minFound.set(90);
    page.timeoutMin.set(-1);
    expect(page.optionsError()).toContain('greater than 0');
    page.timeoutMin.set(null);
    expect(page.optionsError()).toBeNull();
  });

  it('wires the inputs to its state', async () => {
    await create();
    const min = el().querySelector<HTMLInputElement>('input[name="minFound"]')!;
    min.value = '80';
    min.dispatchEvent(new Event('input'));
    const timeout = el().querySelector<HTMLInputElement>('input[name="timeoutMin"]')!;
    timeout.value = '9';
    timeout.dispatchEvent(new Event('input'));
    const noBuild = el().querySelector<HTMLInputElement>('input[name="noBuild"]')!;
    noBuild.checked = true;
    noBuild.dispatchEvent(new Event('change'));
    const all = el().querySelector<HTMLInputElement>('thead input')!;
    all.checked = true;
    all.dispatchEvent(new Event('change'));
    const one = el().querySelector<HTMLInputElement>('tbody input')!;
    one.checked = false;
    one.dispatchEvent(new Event('change'));
    expect(page.minFound()).toBe(80);
    expect(page.timeoutMin()).toBe(9);
    expect(page.noBuild()).toBe(true);
    expect([...page.selected()]).toEqual(['ui-java']);
    timeout.value = '';
    timeout.dispatchEvent(new Event('input'));
    expect(page.timeoutMin()).toBeNull();
  });
});
