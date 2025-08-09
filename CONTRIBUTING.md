# Contributing to Pilar2

Thank you for your interest in contributing to Pilar2! This document provides guidelines and information for contributors.

## 🤝 How to Contribute

### 1. Fork the Repository
1. Go to the [Pilar2 repository](https://github.com/yourusername/pilar2)
2. Click the "Fork" button in the top right corner
3. Clone your forked repository to your local machine

### 2. Create a Feature Branch
```bash
git checkout -b feature/your-feature-name
```

### 3. Make Your Changes
- Follow the coding standards (see below)
- Add tests for new functionality
- Update documentation as needed
- Ensure all tests pass

### 4. Commit Your Changes
```bash
git add .
git commit -m "feat: add new feature description"
```

### 5. Push and Create a Pull Request
```bash
git push origin feature/your-feature-name
```

Then create a pull request on GitHub.

## 📋 Development Setup

### Prerequisites
- Python 3.8+
- Git
- pip

### Local Development Setup
```bash
# Clone your fork
git clone https://github.com/yourusername/pilar2.git
cd pilar2

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install -r requirements-dev.txt  # if available

# Set up environment variables
cp config/secrets.env.example .env
# Edit .env with your API keys
```

## 🧪 Testing

### Run Tests
```bash
# Run all tests
python -m pytest tests/

# Run specific test file
python -m pytest tests/test_specific.py

# Run with coverage
python -m pytest --cov=.

# Run comprehensive system test
python comprehensive_tax_system_test.py
```

### Test Individual Components
```bash
# Test Serper integration
python test_serper_integration.py

# Test web scraping
python test_web_scraping_integration.py
```

## 📝 Coding Standards

### Python Code Style
- Follow PEP 8 style guidelines
- Use meaningful variable and function names
- Add docstrings to all functions and classes
- Keep functions small and focused

### Commit Message Format
Use conventional commit format:
```
type(scope): description

[optional body]

[optional footer]
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes
- `refactor`: Code refactoring
- `test`: Test changes
- `chore`: Maintenance tasks

### Code Quality Tools
```bash
# Format code
black .

# Lint code
flake8 .

# Type checking (if using type hints)
mypy .
```

## 🏗️ Project Structure

### Key Directories
- `agents/`: AI agents and tools
- `backend/`: FastAPI backend application
- `frontend/`: Streamlit frontend application
- `config/`: Configuration files
- `tests/`: Test files
- `docs/`: Documentation

### Adding New Features

#### Backend API Endpoints
1. Create route in `backend/routes/`
2. Add business logic in `backend/services/`
3. Update API documentation
4. Add tests

#### Frontend Components
1. Create component in `frontend/components/`
2. Update main app in `frontend/app.py`
3. Add styling and functionality
4. Test user interface

#### AI Agents
1. Create agent file in `agents/`
2. Update `agents/crew_config.yaml`
3. Add tools and capabilities
4. Test agent functionality

## 🐛 Bug Reports

### Before Submitting a Bug Report
1. Check existing issues
2. Try to reproduce the bug
3. Check the logs in `logs/` directory
4. Test with different data/files

### Bug Report Template
```markdown
**Bug Description**
Brief description of the bug

**Steps to Reproduce**
1. Step 1
2. Step 2
3. Step 3

**Expected Behavior**
What should happen

**Actual Behavior**
What actually happens

**Environment**
- OS: [e.g., Windows 10, macOS, Linux]
- Python version: [e.g., 3.8.10]
- Pilar2 version: [e.g., 2.0.0]

**Additional Information**
- Error messages
- Screenshots
- Log files
```

## 💡 Feature Requests

### Feature Request Template
```markdown
**Feature Description**
Brief description of the feature

**Use Case**
Why this feature is needed

**Proposed Implementation**
How you think it should work

**Alternatives Considered**
Other approaches you considered

**Additional Information**
Any other relevant details
```

## 📚 Documentation

### Updating Documentation
- Keep README.md up to date
- Update API documentation
- Add inline code comments
- Update configuration examples

### Documentation Standards
- Use clear, concise language
- Include code examples
- Add screenshots for UI changes
- Keep documentation in sync with code

## 🔒 Security

### Security Guidelines
- Never commit API keys or secrets
- Use environment variables for sensitive data
- Validate all user inputs
- Follow secure coding practices
- Report security issues privately

### Reporting Security Issues
If you find a security vulnerability:
1. **DO NOT** create a public issue
2. Email the maintainers privately
3. Provide detailed information about the vulnerability
4. Allow time for the issue to be addressed

## 🎯 Areas for Contribution

### High Priority
- Bug fixes
- Performance improvements
- Security enhancements
- Documentation updates

### Medium Priority
- New AI agent capabilities
- Additional web scraping sources
- Enhanced UI/UX features
- Additional report formats

### Low Priority
- Code refactoring
- Test coverage improvements
- Minor UI improvements
- Additional language support

## 🤝 Community Guidelines

### Be Respectful
- Be kind and respectful to other contributors
- Use inclusive language
- Welcome newcomers
- Provide constructive feedback

### Communication
- Use clear, professional language
- Ask questions when unsure
- Share knowledge and help others
- Be patient with responses

## 📞 Getting Help

### Questions and Support
- Check existing documentation
- Search existing issues
- Ask questions in discussions
- Contact maintainers if needed

### Resources
- [Python Documentation](https://docs.python.org/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [CrewAI Documentation](https://docs.crewai.com/)

## 🏆 Recognition

### Contributors
All contributors will be recognized in:
- README.md contributors section
- Release notes
- Project documentation

### Types of Contributions
- Code contributions
- Bug reports
- Feature requests
- Documentation improvements
- Testing and feedback

Thank you for contributing to Pilar2! 🚀
