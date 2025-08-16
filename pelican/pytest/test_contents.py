import os
import types
import pytest
from pelican.contents import Content, Author
from pelican.settings import DEFAULT_CONFIG

@pytest.fixture(name="content_obj")
def _content_obj():
    settings = DEFAULT_CONFIG.copy()
    settings["INTRASITE_LINK_REGEX"] = r"{(?P<what>\w+)}" 
    settings["PATH"] = "/site"

    content = ""
    metadata = {"title": "Post", "author": Author("Blogger", DEFAULT_CONFIG)}
    source_path = "/site/blog/post.md"
    context = {
        "localsiteurl": "",
        "generated_content": {},
        "static_content": {},
        "static_links": set(),
    }

    obj = Content(content, metadata, settings, source_path, context)

    def _fake_grsp(self, source_path=None):
        return f"JOINED:{source_path}"
    obj.get_relative_source_path = types.MethodType(_fake_grsp, obj)

    return obj

CASES = [
    ("T1",  True,  True,  "static", "/img/pic.png"),
    ("T2",  True,  False, "static", "img/pic.png"),
    ("T3",   False, True,  "other",  "/x/ignored.png"),
    ("T4",   False, False, "other",  "ignored.png"),
]

@pytest.mark.parametrize(
    "case_id, allowed, starts_slash, what, path",
    CASES,
    ids=[c[0] for c in CASES],
)
def test_get_static_links(content_obj, case_id, allowed, starts_slash, what, path):
    content_obj._content = f'<a href="{{{what}}}{path}">link</a>'

    result = content_obj.get_static_links()

    if not allowed:
        assert result == set()
        return

    if starts_slash:
        expected = path.lstrip("/")
    else:
        expected = f"JOINED:{os.path.join(content_obj.relative_dir, path)}"

    expected = expected.replace("%20", " ")

    assert result == {expected}
