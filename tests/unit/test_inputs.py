"""Inputs test suite."""

from pathlib import Path

import pytest

from bda_svc import inputs

# ----------------------------------------------------------------------
# Test: Input Folder Validation (get_input_folder)
# ----------------------------------------------------------------------


def test_uses_command_line_path(tmp_path: Path) -> None:
    """If a valid path is passed as an argument, use it."""
    # tmp_path is a built-in pytest fixture that creates a temporary folder
    real_folder = tmp_path / "my_test_images"
    real_folder.mkdir()

    # Run the function with the string version of that path
    result = inputs.get_input_folder(str(real_folder))

    # Assert it returned the correct Path object
    assert result == real_folder


def test_uses_default_path_if_no_arg(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """If arg is None, it should use DEFAULT_INPUT_PATH constant."""
    default_folder = tmp_path / "default_images"
    default_folder.mkdir()

    # 'monkeypatch' lets us safely fake variables just for this test
    monkeypatch.setattr(inputs.constants, "DEFAULT_INPUT_PATH", str(default_folder))

    # Pass None to simulate no command line flag being used
    result = inputs.get_input_folder(None)

    assert result == default_folder


def test_exits_if_folder_missing() -> None:
    """If the folder doesn't exist, the program should SystemExit."""
    bad_path = "/this/path/definitely/does/not/exist"

    # bda_svc.app uses sys.exit(), so we must catch it or the test crashes
    with pytest.raises(SystemExit):
        inputs.get_input_folder(bad_path)


# ----------------------------------------------------------------------
# Test: File Discovery (get_input_paths)
# ----------------------------------------------------------------------


def test_get_input_paths_finds_images(tmp_path: Path) -> None:
    """It should find valid image extensions recursively."""
    # Setup: Create dummy files
    (tmp_path / "subfolder").mkdir()
    (tmp_path / "image1.png").touch()
    (tmp_path / "subfolder/image2.jpg").touch()
    (tmp_path / "ignore_me.txt").touch()
    files = inputs.get_input_paths(tmp_path)

    # Should find the 2 images, ignore the text file
    assert len(files) == 2
    # Convert paths to filenames for easier checking
    filenames = [f.name for f in files]
    assert "image1.png" in filenames
    assert "image2.jpg" in filenames


def test_get_input_paths_empty_exits(tmp_path: Path) -> None:
    """It should SystemExit if the folder has no valid images."""
    # Folder exists but is empty
    with pytest.raises(SystemExit):
        inputs.get_input_paths(tmp_path)


def test_get_input_paths_single_invalid_file(tmp_path):
    """Return SystemExit if folder path is actually a file of invalid extension."""
    # Setup: Create dummy file
    path_invalid_file = tmp_path / "ignore_me.txt"
    path_invalid_file.touch()

    with pytest.raises(SystemExit):
        inputs.get_input_paths(path_invalid_file)


def test_get_input_paths_single_valid_file(tmp_path):
    """Return SystemExit if folder path is actually a file of invalid extension."""
    # Setup: Create dummy file
    valid_filename = "image42.png"
    path_valid_file = tmp_path / valid_filename
    path_valid_file.touch()

    files = inputs.get_input_paths(path_valid_file)

    assert len(files) == 1
    assert valid_filename in files[0].name
