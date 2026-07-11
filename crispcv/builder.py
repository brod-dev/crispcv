"""Parse a resume TOML file and render it to standalone HTML."""

import html

try:
    import tomllib  # Python 3.11+
except ModuleNotFoundError:  # pragma: no cover
    import tomli as tomllib

from .themes import get_theme

REQUIRED_BASICS = ("name",)


class ResumeError(ValueError):
    """Raised when the resume file is missing required fields."""


def esc(value):
    return html.escape(str(value), quote=True)


def load(path):
    with open(path, "rb") as fh:
        data = tomllib.load(fh)
    validate(data)
    return data


def validate(data):
    basics = data.get("basics")
    if not isinstance(basics, dict):
        raise ResumeError("resume needs a [basics] table")
    for key in REQUIRED_BASICS:
        if not basics.get(key):
            raise ResumeError(f"[basics] is missing required field '{key}'")


def _contact_bits(basics):
    bits = []
    for key in ("email", "phone", "location"):
        if basics.get(key):
            bits.append(f"<span>{esc(basics[key])}</span>")
    site = basics.get("website")
    if site:
        href = site if site.startswith(("http://", "https://")) else f"https://{site}"
        bits.append(f'<a href="{esc(href)}">{esc(site)}</a>')
    return bits


def _entry(title, sub, start, end, highlights):
    dates = ""
    if start or end:
        dates = f'<span class="entry-dates">{esc(start)} &ndash; {esc(end)}</span>'
    sub_html = f'<div class="entry-sub">{esc(sub)}</div>' if sub else ""
    items = "".join(f"<li>{esc(h)}</li>" for h in highlights)
    list_html = f'<ul class="highlights">{items}</ul>' if items else ""
    return (
        '<div class="entry">'
        f'<div class="entry-head"><span class="entry-title">{esc(title)}</span>{dates}</div>'
        f"{sub_html}{list_html}</div>"
    )


def _work_section(entries):
    body = "".join(
        _entry(
            e.get("role", ""),
            e.get("company", ""),
            e.get("start", ""),
            e.get("end", ""),
            e.get("highlights", []),
        )
        for e in entries
    )
    return f"<section><h2>Experience</h2>{body}</section>"


def _education_section(entries):
    body = "".join(
        _entry(
            e.get("degree", ""),
            e.get("school", ""),
            e.get("start", ""),
            e.get("end", ""),
            e.get("highlights", []),
        )
        for e in entries
    )
    return f"<section><h2>Education</h2>{body}</section>"


def _projects_section(entries):
    parts = []
    for e in entries:
        name = esc(e.get("name", ""))
        link = e.get("link", "")
        if link:
            name = f'<a href="{esc(link)}">{name}</a>'
        desc = (
            f'<div class="entry-sub">{esc(e["description"])}</div>'
            if e.get("description")
            else ""
        )
        parts.append(
            f'<div class="entry"><div class="entry-head">'
            f'<span class="entry-title">{name}</span></div>{desc}</div>'
        )
    return f"<section><h2>Projects</h2>{''.join(parts)}</section>"


def _skills_section(skills):
    groups = skills.get("groups", [])
    rows = "".join(
        '<div class="skill-group">'
        f'<span class="skill-name">{esc(g.get("name", ""))}</span>'
        f'<span class="skill-items">{esc(", ".join(g.get("items", [])))}</span></div>'
        for g in groups
    )
    return f"<section><h2>Skills</h2>{rows}</section>"


def render(data, theme="slate"):
    css = get_theme(theme)
    basics = data["basics"]

    head = [f"<h1>{esc(basics['name'])}</h1>"]
    if basics.get("label"):
        head.append(f'<div class="label">{esc(basics["label"])}</div>')
    contact = _contact_bits(basics)
    if contact:
        head.append(f'<div class="contact">{"".join(contact)}</div>')
    if basics.get("summary"):
        head.append(f'<p class="summary">{esc(basics["summary"])}</p>')

    sections = []
    if data.get("work"):
        sections.append(_work_section(data["work"]))
    if data.get("projects"):
        sections.append(_projects_section(data["projects"]))
    if data.get("education"):
        sections.append(_education_section(data["education"]))
    if isinstance(data.get("skills"), dict) and data["skills"].get("groups"):
        sections.append(_skills_section(data["skills"]))

    return (
        "<!DOCTYPE html>\n"
        '<html lang="en"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width, initial-scale=1">'
        f"<title>{esc(basics['name'])} &mdash; Resume</title>"
        f"<style>{css}</style></head><body>"
        f"<header>{''.join(head)}</header>"
        f"{''.join(sections)}"
        "</body></html>"
    )


def build(src, out, theme="slate"):
    data = load(src)
    html_text = render(data, theme=theme)
    with open(out, "w", encoding="utf-8") as fh:
        fh.write(html_text)
    return out
