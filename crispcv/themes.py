"""Built-in themes. Each theme is a complete stylesheet for the resume body."""

BASE = """
* { box-sizing: border-box; margin: 0; padding: 0; }
body { max-width: 760px; margin: 0 auto; padding: 56px 48px; }
h1 { font-size: 2rem; letter-spacing: -0.02em; }
.label { font-size: 1.05rem; margin-top: 4px; }
.contact { margin-top: 12px; font-size: 0.85rem; display: flex; flex-wrap: wrap; gap: 6px 18px; }
.contact a { text-decoration: none; }
section { margin-top: 32px; }
h2 { font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.14em; margin-bottom: 14px; }
.entry { margin-bottom: 18px; }
.entry-head { display: flex; justify-content: space-between; align-items: baseline; gap: 12px; }
.entry-title { font-weight: 600; }
.entry-sub { font-size: 0.9rem; }
.entry-dates { font-size: 0.8rem; white-space: nowrap; }
ul.highlights { margin: 8px 0 0 18px; }
ul.highlights li { margin-bottom: 4px; font-size: 0.92rem; line-height: 1.5; }
.summary { margin-top: 16px; line-height: 1.6; font-size: 0.95rem; }
.skill-group { display: flex; gap: 10px; margin-bottom: 8px; font-size: 0.9rem; }
.skill-name { font-weight: 600; min-width: 110px; }
.skill-items { line-height: 1.5; }
@media print {
  body { padding: 24px 8px; max-width: 100%; }
  a { color: inherit; }
  section { break-inside: avoid; }
}
@media (max-width: 600px) {
  body { padding: 32px 20px; }
  .entry-head { flex-direction: column; gap: 2px; }
}
"""

THEMES = {
    "slate": BASE
    + """
body { font-family: -apple-system, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
       color: #1e293b; background: #ffffff; }
h1 { color: #0f172a; }
.label { color: #475569; }
h2 { color: #2563eb; border-bottom: 2px solid #dbeafe; padding-bottom: 6px; }
.contact, .entry-dates, .entry-sub { color: #64748b; }
.contact a { color: #2563eb; }
ul.highlights li::marker { color: #2563eb; }
""",
    "ivory": BASE
    + """
body { font-family: Georgia, 'Times New Roman', serif;
       color: #292524; background: #fffdf7; }
h1 { font-weight: 500; color: #1c1917; }
.label { color: #78716c; font-style: italic; }
h2 { color: #9a3412; letter-spacing: 0.18em; }
.contact, .entry-dates, .entry-sub { color: #78716c; }
.contact a { color: #9a3412; }
ul.highlights li::marker { color: #9a3412; }
""",
    "mono": BASE
    + """
body { font-family: 'SF Mono', 'Cascadia Code', Consolas, Menlo, monospace;
       color: #18181b; background: #ffffff; font-size: 0.95em; }
h1 { font-size: 1.6rem; }
.label { color: #52525b; }
h2 { color: #18181b; }
h2::before { content: '## '; color: #a1a1aa; }
.contact, .entry-dates, .entry-sub { color: #71717a; }
.contact a { color: #18181b; }
ul.highlights { list-style: none; margin-left: 0; }
ul.highlights li::before { content: '- '; color: #a1a1aa; }
""",
}


def theme_names():
    return sorted(THEMES)


def get_theme(name):
    if name not in THEMES:
        raise KeyError(
            f"unknown theme '{name}' -- available: {', '.join(theme_names())}"
        )
    return THEMES[name]
