#!/usr/bin/env python3
"""
RegexForge-CLI - Main Entry Point
主入口点

A lightweight terminal regex testing and building engine.

Usage:
    regexforge                    # Launch interactive TUI
    regexforge test <pattern>     # Test a pattern
    regexforge match <pattern> <text>  # Match pattern against text
    regexforge find <pattern> <text>   # Find all matches
    regexforge generate <pattern>      # Generate code
    regexforge library                 # Browse pattern library
    regexforge --help                  # Show help
"""

import sys
import argparse
import os
from typing import Optional

from .core.matcher import RegexMatcher, RegexFlag
from .core.highlight import Highlighter, ColorScheme
from .core.generator import CodeGenerator, Language
from .templates.patterns import PatternLibrary, PatternCategory
from .utils.history import HistoryManager
from . import __version__


def create_parser() -> argparse.ArgumentParser:
    """Create the argument parser"""
    parser = argparse.ArgumentParser(
        prog="regexforge",
        description="🔧 RegexForge-CLI - Lightweight Terminal Regex Testing & Building Engine",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  regexforge                           Launch interactive TUI dashboard
  regexforge test "^\d+$"              Test if pattern is valid
  regexforge match "hello" "hello world"     Match pattern at start
  regexforge find "\d+" "a1b2c3"       Find all digit sequences
  regexforge generate "^\w+$" -l python      Generate Python code
  regexforge library                   Browse pattern library
  regexforge library email             Search for email patterns

Flags:
  -i, --ignore-case    Case-insensitive matching
  -m, --multiline      ^/$ match at line boundaries
  -s, --dotall         . matches newlines
  -x, --verbose        Allow whitespace and comments

For more information, visit: https://github.com/gitstq/RegexForge-CLI
        """
    )
    
    parser.add_argument(
        "-v", "--version",
        action="version",
        version=f"%(prog)s {__version__}"
    )
    
    parser.add_argument(
        "--no-color",
        action="store_true",
        help="Disable colored output"
    )
    
    # Subcommands
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Test command
    test_parser = subparsers.add_parser("test", help="Test if a regex pattern is valid")
    test_parser.add_argument("pattern", help="Regex pattern to test")
    test_parser.add_argument("-f", "--flags", default="", help="Regex flags (e.g., 'ims')")
    
    # Match command
    match_parser = subparsers.add_parser("match", help="Match pattern at the beginning of text")
    match_parser.add_argument("pattern", help="Regex pattern")
    match_parser.add_argument("text", help="Text to match against")
    match_parser.add_argument("-f", "--flags", default="", help="Regex flags")
    
    # Find command
    find_parser = subparsers.add_parser("find", help="Find all matches in text")
    find_parser.add_argument("pattern", help="Regex pattern")
    find_parser.add_argument("text", help="Text to search in")
    find_parser.add_argument("-f", "--flags", default="", help="Regex flags")
    find_parser.add_argument("-g", "--groups", action="store_true", help="Show capture groups")
    
    # Generate command
    gen_parser = subparsers.add_parser("generate", help="Generate code from pattern")
    gen_parser.add_argument("pattern", help="Regex pattern")
    gen_parser.add_argument("-l", "--language", default="python", 
                           choices=["python", "javascript", "typescript", "go", "rust", "java", "php", "ruby"],
                           help="Target language")
    gen_parser.add_argument("-f", "--flags", default="", help="Regex flags")
    gen_parser.add_argument("-t", "--text", help="Test text to include")
    
    # Library command
    lib_parser = subparsers.add_parser("library", help="Browse pattern library")
    lib_parser.add_argument("search", nargs="?", help="Search query")
    lib_parser.add_argument("-c", "--category", help="Filter by category")
    lib_parser.add_argument("--list-categories", action="store_true", help="List all categories")
    
    # History command
    hist_parser = subparsers.add_parser("history", help="View test history")
    hist_parser.add_argument("-c", "--clear", action="store_true", help="Clear history")
    hist_parser.add_argument("-n", "--count", type=int, default=10, help="Number of entries to show")
    
    # Flags shortcuts
    for p in [test_parser, match_parser, find_parser, gen_parser]:
        if p:
            p.add_argument("-i", "--ignore-case", action="store_true", help="Case-insensitive")
            p.add_argument("-m", "--multiline", action="store_true", help="Multiline mode")
            p.add_argument("-s", "--dotall", action="store_true", help="Dot matches newline")
    
    return parser


def main(args: Optional[list] = None) -> int:
    """Main entry point"""
    parser = create_parser()
    parsed = parser.parse_args(args)
    
    use_color = not parsed.no_color
    highlighter = Highlighter(use_color=use_color)
    matcher = RegexMatcher()
    generator = CodeGenerator()
    library = PatternLibrary()
    history = HistoryManager()
    
    # No command - launch TUI
    if not parsed.command:
        return launch_tui(use_color)
    
    # Handle commands
    if parsed.command == "test":
        return cmd_test(matcher, highlighter, parsed)
    elif parsed.command == "match":
        return cmd_match(matcher, highlighter, history, parsed)
    elif parsed.command == "find":
        return cmd_find(matcher, highlighter, history, parsed)
    elif parsed.command == "generate":
        return cmd_generate(generator, highlighter, parsed)
    elif parsed.command == "library":
        return cmd_library(library, highlighter, parsed)
    elif parsed.command == "history":
        return cmd_history(history, highlighter, parsed)
    
    return 0


def launch_tui(use_color: bool) -> int:
    """Launch the TUI dashboard"""
    try:
        from .tui.dashboard import TUIDashboard
        dashboard = TUIDashboard(use_color=use_color)
        dashboard.run()
        return 0
    except ImportError as e:
        print(f"Error: Could not import TUI module: {e}")
        print("Make sure curses is available on your system.")
        return 1


def cmd_test(matcher: RegexMatcher, highlighter: Highlighter, args) -> int:
    """Handle test command"""
    flags = build_flags(args)
    is_valid, error = matcher.validate_pattern(args.pattern)
    
    if is_valid:
        print(highlighter.success(f"Pattern is valid: {args.pattern}"))
        print(f"  Flags: {flags.upper() if flags else '(none)'}")
        return 0
    else:
        print(highlighter.error(error))
        return 1


def cmd_match(matcher: RegexMatcher, highlighter: Highlighter, history: HistoryManager, args) -> int:
    """Handle match command"""
    flags = matcher.parse_flags(build_flags(args))
    result = matcher.match(args.pattern, args.text, flags)
    
    history.add(args.pattern, args.text, build_flags(args), result.match_count, result.success)
    
    if result.success:
        print(highlighter.success(f"Match found!"))
        print(f"  Pattern: {highlighter.highlight_pattern(args.pattern)}")
        print(f"  Matched: {result.matches[0].group()}")
        print(f"  Position: {result.matches[0].start()}-{result.matches[0].end()}")
        print(f"  Time: {result.elapsed_time * 1000:.3f}ms")
        
        if result.groups:
            print("\n  Capture Groups:")
            for name, value in result.groups:
                print(f"    {name}: {value}")
        
        if result.named_groups:
            print("\n  Named Groups:")
            for name, value in result.named_groups.items():
                print(f"    {name}: {value}")
        
        return 0
    else:
        if result.error:
            print(highlighter.error(result.error))
        else:
            print(highlighter.warning("No match found"))
        return 1


def cmd_find(matcher: RegexMatcher, highlighter: Highlighter, history: HistoryManager, args) -> int:
    """Handle find command"""
    flags = matcher.parse_flags(build_flags(args))
    result = matcher.findall(args.pattern, args.text, flags)
    
    history.add(args.pattern, args.text, build_flags(args), result.match_count, result.success)
    
    if result.success:
        print(highlighter.success(f"Found {result.match_count} match(es)"))
        print(f"  Pattern: {highlighter.highlight_pattern(args.pattern)}")
        print(f"  Time: {result.elapsed_time * 1000:.3f}ms")
        print()
        
        # Highlight matches in text
        positions = []
        for match in result.matches:
            positions.append((match.start(), match.end(), match.group()))
        
        highlighted_text = highlighter.highlight_match(args.text, positions, show_groups=args.groups)
        print("  Text:")
        for line in highlighted_text.split('\n'):
            print(f"    {line}")
        
        if args.groups and result.matches:
            print("\n  All Capture Groups:")
            for i, match in enumerate(result.matches[:10]):
                if match.lastindex:
                    groups = [match.group(g) for g in range(1, match.lastindex + 1)]
                    print(f"    Match {i+1}: {groups}")
        
        return 0
    else:
        if result.error:
            print(highlighter.error(result.error))
        else:
            print(highlighter.warning("No matches found"))
        return 1


def cmd_generate(generator: CodeGenerator, highlighter: Highlighter, args) -> int:
    """Handle generate command"""
    lang_map = {
        "python": Language.PYTHON,
        "javascript": Language.JAVASCRIPT,
        "typescript": Language.TYPESCRIPT,
        "go": Language.GO,
        "rust": Language.RUST,
        "java": Language.JAVA,
        "php": Language.PHP,
        "ruby": Language.RUBY,
    }
    
    language = lang_map.get(args.language.lower(), Language.PYTHON)
    code = generator.generate(args.pattern, language, args.flags, args.text)
    
    print(highlighter.info(f"Generated {code.language} code:"))
    print()
    print(code.code)
    
    return 0


def cmd_library(library: PatternLibrary, highlighter: Highlighter, args) -> int:
    """Handle library command"""
    if args.list_categories:
        print("Available categories:")
        for cat in library.get_categories():
            print(f"  - {cat.value}")
        return 0
    
    if args.category:
        try:
            category = PatternCategory(args.category)
            patterns = library.list_by_category(category)
        except ValueError:
            print(highlighter.error(f"Unknown category: {args.category}"))
            return 1
    elif args.search:
        patterns = library.search(args.search)
    else:
        patterns = library.list_all()
    
    if not patterns:
        print(highlighter.warning("No patterns found"))
        return 1
    
    print(highlighter.info(f"Found {len(patterns)} pattern(s):"))
    print()
    
    for p in patterns[:20]:
        print(f"  📌 {highlighter.bold(p.name)}")
        print(f"     Pattern: {p.pattern}")
        print(f"     Description: {p.description}")
        if p.examples:
            print(f"     Example: {p.examples[0]}")
        if p.flags:
            print(f"     Flags: {p.flags}")
        print()
    
    if len(patterns) > 20:
        print(f"  ... and {len(patterns) - 20} more patterns")
    
    return 0


def cmd_history(history: HistoryManager, highlighter: Highlighter, args) -> int:
    """Handle history command"""
    if args.clear:
        history.clear()
        print(highlighter.success("History cleared"))
        return 0
    
    entries = history.get_recent(args.count)
    
    if not entries:
        print(highlighter.info("No history entries"))
        return 0
    
    print(highlighter.info(f"Recent {len(entries)} history entries:"))
    print()
    
    for i, entry in enumerate(entries, 1):
        status = "✓" if entry.success else "✗"
        status_color = highlighter.success if entry.success else highlighter.error
        print(f"  {i}. {status_color(status)} {highlighter.bold(entry.pattern[:40])}")
        print(f"     Matches: {entry.match_count} | Flags: {entry.flags or 'none'} | {entry.timestamp[:19]}")
        if entry.test_text:
            preview = entry.test_text[:50] + "..." if len(entry.test_text) > 50 else entry.test_text
            print(f"     Text: {preview}")
        print()
    
    # Show stats
    stats = history.get_stats()
    print(highlighter.dim(f"  Stats: {stats['total_tests']} tests, {stats['unique_patterns']} unique patterns"))
    
    return 0


def build_flags(args) -> str:
    """Build flags string from args"""
    flags = getattr(args, 'flags', '') or ""
    
    if getattr(args, 'ignore_case', False):
        flags += 'i'
    if getattr(args, 'multiline', False):
        flags += 'm'
    if getattr(args, 'dotall', False):
        flags += 's'
    
    return flags


if __name__ == "__main__":
    sys.exit(main())
