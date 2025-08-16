import pytest
from pelican.readers import HTMLReader
from pelican.settings import DEFAULT_CONFIG


build_tag_data = [
    ("meta", [("name", "description")], True, '<meta name="description" />'),
    ("body", [("name", None)], False, "<body name>"),
    ("title", [], True, "<title />"),
    ("", [("name", "description")], False, '< name="description">'),
    ("", [("name", None)], True,  "< name />"),
    ("", [], False, "<>"),
    ("123", [("name", "de$cription")], True, '<123 name="de$cription" />'),
    ("!!", [("name", None)], False, "<!! name>"),
    ("$$$", None, True, TypeError)
]

read_data = [
    ("./data/T1.html", ('TEST HTML', {})),
    ("./data/T2.html", ('', {})),
    ("./data/T3.html", FileNotFoundError),
]


@pytest.fixture(name="html_reader")
def html_reader_obj():
    settings = DEFAULT_CONFIG
    yield HTMLReader(settings)


@pytest.fixture(name="html_parser")
def html_parser_obj():
    settings = DEFAULT_CONFIG
    filename = ""
    yield HTMLReader._HTMLParser(settings, filename)


@pytest.mark.parametrize("tag, attrs, close_tag, expected", build_tag_data, ids=["T1", "T2", "T3", "T4",
                                                                                 "T5", "T6", "T7", "T8", "T9"])
def test_parser_build_tag(tag, attrs, close_tag, expected, html_parser):
    """
    Test HTMLReader.HTMLParser build tag functionality
    """
    try:
        output = html_parser.build_tag(tag, attrs, close_tag)
        assert output == expected
    except TypeError:
        # Error Case
        assert expected == TypeError


@pytest.mark.parametrize("filename, expected", read_data, ids=["T1", "T2", "T3"])
def test_parser_read(filename, expected, html_reader):
    """
    Test HTMLReader read html functionality
    """
    try:
        output = html_reader.read(filename)
        assert output == expected
    except FileNotFoundError:
        # Error Case
        assert expected == FileNotFoundError
