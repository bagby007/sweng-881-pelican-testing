import pytest
from datetime import datetime, timezone
from pelican.utils import (
    posixize_path,
    sanitised_join,
    strftime as pelican_strftime,
    get_date as pelican_get_date,
)

@pytest.mark.parametrize("input_path, expected", [
    ("/usr/local/bin", "/usr/local/bin"),                   # TC1: POSIX absolute
    (r"C:/Users\user/project", "C:/Users/user/project"),    # TC2: mixed separators
    ("", ""),                                               # TC3: empty string
])
def test_posixize_path(input_path, expected):
    assert posixize_path(input_path) == expected

@pytest.mark.parametrize("base, parts, expected, error", [
    ("/home/user/site", ["content", "blog"],
     "/home/user/site/content/blog", None),             # TC1: normal join
    ("/home/user/site", ["..", "etc"],
     None, RuntimeError),                               # TC2: traversal
    ("/home/user/site", ["/etc/passwd"],
     None, RuntimeError),                               # TC3: absolute override
])
def test_sanitised_join(base, parts, expected, error):
    if error:
        with pytest.raises(error):
            sanitised_join(base, *parts)
    else:
        assert sanitised_join(base, *parts) == expected

@pytest.mark.parametrize("dt, fmt, expected, error", [
    (datetime(2021, 8, 15, 12, 34, 0), "%Y-%m-%d",
     "2021-08-15", None),                            # TC1: standard
    (datetime(2020, 2, 29, 0, 0, 0), "%-m/%-d/%Y",
     "2/29/2020", None),                             # TC2: strip-zero
    (datetime(2021, 8, 15, 12, 34, 0), "%Q-%W",
     None, ValueError),                              # TC3: invalid directive
])
def test_pelican_strftime(dt, fmt, expected, error):
    if error:
        with pytest.raises(error):
            pelican_strftime(dt, fmt)
    else:
        assert pelican_strftime(dt, fmt) == expected

@pytest.mark.parametrize("input_str, expected, error", [
    ("2021-08-15T14:30:00Z",
     datetime(2021, 8, 15, 14, 30, 0, tzinfo=timezone.utc), None),  # TC1: ISO + Z
    ("March 3, 2020 14:00",
     datetime(2020, 3, 3, 14, 0, 0), None),                         # TC2: natural language
    ("Feb 30 2021", None, ValueError),                              # TC3: invalid date
])
def test_pelican_get_date(input_str, expected, error):
    if error:
        with pytest.raises(error):
            pelican_get_date(input_str)
    else:
        result = pelican_get_date(input_str)
        assert result.isoformat() == expected.isoformat()