"""Apply the author-approved positioning paragraphs; no scientific edits."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]
DRAFT = (ROOT / 'research/submission_readiness_2026-09-20/MANUSCRIPT_POSITIONING_DRAFT.md').read_text()
sections = re.split(r'\n## [123]\. ', DRAFT)[1:]
for language, folder in [('Inglés', 'manuscript'), ('Español', 'manuscript_es')]:
    paragraphs = [re.search(r'### ' + language + r'\n\n([^\n]+)', s).group(1) for s in sections]
    path = ROOT / folder / 'main.tex'
    text = path.read_text()
    assert paragraphs[0] not in text, 'Already applied'
    marker = '\n\\section{Background and research questions}' if language == 'Inglés' else '\n\\section{Antecedentes y preguntas de investigación}'
    assert marker in text
    text = text.replace(marker, '\n' + paragraphs[0] + '\n' + marker, 1)
    prior = text.split('\\subsection')[1]
    candidates = [p for p in prior.split('\n\n') if 'ref4e1e0d5582' in p]
    assert len(candidates) == 1
    paragraph = paragraphs[1]
    for name, key in [('Caspari et al. (2024)', 'ref4e1e0d5582'), ('Imel and Hafen (2025)', 'ref6da178065c'), ('Imel y Hafen (2025)', 'ref6da178065c'), ('Raju (2026)', 'ref483cb38608')]:
        paragraph = paragraph.replace(name, '\\citet{' + key + '}')
    text = text.replace(candidates[0], paragraph, 1)
    # Remove the repeated positioning sentence; retain its preceding citations.
    duplicate = ("The contribution here is the controlled comparison across levels, text choices and repeated area comparisons, including cases where a result persists within models but reverses between them." if language == 'Inglés' else "La aportación aquí es la comparación controlada entre niveles, decisiones de texto y comparaciones repetidas de áreas, incluidos los casos en que un resultado se mantiene dentro de cada modelo y se invierte entre modelos.")
    assert duplicate in text
    text = text.replace(' ' + duplicate, '', 1)
    marker = '\n\\subsection{What the additional checks change}' if language == 'Inglés' else '\n\\subsection{Qué cambian las comprobaciones adicionales}'
    assert marker in text
    text = text.replace(marker, '\n' + paragraphs[2] + '\n' + marker, 1)
    path.write_text(text)
    print(folder, 'three approved positioning edits applied')
