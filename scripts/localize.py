"""Localise Quarto's shared navbar after rendering. Python standard library only.

English pages live at the project root, German pages in de/.
Runs automatically for both `quarto render` and `quarto preview`.
"""
import html
import os
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent.parent
output = os.environ.get('QUARTO_PROJECT_OUTPUT_DIR')
if not output:
    config = (ROOT / '_quarto.yml').read_text(encoding='utf-8')
    match = re.search(r'^\s+output-dir:\s*([^\n#]+)', config, re.M)
    output = match.group(1).strip().strip('\"\'') if match else '_site'
SITE = (ROOT / output).resolve()
LABELS = {
    'en': {'index': 'Home', 'about': 'About', 'experience': 'Experience', 'projects': 'Projects', 'cv': 'CV'},
    'de': {'index': 'Startseite', 'about': 'Über mich', 'experience': 'Berufserfahrung', 'projects': 'Projekte', 'cv': 'Lebenslauf'},
}
SLUGS = {label: slug for labels in LABELS.values() for slug, label in labels.items()}

def attr(attrs, key, value):
    attrs = re.sub(r'\s+' + re.escape(key) + r'="[^"]*"', '', attrs)
    return attrs + f' {key}="{html.escape(value, quote=True)}"'

def without_attr(attrs, key):
    return re.sub(r'\s+' + re.escape(key) + r'="[^"]*"', '', attrs)

for lang, labels in LABELS.items():
    folder = SITE / ('de' if lang == 'de' else '')
    for slug in labels:
        path = folder / f'{slug}.html'
        if not path.exists():
            continue
        def relative(target_lang, target_slug):
            target = SITE / ('de' if target_lang == 'de' else '') / f'{target_slug}.html'
            return os.path.relpath(target, path.parent).replace(os.sep, '/')
        def anchor(match):
            attrs, content = match.groups()
            text = html.unescape(re.sub('<[^>]+>', '', content)).strip()
            if text in ('English', 'Deutsch'):
                target_lang = 'en' if text == 'English' else 'de'
                attrs = attr(attrs, 'href', relative(target_lang, slug))
                attrs = attr(attrs, 'hreflang', target_lang)
                attrs = attr(attrs, 'lang', target_lang)
                attrs = attr(attrs, 'aria-label', ('Switch to English' if target_lang == 'en' else 'Auf Deutsch wechseln'))
                attrs = without_attr(attrs, 'aria-current')
                old_class = re.search(r'class="([^"]*)"', attrs)
                classes = [c for c in (old_class.group(1).split() if old_class else []) if c not in ('active', 'language-current', 'language-link')]
                classes.append('language-link')
                if target_lang == lang:
                    classes.append('language-current')
                    attrs = attr(attrs, 'aria-current', 'true')
                attrs = attr(attrs, 'class', ' '.join(classes))
            elif 'navbar-brand' in attrs:
                attrs = attr(attrs, 'href', relative(lang, 'index'))
            elif text in SLUGS:
                target_slug = SLUGS[text]
                attrs = attr(attrs, 'href', relative(lang, target_slug))
                attrs = without_attr(attrs, 'aria-current')
                old_class = re.search(r'class="([^"]*)"', attrs)
                classes = [c for c in (old_class.group(1).split() if old_class else []) if c != 'active']
                if target_slug == slug:
                    classes.append('active')
                    attrs = attr(attrs, 'aria-current', 'page')
                attrs = attr(attrs, 'class', ' '.join(classes))
                content = re.sub(r'(<span class="menu-text">).*?(</span>)', lambda m: m[1] + html.escape(labels[target_slug]) + m[2], content, flags=re.S)
            elif 'mailto:' in attrs and lang == 'de':
                content = content.replace('aria-label="Email"', 'aria-label="E-Mail"')
            return '<a' + attrs + '>' + content + '</a>'
        source = path.read_text(encoding='utf-8')
        def header(match):
            return re.sub(r'<a\b([^>]*)>(.*?)</a>', anchor, match[0], flags=re.S)
        source = re.sub(r'<header id="quarto-header".*?</header>', header, source, flags=re.S)
        if lang == 'de':
            source = source.replace('Built with Quarto', 'Erstellt mit Quarto')
        source = re.sub(r'\n<link rel="alternate" hreflang="(?:en|de|x-default)"[^>]*>', '', source)
        alternates = '\n'.join(f'<link rel="alternate" hreflang="{code}" href="{relative(target, slug)}">' for code, target in [('en', 'en'), ('de', 'de'), ('x-default', 'en')])
        source = source.replace('</head>', alternates + '\n</head>')
        path.write_text(source, encoding='utf-8')
print('Localised English/German navigation and same-page language links.')
