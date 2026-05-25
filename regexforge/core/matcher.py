"""
RegexForge Matcher Engine
正则匹配引擎

Provides comprehensive regex matching with support for all Python re flags,
capture groups, and performance timing.
"""

import re
import time
from dataclasses import dataclass, field
from typing import List, Optional, Tuple, Pattern
from enum import Enum


class RegexFlag(Enum):
    """Supported regex flags with descriptions"""
    IGNORECASE = (re.IGNORECASE, "i", "Case-insensitive matching")
    MULTILINE = (re.MULTILINE, "m", "^/$ match at line boundaries")
    DOTALL = (re.DOTALL, "s", ". matches newlines")
    VERBOSE = (re.VERBOSE, "x", "Allow whitespace and comments")
    ASCII = (re.ASCII, "a", "ASCII-only matching")
    UNICODE = (re.UNICODE, "u", "Unicode matching (default)")

    def __init__(self, flag_value: int, short: str, description: str):
        self.flag_value = flag_value
        self.short = short
        self.description = description


@dataclass
class MatchResult:
    """Result of a regex match operation"""
    success: bool
    pattern: str
    text: str
    matches: List[re.Match] = field(default_factory=list)
    groups: List[Tuple[str, Optional[str]]] = field(default_factory=list)
    named_groups: dict = field(default_factory=dict)
    match_count: int = 0
    elapsed_time: float = 0.0
    error: Optional[str] = None
    flags_used: int = 0

    def to_dict(self) -> dict:
        """Convert match result to dictionary"""
        return {
            "success": self.success,
            "pattern": self.pattern,
            "text": self.text,
            "match_count": self.match_count,
            "elapsed_time_ms": round(self.elapsed_time * 1000, 3),
            "groups": self.groups,
            "named_groups": self.named_groups,
            "error": self.error,
        }


