#!/usr/bin/env python3
"""
RegexForge-CLI - Main Module Entry Point
支持 python -m regexforge 运行方式
"""

from .cli import main
import sys

if __name__ == "__main__":
    sys.exit(main())
