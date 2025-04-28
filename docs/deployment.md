# Package Deployment Workflow

This document outlines the steps to create a new release of the `chatgpt_md_converter` package.

## Prerequisites

- GitHub CLI (`gh`) installed and authenticated
- Python build tools installed in your environment

## Step-by-Step Deployment Process

### 1. Update Version Number

Update the version number in `setup.py`:

```python
setup(
    name="chatgpt_md_converter",
    version="X.Y.Z",  # Change this to the new version
    # ...
)
```

### 2. Commit and Push Changes

```bash
# Stage the changed files
git add setup.py
git add <any other modified files>

# Commit with a descriptive message
git commit -m "Fix <issue description>, bump version to X.Y.Z"

# Push to GitHub
git push
```

### 3. Create and Push a Git Tag

```bash
# Create an annotated tag
git tag -a vX.Y.Z -m "Version X.Y.Z: <brief description of changes>"

# Push the tag to GitHub
git push --tags
```

### 4. Create a GitHub Release

Using GitHub CLI:

```bash
gh release create vX.Y.Z --title "Version X.Y.Z" --notes "## Changes in this release:

- <Change description 1>
- <Change description 2>
- <Change description 3>"
```

### 5. Build Distribution Packages

Using standard build tools:

```bash
# Install build dependencies if needed
uv pip install --upgrade build twine

# Build the package
python -m build
```

This will create both source distribution and wheel files in the `dist/` directory.

### 6. Upload to PyPI

```bash
# Check the build artifacts for issues
twine check dist/*

# Upload to PyPI
twine upload dist/*
```

You'll be prompted for your PyPI username and password.

## Verification

After deploying, verify the following:

1. The new version appears on your GitHub releases page
2. The package is available on PyPI with the correct version
3. You can install the new version with pip: `pip install --upgrade chatgpt_md_converter`
4. The installed version is correct: `pip show chatgpt_md_converter`

## Troubleshooting

- If the GitHub release fails, check that you have the proper permissions and that the tag exists
- If the PyPI upload fails, ensure your PyPI credentials are correct and you have permission to upload to the package
- If the package doesn't install correctly, verify the build artifacts in the `dist/` directory
