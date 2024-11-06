"""Test configuration module functionality."""
import pytest
from pathlib import Path
from python_project_manager.config import Config, load_template, config

def test_config_defaults():
    """Test default configuration values."""
    config = Config.from_env()
    assert config.git_host_url == "https://github.com"
    assert config.default_branch == "main"
    assert config.venv_dir == ".venv"
    assert config.requirements_file == "requirements.txt"

def test_config_from_env(mock_env):
    """Test configuration from environment variables."""
    config = Config.from_env()
    assert config.git_host_url == mock_env["GIT_HOST_URL"]
    assert config.default_branch == mock_env["DEFAULT_BRANCH"]
    assert config.venv_dir == mock_env["VENV_DIR"]
    assert config.requirements_file == mock_env["REQUIREMENTS_FILE"]

def test_load_template():
    """Test template loading functionality."""
    template = load_template("gitignore.template")
    assert template, "Template should not be empty"
    assert "# Fichiers cache de Python" in template

def test_load_template_missing():
    """Test error handling for missing template."""
    with pytest.raises(FileNotFoundError):
        load_template("non_existent.template")

def test_config_invalid_template():
    """Test loading template from invalid path."""
    config.TEMPLATES_DIR = Path("/nonexistent")
    with pytest.raises(FileNotFoundError):
        load_template("any.template")