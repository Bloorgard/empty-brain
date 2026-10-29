import tempfile
import unittest
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path

spec = spec_from_file_location("site_links", Path(__file__).with_name("check-site-links.py"))
checker = module_from_spec(spec)
spec.loader.exec_module(checker)


class SiteLinksTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.output = Path(self.temp.name)
        self.write("index.html", '<h1 id="home">Home</h1>')
        self.write("tags/туториал.html", '<h1 id="tag">Tag</h1>')

    def write(self, name, content):
        path = self.output / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")

    def check(self):
        return checker.check_site(self.output, "https://example.com/brain")

    def test_encoded_tags_anchors_assets_and_project_home(self):
        self.write("static/icon.png", "image")
        self.write("404.html", '<a href="/brain">Home</a>')
        self.write("AI/note.html", '''
            <a href="../tags/%D1%82%D1%83%D1%82%D0%BE%D1%80%D0%B8%D0%B0%D0%BB?x=1#tag">Tag</a>
            <a href="https://example.com/brain/#home">Home</a>
            <a href="https://example.com/another-project/">Other project</a>
            <a href="https://external.example/missing">External</a>
            <a href="mailto:hello@example.com">Mail</a>
            <img src="../static/icon.png">
        ''')
        self.assertEqual(self.check(), [])

    def test_missing_folder_tag_and_double_root_prefix(self):
        self.write("AI/index.html", '<a href="../tags/folder">Folder</a>')
        self.write("AI/audio/note.html", '<a href="../../../tags/туториал">Tag</a>')
        errors = self.check()
        self.assertEqual(len(errors), 2)
        self.assertEqual({error[2] for error in errors}, {
            "target file not found", "link escapes the site base path",
        })

    def test_folder_index_and_missing_anchor(self):
        self.write("AI/index.html", '<h1 id="intro">Intro</h1>')
        self.write("index.html", '<a href="AI/#intro">OK</a><a href="AI/#missing">Bad</a>')
        self.assertEqual(self.check(), [("index.html", "AI/#missing", "anchor not found")])

    def test_root_hosting_and_empty_build(self):
        self.write("404.html", '<a href="/">Home</a>')
        self.assertEqual(checker.check_site(self.output, "https://example.com"), [])
        self.assertTrue(checker.check_site(self.output / "empty", "https://example.com"))


if __name__ == "__main__":
    unittest.main()
