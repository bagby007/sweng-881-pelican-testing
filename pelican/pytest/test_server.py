import pytest
from io import BytesIO
from pelican.server import ComplexHTTPRequestHandler

server_data = [
    ("/test/normal/path", "base", "base/test/normal/path"),
    ("C:/Test\\alternative/path", "", "C:/Test\\alternative/path"),
    ("", 10, 10)]

original_data = [
    ("/test/normal/path", "base", "base/test/normal/path"),
    ("C:/Test\\alternative/path", "", "C:/Test\\alternative/path"),
    ("", 10, 10)]

class MockRequest:
    def makefile(self, *args, **kwargs):
        return BytesIO(b"")

class MockServer:
    pass

@pytest.fixture(name="html_handler")
def html_handler_obj():
    yield ComplexHTTPRequestHandler(
            MockRequest(),
            ("0.0.0.0", 8888),
            MockServer())

@pytest.mark.parametrize("path, prefix, expected", server_data, ids=["T1", "T2", "T3"])
def test_translate_path(path, prefix, expected, html_handler):
    """
    """
    html_handler.base_path = prefix
    output = html_handler.translate_path(path)
    assert output == expected
