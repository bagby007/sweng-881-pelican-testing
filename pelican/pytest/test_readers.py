import pytest
from readers import HTMLReader

class TestHTMLReader(HTMLReader):

    class TestHTMLParser(self._HTMLParser):
        
        ids = ["T1", "T2",
               "T3", "T4",
               "T5", "T6",
               "T7", "T8",
               "T9"]

        start_tag_data = [
            ("meta", [("name", "description")], ""),
            ("body", [("name", None)], ""),
            ("title", [], ""),
            ("", [("name", "description")], ""),
            ("", [("name", None)], ""),
            ("", [], ""),
            ("123", [("name", "de$cription")], ""),
            ("!!", [("name", None)], ""),
            ("$$$", [], "")
        ]

        build_tag_data = [
            ("meta", [("name", "description")], True, ""),
            ("body", [("name", None)], False, ""),
            ("title", [], True, ""),
            ("", [("name", "description")], False, ""),
            ("", [("name", None)], True,  ""),
            ("", [], False, ""),
            ("123", [("name", "de$cription")], True, ""),
            ("!!", [("name", None)], False, ""),
            ("$$$", [], True, "")
        ]

        pytest.mark.parametrize("tag, attrs, expected", start_tag_data, ids=ids)
        def test_handle_start_tag(tag, attrs, expected):
            """
            """
            pass
    
        pytest.mark.parametrize("tag, attrs, close_tag, expected", build_tag_data, ids=ids)
        def test_build_tag(tag, attrs, close_tag, expected):
            """
            """
            pass

