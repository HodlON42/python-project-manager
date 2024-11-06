# Contributing to Python Project Manager

We love your input! We want to make contributing to Python Project Manager as easy and transparent as possible.

## Security

### Reporting Security Issues

If you discover a security vulnerability, please do NOT open an issue.
Email [contact@hodlon.com] instead.

### Security Best Practices

When contributing code:
- Never store sensitive data in code or comments
- All Git URLs must use HTTPS or SSH format
- Shell commands must be validated through the security module
- Always use the provided security validation functions

## Development Process

1. Fork the repo and create your branch from `main`
2. Make your changes
3. Add or update tests as needed
4. Update documentation as needed
5. Push your changes and create a pull request

## Development Environment Setup

1. Clone the repository:
```bash
git clone https://github.com/HodlON42/python-project-manager.git
cd python-project-manager
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install development dependencies:
```bash
pip install -e ".[test]"
```

## Running Tests

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov

# Run specific test file
pytest tests/test_utils.py
```

## Code Quality

We use several tools to maintain code quality:
- pytest for testing
- Coverage.py for test coverage
- Type hints for better code documentation

All PRs must:
- Maintain 100% test coverage
- Include proper type hints
- Follow PEP 8 style guide

## Code Style

- Follow PEP 8
- Use type hints
- Write docstrings in Google format
- Keep functions focused and small
- Add comments for complex logic

## Versioning

We follow Semantic Versioning (SemVer):
- MAJOR version for incompatible API changes (X.0.0)
- MINOR version for added functionality (0.X.0)
- PATCH version for bug fixes (0.0.X)

## Documentation

- Update README.md if needed
- Add docstrings to new functions/classes
- Comment non-obvious code sections
- Update CHANGELOG.md

## Pull Request Process

1. Update documentation
2. Update tests
3. Update CHANGELOG.md
4. Wait for review