"""Source-import closure for a Lean module. NOT a theorem-dependency graph."""
from __future__ import annotations
from collections import Counter, deque
import argparse
import json
from pathlib import Path
import re

IMPORT_RE = re.compile(r'^\s*(?:public\s+)?import\s+(.+?)\s*$')
MODULE_RE = re.compile(r'^[A-Za-z_]\w*(?:\.[A-Za-z_]\w*)*$')


def parse_imports(file: Path) -> list[str]:
    imports = []
    with file.open('r', encoding='utf-8', errors='replace') as stream:
        for raw in stream:
            line = raw.split('--', 1)[0].strip()
            m = IMPORT_RE.match(line)
            if m:
                for name in m.group(1).split():
                    if MODULE_RE.fullmatch(name):
                        imports.append(name)
    return list(dict.fromkeys(imports))


def module_file(root: Path, module: str) -> Path:
    return root / 'lean' / (module.replace('.', '/') + '.lean')


def inspect_import_closure(root: Path, seed: str, limit: int = 100_000) -> dict:
    root = root.resolve()
    start = module_file(root, seed)
    if not start.is_file():
        raise FileNotFoundError(f'Missing seed module: {start}')
    queue = deque([seed])
    visited: set[str] = set()
    direct: dict[str, list[str]] = {}
    outside: Counter[str] = Counter()
    while queue:
        module = queue.popleft()
        if module in visited:
            continue
        if len(visited) >= limit:
            raise RuntimeError(f'Closure exceeds limit {limit}')
        file = module_file(root, module)
        if not file.is_file():
            outside[module] += 1
            continue
        visited.add(module)
        children = parse_imports(file)
        direct[module] = children
        for child in children:
            if module_file(root, child).is_file():
                if child not in visited:
                    queue.append(child)
            else:
                outside[child] += 1

    internal_edges = sum(sum(module_file(root, child).is_file() for child in imports)
                         for imports in direct.values())
    namespaces = Counter(m.split('.')[0] for m in visited)
    fanout = sorted(((len(v), m) for m,v in direct.items()),reverse=True)[:20]
    return {
        'schema_version':'0.1',
        'seed_module':seed,
        'seed_path':str(start.relative_to(root)),
        'internal_import_closure_modules':len(visited),
        'internal_import_edges':internal_edges,
        'seed_direct_imports':direct[seed],
        'external_module_names_unique':len(outside),
        'external_imports_sample':sorted(outside)[:25],
        'modules_by_root_namespace':dict(namespaces.most_common()),
        'largest_syntactic_fanout':[{'module':m,'imports':n} for n,m in fanout],
        'module_paths':sorted(visited),
        'caveats':[
            'Syntactic imports of files under lean/ only; Mathlib and Lake dependencies are not expanded.',
            'A Lean import is neither a used theorem nor a minimal logical proof dependency.',
            'No mathematical conclusion or Lean build is checked by this script.'
        ]
    }


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--root',default='.')
    p.add_argument('--module',default='OAI.NumberTheory.PiExponent.Main')
    p.add_argument('--output',required=True)
    a=p.parse_args()
    d=inspect_import_closure(Path(a.root),a.module)
    out=Path(a.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:d[k] for k in ('seed_module','internal_import_closure_modules','internal_import_edges',
                    'external_module_names_unique','seed_direct_imports')},indent=2))


if __name__=='__main__':
    main()
