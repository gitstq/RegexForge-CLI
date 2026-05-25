#!/usr/bin/env python3
"""
RegexForge-CLI Setup Configuration
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="regexforge-cli",
    version="1.0.0",
    author="RegexForge Team",
    author_email="regexforge@example.com",
    description="🔧 Lightweight Terminal Regex Testing & Building Engine",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gitstq/RegexForge-CLI",
    license="MIT",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development",
        "Topic :: Text Processing",
        "Topic :: Utilities",
    ],
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "regexforge=regexforge.cli:main",
        ],
    },
    keywords="regex,regular expression,cli,terminal,tui,testing,development tools",
    project_urls={
        "Bug Reports": "https://github.com/gitstq/RegexForge-CLI/issues",
        "Source": "https://github.com/gitstq/RegexForge-CLI",
    },
)
