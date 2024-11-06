"""Common test fixtures and utilities."""
import os
import pytest
from pathlib import Path
import tempfile
import shutil

@pytest.fixture
def temp_dir():
    """Create a temporary directory for tests."""
    with tempfile.TemporaryDirectory() as tmpdir:
        original_dir = os.getcwd()
        os.chdir(tmpdir)
        yield Path(tmpdir)
        os.chdir(original_dir)

@pytest.fixture
def mock_env(monkeypatch):
    """Mock environment variables for testing."""
    env_vars = {
        "GIT_HOST_URL": "https://test.git",
        "DEFAULT_BRANCH": "test-branch",
        "VENV_DIR": "test-venv",
        "REQUIREMENTS_FILE": "test-requirements.txt"
    }
    for key, value in env_vars.items():
        monkeypatch.setenv(key, value)
    return env_vars

@pytest.fixture
def requirements_file(temp_dir):
    """Create a dummy requirements.txt file."""
    content = "pytest>=7.0.0\nrequests>=2.0.0"
    req_file = temp_dir / "requirements.txt"
    req_file.write_text(content)
    return req_file