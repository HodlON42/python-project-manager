"""Test command line interface."""

import pytest
from python_project_manager.main import main
from python_project_manager.security import SecurityError, ValidationError
import sys
from unittest.mock import patch
import logging


def test_main_no_args():
    """Test main function with no arguments."""
    with patch(
        "python_project_manager.security.execute_command"
    ) as mock_execute, patch.object(sys, "argv", ["pysetup"]):
        mock_execute.return_value = ""
        main()


def test_main_with_repo(temp_dir):
    """Test main function with repository name."""
    with patch(
        "python_project_manager.security.execute_command"
    ) as mock_execute, patch.object(
        sys, "argv", ["pysetup", "--repo-name", "test-repo"]
    ):
        mock_execute.return_value = ""
        try:
            main()
        except SystemExit as e:
            assert e.code == 0  # On s'assure que le programme s'est terminé avec succès
        assert (temp_dir / ".gitignore").exists()


def test_main_force_venv(temp_dir):
    """Test main function with force venv flag."""
    with patch(
        "python_project_manager.security.execute_command"
    ) as mock_execute, patch.object(sys, "argv", ["pysetup", "--force-venv"]):
        mock_execute.return_value = ""
        main()


def test_main_all_options(temp_dir):
    """Test main function with all options."""
    with patch(
        "python_project_manager.security.execute_command"
    ) as mock_execute, patch.object(
        sys, "argv", ["pysetup", "--repo-name", "test-repo", "--force-venv"]
    ):
        mock_execute.return_value = ""
        main()
        assert (temp_dir / ".gitignore").exists()


@pytest.fixture
def mock_venv_active(monkeypatch):
    """Mock an active virtual environment."""
    monkeypatch.setattr(sys, "prefix", "/fake/venv/prefix")
    monkeypatch.setattr(sys, "base_prefix", "/fake/base/prefix")
    return True


def test_main_with_active_venv(mock_venv_active, capsys):
    """Test main function when virtual environment is already active."""
    with patch.object(sys, "argv", ["pysetup"]), patch(
        "python_project_manager.security.execute_command"
    ) as mock_execute:
        mock_execute.return_value = ""
        main()
        captured = capsys.readouterr()
        assert "Virtual environment already activated" in captured.out


def test_main_with_requirements(temp_dir, requirements_file):
    """Test main function with requirements.txt present."""
    with patch(
        "python_project_manager.security.execute_command"
    ) as mock_execute, patch.object(sys, "argv", ["pysetup"]):
        mock_execute.return_value = ""
        main()
        assert requirements_file.exists()


def test_main_security_error(capsys):
    """Test main function handling of SecurityError."""
    with patch(
        "python_project_manager.main.setup_venv"
    ) as mock_setup_venv, patch.object(sys, "argv", ["pysetup"]), patch.object(
        sys, "prefix", "/fake/prefix"
    ), patch.object(
        sys, "base_prefix", "/fake/prefix"
    ):
        mock_setup_venv.side_effect = SecurityError("Test security error")
        with pytest.raises(SystemExit) as exit_info:
            main()
        assert exit_info.value.code == 1  # Vérification du code de sortie
        captured = capsys.readouterr()
        assert "❌ Security error: Test security error" in captured.out


def test_main_validation_error(capsys):
    """Test main function handling of ValidationError."""
    with patch(
        "python_project_manager.main.setup_venv"
    ) as mock_setup_venv, patch.object(sys, "argv", ["pysetup"]), patch.object(
        sys, "prefix", "/fake/prefix"
    ), patch.object(
        sys, "base_prefix", "/fake/prefix"
    ):
        mock_setup_venv.side_effect = ValidationError("Test validation error")
        with pytest.raises(SystemExit) as exit_info:
            main()
        assert exit_info.value.code == 1  # Vérification du code de sortie
        captured = capsys.readouterr()
        assert "❌ Security error: Test validation error" in captured.out


def test_main_unexpected_error(caplog, capsys):
    """Test main function handling of unexpected errors."""
    with patch(
        "python_project_manager.main.setup_venv"
    ) as mock_setup_venv, patch.object(sys, "argv", ["pysetup"]), patch.object(
        sys, "prefix", "/fake/prefix"
    ), patch.object(
        sys, "base_prefix", "/fake/prefix"
    ):
        mock_setup_venv.side_effect = ValueError("Test unexpected error")
        with pytest.raises(SystemExit) as exit_info:
            main()
        assert exit_info.value.code == 1  # Vérification du code de sortie
        captured = capsys.readouterr()
        assert "❌ Unexpected error: Test unexpected error" in captured.out
