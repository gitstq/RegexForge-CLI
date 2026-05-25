"""
RegexForge TUI Dashboard
终端交互式仪表盘

Provides an interactive terminal UI for regex testing and building.
Uses curses for cross-platform compatibility.
"""

import curses
import curses.textpad
import re
from typing import Optional, Tuple, List
from ..core.matcher import RegexMatcher, MatchResult
from ..core.highlight import Highlighter, ColorScheme
from ..core.generator import CodeGenerator, Language
from ..templates.patterns import PatternLibrary


class TUIDashboard:
    """
    Interactive Terminal UI Dashboard for RegexForge
    
    Features:
    - Real-time regex testing
    - Pattern input with syntax highlighting
    - Test text input
    - Match results display
    - Pattern library browser
    - Code generation preview
    """

    def __init__(self, use_color: bool = True):
        self.matcher = RegexMatcher()
        self.highlighter = Highlighter(use_color=use_color)
        self.generator = CodeGenerator()
        self.library = PatternLibrary()
        
        # State
        self.pattern = ""
        self.test_text = ""
        self.flags = ""
        self.result: Optional[MatchResult] = None
        self.current_view = "main"  # main, library, code
        self.selected_language = Language.PYTHON
        self.message = ""
        self.message_type = "info"
        
        # Cursor positions
        self.pattern_cursor = 0
        self.text_cursor = 0
        self.active_input = "pattern"  # pattern, text
        
        # Library state
        self.library_index = 0
        self.library_patterns = []
        
        # Languages for code gen
        self.languages = list(Language)
        self.language_index = 0

    def run(self) -> None:
        """Run the TUI dashboard"""
        curses.wrapper(self._main_loop)

    def _main_loop(self, stdscr) -> None:
        """Main event loop"""
        # Initialize curses
        curses.curs_set(1)  # Show cursor
        curses.noecho()
        stdscr.keypad(True)
        
        # Enable colors if available
        if curses.has_colors() and self.highlighter.use_color:
            curses.start_color()
            curses.use_default_colors()
            # Define color pairs
            curses.init_pair(1, curses.COLOR_GREEN, -1)  # Success
            curses.init_pair(2, curses.COLOR_RED, -1)    # Error
            curses.init_pair(3, curses.COLOR_CYAN, -1)   # Info
            curses.init_pair(4, curses.COLOR_YELLOW, -1) # Warning
            curses.init_pair(5, curses.COLOR_WHITE, curses.COLOR_GREEN)  # Match highlight
            curses.init_pair(6, curses.COLOR_WHITE, curses.COLOR_CYAN)   # Group highlight
        
        # Main loop
        running = True
        while running:
            self._draw(stdscr)
            
            try:
                key = stdscr.getch()
            except curses.error:
                continue
            
            # Handle input
            running = self._handle_input(stdscr, key)

    def _draw(self, stdscr) -> None:
        """Draw the dashboard"""
        stdscr.clear()
        
        height, width = stdscr.getmaxyx()
        
        # Draw header
        self._draw_header(stdscr, width)
        
        # Draw based on current view
        if self.current_view == "main":
            self._draw_main_view(stdscr, height, width)
        elif self.current_view == "library":
            self._draw_library_view(stdscr, height, width)
        elif self.current_view == "code":
            self._draw_code_view(stdscr, height, width)
        
        # Draw footer
        self._draw_footer(stdscr, height, width)
        
        # Draw message if any
        if self.message:
            self._draw_message(stdscr, height, width)
        
        stdscr.refresh()

    def _draw_header(self, stdscr, width: int) -> None:
        """Draw header"""
        title = "╔══════════════════════════════════════════════════════════════════════════════╗"
        stdscr.addstr(0, 0, title[:width])
        
        header = "║  🔧 RegexForge-CLI - Lightweight Terminal Regex Testing & Building Engine   ║"
        stdscr.addstr(1, 0, header[:width])
        
        bottom = "╚══════════════════════════════════════════════════════════════════════════════╝"
        stdscr.addstr(2, 0, bottom[:width])

    def _draw_footer(self, stdscr, height: int, width: int) -> None:
        """Draw footer with keybindings"""
        footer = "║ [Enter] Test │ [L] Library │ [G] Code │ [F] Flags │ [Tab] Switch │ [Q] Quit ║"
        y = height - 2
        stdscr.addstr(y, 0, "╠" + "═" * (width - 2) + "╣")
        stdscr.addstr(y + 1, 0, footer[:width])

    def _draw_message(self, stdscr, height: int, width: int) -> None:
        """Draw message bar"""
        y = height - 4
        if self.message_type == "error":
            color = curses.color_pair(2)
        elif self.message_type == "success":
            color = curses.color_pair(1)
        else:
            color = curses.color_pair(3)
        
        stdscr.addstr(y, 2, self.message[:width - 4], color)

    def _draw_main_view(self, stdscr, height: int, width: int) -> None:
        """Draw main testing view"""
        y = 4
        
        # Pattern input
        stdscr.addstr(y, 2, "Pattern:", curses.A_BOLD)
        y += 1
        
        # Pattern box
        pattern_display = self.pattern or "(enter pattern)"
        if self.active_input == "pattern":
            stdscr.addstr(y, 2, "┌" + "─" * (width - 6) + "┐")
            stdscr.addstr(y + 1, 2, "│ ")
            stdscr.addstr(y + 1, 4, pattern_display[:width - 8])
            stdscr.addstr(y + 1, width - 2, "│")
            stdscr.addstr(y + 2, 2, "└" + "─" * (width - 6) + "┘")
            # Draw cursor
            stdscr.move(y + 1, 4 + min(self.pattern_cursor, width - 8))
        else:
            stdscr.addstr(y, 2, "┌" + "─" * (width - 6) + "┐")
            stdscr.addstr(y + 1, 2, "│ ")
            stdscr.addstr(y + 1, 4, pattern_display[:width - 8], curses.A_DIM)
            stdscr.addstr(y + 1, width - 2, "│")
            stdscr.addstr(y + 2, 2, "└" + "─" * (width - 6) + "┘")
        
        y += 4
        
        # Flags display
        flags_display = f"Flags: {self.flags.upper() if self.flags else '(none)'}"
        stdscr.addstr(y, 2, flags_display, curses.color_pair(3))
        y += 2
        
        # Test text input
        stdscr.addstr(y, 2, "Test Text:", curses.A_BOLD)
        y += 1
        
        text_lines = self.test_text.split('\n') if self.test_text else ["(enter test text)"]
        if self.active_input == "text":
            stdscr.addstr(y, 2, "┌" + "─" * (width - 6) + "┐")
            for i, line in enumerate(text_lines[:5]):
                stdscr.addstr(y + 1 + i, 2, "│ ")
                stdscr.addstr(y + 1 + i, 4, line[:width - 8])
                stdscr.addstr(y + 1 + i, width - 2, "│")
            if len(text_lines) < 5:
                for i in range(len(text_lines), 5):
                    stdscr.addstr(y + 1 + i, 2, "│" + " " * (width - 4) + "│")
            stdscr.addstr(y + 6, 2, "└" + "─" * (width - 6) + "┘")
        else:
            stdscr.addstr(y, 2, "┌" + "─" * (width - 6) + "┐")
            for i, line in enumerate(text_lines[:5]):
                stdscr.addstr(y + 1 + i, 2, "│ ")
                stdscr.addstr(y + 1 + i, 4, line[:width - 8], curses.A_DIM)
                stdscr.addstr(y + 1 + i, width - 2, "│")
            if len(text_lines) < 5:
                for i in range(len(text_lines), 5):
                    stdscr.addstr(y + 1 + i, 2, "│" + " " * (width - 4) + "│")
            stdscr.addstr(y + 6, 2, "└" + "─" * (width - 6) + "┘")
        
        y += 8
        
        # Results
        stdscr.addstr(y, 2, "Results:", curses.A_BOLD)
        y += 1
        
        if self.result:
            if self.result.success:
                stdscr.addstr(y, 2, f"✓ Found {self.result.match_count} match(es)", curses.color_pair(1))
                y += 1
                
                # Show matched text
                if self.result.matches:
                    for i, match in enumerate(self.result.matches[:3]):
                        match_text = match.group()[:width - 20]
                        stdscr.addstr(y, 4, f"[{i+1}] {match_text}", curses.color_pair(5))
                        y += 1
                    
                    if self.result.match_count > 3:
                        stdscr.addstr(y, 4, f"... and {self.result.match_count - 3} more", curses.A_DIM)
                        y += 1
                
                # Show groups
                if self.result.groups:
                    y += 1
                    stdscr.addstr(y, 2, "Groups:", curses.A_BOLD)
                    y += 1
                    for name, value in self.result.groups[:5]:
                        group_text = f"{name}: {value}"[:width - 6]
                        stdscr.addstr(y, 4, group_text, curses.color_pair(6))
                        y += 1
                
                # Show timing
                y += 1
                timing = f"⏱ Time: {self.result.elapsed_time * 1000:.3f}ms"
                stdscr.addstr(y, 2, timing, curses.A_DIM)
            else:
                if self.result.error:
                    stdscr.addstr(y, 2, f"✗ {self.result.error}", curses.color_pair(2))
                else:
                    stdscr.addstr(y, 2, "✗ No matches found", curses.color_pair(4))
        else:
            stdscr.addstr(y, 2, "Press Enter to test pattern", curses.A_DIM)

    def _draw_library_view(self, stdscr, height: int, width: int) -> None:
        """Draw pattern library view"""
        y = 4
        
        stdscr.addstr(y, 2, "📚 Pattern Library (↑↓ to navigate, Enter to select, Esc to cancel)", curses.A_BOLD)
        y += 2
        
        # Get all patterns
        if not self.library_patterns:
            self.library_patterns = self.library.list_all()
        
        # Draw pattern list
        visible_count = height - y - 4
        start_idx = max(0, self.library_index - visible_count // 2)
        end_idx = min(len(self.library_patterns), start_idx + visible_count)
        
        for i in range(start_idx, end_idx):
            pattern = self.library_patterns[i]
            if i == self.library_index:
                stdscr.addstr(y, 2, "► ", curses.A_BOLD)
                stdscr.addstr(y, 4, f"{pattern.name}", curses.A_BOLD | curses.color_pair(3))
                stdscr.addstr(y, 4 + len(pattern.name) + 2, f"- {pattern.description[:width - len(pattern.name) - 20]}", curses.A_BOLD)
            else:
                stdscr.addstr(y, 2, "  ")
                stdscr.addstr(y, 4, f"{pattern.name}", curses.color_pair(3))
                stdscr.addstr(y, 4 + len(pattern.name) + 2, f"- {pattern.description[:width - len(pattern.name) - 20]}")
            y += 1
        
        # Show selected pattern details
        if self.library_patterns:
            selected = self.library_patterns[self.library_index]
            y = height - 6
            stdscr.addstr(y, 2, "─" * (width - 4))
            y += 1
            stdscr.addstr(y, 2, f"Pattern: {selected.pattern}", curses.color_pair(5))
            y += 1
            stdscr.addstr(y, 2, f"Example: {selected.examples[0] if selected.examples else 'N/A'}", curses.A_DIM)

    def _draw_code_view(self, stdscr, height: int, width: int) -> None:
        """Draw code generation view"""
        y = 4
        
        stdscr.addstr(y, 2, "💻 Code Generation (←→ to change language, Esc to cancel)", curses.A_BOLD)
        y += 2
        
        # Language selector
        lang_str = " │ ".join([f"[{l.value}]" if l == self.selected_language else f" {l.value} " for l in self.languages])
        stdscr.addstr(y, 2, lang_str[:width - 4], curses.A_DIM)
        y += 2
        
        # Generate code
        if self.pattern:
            code = self.generator.generate(self.pattern, self.selected_language, self.flags, self.test_text)
            
            stdscr.addstr(y, 2, f"Generated {code.language} Code:", curses.A_BOLD)
            y += 1
            
            # Draw code
            code_lines = code.code.split('\n')
            for line in code_lines[:height - y - 4]:
                stdscr.addstr(y, 2, line[:width - 4])
                y += 1
        else:
            stdscr.addstr(y, 2, "Enter a pattern first to generate code", curses.A_DIM)

    def _handle_input(self, stdscr, key: int) -> bool:
        """Handle keyboard input"""
        # Global keys
        if key == ord('q') or key == ord('Q'):
            return False
        
        if key == 27:  # Escape
            if self.current_view != "main":
                self.current_view = "main"
            return True
        
        # View-specific keys
        if self.current_view == "main":
            return self._handle_main_input(stdscr, key)
        elif self.current_view == "library":
            return self._handle_library_input(stdscr, key)
        elif self.current_view == "code":
            return self._handle_code_input(stdscr, key)
        
        return True

    def _handle_main_input(self, stdscr, key: int) -> bool:
        """Handle input in main view"""
        if key == ord('\t'):  # Tab
            self.active_input = "text" if self.active_input == "pattern" else "pattern"
        
        elif key == ord('\n') or key == curses.KEY_ENTER:  # Enter
            self._run_test()
        
        elif key == ord('l') or key == ord('L'):
            self.current_view = "library"
            self.library_patterns = self.library.list_all()
        
        elif key == ord('g') or key == ord('G'):
            self.current_view = "code"
        
        elif key == ord('f') or key == ord('F'):
            # Toggle flags
            self._cycle_flags()
        
        elif self.active_input == "pattern":
            if key == curses.KEY_BACKSPACE or key == 127:
                if self.pattern_cursor > 0:
                    self.pattern = self.pattern[:self.pattern_cursor-1] + self.pattern[self.pattern_cursor:]
                    self.pattern_cursor -= 1
            elif key == curses.KEY_LEFT:
                self.pattern_cursor = max(0, self.pattern_cursor - 1)
            elif key == curses.KEY_RIGHT:
                self.pattern_cursor = min(len(self.pattern), self.pattern_cursor + 1)
            elif 32 <= key <= 126:  # Printable ASCII
                self.pattern = self.pattern[:self.pattern_cursor] + chr(key) + self.pattern[self.pattern_cursor:]
                self.pattern_cursor += 1
        
        elif self.active_input == "text":
            if key == curses.KEY_BACKSPACE or key == 127:
                if self.text_cursor > 0:
                    self.test_text = self.test_text[:self.text_cursor-1] + self.test_text[self.text_cursor:]
                    self.text_cursor -= 1
            elif key == curses.KEY_LEFT:
                self.text_cursor = max(0, self.text_cursor - 1)
            elif key == curses.KEY_RIGHT:
                self.text_cursor = min(len(self.test_text), self.text_cursor + 1)
            elif key == curses.KEY_DOWN or key == curses.KEY_UP:
                pass  # Ignore arrow keys for simplicity
            elif 32 <= key <= 126:  # Printable ASCII
                self.test_text = self.test_text[:self.text_cursor] + chr(key) + self.test_text[self.text_cursor:]
                self.text_cursor += 1
        
        return True

    def _handle_library_input(self, stdscr, key: int) -> bool:
        """Handle input in library view"""
        if key == curses.KEY_UP:
            self.library_index = max(0, self.library_index - 1)
        elif key == curses.KEY_DOWN:
            self.library_index = min(len(self.library_patterns) - 1, self.library_index + 1)
        elif key == ord('\n') or key == curses.KEY_ENTER:
            if self.library_patterns:
                selected = self.library_patterns[self.library_index]
                self.pattern = selected.pattern
                self.flags = selected.flags
                self.pattern_cursor = len(self.pattern)
                if selected.examples:
                    self.test_text = selected.examples[0]
                    self.text_cursor = len(self.test_text)
                self.current_view = "main"
                self._run_test()
        
        return True

    def _handle_code_input(self, stdscr, key: int) -> bool:
        """Handle input in code view"""
        if key == curses.KEY_LEFT:
            self.language_index = max(0, self.language_index - 1)
            self.selected_language = self.languages[self.language_index]
        elif key == curses.KEY_RIGHT:
            self.language_index = min(len(self.languages) - 1, self.language_index + 1)
            self.selected_language = self.languages[self.language_index]
        
        return True

    def _run_test(self) -> None:
        """Run regex test"""
        if not self.pattern:
            self.message = "Please enter a pattern"
            self.message_type = "warning"
            return
        
        flags = self.matcher.parse_flags(self.flags)
        self.result = self.matcher.findall(self.pattern, self.test_text, flags)
        
        if self.result.success:
            self.message = f"Found {self.result.match_count} match(es) in {self.result.elapsed_time * 1000:.3f}ms"
            self.message_type = "success"
        elif self.result.error:
            self.message = self.result.error
            self.message_type = "error"
        else:
            self.message = "No matches found"
            self.message_type = "info"

    def _cycle_flags(self) -> None:
        """Cycle through common flag combinations"""
        flag_options = ["", "i", "m", "im", "s", "is", "ms", "ims"]
        current_idx = flag_options.index(self.flags) if self.flags in flag_options else 0
        next_idx = (current_idx + 1) % len(flag_options)
        self.flags = flag_options[next_idx]
        self.message = f"Flags: {self.flags.upper() if self.flags else 'none'}"
        self.message_type = "info"
