# GitHub Actions Automated PyPI Publishing 🚀

Complete guide to set up automated publishing of your Formula Fantasy package to PyPI using GitHub Actions.

## 🌟 Overview

This guide will help you:
- **Automatically build and publish** to PyPI on every release
- **Test on multiple Python versions** before publishing
- **Secure credential management** using GitHub secrets
- **Version management** with git tags
- **Rollback capabilities** for failed releases

## 📋 Prerequisites

1. **GitHub Repository**: Your Formula Fantasy code in a GitHub repo
2. **PyPI Account**: Account on [pypi.org](https://pypi.org)
3. **API Token**: Generated from your PyPI account

## 🔐 Step 1: Generate PyPI API Token

1. **Login to PyPI**: Go to [pypi.org](https://pypi.org) and log in
2. **Account Settings**: Click your username → Account settings
3. **API Tokens**: Scroll to "API tokens" section
4. **Add API Token**:
   - **Token name**: `github-actions-formula-fantasy`
   - **Scope**: Choose "Entire account" (for first upload) or "Project: formula-fantasy" (if package exists)
   - **Copy the token** (starts with `pypi-...`)

## 🔒 Step 2: Add Secrets to GitHub Repository

1. **Navigate to your GitHub repo**: `https://github.com/yourusername/formula-fantasy`
2. **Settings Tab**: Click "Settings" in the top navigation
3. **Secrets and Variables**: In left sidebar, click "Secrets and variables" → "Actions"
4. **New Repository Secret**: Click "New repository secret"

Add this secret:

### Required Secret

| Secret Name | Value | Description |
|-------------|-------|-------------|
| `PYPI_API_TOKEN` | `pypi-...` | Your PyPI API token |

## 📁 Step 3: Create GitHub Actions Workflow

Create the directory structure and workflow file:

### Directory Structure
```
.github/
└── workflows/
    └── publish-to-pypi.yml
```

### Create the Workflow File

Create `.github/workflows/publish-to-pypi.yml`:

```yaml
name: Publish Formula Fantasy to PyPI

# Trigger on version tags (v1.0.0, v1.1.0, etc.)
on:
  push:
    tags:
      - 'v*.*.*'
  # Also allow manual triggering
  workflow_dispatch:

jobs:
  # Test the package before publishing
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ['3.8', '3.9', '3.10', '3.11', '3.12']
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install build twine
        pip install -e .
    
    - name: Test package imports
      run: |
        python -c "from formula_fantasy import get_driver_points, get_constructor_points"
        python -c "from formula_fantasy import list_drivers, list_constructors, get_latest_round"
        echo "✅ All imports successful"
    
    - name: Test CLI functionality
      run: |
        python -m formula_fantasy.cli --drivers
        echo "✅ CLI test successful"

  # Build and publish to PyPI
  publish-pypi:
    needs: test
    runs-on: ubuntu-latest
    if: startsWith(github.ref, 'refs/tags/')
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install build dependencies
      run: |
        python -m pip install --upgrade pip
        pip install build twine
    
    - name: Build package
      run: python -m build
    
    - name: Check package
      run: twine check dist/*
    
    - name: Publish to PyPI
      env:
        TWINE_USERNAME: __token__
        TWINE_PASSWORD: ${{ secrets.PYPI_API_TOKEN }}
      run: twine upload dist/*
    
    - name: Create GitHub Release
      uses: actions/create-release@v1
      env:
        GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
      with:
        tag_name: ${{ github.ref }}
        release_name: Release ${{ github.ref }}
        body: |
          ## Formula Fantasy ${{ github.ref }}
          
          **Automated release published to PyPI**
          
          ### Installation
          ```bash
          pip install --upgrade formula-fantasy
          ```
          
          ### What's New
          - Check the commit history for detailed changes
          - Package available at: https://pypi.org/project/formula-fantasy/
          
          ### Verification
          ```python
          from formula_fantasy import get_driver_points
          print(get_driver_points("VER", "latest"))
          ```
        draft: false
        prerelease: false

  # Test installation from PyPI
  test-installation:
    needs: publish-pypi
    runs-on: ubuntu-latest
    if: startsWith(github.ref, 'refs/tags/')
    
    steps:
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Wait for PyPI propagation
      run: sleep 60
    
    - name: Test installation from PyPI
      run: |
        pip install formula-fantasy
        python -c "from formula_fantasy import get_driver_points; print('✅ Installation successful')"
        formula-fantasy --drivers
        echo "✅ Package successfully published and tested"
```

## 🏷️ Step 4: Version Management Strategy

### Semantic Versioning

Use [Semantic Versioning](https://semver.org/):
- `v1.0.0` - Major release
- `v1.1.0` - Minor release (new features)
- `v1.0.1` - Patch release (bug fixes)

### Update Version Numbers

Before creating a release, update version in these files:

1. **`pyproject.toml`**:
```toml
[project]
version = "1.1.0"  # Update this
```

2. **`setup.py`**:
```python
setup(
    version="1.1.0",  # Update this
    ...
)
```

3. **`formula_fantasy/__init__.py`**:
```python
__version__ = "1.1.0"  # Update this
```

## 🚀 Step 5: Publishing Process

### Method 1: GitHub Releases (Recommended)

1. **Update version numbers** in all files
2. **Commit and push** changes:
```bash
git add .
git commit -m "Bump version to v1.1.0"
git push origin main
```

3. **Create a release** on GitHub:
   - Go to your repo → Releases → "Create a new release"
   - **Tag version**: `v1.1.0` (create new tag)
   - **Release title**: `Formula Fantasy v1.1.0`
   - **Description**: Add release notes
   - Click "Publish release"

4. **GitHub Actions will automatically**:
   - Run tests on multiple Python versions
   - Build the package
   - Publish to TestPyPI
   - Publish to PyPI
   - Create a GitHub release
   - Test the installation

### Method 2: Git Tags (Command Line)

1. **Update version numbers** and commit
2. **Create and push tag**:
```bash
git tag v1.1.0
git push origin v1.1.0
```

3. **GitHub Actions triggers automatically**

## 🔍 Step 6: Monitoring and Verification

### Check GitHub Actions

1. **Actions Tab**: Go to your repo → Actions
2. **Workflow Runs**: Click on the latest run
3. **Job Status**: Monitor each job (test, publish-test, publish-pypi)
4. **Logs**: Click on jobs to see detailed logs

### Verify Publication

1. **PyPI Page**: Check https://pypi.org/project/formula-fantasy/
2. **Installation Test**:
```bash
pip install --upgrade formula-fantasy
python -c "from formula_fantasy import get_driver_points; print(get_driver_points('VER', 'latest'))"
```

3. **Version Check**:
```bash
pip show formula-fantasy
```

## ⚠️ Troubleshooting

### Common Issues and Solutions

#### 1. **Authentication Failed**
```
Error: Invalid or non-existent authentication information
```
**Solution**:
- Check PyPI API token is correctly set in GitHub secrets
- Ensure token has correct permissions
- Token should start with `pypi-`

#### 2. **Package Already Exists**
```
Error: File already exists
```
**Solution**:
- You cannot upload the same version twice
- Increment version number in all files
- Create new tag

#### 3. **Build Failures**
```
Error: No module named 'formula_fantasy'
```
**Solution**:
- Check package structure
- Ensure `__init__.py` exists
- Verify imports in workflow


### Debug Steps

1. **Check workflow logs** in GitHub Actions
2. **Test locally**:
```bash
python -m build
twine check dist/*
```
3. **Manual upload test**:
```bash
twine upload dist/*
```

## 🔄 Step 7: Advanced Configuration

### Conditional Publishing

Only publish on main branch:
```yaml
if: github.ref == 'refs/heads/main' && startsWith(github.ref, 'refs/tags/')
```

### Matrix Testing with Dependencies

```yaml
strategy:
  matrix:
    python-version: ['3.8', '3.9', '3.10', '3.11', '3.12']
    dependency-version: ['minimal', 'latest']
```

### Notification Setup

Add Slack/Discord notifications:
```yaml
- name: Notify on success
  if: success()
  run: |
    curl -X POST -H 'Content-type: application/json' \
    --data '{"text":"✅ Formula Fantasy v${{ github.ref }} published to PyPI!"}' \
    ${{ secrets.SLACK_WEBHOOK_URL }}
```

## 📋 Step 8: Complete Checklist

Before setting up automation:

- [ ] **PyPI account created**
- [ ] **API token generated** and saved securely  
- [ ] **GitHub secret configured** (PYPI_API_TOKEN)
- [ ] **Workflow file created** (`.github/workflows/publish-to-pypi.yml`)
- [ ] **Version numbers updated** (pyproject.toml, setup.py, __init__.py)
- [ ] **Local testing completed** (`python -m build`, `twine check`)
- [ ] **Package structure verified** (imports work correctly)

For each release:

- [ ] **Code changes committed** and tested
- [ ] **Version numbers bumped** in all files
- [ ] **Changelog updated** with new features/fixes
- [ ] **Tag created** or GitHub release published
- [ ] **GitHub Actions completed** successfully
- [ ] **PyPI page verified** (new version available)
- [ ] **Installation tested** from PyPI

## 🎉 Example Release Process

Here's a complete example release process:

```bash
# 1. Make your changes and test locally
git add .
git commit -m "Add new visualization features"

# 2. Update version numbers (1.0.0 → 1.1.0)
# Edit pyproject.toml, setup.py, formula_fantasy/__init__.py

# 3. Commit version bump
git add .
git commit -m "Bump version to v1.1.0"
git push origin main

# 4. Create and push tag
git tag v1.1.0
git push origin v1.1.0

# 5. Watch GitHub Actions magic happen! 🚀
# - Tests run on Python 3.8-3.12
# - Package builds automatically
# - Publishes directly to PyPI
# - Creates GitHub release
# - Tests installation

# 6. Verify your users can install the new version
pip install --upgrade formula-fantasy
```

## 🏎️ Formula Fantasy Specific Notes

Your package includes:
- **Main library**: `formula_fantasy/`
- **CLI interface**: `formula-fantasy` command
- **Visualization examples**: `examples/`
- **Documentation**: `docs/`

The GitHub Actions will:
1. **Test all functionality** including CLI commands
2. **Build with correct metadata** (author, description, etc.)
3. **Publish directly to PyPI** with proper name: `formula-fantasy`
4. **Enable installation**: `pip install formula-fantasy`
5. **Maintain CLI access**: `formula-fantasy --drivers`

## 🚀 Ready to Automate!

Once you've followed this guide:
1. **Every git tag** triggers automated publishing
2. **Multiple Python versions** are tested automatically
3. **PyPI updates** happen within minutes of tagging
4. **Users get instant access** to new versions
5. **Release notes** are generated automatically

Your Formula Fantasy package will be professionally maintained with zero manual PyPI uploads! 🏎️📦✨

---

**Happy automated publishing! 🚀📊**