"""
CodePulse Setup Configuration
=============================

Check your code's pulse with AI-powered analysis!

Usage:
    pip install -e .          # Development installation
    pip install .             # Regular installation
    python setup.py sdist     # Create source distribution
"""

from setuptools import setup, find_packages
import os

# Read the README for the long description
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Read requirements
with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="codepulse",
    version="0.4.0",
    author="Saleh Almqati",
    author_email="xsll7c@gmail.com",
    description="AI-powered code analysis tool - Check your code's pulse with advanced metrics, pattern detection, and performance analysis",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/DeftonesL/CodePulse",
    project_urls={
        "Bug Tracker": "https://github.com/DeftonesL/CodePulse/issues",
        "Source Code": "https://github.com/DeftonesL/CodePulse",
        "Documentation": "https://github.com/DeftonesL/CodePulse/tree/main/docs"
    },
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Testing",
        "Topic :: Software Development :: Quality Assurance",
        "Topic :: Security",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=8.0.0",
            "pytest-cov>=4.1.0",
            "pytest-mock>=3.12.0",
            "black>=24.0.0",
            "mypy>=1.8.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "codepulse=core.cli:main",
            "pulse=core.cli:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
    keywords=[
        "code-analysis", "static-analysis", "code-quality", "security-scanner",
        "halstead-metrics", "maintainability-index", "technical-debt",
        "pattern-detection", "performance-analysis", "ai", "linter"
    ],
)
