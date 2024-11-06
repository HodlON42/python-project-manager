"""Configuration module for python project manager."""
import os
from pathlib import Path
from dataclasses import dataclass
from typing import Optional

@dataclass
class Config:
    """Configuration settings for the project."""
    
    git_host_url: str
    default_branch: str = "main"
    venv_dir: str = ".venv"
    requirements_file: str = "requirements.txt"
    
    @classmethod
    def from_env(cls) -> 'Config':
        """Create configuration from environment variables."""
        return cls(
            git_host_url=os.getenv("GIT_HOST_URL", "https://github.com"),
            default_branch=os.getenv("DEFAULT_BRANCH", "main"),
            venv_dir=os.getenv("VENV_DIR", ".venv"),
            requirements_file=os.getenv("REQUIREMENTS_FILE", "requirements.txt")
        )

# Project paths
PROJECT_ROOT = Path(__file__).parent
TEMPLATES_DIR = PROJECT_ROOT / "templates"

# Global configuration instance
config = Config.from_env()

def load_template(template_name: str) -> str:
    """
    Load a template file from the templates directory.

    Args:
        template_name: Name of the template file

    Returns:
        str: Content of the template file
    """
    template_path = TEMPLATES_DIR / template_name
    if not template_path.exists():
        raise FileNotFoundError(f"Template {template_name} not found")
    
    return template_path.read_text()