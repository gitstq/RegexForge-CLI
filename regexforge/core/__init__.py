"""
RegexForge Core Module
核心功能模块
"""

from .matcher import RegexMatcher, MatchResult
from .highlight import Highlighter, ColorScheme
from .generator import CodeGenerator

__all__ = [
    "RegexMatcher",
    "MatchResult", 
    "Highlighter",
    "ColorScheme",
    "CodeGenerator",
]
