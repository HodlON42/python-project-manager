"""Utility functions for python project manager."""
from typing import Optional
from pathlib import Path
import shutil
import sys

from .config import config
from .security import SecurityError, execute_command

def run_command(command: str, cwd: Optional[Path] = None) -> Optional[str]:
    """
    Execute a shell command safely.
    
    Args:
        command: Command string to execute
        cwd: Working directory for command execution
        
    Returns:
        Optional[str]: Command output if successful
    """
    cmd_list = command.split()
    return execute_command(cmd_list, cwd)

def setup_venv(force: bool = False) -> None:
    """
    Set up Python virtual environment.

    Args:
        force: If True, recreate the virtual environment if it exists
        
    Raises:
        SecurityError: If command execution fails
    """
    venv_path = Path(config.venv_dir)
    
    if venv_path.exists() and force:
        print("Removing existing virtual environment...")
        shutil.rmtree(venv_path)
    
    # Modifier cette condition pour qu'elle s'exécute aussi après un force=True
    if force or not venv_path.exists():  # Changement ici
        print("Creating virtual environment...")
        command = ['python', '-m', 'venv', config.venv_dir]
        if execute_command(command, None) is None:
            raise SecurityError("Failed to create virtual environment")
    
    activate_script = f'{config.venv_dir}\\Scripts\\activate.bat' if sys.platform == 'win32' else f'source {config.venv_dir}/bin/activate'
    print(f"\nTo activate the virtual environment, run:\n{activate_script}")

def setup_git(repo_name: str, gitignore_content: str) -> None:
    """
    Initialize git repository and configure remote origin.
    
    Args:
        repo_name: Name of the repository
        gitignore_content: Content to write to the .gitignore file
        
    Raises:
        ValueError: If repository name is invalid
    """
    if not repo_name or not repo_name.strip():
        raise ValueError("Repository name cannot be empty")
    if '/' in repo_name:
        raise ValueError("Repository name cannot contain slashes")
    if not all(c.isalnum() or c in '-_.' for c in repo_name):
        raise ValueError("Repository name can only contain alphanumeric characters, hyphens, underscores, and dots")
    
    if not Path('.git').exists():
        execute_command(['git', 'init'], None)
        execute_command(['git', 'branch', '-M', config.default_branch], None)
        
        Path('.gitignore').write_text(gitignore_content)
        
        remote_url = f"{config.git_host_url}/{repo_name}.git"
        execute_command(['git', 'remote', 'add', 'origin', remote_url], None)
        
        print(f"\nGit repository initialized with remote: {remote_url}")
        print("Don't forget to create the repository on your Git host before pushing")

def install_dependencies() -> None:
    """Install dependencies from requirements.txt if it exists."""
    requirements_path = Path(config.requirements_file)
    if requirements_path.exists():
        print("\nInstalling dependencies...")
        execute_command(['pip', 'install', '-r', config.requirements_file], None)