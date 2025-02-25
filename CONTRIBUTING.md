# Contributing to YouTube Transcription and Download API

Thank you for considering contributing to the YouTube Transcription and Download API! This document provides guidelines and instructions for contributing to this project.

## Code of Conduct

By participating in this project, you agree to abide by the [Code of Conduct](CODE_OF_CONDUCT.md).

## How Can I Contribute?

### Reporting Bugs

If you find a bug, please create an issue with the following information:

- A clear and descriptive title
- Steps to reproduce the bug
- Expected behavior
- Actual behavior
- Screenshots (if applicable)
- Environment information (OS, Python version, etc.)

### Suggesting Enhancements

If you have an idea for an enhancement, please create an issue with the following information:

- A clear and descriptive title
- A detailed description of the enhancement
- Why this enhancement would be useful
- Any relevant examples or mockups

### Pull Requests

1. Fork the repository
2. Create a new branch for your feature or bug fix
3. Make your changes
4. Run tests to ensure your changes don't break existing functionality
5. Submit a pull request

## Development Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd youtube-claude
```

2. Create and activate a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install the required dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file:
```bash
cp .env.example .env
```

5. Run the application:
```bash
python app.py
```

## Coding Guidelines

- Follow PEP 8 style guide for Python code
- Write clear, descriptive commit messages
- Include comments and docstrings for new functions and classes
- Add tests for new features
- Update documentation as needed

## Testing

Before submitting a pull request, please run the tests to ensure your changes don't break existing functionality:

```bash
# TODO: Add testing instructions
```

## Documentation

If you're adding a new feature, please update the documentation accordingly. This includes:

- README.md
- Code comments and docstrings
- Any relevant documentation files

## License

By contributing to this project, you agree that your contributions will be licensed under the project's license.
