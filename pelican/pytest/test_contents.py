import pytest
from ..contents import Content, Author
from ..settings import DEFAULT_CONFIG
from jinja2.utils import generate_lorem_ipsum

# generate 3 test paragraphs, each enclosed with <p>
# save the first paragraph separately for testing the summary generation algorithm
# NOTE: these values are nondeterministic between test runs
TEST_CONTENT_FIRST_PARAGRAPH = str(generate_lorem_ipsum(n=1))
TEST_CONTENT_REMAINING_PARAGRAPHS = str(generate_lorem_ipsum(n=2))
TEST_CONTENT = TEST_CONTENT_FIRST_PARAGRAPH + TEST_CONTENT_REMAINING_PARAGRAPHS
TEST_SUMMARY = generate_lorem_ipsum(n=1, html=False)

graph_paths = [[],[],[]]

@pytest.fixture(name="content_obj")
def content_obj():
    settings = DEFAULT_CONFIG
    content = TEST_CONTENT
    metadata = {"summary": TEST_SUMMARY,
                "title": "foo bar",
                "author": Author("Blogger", DEFAULT_CONFIG)}
    source_path = "/path/to/file/foo.ext"
    context = {"localsiteurl": "",
                "generated_content": {},
                "static_content": {},
                "static_links": set()}
    yield Content(content, metadata, settings, source_path, context)


@pytest.mark.parametrize("path", graph_paths, ids=["T1", "T2", "T3"])
def test_get_static_links(path, content_obj):
    """
    """
    content_obj._content = r'<p>Here is an <a href="link://static/images/photo.jpg">image</a>.</p>'
    content_obj.get_static_links()
