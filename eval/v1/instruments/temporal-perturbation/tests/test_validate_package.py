"""The zero-spend claim is checked, not asserted."""
import ast
import pathlib

import validate_package as V


def test_package_passes_its_own_checks():
    problems, scanned = V.run()
    assert scanned >= 6
    assert problems == [], problems


def test_a_network_import_would_be_caught(tmp_path):
    p = tmp_path / "leaky.py"
    p.write_text("import requests\n")
    bad = V.check_imports(p, ast.parse(p.read_text()))
    assert bad and "requests" in bad[0]


def test_a_provider_sdk_import_would_be_caught(tmp_path):
    p = tmp_path / "paid.py"
    p.write_text("from anthropic import Anthropic\n")
    assert V.check_imports(p, ast.parse(p.read_text()))


def test_subprocess_outside_the_allow_list_would_be_caught(tmp_path):
    p = tmp_path / "shelly.py"
    src = "import subprocess\nsubprocess.run(['ls'])\n"
    p.write_text(src)
    assert V.check_subprocess(p, src, ast.parse(src))


def test_an_unexpected_binary_lookup_would_be_caught():
    p = pathlib.Path("ingest_clips.py")
    src = "import shutil, subprocess\nshutil.which('curl')\n"
    bad = V.check_subprocess(p, src, ast.parse(src))
    assert bad and "curl" in bad[0]


def test_an_invented_pass_mark_would_be_caught(tmp_path):
    p = tmp_path / "gate.py"
    src = "MIN_RECALL = 0.9\n"
    assert V.check_thresholds(p, src)


def test_no_source_file_imports_a_provider_or_a_network_client():
    """The claim in plain terms: nothing in this package can reach off this
    machine, so nothing in it can cost money."""
    for f in V.python_files():
        tree = ast.parse(f.read_text(), filename=str(f))
        assert V.check_imports(f, tree) == []
