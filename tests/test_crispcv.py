import os
import tempfile
import unittest

from crispcv.__main__ import SAMPLE, main, preview_html
from crispcv.builder import ResumeError, load, render, validate
from crispcv.themes import get_theme, theme_names

DATA = {
    "basics": {
        "name": "Jordan Avery",
        "label": "Senior Product Designer",
        "email": "jordan@example.com",
        "website": "jordanavery.example",
        "summary": "Designs things & ships them.",
    },
    "work": [
        {
            "company": "Northwind Labs",
            "role": "Senior Designer",
            "start": "2021",
            "end": "Present",
            "highlights": ["Grew activation 12% -> 19%", "Led a team of <4> designers"],
        }
    ],
    "education": [{"school": "State University", "degree": "B.F.A. Design"}],
    "skills": {"groups": [{"name": "Design", "items": ["Research", "Prototyping"]}]},
}


class ValidateTests(unittest.TestCase):
    def test_missing_basics_rejected(self):
        with self.assertRaises(ResumeError):
            validate({})

    def test_missing_name_rejected(self):
        with self.assertRaises(ResumeError):
            validate({"basics": {"label": "Engineer"}})

    def test_valid_data_passes(self):
        validate(DATA)


class RenderTests(unittest.TestCase):
    def test_contains_all_sections(self):
        out = render(DATA)
        for text in (
            "Jordan Avery",
            "Experience",
            "Education",
            "Skills",
            "Northwind Labs",
            "State University",
            "Prototyping",
        ):
            self.assertIn(text, out)

    def test_empty_sections_skipped(self):
        out = render({"basics": {"name": "Sam"}})
        for text in ("Experience", "Education", "Skills", "Projects"):
            self.assertNotIn(text, out)

    def test_html_is_escaped(self):
        out = render(DATA)
        self.assertIn("&lt;4&gt;", out)
        self.assertIn("Designs things &amp; ships them.", out)
        self.assertNotIn("<4>", out)

    def test_website_gets_https_scheme(self):
        out = render(DATA)
        self.assertIn('href="https://jordanavery.example"', out)

    def test_all_themes_render(self):
        for name in theme_names():
            self.assertIn("<!DOCTYPE html>", render(DATA, theme=name))

    def test_unknown_theme_raises(self):
        with self.assertRaises(KeyError):
            get_theme("neon")


class FileTests(unittest.TestCase):
    def test_sample_round_trips(self):
        with tempfile.TemporaryDirectory() as tmp:
            src = os.path.join(tmp, "resume.toml")
            with open(src, "w", encoding="utf-8") as fh:
                fh.write(SAMPLE)
            data = load(src)
            self.assertEqual(data["basics"]["name"], "Your Name")
            self.assertEqual(len(data["work"]), 1)

    def test_cli_build_writes_html(self):
        with tempfile.TemporaryDirectory() as tmp:
            src = os.path.join(tmp, "resume.toml")
            out = os.path.join(tmp, "resume.html")
            self.assertEqual(main(["init", src]), 0)
            self.assertEqual(main(["build", src, "-o", out, "-t", "ivory"]), 0)
            with open(out, encoding="utf-8") as fh:
                self.assertIn("Your Name", fh.read())

    def test_init_refuses_overwrite(self):
        with tempfile.TemporaryDirectory() as tmp:
            src = os.path.join(tmp, "resume.toml")
            self.assertEqual(main(["init", src]), 0)
            self.assertEqual(main(["init", src]), 1)

    def test_build_missing_file_errors(self):
        self.assertEqual(main(["build", "/nonexistent/resume.toml"]), 1)

    def test_preview_contains_logo_and_toolbar(self):
        out = preview_html(DATA, "slate")
        self.assertIn("crispcv logo", out)
        self.assertIn("Print / PDF", out)


if __name__ == "__main__":
    unittest.main()
