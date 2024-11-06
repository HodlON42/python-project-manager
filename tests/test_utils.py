"""Test utility functions."""
import pytest
from unittest.mock import patch
from pathlib import Path
from python_project_manager.utils import run_command, setup_venv, setup_git, install_dependencies
from python_project_manager.security import SecurityError

@patch('python_project_manager.utils.execute_command')
def test_run_command_success(mock_execute):
    """Test successful command execution."""
    expected_output = "test output"
    mock_execute.return_value = expected_output
    result = run_command("python -m venv test-venv")
    assert result == expected_output
    mock_execute.assert_called_once_with(['python', '-m', 'venv', 'test-venv'], None)

@patch('python_project_manager.utils.execute_command')
def test_run_command_failure(mock_execute):
    """Test failed command execution."""
    mock_execute.side_effect = SecurityError("Command not allowed")
    with pytest.raises(SecurityError):
        run_command("nonexistent-command")

@patch('python_project_manager.utils.execute_command')
@patch('shutil.rmtree')
@patch('pathlib.Path.exists')
def test_setup_venv(mock_exists, mock_rmtree, mock_execute, temp_dir):
    """Test virtual environment setup."""
    # Configure mocks
    mock_exists.return_value = False  # venv doesn't exist
    mock_execute.return_value = "Success"
    
    # Test initial setup
    setup_venv()
    
    # Check command was called with correct arguments
    mock_execute.assert_called_with(['python', '-m', 'venv', '.venv'], None)
    
    # Reset mocks for force recreation test
    mock_execute.reset_mock()
    mock_exists.return_value = True  # venv exists, then doesn't after removal
    
    # Test force recreation
    setup_venv(force=True)
    mock_rmtree.assert_called_once()
    mock_execute.assert_called_once_with(['python', '-m', 'venv', '.venv'], None)

@patch('python_project_manager.security.execute_command')
def test_setup_git(mock_execute, temp_dir):
    """Test git repository initialization."""
    mock_execute.return_value = ""
    gitignore_content = "# Test gitignore"
    setup_git("test-repo", gitignore_content)
    
    gitignore_path = temp_dir / ".gitignore"
    assert gitignore_path.exists()
    assert gitignore_path.read_text() == gitignore_content

def test_setup_git_invalid_name():
    """Test git repository initialization with invalid names."""
    with pytest.raises(ValueError, match="cannot be empty"):
        setup_git("", "content")
    
    with pytest.raises(ValueError, match="cannot contain slashes"):
        setup_git("invalid/name", "content")
    
    with pytest.raises(ValueError, match="can only contain"):
        setup_git("invalid#name", "content")

@pytest.mark.parametrize("command,error_message", [
    ("git init", "Git initialization failed"),
    ("git branch -M main", "Branch creation failed"),
    ("git remote add origin", "Remote addition failed"),
])
@patch('python_project_manager.security.execute_command')
def test_git_command_failures(mock_execute, command, error_message, temp_dir):
    """Test handling of git command failures."""
    def mock_command_execution(cmd, *args, **kwargs):
        cmd_str = ' '.join(cmd)
        if command in cmd_str:
            raise SecurityError(error_message)
        return "success"
    
    mock_execute.side_effect = mock_command_execution
    
    # Should not raise exception despite git command failures
    setup_git("test-repo", "# Test content")
    
    # Should still create .gitignore
    gitignore_path = temp_dir / ".gitignore"
    assert gitignore_path.exists()
    assert gitignore_path.read_text() == "# Test content"

def test_git_invalid_names():
    """Test git repository initialization with invalid names."""
    with pytest.raises(ValueError, match="Repository name cannot be empty"):
        setup_git("", "content")
    
    with pytest.raises(ValueError, match="Repository name cannot contain slashes"):
        setup_git("invalid/name", "content")
    
    with pytest.raises(ValueError, match="Repository name can only contain"):
        setup_git("invalid#name", "content")

@patch('python_project_manager.security.execute_command')
def test_install_dependencies(mock_execute, temp_dir, requirements_file):
    """Test dependencies installation."""
    mock_execute.return_value = ""
    install_dependencies()
    assert requirements_file.exists()