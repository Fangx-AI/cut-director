#!/usr/bin/env python3
"""Check tracked Markdown's explicit local file/image links, not remote URLs or anchors."""
import re
import subprocess
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT=Path(__file__).resolve().parents[1]

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
    result=subprocess.run(['git','ls-files','--cached','--others','--exclude-standard','-z'],cwd=ROOT,check=True,capture_output=True)
    paths=sorted({p for p in result.stdout.decode('utf-8').split('\0') if p.endswith('.md')})
    errors=[]
    for name in paths:
        path=ROOT/name
        if path.exists():
            errors.extend(f'{name}: {target}' for target in missing_links(path,path.read_text(encoding='utf-8')))
    if errors:
        print('\n'.join(errors));raise SystemExit(1)
    print(f'Checked local file targets in {len(paths)} Markdown files (remote URLs and anchors excluded).')

if __name__=='__main__':main()
