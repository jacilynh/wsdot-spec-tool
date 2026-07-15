"""The build-time transforms that shape the app's data: chunking and prose filtering.

These are small, but they feed the Ask-the-Specs retrieval corpus, so a regression here
would put contents-listing junk in front of the model or split text mid-line.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "pipeline"))

from build_app_data import chunk_text, is_prose


class TestChunkText:
    def test_short_text_is_one_chunk(self):
        assert chunk_text("The Contractor shall comply.") == ["The Contractor shall comply."]

    def test_splits_long_text_on_line_boundaries(self):
        # Three ~30-char lines with a 50-char limit must not merge into one chunk, and no
        # chunk may exceed the limit by a whole line.
        text = "\n".join(["a" * 30, "b" * 30, "c" * 30])
        chunks = chunk_text(text, limit=50)
        assert len(chunks) >= 2
        assert all("\n" not in c for c in chunks)

    def test_never_splits_a_single_line(self):
        line = "word " * 40
        assert chunk_text(line.strip(), limit=50) == [line.strip()]


class TestIsProse:
    def test_accepts_ordinary_specification_text(self):
        assert is_prose("The Contractor shall submit a Type 2 Working Drawing.")

    def test_rejects_a_contents_listing_dot_leader_run(self):
        assert not is_prose("1-01.1 General . . . . . . . . . . . . . . . . 1-1")

    def test_rejects_text_that_is_mostly_punctuation(self):
        assert not is_prose(".................................................")
