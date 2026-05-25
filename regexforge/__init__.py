"""
RegexForge-CLI - Lightweight Terminal Regex Testing & Building Engine
轻量级终端正则表达式测试与构建引擎

A powerful, zero-dependency CLI tool for testing, building, and debugging
regular expressions with real-time matching, syntax highlighting, and
multi-language code generation.

Author: RegexForge Team
License: MIT
Version: 1.0.0
"""

__version__ = "1.0.0"
__author__ = "RegexForge Team"
__description__ = "Lightweight Terminal Regex Testing & Building Engine"

from .cli import main

__all__ = ["main", "__version__", "__author__", "__description__"]
