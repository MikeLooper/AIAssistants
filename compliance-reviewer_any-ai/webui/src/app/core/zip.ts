import { Zippable, zip } from 'fflate';

/** Folders left out of a directory upload by default: build output, dependencies and VCS data. They add
 * review findings that aren't about the source and make the upload large. */
export const DEFAULT_SKIPPED_FOLDERS: readonly string[] = [
  '.git', 'node_modules', 'bin', 'obj', 'target', 'dist', 'build', '.venv', 'venv', '__pycache__',
  '.angular', '.gradle', '.idea', '.vs', '.pytest_cache', '.mypy_cache',
];

export interface DirectorySelection {
  /** The picked folder's name (the first segment of every relative path). */
  rootName: string;
  /** Files to upload, with their paths relative to the picked folder's parent. */
  files: { path: string; file: File }[];
  skippedCount: number;
  totalBytes: number;
}

/** The path a browser gives a file picked with `<input webkitdirectory>`, e.g. `myapp/src/main.py`. */
export function relativePath(file: File): string {
  const rel = (file as File & { webkitRelativePath?: string }).webkitRelativePath;
  return (rel || file.name).replace(/\\/g, '/');
}

/** Picks the files to zip from a directory selection, leaving out files under any skipped folder. */
export function selectDirectoryFiles(files: ArrayLike<File>, skipFolders: readonly string[] = []): DirectorySelection {
  const skip = new Set(skipFolders.map((f) => f.toLowerCase()));
  const selected: { path: string; file: File }[] = [];
  let skippedCount = 0;
  let totalBytes = 0;
  let rootName = '';
  for (const file of Array.from(files)) {
    const parts = relativePath(file).split('/').filter(Boolean);
    rootName ||= parts.length > 1 ? parts[0] : '';
    const folders = parts.slice(1, -1); // the picked folder itself is never skipped
    if (folders.some((p) => skip.has(p.toLowerCase()))) {
      skippedCount++;
      continue;
    }
    selected.push({ path: parts.join('/'), file });
    totalBytes += file.size;
  }
  return { rootName: rootName || 'source', files: selected, skippedCount, totalBytes };
}

/** Zips the selection in the browser. The picked folder stays the single top-level folder, so the API
 * names the review after it. */
export async function zipSelection(selection: DirectorySelection): Promise<Blob> {
  if (!selection.files.length) {
    throw new Error('The folder has no files to upload.');
  }
  const tree: Zippable = {};
  for (const { path, file } of selection.files) {
    tree[path] = new Uint8Array(await file.arrayBuffer());
  }
  const data = await new Promise<Uint8Array>((resolve, reject) =>
    zip(tree, { level: 6 }, (err, out) => (err ? reject(err) : resolve(out))),
  );
  return new Blob([data as BlobPart], { type: 'application/zip' });
}

export function formatBytes(bytes: number): string {
  if (bytes < 1024) return `${bytes} B`;
  const units = ['KB', 'MB', 'GB'];
  let value = bytes;
  let unit = -1;
  do {
    value /= 1024;
    unit++;
  } while (value >= 1024 && unit < units.length - 1);
  return `${value.toFixed(value < 10 ? 1 : 0)} ${units[unit]}`;
}
