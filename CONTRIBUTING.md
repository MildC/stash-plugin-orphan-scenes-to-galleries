# Contributing to Orphan Scenes to Galleries

Thank you for your interest in contributing! This document provides guidelines and information for contributors.

## How to Contribute

### Reporting Bugs

If you find a bug, please create an issue on GitHub with:

- **Clear title** describing the issue
- **Steps to reproduce** the problem
- **Expected behavior** vs actual behavior
- **Environment details**:
  - Stash version
  - Python version
  - Operating system
  - Plugin version
- **Relevant log output** from Stash (Settings → Logs → Plugins)

### Suggesting Features

Feature requests are welcome! Please create an issue with:

- **Clear description** of the feature
- **Use case**: Why is this feature needed?
- **Proposed solution** (if you have ideas)
- **Alternatives considered**

### Pull Requests

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/my-feature`
3. **Make your changes**
4. **Test thoroughly** (see Testing section below)
5. **Commit with clear messages**
6. **Push to your fork**
7. **Create a pull request**

## Development Setup

### Prerequisites

- Python 3.7+
- Git
- Stash (for testing)

### Clone and Setup

```bash
# Clone your fork
git clone https://github.com/yourusername/stash-plugin-orphan-scenes-to-galleries.git
cd stash-plugin-orphan-scenes-to-galleries

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install pyyaml flake8 pytest
```

### Running Validation

```bash
# Validate plugin structure
python validate.py

# Check Python syntax
python -m py_compile orphan_scenes_to_galleries.py

# Lint code
flake8 orphan_scenes_to_galleries.py
```

## Code Style

### Python

- Follow [PEP 8](https://pep8.org/) style guide
- Use 4 spaces for indentation (not tabs)
- Maximum line length: 127 characters
- Use meaningful variable and function names
- Add docstrings to functions and classes

### Example

```python
def process_scene(self, scene: Dict, galleries: List[Dict]):
    """
    Process a single orphan scene and try to assign it to a gallery.

    Args:
        scene: Scene dictionary with id, files, performers, etc.
        galleries: List of gallery dictionaries to match against

    Returns:
        None (updates scene in Stash if match found)
    """
    # Implementation here
```

### YAML

- Use 2 spaces for indentation
- Follow existing structure in `orphan_scenes_to_galleries.yml`
- Keep descriptions clear and concise

## Testing

### Manual Testing

Always test your changes before submitting:

1. **Enable Dry Run** in plugin settings
2. **Run the task** in Stash
3. **Check logs** for errors and correctness
4. **Disable Dry Run** and test actual functionality
5. **Verify results** in Stash UI

### Test Scenarios

Test with various configurations:

- ✅ Empty database (no scenes/galleries)
- ✅ All scenes already have galleries
- ✅ Mix of orphan and assigned scenes
- ✅ Different matching strategies enabled/disabled
- ✅ Edge cases: scenes with no files, galleries with no path, etc.

### Automated Testing

If adding new features, consider adding unit tests:

```python
# test_plugin.py
import unittest
from orphan_scenes_to_galleries import OrphanSceneProcessor

class TestOrphanSceneProcessor(unittest.TestCase):
    def test_match_by_path(self):
        # Test implementation
        pass
```

## Project Structure

```
stash-plugin-orphan-scenes-to-galleries/
├── .github/
│   └── workflows/
│       └── validate.yml          # CI/CD workflow
├── .gitignore
├── LICENSE
├── README.md                     # Main documentation
├── QUICKSTART.md                # Quick start guide
├── TESTING.md                   # Testing documentation
├── CONTRIBUTING.md              # This file
├── orphan_scenes_to_galleries.yml   # Plugin config
├── orphan_scenes_to_galleries.py    # Main plugin code
├── requirements.txt             # Python dependencies
└── validate.py                  # Validation script
```

## Adding New Features

### Checklist

When adding a new feature:

- [ ] Add configuration options to YAML if needed
- [ ] Implement functionality in Python
- [ ] Update default settings in Python code
- [ ] Test with dry run mode
- [ ] Update README.md with new feature documentation
- [ ] Add example usage if applicable
- [ ] Test on clean Stash instance
- [ ] Update CHANGELOG section in README

### Example: Adding New Matching Strategy

1. **Add YAML setting:**
```yaml
settings:
  matchByStudio:
    displayName: Match by Studio
    description: Assign scenes to galleries with matching studio
    type: BOOLEAN
```

2. **Add to Python defaults:**
```python
settings = {
    # ... existing settings ...
    "matchByStudio": False,
}
```

3. **Implement matching function:**
```python
def match_by_studio(self, scene: Dict, galleries: List[Dict]) -> Optional[Dict]:
    """Match scene to gallery by studio."""
    if not self.settings.get('matchByStudio', False):
        return None
    # Implementation here
```

4. **Add to processing pipeline:**
```python
def process_scene(self, scene: Dict, galleries: List[Dict]):
    # Try new matching strategy
    if not matched_gallery:
        matched_gallery = self.match_by_studio(scene, galleries)
```

5. **Test and document**

## Commit Message Guidelines

Use clear, descriptive commit messages:

- **feat**: New feature (`feat: add studio-based matching`)
- **fix**: Bug fix (`fix: handle scenes with no files`)
- **docs**: Documentation (`docs: update README with examples`)
- **test**: Tests (`test: add unit tests for path matching`)
- **refactor**: Code refactoring (`refactor: simplify matching logic`)
- **chore**: Maintenance (`chore: update dependencies`)

### Examples

```bash
# Good
git commit -m "feat: add date tolerance configuration option"
git commit -m "fix: handle galleries without folder paths"
git commit -m "docs: add troubleshooting section to README"

# Avoid
git commit -m "update"
git commit -m "fixes"
git commit -m "changes"
```

## Release Process

Maintainers follow this process for releases:

1. Update version in `orphan_scenes_to_galleries.yml`
2. Update CHANGELOG in README.md
3. Create git tag: `git tag -a v1.0.1 -m "Release v1.0.1"`
4. Push tag: `git push origin v1.0.1`
5. Create GitHub release with notes

## Code of Conduct

### Our Standards

- Be respectful and inclusive
- Welcome newcomers
- Accept constructive criticism
- Focus on what's best for the community
- Show empathy towards others

### Unacceptable Behavior

- Harassment or discrimination
- Trolling or insulting comments
- Personal or political attacks
- Publishing others' private information
- Other conduct that's unprofessional

## Questions?

- Open an issue for questions
- Join [Stash Discord](https://discord.gg/2TsNFKt)
- Post on [Stash Discourse](https://discourse.stashapp.cc/)

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing! 🎉
