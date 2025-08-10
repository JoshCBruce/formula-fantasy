#!/usr/bin/env python3
"""
Setup configuration for F1 Fantasy Python Library
"""

from setuptools import setup, find_packages
import os

# Read the README file
def read_long_description():
    readme_path = os.path.join(os.path.dirname(__file__), "formula_fantasy", "README.md")
    if os.path.exists(readme_path):
        with open(readme_path, "r", encoding="utf-8") as fh:
            return fh.read()
    return "A simple Python library for fetching F1 Fantasy data"

setup(
    name="formula-fantasy",
    version="1.0.0",
    author="F1 Fantasy Data Team",
    author_email="noreply@f1fantasy.dev",
    description="A simple Python library for fetching F1 Fantasy driver and constructor data",
    long_description=read_long_description(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/formula-fantasy",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Games/Entertainment",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=[
        "requests>=2.25.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov",
            "black",
            "flake8",
            "mypy",
        ],
    },
    entry_points={
        "console_scripts": [
            "formula-fantasy=formula_fantasy.cli:main",
        ],
    },
    keywords=[
        "f1",
        "formula1", 
        "fantasy",
        "racing",
        "motorsport",
        "api",
        "data",
        "statistics",
        "scraping"
    ],
    project_urls={
        "Bug Reports": "https://github.com/yourusername/formula-fantasy/issues",
        "Source": "https://github.com/yourusername/formula-fantasy",
        "Documentation": "https://github.com/yourusername/formula-fantasy#readme",
        "Data Source": "https://github.com/JoshCBruce/fantasy-data",
    },
    include_package_data=True,
    zip_safe=False,
)