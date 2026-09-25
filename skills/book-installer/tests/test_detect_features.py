import importlib.util
import tempfile
import unittest
from pathlib import Path


SCRIPT_PATH = Path(__file__).parents[1] / "scripts" / "detect_features.py"
SPEC = importlib.util.spec_from_file_location("detect_features", SCRIPT_PATH)
detect_features = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(detect_features)


class FeatureDetectionTests(unittest.TestCase):
    def test_counts_flat_numbered_chapters_without_index(self):
        with tempfile.TemporaryDirectory() as directory:
            chapters = Path(directory)
            (chapters / "index.md").write_text("# Chapters\n", encoding="utf-8")
            (chapters / "01-introduction.md").write_text("# One\n", encoding="utf-8")
            (chapters / "02-method.md").write_text("# Two\n", encoding="utf-8")

            self.assertEqual(detect_features.count_chapters(chapters), 2)

    def test_prefers_directory_chapters_when_present(self):
        with tempfile.TemporaryDirectory() as directory:
            chapters = Path(directory)
            (chapters / "chapter-1").mkdir()
            (chapters / "chapter-2").mkdir()
            (chapters / "index.md").write_text("# Chapters\n", encoding="utf-8")

            self.assertEqual(detect_features.count_chapters(chapters), 2)

    def test_counts_only_runnable_microsims(self):
        with tempfile.TemporaryDirectory() as directory:
            sims = Path(directory)
            (sims / "working-sim").mkdir()
            (sims / "working-sim" / "main.html").write_text("<main></main>", encoding="utf-8")
            (sims / "shared").mkdir()
            (sims / "shared" / "microsim.js").write_text("", encoding="utf-8")

            self.assertEqual(detect_features.count_microsims(sims), 1)

    def test_detects_social_hook_and_learning_graph_explorer(self):
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            docs = project / "docs"
            graph = docs / "learning-graph"
            hook = project / "plugins" / "social_override.py"
            graph.mkdir(parents=True)
            hook.parent.mkdir()
            hook.write_text("", encoding="utf-8")
            (graph / "explorer.md").write_text("# Explorer\n", encoding="utf-8")
            (graph / "explorer.js").write_text("", encoding="utf-8")

            self.assertTrue(
                detect_features.has_social_media_cards(
                    project, [], ["plugins/social_override.py"]
                )
            )
            self.assertTrue(detect_features.has_graph_viewer(docs))


if __name__ == "__main__":
    unittest.main()
