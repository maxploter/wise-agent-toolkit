# Wise Agent Toolkit - Version Management & Publishing Instructions

## Overview

This document provides step-by-step instructions for updating the `wise-api-client` dependency and publishing new versions of the `wise-agent-toolkit` package to PyPI.

## Version Update & Publishing Workflow

### Step 1: Check for Latest wise-api-client Version

Before updating, verify the latest version of `wise-api-client` available on PyPI:

```bash
pip index versions wise-api-client
```

Or check programmatically:
```bash
pip install --upgrade pip
pip search wise-api-client 2>/dev/null || curl -s https://pypi.org/pypi/wise-api-client/json | python -c "import sys, json; print(json.load(sys.stdin)['info']['version'])"
```

**Alternative method (recommended):**
Visit https://pypi.org/project/wise-api-client/ to see the latest version.

### Step 2: Update pyproject.toml

Update the `wise-api-client` version in the dependencies section:

**Location:** `/pyproject.toml`

```toml
[project]
name = "wise-agent-toolkit"
version = "{NEW_VERSION}"  # Bump this version
# ...existing config...

dependencies = [
    "wise-api-client>={NEW_API_CLIENT_VERSION}",  # Update this version
    "pydantic>=2.10",
]
```

**Version Bumping Guidelines:**
- **Patch version** (0.2.4 → 0.2.5): Bug fixes, minor updates to dependencies
- **Minor version** (0.2.4 → 0.3.0): New features, new API methods, backward-compatible changes
- **Major version** (0.2.4 → 1.0.0): Breaking changes, major API overhauls

### Step 3: Update requirements.txt

Update the pinned version in `requirements.txt`:

**Location:** `/requirements.txt`

```
wise-api-client=={NEW_API_CLIENT_VERSION}
pydantic>=2.10
```

### Step 4: Update Version References in Documentation

Check and update version references in:

1. **README.md**: Update any version-specific examples or installation instructions
2. **CHANGELOG.md** (if exists): Add entry for the new version
3. **Documentation**: Update any hardcoded version references

### Step 5: Clean Build Artifacts

Remove old build artifacts before creating a new distribution:

```bash
# Remove dist folder if it exists
rm -rf dist/

# Remove build artifacts
rm -rf build/
rm -rf *.egg-info
rm -rf wise_agent_toolkit.egg-info

# Remove Python cache files (optional but recommended)
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find . -type f -name "*.pyc" -delete
```

### Step 6: Run Tests

Always run tests before publishing to ensure nothing is broken:

```bash
# Run unit tests
python -m unittest discover tests/

# Run specific test files if needed
python -m unittest tests/test_functions.py
python -m unittest tests/test_configuration.py
```

**Important:** Fix any failing tests before proceeding to publish.

### Step 7: Build the Distribution

Create both wheel and source distribution:

```bash
python -m build
```

This will create:
- `dist/wise-agent-toolkit-{VERSION}-py3-none-any.whl` (wheel distribution)
- `dist/wise-agent-toolkit-{VERSION}.tar.gz` (source distribution)

**Verify build output:**
```bash
ls -lh dist/
```

### Step 8: Test the Build Locally (Optional but Recommended)

Before publishing to PyPI, test the package installation locally:

```bash
# Create a virtual environment for testing
python -m venv test_env
source test_env/bin/activate  # On Windows: test_env\Scripts\activate

# Install from local wheel
pip install dist/wise-agent-toolkit-{VERSION}-py3-none-any.whl

# Test import
python -c "from wise_agent_toolkit import get_available_integrations; print(get_available_integrations())"

# Deactivate and remove test environment
deactivate
rm -rf test_env
```

### Step 9: Publish to PyPI

Upload the distribution to PyPI using twine:

```bash
# Install/upgrade twine if needed
pip install --upgrade twine

# Upload to PyPI (will prompt for credentials)
twine upload dist/*
```

