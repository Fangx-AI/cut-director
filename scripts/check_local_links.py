#!/usr/bin/env python3
"""Check tracked Markdown's explicit local file/image links, not remote URLs or anchors."""
import os
import re
import subprocess
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT=Path(__file__).resolve().parents[1]
ARTIFACT_DIRS={'.git', '.agents', '.codex', '.talkdirector', '.worktrees', '.superpowers',
               'node_modules', 'test-results', 'playwright-report', '__pycache__'}

def markdown_paths(root):
    # Git defines the source set in a checkout; copied skill installations have no Git metadata.
    try:
        repo=subprocess.run(['git','rev-parse','--show-toplevel'],cwd=root,check=False,capture_output=True)
        is_checkout=repo.returncode == 0 and Path(repo.stdout.decode('utf-8').strip()).resolve() == root.resolve()
        result=subprocess.run(['git','ls-files','--cached','--others','--exclude-standard','-z'],
                              cwd=root,check=False,capture_output=True) if is_checkout else None
    except FileNotFoundError:
        result=None
    if result is not None and result.returncode == 0:
        return sorted({p for p in result.stdout.decode('utf-8').split('\0') if p.endswith('.md')})
    paths=[]
    for directory, subdirs, files in os.walk(root):
        subdirs[:]=[name for name in subdirs if name not in ARTIFACT_DIRS]
        paths.extend((Path(directory)/name).relative_to(root).as_posix()
                     for name in files if name.endswith('.md'))
    return sorted(paths)

def missing_links(path, text):
    # Ignore code examples, which may contain placeholder URLs or paths.
    text=re.sub(r'```.*?```','',text,flags=re.S)
    targets=re.findall(r'\]\((<[^>]+>|[^\s)]+)(?:\s+"[^"]*")?\)',text)
    targets+=re.findall(r'(?:src|href)=["\']([^"\']+)["\']',text)
    missing=[]
    for target in targets:
        target=target.strip('<>')
        parsed=urlsplit(target)
        if parsed.scheme or target.startswith(('#','//')) or not parsed.path:
            continue
        local=path.parent/unquote(parsed.path)
        if not local.exists():
            missing.append(target)
    return sorted(set(missing))

def main():
    # Include new files before their first commit; omit ignored dependencies and artifacts.
    paths=markdown_paths(ROOT)
    errors=[]
    for name in paths:
        path=ROOT/name
        if path.exists():
            errors.extend(f'{name}: {target}' for target in missing_links(path,path.read_text(encoding='utf-8')))
    if errors:
        print('\n'.join(errors));raise SystemExit(1)
    print(f'Checked local file targets in {len(paths)} Markdown files (remote URLs and anchors excluded).')

if __name__=='__main__':main()
