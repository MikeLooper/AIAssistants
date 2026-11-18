import { unzipSync, strFromU8 } from 'fflate';

import { dirFile } from '../testing/helpers';
import { DEFAULT_SKIPPED_FOLDERS, formatBytes, relativePath, selectDirectoryFiles, zipSelection } from './zip';

async function blobBytes(blob: Blob): Promise<Uint8Array> {
  return new Uint8Array(await blob.arrayBuffer());
}

describe('zip helpers', () => {
  it('relativePath uses webkitRelativePath, else the name', () => {
    expect(relativePath(dirFile('app\\src\\a.py'))).toBe('app/src/a.py');
    expect(relativePath(new File(['x'], 'plain.txt'))).toBe('plain.txt');
  });

  it('selectDirectoryFiles leaves out skipped folders but never the picked folder', () => {
    const files = [
      dirFile('bin/src/main.py', 'abc'), // the picked folder is called "bin"
      dirFile('bin/README.md', 'r'),
      dirFile('bin/node_modules/x/index.js'),
      dirFile('bin/src/obj/Debug/a.dll'),
      dirFile('bin/.GIT/config'),
    ];
    const sel = selectDirectoryFiles(files, DEFAULT_SKIPPED_FOLDERS);
    expect(sel.rootName).toBe('bin');
    expect(sel.files.map((f) => f.path)).toEqual(['bin/src/main.py', 'bin/README.md']);
    expect(sel.skippedCount).toBe(3);
    expect(sel.totalBytes).toBe(4);
  });

  it('selectDirectoryFiles keeps everything without a skip list', () => {
    const sel = selectDirectoryFiles([dirFile('app/node_modules/a.js')]);
    expect(sel.files.length).toBe(1);
    expect(sel.skippedCount).toBe(0);
  });

  it('falls back to "source" when files have no folder', () => {
    expect(selectDirectoryFiles([new File(['x'], 'a.txt')]).rootName).toBe('source');
  });

  it('zipSelection builds a zip with the picked folder at the top', async () => {
    const sel = selectDirectoryFiles([dirFile('app/a.txt', 'hello'), dirFile('app/sub/b.txt', 'world')]);
    const blob = await zipSelection(sel);
    expect(blob.type).toBe('application/zip');
    const entries = unzipSync(await blobBytes(blob));
    expect(Object.keys(entries).sort()).toEqual(['app/a.txt', 'app/sub/b.txt']);
    expect(strFromU8(entries['app/sub/b.txt'])).toBe('world');
  });

  it('zipSelection refuses an empty selection', async () => {
    await expect(zipSelection({ rootName: 'x', files: [], skippedCount: 0, totalBytes: 0 }))
      .rejects.toThrow('no files');
  });

  it('formatBytes', () => {
    expect(formatBytes(512)).toBe('512 B');
    expect(formatBytes(1536)).toBe('1.5 KB');
    expect(formatBytes(20 * 1024 * 1024)).toBe('20 MB');
    expect(formatBytes(3 * 1024 ** 3)).toBe('3.0 GB');
    expect(formatBytes(5000 * 1024 ** 3)).toBe('5000 GB');
  });
});
