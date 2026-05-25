"""
RegexForge Highlight Engine
语法高亮引擎

Provides ANSI color highlighting for regex matches and terminal output.
Zero external dependencies - uses only standard library.
"""

import re
from dataclasses import dataclass
from typing import List, Tuple, Optional
from enum import Enum


class Color(Enum):
    """ANSI color codes"""
    # Reset
    RESET = "\033[0m"
    
    # Basic colors
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"
    
    # Bright colors
    BRIGHT_BLACK = "\033[90m"
    BRIGHT_RED = "\033[91m"
    BRIGHT_GREEN = "\033[92m"
    BRIGHT_YELLOW = "\033[93m"
    BRIGHT_BLUE = "\033[94m"
    BRIGHT_MAGENTA = "\033[95m"
    BRIGHT_CYAN = "\033[96m"
    BRIGHT_WHITE = "\033[97m"
    
    # Background colors
    BG_BLACK = "\033[40m"
    BG_RED = "\033[41m"
    BG_GREEN = "\033[42m"
    BG_YELLOW = "\033[43m"
    BG_BLUE = "\033[44m"
    BG_MAGENTA = "\033[45m"
    BG_CYAN = "\033[46m"
    BG_WHITE = "\033[47m"
    
    # Styles
    BOLD = "\033[1m"
    DIM = "\033[2m"
    ITALIC = "\033[3m"
    UNDERLINE = "\033[4m"
    BLINK = "\033[5m"
    REVERSE = "\033[7m"
    STRIKETHROUGH = "\033[9m"


@dataclass
class ColorScheme:
    """Color scheme configuration for highlighting"""
    match_bg: str = Color.BG_GREEN.value
    match_fg: str = Color.BRIGHT_WHITE.value
    group_bg: str = Color.BG_CYAN.value
    group_fg: str = Color.BRIGHT_WHITE.value
    error_fg: str = Color.BRIGHT_RED.value
    success_fg: str = Color.BRIGHT_GREEN.value
    info_fg: str = Color.BRIGHT_BLUE.value
    warning_fg: str = Color.BRIGHT_YELLOW.value
    dim_fg: str = Color.BRIGHT_BLACK.value
    highlight_bg: str = Color.BG_YELLOW.value
    highlight_fg: str = Color.BLACK.value