**For TestPyPI (testing before production):**
```bash
# Upload to TestPyPI first
twine upload --repository testpypi dist/*

# Test installation from TestPyPI
pip install --index-url https://test.pypi.org/simple/ wise-agent-toolkit
```

### Step 10: Verify Publication

After publishing, verify the package is available:

```bash
# Check PyPI page
open https://pypi.org/project/wise-agent-toolkit/

# Try installing the new version
pip install --upgrade wise-agent-toolkit

# Verify version
python -c "import wise_agent_toolkit; print(wise_agent_toolkit.__version__ if hasattr(wise_agent_toolkit, '__version__') else 'Version check not implemented')"
```

### Step 11: Create Git Tag and Release

After successful publication:

```bash
# Commit version changes
git add pyproject.toml requirements.txt README.md
git commit -m "Bump version to {NEW_VERSION} and update wise-api-client to {NEW_API_CLIENT_VERSION}"

# Create and push tag
git tag -a v{NEW_VERSION} -m "Release version {NEW_VERSION}"
git push origin main
git push origin v{NEW_VERSION}
```

## Authentication Setup

### PyPI Authentication Options

**Option 1: API Token (Recommended)**

1. Generate API token at https://pypi.org/manage/account/token/
2. Configure in `~/.pypirc`:

```ini
[pypi]
username = __token__
password = pypi-AgEIcHlwaS5vcmcC...  # Your token here
```

**Option 2: Environment Variables**

```bash
export TWINE_USERNAME=__token__
export TWINE_PASSWORD=pypi-AgEIcHlwaS5vcmcC...
```

**Option 3: Interactive (twine will prompt)**

Just run `twine upload dist/*` and enter credentials when prompted.

## Complete Update Script

Here's a complete bash script that automates the entire process:

```bash
#!/bin/bash
# update_and_publish.sh

set -e  # Exit on error

echo "=== Wise Agent Toolkit - Update & Publish Script ==="

# Step 1: Check for latest wise-api-client version
echo -e "\n[1/11] Checking latest wise-api-client version..."
LATEST_API_VERSION=$(curl -s https://pypi.org/pypi/wise-api-client/json | python -c "import sys, json; print(json.load(sys.stdin)['info']['version'])" 2>/dev/null || echo "Unable to fetch")
echo "Latest wise-api-client version: $LATEST_API_VERSION"

# Step 2: Prompt for new version
echo -e "\n[2/11] Current version in pyproject.toml:"
grep "^version = " pyproject.toml
read -p "Enter new wise-agent-toolkit version (e.g., 0.2.5): " NEW_VERSION
read -p "Enter wise-api-client version to use (default: $LATEST_API_VERSION): " API_VERSION
API_VERSION=${API_VERSION:-$LATEST_API_VERSION}

# Step 3: Update pyproject.toml
echo -e "\n[3/11] Updating pyproject.toml..."
sed -i.bak "s/^version = .*/version = \"$NEW_VERSION\"/" pyproject.toml
sed -i.bak "s/wise-api-client>=.*/wise-api-client>=$API_VERSION\",/" pyproject.toml
rm pyproject.toml.bak

# Step 4: Update requirements.txt
echo -e "\n[4/11] Updating requirements.txt..."
sed -i.bak "s/wise-api-client==.*/wise-api-client==$API_VERSION/" requirements.txt
rm requirements.txt.bak

# Step 5: Clean build artifacts
echo -e "\n[5/11] Cleaning build artifacts..."
rm -rf dist/ build/ *.egg-info wise_agent_toolkit.egg-info
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find . -type f -name "*.pyc" -delete

# Step 6: Run tests
echo -e "\n[6/11] Running tests..."
python -m unittest discover tests/ || { echo "Tests failed! Aborting."; exit 1; }

# Step 7: Build distribution
echo -e "\n[7/11] Building distribution..."
python -m build

# Step 8: Verify build
echo -e "\n[8/11] Build artifacts:"
ls -lh dist/

# Step 9: Prompt for upload
read -p "Upload to PyPI? (y/n): " UPLOAD
if [ "$UPLOAD" = "y" ]; then
    echo -e "\n[9/11] Uploading to PyPI..."
    twine upload dist/*
else
    echo "Skipping upload. Run 'twine upload dist/*' manually when ready."
fi

# Step 10: Verify (if uploaded)
if [ "$UPLOAD" = "y" ]; then
    echo -e "\n[10/11] Waiting 30 seconds for PyPI to update..."
    sleep 30
    echo "Visit: https://pypi.org/project/wise-agent-toolkit/$NEW_VERSION/"
fi

# Step 11: Git operations
echo -e "\n[11/11] Git operations..."
read -p "Commit and tag release? (y/n): " GIT_COMMIT
if [ "$GIT_COMMIT" = "y" ]; then
    git add pyproject.toml requirements.txt
    git commit -m "Bump version to $NEW_VERSION and update wise-api-client to $API_VERSION"
    git tag -a "v$NEW_VERSION" -m "Release version $NEW_VERSION"
    echo "Don't forget to: git push origin main && git push origin v$NEW_VERSION"
fi

echo -e "\n=== Done! ==="
```

