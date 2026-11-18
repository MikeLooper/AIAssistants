/** Shapes of comp-review-api responses (camelCase JSON). */

export type Tool = 'auto' | 'claude' | 'copilot';
export type JobStatus = 'queued' | 'running' | 'completed' | 'failed' | 'cancelled';
export type JobKind = 'review' | 'test';

export const FINISHED_STATUSES: readonly JobStatus[] = ['completed', 'failed', 'cancelled'];

export function isFinished(status: JobStatus): boolean {
  return FINISHED_STATUSES.includes(status);
}

export interface ToolInfo {
  name: string;
  found: boolean;
  path: string | null;
}

export interface About {
  name: string;
  reviewerVersion: string | null;
  environment: 'development' | 'production';
  pythonVersion: string;
  tools: ToolInfo[];
  subjects: string[];
  configuration: Record<string, unknown>;
}

export interface Health {
  status: 'healthy' | 'degraded' | 'unhealthy';
  checks: Record<string, boolean>;
  details: Record<string, string>;
}

export interface TesterInfo {
  name: string;
  title: string;
  kind: string;
  language: string;
  script: string;
}

export interface JobSummary {
  id: string;
  kind: JobKind;
  name: string;
  status: JobStatus;
  createdAt: string;
  startedAt: string | null;
  finishedAt: string | null;
  durationSeconds: number | null;
  error: string | null;
  overallScore: number | null;
  overallBand: string | null;
  verdict: string | null;
}

export interface JobResult {
  report?: string | null;
  testResultMarkdown?: string | null;
  runId?: string | null;
  overallScore?: number | null;
  overallBand?: string | null;
  verdict?: string | null;
  summary?: Record<string, unknown> | null;
  testResult?: Record<string, unknown> | null;
  [key: string]: unknown;
}

export interface JobDetail extends JobSummary {
  options: Record<string, unknown>;
  exitCode: number | null;
  log: string[];
  logLineCount: number;
  result: JobResult | null;
}

export interface ReviewOptions {
  tool: Tool;
  model?: string | null;
  subjects: string;
  advanced: boolean;
  analyzers?: string;
  timeoutMin?: number | null;
}

export interface TesterRunOptions {
  tool: Tool;
  model?: string | null;
  minFound: number;
  noBuild: boolean;
  timeoutMin?: number | null;
}