class Highlighter:
    """
    ANSI highlighter for terminal output
    
    Features:
    - Match highlighting with background colors
    - Group highlighting with different colors
    - Error/success/warning message styling
    - Table formatting
    - Progress bars
    """

    def __init__(self, color_scheme: Optional[ColorScheme] = None, use_color: bool = True):
        self.scheme = color_scheme or ColorScheme()
        self.use_color = use_color

    def _apply_color(self, text: str, *colors: str) -> str:
        """Apply ANSI colors to text"""
        if not self.use_color:
            return text
        return f"{''.join(colors)}{text}{Color.RESET.value}"

    def highlight_match(
        self, 
        text: str, 
        positions: List[Tuple[int, int, str]],
        show_groups: bool = True
    ) -> str:
        """
        Highlight matched positions in text
        
        Args:
            text: Original text
            positions: List of (start, end, matched_text) tuples
            show_groups: Whether to highlight groups differently
            
        Returns:
            Text with ANSI highlighting
        """
        if not positions:
            return text

        # Sort positions by start index
        sorted_positions = sorted(positions, key=lambda x: x[0])
        
        result = []
        last_end = 0
        
        for i, (start, end, matched) in enumerate(sorted_positions):
            # Add text before this match
            if start > last_end:
                result.append(text[last_end:start])
            
            # Highlight the match
            if i == 0:
                # Full match - use match colors
                result.append(self._apply_color(
                    matched,
                    self.scheme.match_bg,
                    self.scheme.match_fg,
                    Color.BOLD.value
                ))
            elif show_groups:
                # Groups - use group colors
                result.append(self._apply_color(
                    matched,
                    self.scheme.group_bg,
                    self.scheme.group_fg
                ))
            else:
                result.append(matched)
            
            last_end = end
        
        # Add remaining text
        if last_end < len(text):
            result.append(text[last_end:])
        
        return ''.join(result)

    def highlight_pattern(self, pattern: str) -> str:
        """
        Highlight regex pattern syntax elements
        
        Args:
            pattern: Regex pattern string
            
        Returns:
            Pattern with syntax highlighting
        """
        if not self.use_color:
            return pattern

        # Highlight special characters
        highlighted = pattern
        
        # Metacharacters
        metachars = r'[\^\$\.\|\?\*\+\(\)\[\]\{\}\\]'
        highlighted = re.sub(
            metachars,
            lambda m: self._apply_color(m.group(), Color.BRIGHT_MAGENTA.value, Color.BOLD.value),
            highlighted
        )
        
        # Character classes
        highlighted = re.sub(
            r'\\[dDwWsS]',
            lambda m: self._apply_color(m.group(), Color.BRIGHT_CYAN.value),
            highlighted
        )
        
        # Quantifiers
        highlighted = re.sub(
            r'\{[\d,]+\}',
            lambda m: self._apply_color(m.group(), Color.BRIGHT_YELLOW.value),
            highlighted
        )
        
        return highlighted

    def error(self, message: str) -> str:
        """Format error message"""
        prefix = self._apply_color("✗ ERROR: ", self.scheme.error_fg, Color.BOLD.value)
        return f"{prefix}{message}"

    def success(self, message: str) -> str:
        """Format success message"""
        prefix = self._apply_color("✓ ", self.scheme.success_fg, Color.BOLD.value)
        return f"{prefix}{message}"

    def warning(self, message: str) -> str:
        """Format warning message"""
        prefix = self._apply_color("⚠ ", self.scheme.warning_fg, Color.BOLD.value)
        return f"{prefix}{message}"

    def info(self, message: str) -> str:
        """Format info message"""
        prefix = self._apply_color("ℹ ", self.scheme.info_fg, Color.BOLD.value)
        return f"{prefix}{message}"

    def dim(self, text: str) -> str:
        """Dim text"""
        return self._apply_color(text, self.scheme.dim_fg)

    def bold(self, text: str) -> str:
        """Bold text"""
        return self._apply_color(text, Color.BOLD.value)

    def underline(self, text: str) -> str:
        """Underline text"""
        return self._apply_color(text, Color.UNDERLINE.value)

    def format_table(
        self, 
        headers: List[str], 
        rows: List[List[str]], 
        title: Optional[str] = None
    ) -> str:
        """
        Format data as a table
        
        Args:
            headers: Column headers
            rows: Data rows
            title: Optional table title
            
        Returns:
            Formatted table string
        """
        if not rows:
            return self.dim("(no data)")

        # Calculate column widths
        col_widths = [len(h) for h in headers]
        for row in rows:
            for i, cell in enumerate(row):
                if i < len(col_widths):
                    col_widths[i] = max(col_widths[i], len(str(cell)))

        # Build separator line
        separator = "+" + "+".join("-" * (w + 2) for w in col_widths) + "+"
        
        # Build header row
        header_cells = []
        for i, header in enumerate(headers):
            padded = f" {header:<{col_widths[i]}} "
            header_cells.append(self._apply_color(padded, Color.BOLD.value))
        header_row = "|" + "|".join(header_cells) + "|"
        
        # Build data rows
        data_rows = []
        for row in rows:
            cells = []
            for i, cell in enumerate(row):
                if i < len(col_widths):
                    cells.append(f" {str(cell):<{col_widths[i]}} ")
            data_rows.append("|" + "|".join(cells) + "|")
        
        # Combine all parts
        result = [separator, header_row, separator]
        result.extend(data_rows)
        result.append(separator)
        
        if title:
            title_line = self._apply_color(f" {title}", Color.BOLD.value, Color.UNDERLINE.value)
            result.insert(0, title_line)
            result.insert(1, "")
        
        return "\n".join(result)

    def format_key_value(self, data: dict, title: Optional[str] = None) -> str:
        """
        Format dictionary as key-value pairs
        
        Args:
            data: Dictionary to format
            title: Optional title
            
        Returns:
            Formatted string
        """
        lines = []
        
        if title:
            lines.append(self._apply_color(f" {title}", Color.BOLD.value, Color.UNDERLINE.value))
            lines.append("")
        
        max_key_len = max(len(str(k)) for k in data.keys()) if data else 0
        
        for key, value in data.items():
            key_str = self._apply_color(f"  {str(key):<{max_key_len}}", Color.BRIGHT_BLUE.value)
            lines.append(f"{key_str}  {value}")
        
        return "\n".join(lines)

    def progress_bar(self, current: int, total: int, width: int = 40) -> str:
        """
        Create a progress bar
        
        Args:
            current: Current progress value
            total: Total value
            width: Bar width in characters
            
        Returns:
            Progress bar string
        """
        if total == 0:
            percentage = 100
        else:
            percentage = min(100, int(current / total * 100))
        
        filled = int(width * percentage / 100)
        empty = width - filled
        
        bar = "█" * filled + "░" * empty
        
        if self.use_color:
            if percentage < 50:
                bar = self._apply_color(bar, Color.BRIGHT_RED.value)
            elif percentage < 80:
                bar = self._apply_color(bar, Color.BRIGHT_YELLOW.value)
            else:
                bar = self._apply_color(bar, Color.BRIGHT_GREEN.value)
        
        return f"[{bar}] {percentage}%"

    def clear_screen(self) -> str:
        """Return ANSI clear screen sequence"""
        return "\033[2J\033[H"

    def move_cursor(self, row: int, col: int) -> str:
        """Move cursor to position"""
        return f"\033[{row};{col}H"

    def save_cursor(self) -> str:
        """Save cursor position"""
        return "\033[s"

    def restore_cursor(self) -> str:
        """Restore cursor position"""
        return "\033[u"
