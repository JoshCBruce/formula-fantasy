# How to Upload Formula Fantasy Python Library to PyPI

This guide will walk you through uploading your Formula Fantasy Python library to PyPI so it can be installed with `pip install formula-fantasy`.

## 📋 Prerequisites

Before you begin, make sure you have:

1. **Python 3.7 or higher** installed
2. **A PyPI account** (create one at https://pypi.org/account/register/)
3. **Your library code** (the `formula_fantasy/` folder and setup files)

## 🛠️ Step 1: Install Required Tools

Install the necessary tools for building and uploading Python packages:

```bash
pip install --upgrade pip setuptools wheel twine build
```

## 🏗️ Step 2: Prepare Your Package

1. **Navigate to your project directory:**
   ```bash
   cd /path/to/your/formula_fantasy/project
   ```

2. **Verify your project structure:**
   ```
   your-project/
   ├── formula_fantasy/
   │   ├── __init__.py
   │   ├── core.py
   │   ├── cli.py
   │   └── README.md
   ├── setup.py
   ├── pyproject.toml
   ├── LICENSE
   ├── MANIFEST.in
   └── UPLOAD_INSTRUCTIONS.md (this file)
   ```

3. **Test your package locally (optional but recommended):**
   ```bash
   pip install -e .
   ```
   
   Test it works:
   ```bash
   python -c "from formula_fantasy import get_driver_points; print(get_driver_points('VER', '14'))"
   formula-fantasy VER 14
   ```

   Uninstall the local version:
   ```bash
   pip uninstall formula-fantasy
   ```

## 🔧 Step 3: Build Your Package

Build the distribution files that will be uploaded to PyPI:

```bash
python -m build
```

This will create a `dist/` directory with two files:
- `formula-fantasy-1.0.0.tar.gz` (source distribution)
- `formula_fantasy-1.0.0-py3-none-any.whl` (wheel distribution)

## 🧪 Step 4: Test Upload to TestPyPI (Recommended)

Before uploading to the main PyPI, test your upload on TestPyPI:

1. **Create a TestPyPI account** at https://test.pypi.org/account/register/

2. **Upload to TestPyPI:**
   ```bash
   python -m twine upload --repository testpypi dist/*
   ```

   You'll be prompted for your TestPyPI username and password.

3. **Test installation from TestPyPI:**
   ```bash
   pip install --index-url https://test.pypi.org/simple/ formula-fantasy
   ```

4. **Test the installed package:**
   ```bash
   python -c "from formula_fantasy import get_driver_points; print('Test successful!')"
   formula-fantasy --help
   ```

5. **Uninstall the test version:**
   ```bash
   pip uninstall formula-fantasy
   ```

## 🚀 Step 5: Upload to PyPI

Once you've tested successfully, upload to the main PyPI:

```bash
python -m twine upload dist/*
```

You'll be prompted for your PyPI username and password.

## ✅ Step 6: Verify Your Upload

1. **Check your package on PyPI:**
   - Visit https://pypi.org/project/formula-fantasy/
   - Verify all information looks correct

2. **Test installation:**
   ```bash
   pip install formula-fantasy
   ```

3. **Test functionality:**
   ```bash
   python -c "from formula_fantasy import get_driver_points; print(get_driver_points('VER', 'latest'))"
   formula-fantasy VER latest
   formula-fantasy --drivers
   ```

## 🔐 Security Best Practices

### Using API Tokens (Recommended)

Instead of using your username/password, use API tokens:

1. **Create an API token:**
   - Go to https://pypi.org/manage/account/
   - Scroll to "API tokens" section
   - Click "Add API token"
   - Choose scope (recommend "Entire account" for first upload, then project-specific)

2. **Use token for upload:**
   ```bash
   python -m twine upload --username __token__ --password pypi-your-token-here dist/*
   ```

### Using .pypirc File

Create a `~/.pypirc` file for easier uploads:

```ini
[distutils]
index-servers = 
  pypi
  testpypi

[pypi]
username = __token__
password = pypi-your-token-here

[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = pypi-your-testpypi-token-here
```

Then upload with:
```bash
python -m twine upload dist/*
```

## 📝 Version Updates

When you want to release a new version:

1. **Update version number** in:
   - `formula_fantasy/__init__.py` (`__version__ = "1.0.1"`)
   - `setup.py` (`version="1.0.1"`)  
   - `pyproject.toml` (`version = "1.0.1"`)

2. **Clean previous builds:**
   ```bash
   rm -rf build/ dist/ *.egg-info/
   ```

3. **Build and upload new version:**
   ```bash
   python -m build
   python -m twine upload dist/*
   ```

## 🛠️ Troubleshooting

### Common Issues

**Error: "File already exists"**
- You can't upload the same version twice
- Increment the version number and try again

**Error: "Invalid authentication"**
- Check your username/password or API token
- Make sure you're using the correct repository (pypi vs testpypi)

**Error: "Package name already exists"**
- Choose a different package name in setup.py and pyproject.toml
- Check https://pypi.org to see if the name is taken

**Error: "README not found"**
- Ensure the README path in setup.py is correct
- Check that `formula_fantasy/README.md` exists

### Testing Locally

```bash
# Create a virtual environment for testing
python -m venv test_env
source test_env/bin/activate  # On Windows: test_env\\Scripts\\activate

# Install and test your package
pip install /path/to/your/project
python -c "from formula_fantasy import get_driver_points; print('Success!')"

# Clean up
deactivate
rm -rf test_env
```

## 📊 After Upload

Your library will be available within a few minutes at:
- **Installation:** `pip install formula-fantasy`
- **PyPI Page:** https://pypi.org/project/formula-fantasy/
- **Documentation:** The README will be displayed on the PyPI page

Users can then install and use your library:

```bash
# Install
pip install formula-fantasy

# Use in Python
python -c "from formula_fantasy import get_driver_points; print(get_driver_points('VER', '14'))"

# Use CLI
formula-fantasy VER 14
formula-fantasy RBR latest --info
```

## 🎉 Congratulations!

Your Formula Fantasy Python library is now available on PyPI! 

### Next Steps

- Share your library with the F1 community
- Consider adding more features based on user feedback
- Monitor download statistics on PyPI
- Update regularly as new race data becomes available

---

**Happy Formula Fantasy data sharing! 🏎️📦**