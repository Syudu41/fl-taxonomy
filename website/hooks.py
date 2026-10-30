"""Discover concept documents and build both navigation views from their files."""
import re
from pathlib import Path
from posixpath import relpath

import yaml
from pathspec import PathSpec
from mkdocs.structure.files import File

_catalog = {}
_readmes = {}


def read_document(path):
    text = path.read_text(encoding='utf-8')
    match = re.match(r'\A---\s*\n(.*?)\n---\s*\n', text, re.S)
    meta = yaml.safe_load(match[1]) or {} if match else {}
    body = text[match.end():] if match else text
    heading = re.search(r'^#\s+(.+)$', body, re.M)
    title = str(meta.get('title') or (heading[1].strip() if heading else path.parent.name if path.stem.lower() == 'readme' else path.stem.replace('-', ' ').title()))
    paragraphs = re.split(r'\n\s*\n', body.strip())
    summary = next((p.replace('\n', ' ') for p in paragraphs if p and not p.startswith(('#', '>', '-', '*', '```'))), f'Notes and references for {title}.')
    return title, str(meta.get('description') or summary), meta


def concept_coverage(document, meta):
    text = document.read_text(encoding='utf-8')
    placeholder = bool(re.search(r'lorem ipsum|placeholder|future fieldnote|future study', text, re.I))
    inferred = {
        'overview': not placeholder,
        'math': not placeholder and bool(re.search(r'^\$\$', text, re.M)),
        'example': not placeholder and bool(re.search(r'^## .*(example|calculation|worked|complete round)', text, re.I | re.M)),
        'sources': not placeholder and bool(re.search(r'\]\(https://', text)),
        'check': not placeholder and bool(re.search(r'^## .*self.check', text, re.I | re.M)),
    }
    return {key: bool(meta.get('coverage', {}).get(key, value)) for key, value in inferred.items()}


def on_config(config):
    _catalog.clear()
    _readmes.clear()
    docs = Path(config.docs_dir)
    dimensions = {}
    exclusions = []
    for listing in sorted((docs / 'dimensions').glob('*/index.md')):
        dimension_title, _, _ = read_document(listing)
        concepts = []
        for document in sorted(listing.parent.rglob('*.md')):
            if document == listing:
                continue
            title, summary, meta = read_document(document)
            if meta.get('draft'):
                continue
            source = document.relative_to(docs).as_posix()
            # README is normally an index alias in MkDocs. Give it its own URL,
            # including when it shares a folder with the dimension index.
            if document.stem.lower() == 'readme':
                exclusions.append('/' + source)
                source = document.relative_to(docs).with_name('readme-note.md').as_posix()
                if (docs / source).exists():
                    raise ValueError(f'README alias conflicts with {source}')
                _readmes[source] = document
            entry = {'title': title, 'summary': summary, 'source': source,
                     'url': str(Path(source).with_suffix('.html')).replace('\\', '/'),
                     'dimension': dimension_title, 'slug': listing.parent.name,
                     'order': meta.get('order', 1000),
                     'coverage': concept_coverage(document, meta),
                     'anchors': meta.get('section_anchors', {})}
            _catalog[source] = entry
            concepts.append(entry)
        concepts.sort(key=lambda entry: (entry['order'], entry['title'].casefold(), entry['source']))
        dimensions[listing.parent.name] = concepts
    if exclusions:
        config.exclude_docs = (config.exclude_docs or PathSpec([])) + PathSpec.from_lines('gitignore', exclusions)
    config.extra['dimension_concepts'] = dimensions
    paper_file = Path(config.config_file_path).parent / 'data' / 'papers.yml'
    papers = yaml.safe_load(paper_file.read_text(encoding='utf-8')) or []
    library = Path(config.config_file_path).parent.parent / 'ref-papers'
    for paper in papers:
        paper['local_available'] = bool(paper.get('local_file') and (library / paper['local_file']).is_file())
    config.extra['papers'] = papers
    return config


def on_files(files, config):
    for source, document in _readmes.items():
        files.append(File.generated(config, source, content=document.read_text(encoding='utf-8')))
    return files


def on_page_markdown(markdown, page, config, files):
    source = page.file.src_uri
    if source in _catalog:
        entry = _catalog[source]
        page.meta.setdefault('layout', 'concept')
        page.meta.setdefault('title', entry['title'])
        page.meta.setdefault('dimension', entry['dimension'])
        page.meta.setdefault('dimension_url', f"dimensions/{entry['slug']}/index.html")
    parts = Path(source).parts
    if len(parts) == 3 and parts[0] == 'dimensions' and parts[2] == 'index.md':
        page.meta.setdefault('layout', 'dimension')
        # The source index contains only its introduction; the list is generated.
        entries = config.extra['dimension_concepts'].get(parts[1], [])
        for entry in entries:
            target = relpath(entry['source'], str(Path(source).parent))
            markdown += f"\n\n## [{entry['title']}]({target})\n\n{entry['summary']}\n"
    return markdown
