# Python Project Manager

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![Coverage](https://img.shields.io/badge/coverage-100%25-brightgreen)
![License](https://img.shields.io/badge/license-AGPL-blue)

A command-line utility for initializing and managing Python projects.

## Features

- Virtual environment creation and management
- Git repository initialization with customizable .gitignore
- Remote Git repository configuration (GitHub, GitLab, etc.)
- Dependencies management

## Prerequisites

- Python 3.8 or higher
- Git installed and configured on your system
- Read/Write access to your remote Git repository (if using --repo-name)

## Installation

```bash
pip install python-project-manager
```

## Usage

Basic usage:
```bash
# Initialize a new project with Git repository
pysetup --repo-name my-project

# Force recreate virtual environment
pysetup --force-venv

# Both options together
pysetup --repo-name my-project --force-venv
```

### Detailed Usage Examples

#### Create a New Project with Virtual Environment

```bash
# Create a new project with virtual environment
pysetup

# View detailed output
pysetup --verbose
```

#### Configure Remote Git Repository

```bash
# GitHub (default)
pysetup --repo-name my-awesome-project

# GitLab
GIT_HOST_URL="https://gitlab.com" pysetup --repo-name my-awesome-project
```

#### Force Virtual Environment Recreation

Useful if your virtual environment is corrupted or you want to start fresh:
```bash
pysetup --force-venv
```

### Repository Naming Rules
Repository names can only contain:
- Alphanumeric characters (a-z, A-Z, 0-9)
- Hyphens (-)
- Underscores (_)
- Dots (.)

### Generated Project Structure

After running pysetup, your project will have the following structure:
```
my-project/
├── .gitignore        # Default Git configuration for Python
├── .venv/            # Python virtual environment
└── requirements.txt  # Dependencies file (if exists)
```

## Configuration

The tool can be configured using environment variables:

- `GIT_HOST_URL`: URL of your Git host (default: https://github.com)
- `DEFAULT_BRANCH`: Default Git branch name (default: main)
- `VENV_DIR`: Virtual environment directory name (default: .venv)
- `REQUIREMENTS_FILE`: Requirements file name (default: requirements.txt)

Example:
```bash
# Using GitHub
GIT_HOST_URL="https://github.com" pysetup --repo-name my-project

# Using GitLab
GIT_HOST_URL="https://gitlab.com" pysetup --repo-name my-project

# Using a self-hosted Git service
GIT_HOST_URL="https://git.company.com" pysetup --repo-name my-project
```

## Development

1. Clone the repository:
```bash
git clone https://github.com/HodlON42/python-project-manager.git
cd python-project-manager
```

2. Create a virtual environment and install development dependencies:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate.bat
pip install -e ".[test]"
```

3. Run tests:
```bash
pytest  # Run all tests
pytest --cov  # Run tests with coverage report
```

## Contributing

Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

This project is licensed under the GNU AGPL License - see [LICENSE](LICENSE) file for details.

## Security

- Git commands are executed using `shell=True` for compatibility. Input validation is performed to mitigate risks.
- Repository names are used as-is in Git commands. Ensure you use valid repository names.
- For security issues, please refer to CONTRIBUTING.md