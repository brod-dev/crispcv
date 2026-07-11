"""Command line interface for crispcv."""

import argparse
import sys

from . import __version__
from .builder import ResumeError, build, load, render
from .logo import LOGO_SVG
from .themes import theme_names

SAMPLE = """[basics]
name = "Your Name"
label = "Your Title"
email = "you@example.com"
phone = "+1 (555) 000-0000"
location = "City, ST"
website = "yoursite.example"
summary = "Two or three sentences about what you do and what you are looking for."

[[work]]
company = "Company Name"
role = "Your Role"
start = "2022"
end = "Present"
highlights = [
  "Something you shipped, with a number attached.",
  "Something you improved, and by how much.",
]

[[education]]
school = "University Name"
degree = "B.S. Something"
start = "2014"
end = "2018"

[skills]
groups = [
  { name = "Core", items = ["Skill one", "Skill two", "Skill three"] },
  { name = "Tools", items = ["Tool one", "Tool two"] },
]
"""

PREVIEW_CHROME = """<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><title>crispcv preview</title>
<style>
body {{ margin: 0; background: #e2e8f0; font-family: -apple-system, 'Segoe UI', sans-serif; }}
.bar {{ display: flex; align-items: center; gap: 10px; padding: 10px 20px;
       background: #0f172a; color: #f8fafc; position: sticky; top: 0; }}
.bar .name {{ font-weight: 700; letter-spacing: -0.01em; }}
.bar .meta {{ color: #94a3b8; font-size: 0.85rem; margin-left: auto; }}
.bar button {{ background: #2563eb; color: #fff; border: 0; border-radius: 6px;
              padding: 6px 14px; font-size: 0.85rem; cursor: pointer; }}
.page {{ max-width: 820px; margin: 28px auto; background: #fff; border-radius: 8px;
        box-shadow: 0 10px 30px rgba(15,23,42,.15); overflow: hidden; }}
iframe {{ width: 100%; height: calc(100vh - 120px); border: 0; display: block; }}
@media print {{ .bar {{ display: none; }} .page {{ margin: 0; box-shadow: none; }} }}
</style></head><body>
<div class="bar">{logo}<span class="name">crispcv</span>
<span class="meta">theme: {theme} &middot; v{version}</span>
<button onclick="document.querySelector('iframe').contentWindow.print()">Print / PDF</button></div>
<div class="page"><iframe srcdoc="{srcdoc}"></iframe></div>
</body></html>"""


def preview_html(data, theme):
    inner = render(data, theme=theme)
    srcdoc = inner.replace("&", "&amp;").replace('"', "&quot;")
    return PREVIEW_CHROME.format(
        logo=LOGO_SVG, theme=theme, version=__version__, srcdoc=srcdoc
    )


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="crispcv",
        description="Turn one TOML file into a polished, print-ready resume.",
    )
    parser.add_argument("--version", action="version", version=f"crispcv {__version__}")
    sub = parser.add_subparsers(dest="command", required=True)

    p_init = sub.add_parser("init", help="write a starter resume.toml")
    p_init.add_argument("path", nargs="?", default="resume.toml")

    p_build = sub.add_parser("build", help="render resume TOML to HTML")
    p_build.add_argument("src")
    p_build.add_argument("-t", "--theme", default="slate", choices=theme_names())
    p_build.add_argument("-o", "--out", default="resume.html")

    p_prev = sub.add_parser("preview", help="render with a preview toolbar")
    p_prev.add_argument("src")
    p_prev.add_argument("-t", "--theme", default="slate", choices=theme_names())
    p_prev.add_argument("-o", "--out", default="preview.html")

    sub.add_parser("themes", help="list available themes")

    args = parser.parse_args(argv)

    try:
        if args.command == "init":
            with open(args.path, "x", encoding="utf-8") as fh:
                fh.write(SAMPLE)
            print(f"wrote {args.path} -- edit it, then run: crispcv build {args.path}")
        elif args.command == "build":
            out = build(args.src, args.out, theme=args.theme)
            print(
                f"wrote {out} (theme: {args.theme}) -- open it in a browser, print to PDF"
            )
        elif args.command == "preview":
            data = load(args.src)
            with open(args.out, "w", encoding="utf-8") as fh:
                fh.write(preview_html(data, args.theme))
            print(f"wrote {args.out} -- open it in a browser")
        elif args.command == "themes":
            for name in theme_names():
                print(name)
    except FileExistsError:
        print(f"error: {args.path} already exists, not overwriting", file=sys.stderr)
        return 1
    except FileNotFoundError as err:
        print(f"error: {err.filename} not found", file=sys.stderr)
        return 1
    except ResumeError as err:
        print(f"error: {err}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
