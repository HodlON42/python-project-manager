"""Main module for python-project-manager command line tool."""
import argparse
import sys
import logging

from .config import load_template
from .security import SecurityError, ValidationError
from .utils import setup_venv, setup_git, install_dependencies

def main():
    """Main entry point for the python-project-manager command line tool."""
    try:
        parser = argparse.ArgumentParser(
            description='Initialize and manage Python projects with virtual environments and Git integration'
        )
        parser.add_argument(
            '--repo-name',
            help='Repository name for the Git remote (alphanumeric, hyphens, underscores, and dots only)'
        )
        parser.add_argument('--force-venv', action='store_true',
                           help='Force virtual environment recreation')
        parser.add_argument('--verbose', action='store_true',
                           help='Enable verbose logging')
        args = parser.parse_args()

        # Setup logging
        logging.basicConfig(
            level=logging.DEBUG if args.verbose else logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )

        # Check if we're in a virtual environment
        in_venv = sys.prefix != sys.base_prefix
        if not in_venv:
            setup_venv(args.force_venv)
        else:
            print("Virtual environment already activated")

        if args.repo_name:
            gitignore_content = load_template('gitignore.template')
            setup_git(args.repo_name, gitignore_content)
        
        install_dependencies()
        
    except (SecurityError, ValidationError) as e:
        print(f"❌ Security error: {str(e)}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
        logging.exception("Unexpected error occurred")
        sys.exit(1)

if __name__ == '__main__':
    main()