## Troubleshooting

### Common Issues and Solutions

**1. Build fails with "No module named 'setuptools'"**
```bash
pip install --upgrade setuptools wheel
```

**2. Twine upload fails with authentication error**
```bash
# Check credentials in ~/.pypirc or use environment variables
export TWINE_USERNAME=__token__
export TWINE_PASSWORD=your_token_here
```

**3. Version already exists on PyPI**
```bash
# You must bump to a new version - PyPI doesn't allow overwriting
# Update version in pyproject.toml and rebuild
```

**4. Import errors after installation**
```bash
# Clear pip cache and reinstall
pip cache purge
pip install --no-cache-dir --force-reinstall wise-agent-toolkit
```

**5. Tests fail after updating wise-api-client**
```bash
# Check for breaking changes in the API client
# Review wise-api-client changelog
# Update function signatures in wise_agent_toolkit/functions.py
```

## Version Compatibility Matrix

| wise-agent-toolkit | wise-api-client | Python | Notes |
|-------------------|-----------------|--------|-------|
| 0.2.4             | 0.2.5          | 3.11+  | Current stable |
| 0.2.3             | 0.2.4          | 3.11+  | Previous version |
| 0.2.2             | 0.2.3          | 3.11+  | Legacy |

## Post-Release Checklist

After publishing a new version:

- [ ] Verify package is visible on PyPI: https://pypi.org/project/wise-agent-toolkit/
- [ ] Test installation: `pip install --upgrade wise-agent-toolkit`
- [ ] Update GitHub release notes
- [ ] Notify users of breaking changes (if any)
- [ ] Update documentation site (if applicable)
- [ ] Check integration examples still work
- [ ] Monitor GitHub issues for installation problems

## Quick Reference Commands

```bash
# Check current version
grep "^version = " pyproject.toml

# Check latest wise-api-client
pip index versions wise-api-client | head -n 1

# Full clean and rebuild
rm -rf dist/ build/ *.egg-info && python -m build

# Test then publish
python -m unittest discover tests/ && twine upload dist/*

# Emergency rollback (unpublish not supported, must publish new version)
# Bump version and republish with fixes
```

## Notes for AI Agents

When updating versions:
1. Always check for breaking changes in the API client changelog
2. Update all 5 tool files if API signatures change (functions.py, schema.py, prompts.py, tools.py, tests)
3. Verify all existing examples still work
4. Run the full test suite before publishing
5. Use semantic versioning consistently
6. Document all changes in commit messages

Remember: Once published to PyPI, versions cannot be deleted or overwritten. Always test thoroughly before publishing!