class RegexMatcher:
    """
    Advanced regex matching engine with comprehensive features
    
    Features:
    - Support for all Python re flags
    - Multiple match modes (match, search, findall, finditer)
    - Capture group extraction
    - Performance timing
    - Error handling with detailed messages
    """

    FLAG_MAP = {
        "i": re.IGNORECASE,
        "m": re.MULTILINE,
        "s": re.DOTALL,
        "x": re.VERBOSE,
        "a": re.ASCII,
        "u": re.UNICODE,
    }

    def __init__(self):
        self._pattern: Optional[Pattern] = None
        self._last_pattern: str = ""
        self._last_flags: int = 0

    def parse_flags(self, flag_str: str) -> int:
        """
        Parse flag string to re flags
        
        Args:
            flag_str: String like "ims" for IGNORECASE, MULTILINE, DOTALL
            
        Returns:
            Combined flag value
        """
        flags = 0
        for char in flag_str.lower():
            if char in self.FLAG_MAP:
                flags |= self.FLAG_MAP[char]
        return flags

    def compile(self, pattern: str, flags: int = 0) -> Tuple[Optional[Pattern], Optional[str]]:
        """
        Compile a regex pattern with error handling
        
        Args:
            pattern: Regex pattern string
            flags: re module flags
            
        Returns:
            Tuple of (compiled_pattern, error_message)
        """
        try:
            self._pattern = re.compile(pattern, flags)
            self._last_pattern = pattern
            self._last_flags = flags
            return self._pattern, None
        except re.error as e:
            return None, f"Regex Error: {e.msg} at position {e.pos if e.pos else 'unknown'}"

    def match(self, pattern: str, text: str, flags: int = 0) -> MatchResult:
        """
        Match pattern at the beginning of text
        
        Args:
            pattern: Regex pattern string
            text: Text to match against
            flags: re module flags
            
        Returns:
            MatchResult object with match details
        """
        start_time = time.perf_counter()
        
        compiled, error = self.compile(pattern, flags)
        if error:
            return MatchResult(
                success=False,
                pattern=pattern,
                text=text,
                error=error,
                flags_used=flags,
                elapsed_time=time.perf_counter() - start_time,
            )

        try:
            match = compiled.match(text)
            elapsed = time.perf_counter() - start_time
            
            if match:
                return self._build_result(pattern, text, [match], flags, elapsed)
            else:
                return MatchResult(
                    success=False,
                    pattern=pattern,
                    text=text,
                    match_count=0,
                    flags_used=flags,
                    elapsed_time=elapsed,
                )
        except Exception as e:
            return MatchResult(
                success=False,
                pattern=pattern,
                text=text,
                error=str(e),
                flags_used=flags,
                elapsed_time=time.perf_counter() - start_time,
            )

    def search(self, pattern: str, text: str, flags: int = 0) -> MatchResult:
        """
        Search for pattern anywhere in text
        
        Args:
            pattern: Regex pattern string
            text: Text to search in
            flags: re module flags
            
        Returns:
            MatchResult object with match details
        """
        start_time = time.perf_counter()
        
        compiled, error = self.compile(pattern, flags)
        if error:
            return MatchResult(
                success=False,
                pattern=pattern,
                text=text,
                error=error,
                flags_used=flags,
                elapsed_time=time.perf_counter() - start_time,
            )

        try:
            match = compiled.search(text)
            elapsed = time.perf_counter() - start_time
            
            if match:
                return self._build_result(pattern, text, [match], flags, elapsed)
            else:
                return MatchResult(
                    success=False,
                    pattern=pattern,
                    text=text,
                    match_count=0,
                    flags_used=flags,
                    elapsed_time=elapsed,
                )
        except Exception as e:
            return MatchResult(
                success=False,
                pattern=pattern,
                text=text,
                error=str(e),
                flags_used=flags,
                elapsed_time=time.perf_counter() - start_time,
            )

    def findall(self, pattern: str, text: str, flags: int = 0) -> MatchResult:
        """
        Find all matches in text
        
        Args:
            pattern: Regex pattern string
            text: Text to search in
            flags: re module flags
            
        Returns:
            MatchResult object with all matches
        """
        start_time = time.perf_counter()
        
        compiled, error = self.compile(pattern, flags)
        if error:
            return MatchResult(
                success=False,
                pattern=pattern,
                text=text,
                error=error,
                flags_used=flags,
                elapsed_time=time.perf_counter() - start_time,
            )

        try:
            matches = list(compiled.finditer(text))
            elapsed = time.perf_counter() - start_time
            
            if matches:
                return self._build_result(pattern, text, matches, flags, elapsed)
            else:
                return MatchResult(
                    success=False,
                    pattern=pattern,
                    text=text,
                    match_count=0,
                    flags_used=flags,
                    elapsed_time=elapsed,
                )
        except Exception as e:
            return MatchResult(
                success=False,
                pattern=pattern,
                text=text,
                error=str(e),
                flags_used=flags,
                elapsed_time=time.perf_counter() - start_time,
            )

    def _build_result(
        self, 
        pattern: str, 
        text: str, 
        matches: List[re.Match], 
        flags: int,
        elapsed: float
    ) -> MatchResult:
        """Build MatchResult from list of matches"""
        groups = []
        named_groups = {}
        
        # Extract groups from first match
        if matches:
            match = matches[0]
            # Numbered groups (skip group 0 which is the full match)
            for i in range(1, match.lastindex + 1 if match.lastindex else 0):
                groups.append((f"Group {i}", match.group(i)))
            
            # Named groups
            if match.groupdict():
                named_groups = match.groupdict()

        return MatchResult(
            success=True,
            pattern=pattern,
            text=text,
            matches=matches,
            groups=groups,
            named_groups=named_groups,
            match_count=len(matches),
            flags_used=flags,
            elapsed_time=elapsed,
        )

    def get_match_positions(self, match: re.Match) -> List[Tuple[int, int, str]]:
        """
        Get all match positions for highlighting
        
        Args:
            match: re.Match object
            
        Returns:
            List of (start, end, matched_text) tuples
        """
        positions = []
        
        # Full match
        positions.append((match.start(), match.end(), match.group()))
        
        # Groups
        for i in range(1, match.lastindex + 1 if match.lastindex else 0):
            try:
                start, end = match.span(i)
                if start != -1:  # Group matched
                    positions.append((start, end, match.group(i)))
            except IndexError:
                continue
                
        return positions

    def validate_pattern(self, pattern: str) -> Tuple[bool, Optional[str]]:
        """
        Validate a regex pattern without matching
        
        Args:
            pattern: Regex pattern string
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        try:
            re.compile(pattern)
            return True, None
        except re.error as e:
            return False, f"Invalid pattern: {e.msg}"
