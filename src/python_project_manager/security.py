"""Security related utilities and constants for the project manager."""
from typing import List, Dict, Optional
from pathlib import Path
import re
import subprocess
import logging
from dataclasses import dataclass

logger = logging.getLogger(__name__)

class SecurityError(Exception):
    """Base exception for security related errors."""
    pass

class CommandNotAllowedError(SecurityError):
    """Raised when trying to execute a forbidden command."""
    pass

class ValidationError(SecurityError):
    """Raised when input validation fails."""
    pass

@dataclass
class CommandConfig:
    """Configuration for allowed command."""
    allowed_args: List[str]
    requires_validation: bool = False
    validation_pattern: Optional[str] = None

# Define allowed commands and their configurations
ALLOWED_COMMANDS: Dict[str, CommandConfig] = {
    'echo': CommandConfig(  # Ajouter cette entrée
        allowed_args=['test'],
        requires_validation=False
    ),
    'git': CommandConfig(
        allowed_args=['init', 'branch', 'remote', 'add', 'origin', '-M'],
        requires_validation=True,
        validation_pattern=r'^[a-zA-Z0-9._@:/-]+$'
    ),
    'python': CommandConfig(
        allowed_args=['-m', 'venv'],
        requires_validation=True,
        validation_pattern=r'^[a-zA-Z0-9._-]+$'
    ),
    'pip': CommandConfig(
        allowed_args=['install', '-r'],
        requires_validation=True,
        validation_pattern=r'^[a-zA-Z0-9._-]+\.txt$'
    )
}

def validate_path(path: Path) -> Path:
    """
    Validate and normalize a path to prevent directory traversal.
    
    Args:
        path: Path to validate
        
    Returns:
        Path: Normalized absolute path
        
    Raises:
        ValidationError: If path validation fails
    """
    try:
        resolved_path = path.resolve(strict=False)  # Changed from True to False
        if not str(resolved_path).startswith(str(Path.cwd())):
            raise ValidationError("Path must be under current working directory")
        return resolved_path
    except Exception as e:
        raise ValidationError(f"Invalid path: {str(e)}")

def validate_command(command: List[str]) -> None:
    """
    Validate a command against the allowed commands configuration.
    
    Args:
        command: Command as list of strings
        
    Raises:
        CommandNotAllowedError: If command validation fails
    """
    if not command:
        raise CommandNotAllowedError("Empty command")
        
    program = command[0]
    if program not in ALLOWED_COMMANDS:
        raise CommandNotAllowedError(f"Program not allowed: {program}")
        
    config = ALLOWED_COMMANDS[program]
    
    # Validate arguments
    args = command[1:]

    if program == 'git':
        if args[:3] == ['remote', 'add', 'origin'] and len(args) == 4:
            url = args[3]
            # Nouvelle expression régulière pour valider l'URL
            url_pattern = r'^(https://|git@)[\w.@:/\-~]+\.git$'
            if not re.match(url_pattern, url):
                raise CommandNotAllowedError(f"Invalid git remote URL: {url}")
        else:
            for arg in args:
                if arg not in config.allowed_args:
                    if not config.requires_validation:
                        raise CommandNotAllowedError(f"Argument not allowed: {arg}")
                    elif config.validation_pattern and not re.match(config.validation_pattern, arg):
                        raise CommandNotAllowedError(f"Invalid argument format: {arg}")
    else:
        for arg in args:
            if arg not in config.allowed_args:
                if not config.requires_validation:
                    raise CommandNotAllowedError(f"Argument not allowed: {arg}")
                elif config.validation_pattern and not re.match(config.validation_pattern, arg):
                    raise CommandNotAllowedError(f"Invalid argument format: {arg}")

def execute_command(command: List[str], cwd: Optional[Path] = None) -> Optional[str]:
    """
    Safely execute a command after validation.
    
    Args:
        command: Command as list of strings
        cwd: Working directory for command execution
        
    Returns:
        Optional[str]: Command output if successful
        
    Raises:
        SecurityError: If command execution fails
    """
    try:
        # Validate command
        validate_command(command)
        
        # Validate working directory if provided
        if cwd:
            cwd = validate_path(cwd)
        
        # Execute command
        process = subprocess.run(
            command,
            cwd=cwd,
            shell=False,
            check=True,
            capture_output=True,
            text=True
        )
        
        logger.debug(f"Command executed successfully: {' '.join(command)}")
        return process.stdout.strip()
        
    except subprocess.CalledProcessError as e:
        logger.error(f"Command execution failed: {e.stderr}")
        raise SecurityError(f"Command execution failed: {e.stderr}")
    except Exception as e:
        logger.error(f"Security error: {str(e)}")
        raise SecurityError(str(e))