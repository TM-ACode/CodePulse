# 🤝 Contributing to CodePulse

First off, thanks for taking the time to contribute! ❤️

CodePulse is a student project that welcomes contributions from everyone!

---

## 🎯 How Can I Contribute?

### 1. Report Bugs 🐛

Found a bug? Please create an issue with:
- Clear title and description
- Steps to reproduce
- Expected vs actual behavior
- Your environment (OS, Python version)
- Code sample (if applicable)

**Template:**
```markdown
**Bug Description:**
Clear description of the bug

**Steps to Reproduce:**
1. Do this
2. Then this
3. Bug happens

**Expected Behavior:**
What should happen

**Actual Behavior:**
What actually happens

**Environment:**
- OS: [e.g., Windows 11, macOS, Ubuntu]
- Python: [e.g., 3.11]
- CodePulse Version: [e.g., 0.4.0]
```

### 2. Suggest Features 💡

Have an idea? Open an issue with:
- Feature description
- Use case / Why it's useful
- Possible implementation (optional)

### 3. Improve Documentation 📝

Documentation can always be better:
- Fix typos
- Add examples
- Clarify confusing parts
- Add tutorials

### 4. Write Code 💻

Want to add a feature or fix a bug?

**Good First Issues:**
- Add support for new languages
- Improve error messages
- Add more code patterns
- Enhance performance analysis

---

## 🔧 Development Setup

### Prerequisites
```bash
# Python 3.9+
python3 --version

# Git
git --version
```

### Setup
```bash
# Fork and clone
git clone https://github.com/YOUR-USERNAME/CodePulse.git
cd CodePulse

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e .

# Install dev dependencies
pip install pytest pytest-cov black mypy
```

### Run Tests
```bash
# Run all tests
pytest tests/

# With coverage
pytest --cov=src tests/

# Specific test
pytest tests/test_scanner.py
```

---

## 📝 Code Style

### Python
- Follow PEP 8
- Use type hints
- Add docstrings
- Run black formatter:
  ```bash
  black src/ tests/
  ```

### JavaScript/TypeScript
- Use ESLint
- Add JSDoc comments
- Follow existing style

### Commit Messages
Use clear, descriptive messages:
```bash
# Good
git commit -m "Add support for Go language"
git commit -m "Fix memory leak in scanner"
git commit -m "Update README with examples"

# Not so good
git commit -m "fix bug"
git commit -m "update"
```

---

## 🔀 Pull Request Process

### 1. Create a Branch
```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/bug-description
```

### 2. Make Changes
- Write clear code
- Add tests if applicable
- Update documentation
- Follow code style

### 3. Test Everything
```bash
# Run tests
pytest tests/

# Test your feature manually
python3 src/core/analyzer.py ./test-project
```

### 4. Commit
```bash
git add .
git commit -m "Add feature: description"
```

### 5. Push
```bash
git push origin feature/your-feature-name
```

### 6. Create Pull Request
- Go to GitHub
- Click "New Pull Request"
- Fill in description:

**Template:**
```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation
- [ ] Performance improvement

## Testing
How did you test this?

## Checklist
- [ ] Code follows style guidelines
- [ ] Tests added/updated
- [ ] Documentation updated
- [ ] All tests pass
```

---

## 🎨 Adding New Features

### Adding a New Language

1. Update `scanner.py`:
```python
LANGUAGE_MAP = {
    # ... existing languages
    '.go': 'Go',  # Add new extension
}
```

2. Create language-specific scanner (optional):
```python
# src/core/go_scanner.py
class GoScanner:
    def scan_file(self, file_path):
        # Implementation
        pass
```

3. Add tests:
```python
# tests/test_go_scanner.py
def test_go_scanner():
    # Test implementation
    pass
```

4. Update documentation in README.md

### Adding New Metrics

1. Add to `advanced_metrics.py`:
```python
def calculate_new_metric(self, tree: ast.AST) -> float:
    """Calculate new metric"""
    # Implementation
    return metric_value
```

2. Update report generation
3. Add tests
4. Document in `ADVANCED_FEATURES.md`

### Adding New Patterns

1. Add to `code_patterns.py`:
```python
def _detect_new_pattern(self, tree, file_path):
    """Detect new pattern"""
    # Implementation
    pass
```

2. Add to detection flow
3. Add tests
4. Update documentation

---

## 🧪 Testing Guidelines

### What to Test
- New features
- Bug fixes
- Edge cases
- Error handling

### Test Structure
```python
def test_feature_name():
    # Arrange - Set up test data
    input_data = "..."
    
    # Act - Run the feature
    result = feature_function(input_data)
    
    # Assert - Verify results
    assert result == expected_output
```

### Coverage
- Aim for >80% coverage
- Test both success and failure cases

---

## 📚 Documentation

### Code Comments
```python
def complex_function(param: int) -> str:
    """
    Brief description.
    
    Detailed explanation of what the function does,
    any important notes, edge cases, etc.
    
    Args:
        param: Description of parameter
        
    Returns:
        Description of return value
        
    Raises:
        ValueError: When and why
        
    Example:
        >>> complex_function(42)
        'result'
    """
    # Implementation
    pass
```

### README Updates
When adding features, update:
- Feature list
- Examples
- Command usage
- Dependencies (if new)

---

## ❓ Questions?

- 📧 Email: xsll7c@gmail.com
- 💬 Open a discussion on GitHub
- 🐛 Create an issue

---

## 🙏 Recognition

All contributors will be:
- Listed in CONTRIBUTORS.md
- Mentioned in release notes
- Credited in documentation

---

## 📜 Code of Conduct

### Our Pledge
- Be respectful
- Be welcoming
- Be collaborative
- Be patient with questions

### Not Tolerated
- Harassment
- Discrimination
- Trolling
- Personal attacks

---

## 🎓 Learning Resources

New to contributing?
- [First Contributions Guide](https://github.com/firstcontributions/first-contributions)
- [How to Contribute to Open Source](https://opensource.guide/how-to-contribute/)
- [GitHub Flow Guide](https://guides.github.com/introduction/flow/)

---

## 💝 Thank You!

Every contribution, no matter how small, helps make CodePulse better!

**Contributors make this project possible.** 🙏

---

**Happy Contributing! 🚀**

*Built with ❤️ by the CodePulse community*
