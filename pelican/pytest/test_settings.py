import os
import copy
import pytest

import pelican.settings as settings_mod
from pelican.settings import (
    read_settings,
    DEFAULT_CONFIG,
)

@pytest.fixture(autouse=True)
def reset_and_patch_defaults(monkeypatch):
    # Reset the global before/after each test
    settings_mod.PYGMENTS_RST_OPTIONS = None

    # Make a fresh copy of DEFAULT_CONFIG, then override:
    patched = copy.deepcopy(DEFAULT_CONFIG)
    # Ensure pages is empty so we know what to assert
    patched["PAGES"] = []
    monkeypatch.setattr(settings_mod, "DEFAULT_CONFIG", patched)

    # Stub configure_settings to be a no-op (avoid real content-dir checks)
    monkeypatch.setattr(settings_mod, "configure_settings", lambda s: s)

    yield
    settings_mod.PYGMENTS_RST_OPTIONS = None

def test_read_settings_no_path_deprecated(monkeypatch):
    # Stub deprecation handler to rename old_key → new_key
    def fake_handle(settings):
        return {"new_key": settings["old_key"]}
    monkeypatch.setattr(settings_mod, "handle_deprecated_settings", fake_handle)

    # Call without a path, with an override that includes 'old_key'
    result = read_settings(path=None, override={"old_key": "v"})

    # Deprecation applied
    assert result["new_key"] == "v"

    # Defaults merged (including our patched-empty 'PAGES')
    assert result["PAGES"] == []

    # Global PYGMENTS_RST_OPTIONS matches DEFAULT_CONFIG
    default_pygments = settings_mod.DEFAULT_CONFIG.get("PYGMENTS_RST_OPTIONS")
    assert settings_mod.PYGMENTS_RST_OPTIONS == default_pygments
    assert result["PYGMENTS_RST_OPTIONS"] == default_pygments

def test_read_settings_with_path_and_loops(monkeypatch, tmp_path):
    # Stub file-load to return empty dict
    monkeypatch.setattr(settings_mod, "get_settings_from_file", lambda p: {})

    # Stub get_settings_from_file to return our relative paths
    monkeypatch.setattr(
        settings_mod,
        "get_settings_from_file",
        lambda p: {
            "PATH": "rel/content",
            "PLUGIN_PATHS": ["rel/plugins"],
        },
    )

    # Stub filesystem checks
    monkeypatch.setattr(os.path, "exists", lambda p: True)
    monkeypatch.setattr(os.path, "isabs", lambda p: not p.startswith("rel"))

    # Execute
    config_path = tmp_path / "config.py"
    result = read_settings(path=str(config_path), override=None)

    # PATH should now be absolute
    base = os.path.dirname(str(config_path))
    expected = os.path.abspath(os.path.normpath(os.path.join(base, "rel/content")))
    assert result["PATH"] == expected

    # Each PLUGIN_PATHS entry is absolute
    for plugin in result["PLUGIN_PATHS"]:
        assert os.path.isabs(plugin)