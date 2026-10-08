"""Evidence-only claim/reference graph from modular LaTeX.

This is NOT a dependency graph and NOT a mathematical truth verifier.
The source nodes describe labels, scoped environments, and text references.
"""
from __future__ import annotations
import argparse
import json
import re
from pathlib import Path
from collections import Counter

LABEL = re.compile(r'\\label\{([^{}]+)\}')
REF = re.compile(r'\\(?:ref|eqref|autoref|cref|Cref)\{([^{}]+)\}')
INPUT = re.compile(r'\\(?:input|include)\{([^{}]+)\}')
BEGIN = re.compile(r'\\begin\{([A-Za-z*]+)\}')
END = re.compile(r'\\end\{([A-Za-z*]+)\}')
SECTION = re.compile(r'\\(?:section|subsection|subsubsection)\*?\{([^{}]*)\}')
CONTROL = re.compile(r'\\(?P<kind>begin|end|label|ref|eqref|autoref|cref|Cref|section|subsection|subsubsection)\*?\{(?P<value>[^{}]*)\}')
STATEMENTS = {'theorem','lemma','proposition','corollary','definition','claim',
              'conjecture','remark','example','theorem*','lemma*'}
EQUATIONS = {'equation','equation*','align','align*','gather','gather*','multline','multline*'}


def strip_comments(line: str) -> str:
    for i, c in enumerate(line):
        if c != '%':
            continue
        num_slashes = 0
        j = i-1
        while j >= 0 and line[j] == '\\':
            num_slashes += 1
            j -= 1
        if num_slashes % 2 == 0:
            return line[:i]
    return line


def expand_sources(root: Path, main_file: str, max_files: int = 200) -> list[tuple[str,int,str]]:
    """Expand literal input/include commands in order. No arbitrary TeX macro evaluation."""
    root = root.resolve()
    stack: list[str] = []
    loaded: set[str] = set()
    result: list[tuple[str,int,str]] = []
    def visit(relative: str):
        file = (root / relative).resolve()
        if not file.is_relative_to(root):
            raise ValueError(f'Include escapes repo root: {relative}')
        key = file.relative_to(root).as_posix()
        if key in stack:
            raise ValueError('LaTeX include cycle: ' + ' -> '.join(stack+[key]))
        if key in loaded:
            raise ValueError(f'Repeated LaTeX include not currently supported: {key}')
        if len(loaded) >= max_files:
            raise ValueError('Too many included LaTeX files')
        if not file.is_file():
            raise FileNotFoundError(f'Missing LaTeX file: {key}')
        loaded.add(key)
        stack.append(key)
        for lineno, raw in enumerate(file.read_text(encoding='utf-8').splitlines(),1):
            line = strip_comments(raw)
            positions=list(INPUT.finditer(line))
            if not positions:
                result.append((key,lineno,line))
                continue
            last=0
            for item in positions:
                before=line[last:item.start()]
                if before.strip(): result.append((key,lineno,before))
                name=item[1] if item[1].endswith('.tex') else item[1]+'.tex'
                target=(file.parent/name).resolve()
                visit(target.relative_to(root).as_posix() if target.is_relative_to(root) else '../outside.tex')
                last=item.end()
            if line[last:].strip():result.append((key,lineno,line[last:]))
        stack.pop()
    visit(main_file)
    return result


def graph_from_lines(lines: list[tuple[str,int,str]]) -> dict:
    labels: dict[str,dict] = {}
    references: list[dict] = []
    duplicate: list[dict] = []
    stack: list[str] = []
    section='(preamble)'
    for path,lineno,line in lines:
        for token in CONTROL.finditer(line):
            kind,value=token.group('kind'),token.group('value')
            if kind in ('section','subsection','subsubsection'):
                section=value
            elif kind=='begin':
                stack.append(value)
            elif kind=='end':
                if value in stack:
                    while stack and stack[-1]!=value:stack.pop()
                    stack.pop()
            elif kind=='label':
                enclosing=next((s for s in reversed(stack) if s in STATEMENTS or s in EQUATIONS),None)
                role='statement' if enclosing in STATEMENTS else ('equation' if enclosing in EQUATIONS else 'section_or_other')
                node={'id':value,'file':path,'line':lineno,'section':section,
                      'environment':enclosing,'role':role}
                if value in labels:duplicate.append({'label':value,'original':labels[value],'repeat':node})
                labels[value]=node
            elif kind in ('ref','eqref','autoref','cref','Cref'):
                references.append({'target':value,'file':path,'line':lineno,
                                   'section':section,'syntax':kind,
                                   'context_environments':list(stack)})
    unresolved=[r for r in references if r['target'] not in labels]
    counts=Counter(r['target'] for r in references)
    cross=sum(1 for r in references if r['target'] in labels and labels[r['target']]['file']!=r['file'])
    return {
        'schema_version':'0.1',
        'graph_type':'syntax_and_provenance_only',
        'not_a_proof_dependency_graph':True,
        'summary':{'source_files':len(set(p for p,_,_ in lines)),
                   'labels':len(labels),'reference_occurrences':len(references),
                   'cross_file_references':cross,'missing_reference_targets':len(unresolved),
                   'duplicate_labels':len(duplicate),
                   'roles':dict(Counter(n['role'] for n in labels.values()))},
        'labels':labels,'references':references,
        'unresolved_references':unresolved,'duplicate_declarations':duplicate,
        'most_referenced':[{'label':k,'count':v} for k,v in counts.most_common(20)],
        'caveats':['The order of expanded TeX labels can be affected by unexpanded macros.',
                   'A source reference is neither formal use of a theorem nor conceptual centrality.',
                   'Labels and prose contain claims that have not been independently verified.'],
    }


def audit(root: Path, main: str) -> dict:
    return graph_from_lines(expand_sources(root,main))


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--root',default='.')
    p.add_argument('--main',required=True,help='Repository-root-relative main TeX file')
    p.add_argument('--output',required=True)
    a=p.parse_args()
    graph=audit(Path(a.root),a.main)
    out=Path(a.output);out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(graph,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps({'main':a.main,**graph['summary']},indent=2))
    if graph['summary']['duplicate_labels']:
        raise SystemExit('Duplicate LaTeX labels detected')


if __name__=='__main__':main()
