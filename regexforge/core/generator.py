"""
RegexForge Code Generator
多语言代码生成器

Generates ready-to-use code snippets in multiple programming languages
from regex patterns.
"""

from dataclasses import dataclass
from typing import Optional, List
from enum import Enum


class Language(Enum):
    """Supported programming languages"""
    PYTHON = "python"
    JAVASCRIPT = "javascript"
    TYPESCRIPT = "typescript"
    GO = "go"
    RUST = "rust"
    JAVA = "java"
    PHP = "php"
    RUBY = "ruby"


@dataclass
class GeneratedCode:
    """Container for generated code"""
    language: str
    code: str
    description: str


class CodeGenerator:
    """
    Multi-language code generator for regex patterns
    
    Features:
    - Generate code in 8+ programming languages
    - Include all regex flags
    - Add helpful comments
    - Ready-to-copy snippets
    """

    FLAG_COMMENTS = {
        "i": "Case-insensitive",
        "m": "Multiline mode",
        "s": "Dot matches newline",
        "x": "Verbose mode",
        "a": "ASCII-only",
        "u": "Unicode mode",
    }

    def __init__(self):
        self._generators = {
            Language.PYTHON: self._generate_python,
            Language.JAVASCRIPT: self._generate_javascript,
            Language.TYPESCRIPT: self._generate_typescript,
            Language.GO: self._generate_go,
            Language.RUST: self._generate_rust,
            Language.JAVA: self._generate_java,
            Language.PHP: self._generate_php,
            Language.RUBY: self._generate_ruby,
        }

    def generate(
        self, 
        pattern: str, 
        language: Language,
        flags: str = "",
        test_text: Optional[str] = None,
        variable_name: str = "pattern"
    ) -> GeneratedCode:
        """
        Generate code for a regex pattern
        
        Args:
            pattern: Regex pattern string
            language: Target language
            flags: Flag string like "ims"
            test_text: Optional test text to include
            variable_name: Variable name for the pattern
            
        Returns:
            GeneratedCode object
        """
        generator = self._generators.get(language, self._generate_python)
        return generator(pattern, flags, test_text, variable_name)

    def generate_all(
        self, 
        pattern: str, 
        flags: str = "",
        test_text: Optional[str] = None
    ) -> List[GeneratedCode]:
        """
        Generate code for all supported languages
        
        Args:
            pattern: Regex pattern string
            flags: Flag string like "ims"
            test_text: Optional test text to include
            
        Returns:
            List of GeneratedCode objects
        """
        return [
            self.generate(pattern, lang, flags, test_text)
            for lang in Language
        ]

    def _get_flag_comments(self, flags: str) -> List[str]:
        """Get comments for used flags"""
        return [
            self.FLAG_COMMENTS[f] 
            for f in flags.lower() 
            if f in self.FLAG_COMMENTS
        ]

    def _escape_string(self, s: str, language: Language) -> str:
        """Escape string for target language"""
        if not s:
            return ""
        
        # Common escapes
        s = s.replace("\\", "\\\\")
        s = s.replace('"', '\\"')
        s = s.replace("\n", "\\n")
        s = s.replace("\r", "\\r")
        s = s.replace("\t", "\\t")
        
        return s

    def _generate_python(
        self, 
        pattern: str, 
        flags: str,
        test_text: Optional[str],
        var_name: str
    ) -> GeneratedCode:
        """Generate Python code"""
        flag_comments = self._get_flag_comments(flags)
        
        lines = [
            "import re",
            "",
            f"# Pattern: {pattern}",
        ]
        
        if flag_comments:
            lines.append(f"# Flags: {', '.join(flag_comments)}")
        
        lines.extend([
            f'{var_name} = r"{self._escape_string(pattern, Language.PYTHON)}"',
            "",
        ])
        
        # Build flags
        if flags:
            flag_code = " | ".join(f"re.{f.upper()}" for f in flags.lower() if f in "imsxau")
            lines.append(f"flags = {flag_code}")
            lines.append(f"regex = re.compile({var_name}, flags)")
        else:
            lines.append(f"regex = re.compile({var_name})")
        
        if test_text:
            lines.extend([
                "",
                f'text = """{test_text}"""',
                "",
                "# Find all matches",
                "matches = regex.findall(text)",
                'print(f"Found {len(matches)} matches:")',
                "for match in matches:",
                '    print(f"  - {match}")',
                "",
                "# Search for first match",
                "match = regex.search(text)",
                "if match:",
                '    print(f"First match: {match.group()}")',
                "    print(f\"Groups: {match.groups()}\")",
            ])
        else:
            lines.extend([
                "",
                "# Usage examples:",
                '# matches = regex.findall("your text here")',
                '# match = regex.search("your text here")',
            ])
        
        return GeneratedCode(
            language="Python",
            code="\n".join(lines),
            description="Python re module usage"
        )

    def _generate_javascript(
        self, 
        pattern: str, 
        flags: str,
        test_text: Optional[str],
        var_name: str
    ) -> GeneratedCode:
        """Generate JavaScript code"""
        flag_comments = self._get_flag_comments(flags)
        
        # JavaScript uses inline flags
        js_flags = flags.lower().replace("a", "").replace("u", "")
        
        lines = [
            f"// Pattern: {pattern}",
        ]
        
        if flag_comments:
            lines.append(f"// Flags: {', '.join(flag_comments)}")
        
        lines.extend([
            f"const {var_name} = /{pattern}/{js_flags};",
            "",
        ])
        
        if test_text:
            escaped_text = self._escape_string(test_text, Language.JAVASCRIPT)
            lines.extend([
                f'const text = "{escaped_text}";',
                "",
                "// Find all matches",
                "const matches = text.match(new RegExp(pattern, 'g'));",
                'console.log(`Found ${matches ? matches.length : 0} matches:`);',
                "matches?.forEach(match => console.log(`  - ${match}`));",
                "",
                "// Get first match with groups",
                "const match = pattern.exec(text);",
                "if (match) {",
                '  console.log(`First match: ${match[0]}`);',
                '  console.log(`Groups: ${match.slice(1)}`);',
                "}",
            ])
        else:
            lines.extend([
                "// Usage examples:",
                '// const matches = text.match(new RegExp(pattern, "g"));',
                "// const match = pattern.exec(text);",
            ])
        
        return GeneratedCode(
            language="JavaScript",
            code="\n".join(lines),
            description="JavaScript RegExp usage"
        )

    def _generate_typescript(
        self, 
        pattern: str, 
        flags: str,
        test_text: Optional[str],
        var_name: str
    ) -> GeneratedCode:
        """Generate TypeScript code"""
        js_code = self._generate_javascript(pattern, flags, test_text, var_name)
        
        # Add TypeScript types
        ts_code = js_code.code.replace(
            "const matches =",
            "const matches: RegExpMatchArray | null ="
        ).replace(
            "const match =",
            "const match: RegExpExecArray | null ="
        )
        
        return GeneratedCode(
            language="TypeScript",
            code=ts_code,
            description="TypeScript RegExp usage"
        )

    def _generate_go(
        self, 
        pattern: str, 
        flags: str,
        test_text: Optional[str],
        var_name: str
    ) -> GeneratedCode:
        """Generate Go code"""
        flag_comments = self._get_flag_comments(flags)
        
        # Go uses (?flags) syntax
        go_flags = ""
        if "i" in flags.lower():
            go_flags += "i"
        if "m" in flags.lower():
            go_flags += "m"
        if "s" in flags.lower():
            go_flags += "s"
        
        pattern_with_flags = f"(?{go_flags}){pattern}" if go_flags else pattern
        
        lines = [
            'package main',
            '',
            'import (',
            '    "fmt"',
            '    "regexp"',
            ')',
            '',
            'func main() {',
            f'    // Pattern: {pattern}',
        ]
        
        if flag_comments:
            lines.append(f'    // Flags: {", ".join(flag_comments)}')
        
        lines.extend([
            f'    {var_name} := `{pattern_with_flags}`',
            '',
            f'    re := regexp.MustCompile({var_name})',
        ])
        
        if test_text:
            lines.extend([
                '',
                f'    text := `{test_text}`',
                '',
                '    // Find all matches',
                '    matches := re.FindAllString(text, -1)',
                '    fmt.Printf("Found %d matches:\\n", len(matches))',
                '    for _, match := range matches {',
                '        fmt.Printf("  - %s\\n", match)',
                '    }',
                '',
                '    // Find with submatches',
                '    submatches := re.FindAllStringSubmatch(text, -1)',
                '    for _, sub := range submatches {',
                '        fmt.Printf("Match: %s, Groups: %v\\n", sub[0], sub[1:])',
                '    }',
            ])
        else:
            lines.extend([
                '',
                '    // Usage examples:',
                '    // matches := re.FindAllString("your text", -1)',
                '    // match := re.FindString("your text")',
            ])
        
        lines.append('}')
        
        return GeneratedCode(
            language="Go",
            code="\n".join(lines),
            description="Go regexp package usage"
        )

    def _generate_rust(
        self, 
        pattern: str, 
        flags: str,
        test_text: Optional[str],
        var_name: str
    ) -> GeneratedCode:
        """Generate Rust code"""
        flag_comments = self._get_flag_comments(flags)
        
        lines = [
            'use regex::Regex;',
            '',
            f'// Pattern: {pattern}',
        ]
        
        if flag_comments:
            lines.append(f'// Flags: {", ".join(flag_comments)}')
        
        # Rust uses inline flags
        rust_flags = ""
        if "i" in flags.lower():
            rust_flags += "i"
        if "m" in flags.lower():
            rust_flags += "m"
        if "s" in flags.lower():
            rust_flags += "s"
        
        pattern_with_flags = f"(?{rust_flags}){pattern}" if rust_flags else pattern
        
        lines.extend([
            '',
            'fn main() {',
            f'    let {var_name} = r#"{pattern_with_flags}"#;',
            '    let re = Regex::new(pattern).unwrap();',
        ])
        
        if test_text:
            lines.extend([
                '',
                f'    let text = r#"{test_text}"#;',
                '',
                '    // Find all matches',
                '    let matches: Vec<_> = re.find_iter(text).collect();',
                '    println!("Found {} matches:", matches.len());',
                '    for m in &matches {',
                '        println!("  - {}", m.as_str());',
                '    }',
                '',
                '    // Capture groups',
                '    if let Some(caps) = re.captures(text) {',
                '        println!("First match: {}", &caps[0]);',
                '        for (i, cap) in caps.iter().enumerate().skip(1) {',
                '            if let Some(m) = cap {',
                '                println!("Group {}: {}", i, m.as_str());',
                '            }',
                '        }',
                '    }',
            ])
        else:
            lines.extend([
                '',
                '    // Usage examples:',
                '    // let matches: Vec<_> = re.find_iter("your text").collect();',
                '    // if let Some(caps) = re.captures("your text") { ... }',
            ])
        
        lines.append('}')
        
        return GeneratedCode(
            language="Rust",
            code="\n".join(lines),
            description="Rust regex crate usage"
        )

    def _generate_java(
        self, 
        pattern: str, 
        flags: str,
        test_text: Optional[str],
        var_name: str
    ) -> GeneratedCode:
        """Generate Java code"""
        flag_comments = self._get_flag_comments(flags)
        
        lines = [
            'import java.util.regex.*;',
            '',
            'public class RegexExample {',
            '    public static void main(String[] args) {',
            f'        // Pattern: {pattern}',
        ]
        
        if flag_comments:
            lines.append(f'        // Flags: {", ".join(flag_comments)}')
        
        # Build flags
        if flags:
            flag_code = " | ".join(
                f"Pattern.{f.upper()}" 
                for f in flags.lower() 
                if f in "ims"
            )
            lines.extend([
                f'        String {var_name} = "{self._escape_string(pattern, Language.JAVA)}";',
                f'        Pattern re = Pattern.compile({var_name}, {flag_code});',
            ])
        else:
            lines.extend([
                f'        String {var_name} = "{self._escape_string(pattern, Language.JAVA)}";',
                f'        Pattern re = Pattern.compile({var_name});',
            ])
        
        if test_text:
            lines.extend([
                '',
                f'        String text = "{self._escape_string(test_text, Language.JAVA)}";',
                '',
                '        // Find all matches',
                '        Matcher matcher = re.matcher(text);',
                '        int count = 0;',
                '        while (matcher.find()) {',
                '            count++;',
                '            System.out.println("  - " + matcher.group());',
                '        }',
                '        System.out.println("Found " + count + " matches");',
            ])
        else:
            lines.extend([
                '',
                '        // Usage:',
                '        // Matcher matcher = re.matcher("your text");',
                '        // while (matcher.find()) { ... }',
            ])
        
        lines.extend([
            '    }',
            '}',
        ])
        
        return GeneratedCode(
            language="Java",
            code="\n".join(lines),
            description="Java Pattern/Matcher usage"
        )

    def _generate_php(
        self, 
        pattern: str, 
        flags: str,
        test_text: Optional[str],
        var_name: str
    ) -> GeneratedCode:
        """Generate PHP code"""
        flag_comments = self._get_flag_comments(flags)
        
        # PHP flags
        php_flags = ""
        if "i" in flags.lower():
            php_flags += "i"
        if "m" in flags.lower():
            php_flags += "m"
        if "s" in flags.lower():
            php_flags += "s"
        
        lines = [
            '<?php',
            '',
            f'// Pattern: {pattern}',
        ]
        
        if flag_comments:
            lines.append(f'// Flags: {", ".join(flag_comments)}')
        
        lines.extend([
            f'${var_name} = \'/\' . \'{self._escape_string(pattern, Language.PHP)}\' . \'/\' . \'{php_flags}\';',
            '',
        ])
        
        if test_text:
            lines.extend([
                f'$text = \'{test_text}\';',
                '',
                '// Find all matches',
                'preg_match_all($pattern, $text, $matches);',
                'echo "Found " . count($matches[0]) . " matches:\\n";',
                'foreach ($matches[0] as $match) {',
                '    echo "  - " . $match . "\\n";',
                '}',
                '',
                '// Match with groups',
                'if (preg_match($pattern, $text, $groups)) {',
                '    echo "First match: " . $groups[0] . "\\n";',
                '    echo "Groups: " . implode(", ", array_slice($groups, 1)) . "\\n";',
                '}',
            ])
        else:
            lines.extend([
                '// Usage examples:',
                '// preg_match_all($pattern, $text, $matches);',
                '// preg_match($pattern, $text, $groups);',
            ])
        
        lines.extend(['', '?>'])
        
        return GeneratedCode(
            language="PHP",
            code="\n".join(lines),
            description="PHP preg functions usage"
        )

    def _generate_ruby(
        self, 
        pattern: str, 
        flags: str,
        test_text: Optional[str],
        var_name: str
    ) -> GeneratedCode:
        """Generate Ruby code"""
        flag_comments = self._get_flag_comments(flags)
        
        # Ruby flags
        ruby_flags = ""
        if "i" in flags.lower():
            ruby_flags += "i"
        if "m" in flags.lower():
            ruby_flags += "m"
        if "s" in flags.lower():
            ruby_flags += "m"  # Ruby uses m for DOTALL
        
        lines = [
            f'# Pattern: {pattern}',
        ]
        
        if flag_comments:
            lines.append(f'# Flags: {", ".join(flag_comments)}')
        
        lines.extend([
            f'{var_name} = /{pattern}/{ruby_flags}',
            '',
        ])
        
        if test_text:
            lines.extend([
                f'text = <<~TEXT',
                test_text,
                'TEXT',
                '',
                '# Find all matches',
                'matches = text.scan(pattern)',
                'puts "Found #{matches.length} matches:"',
                'matches.each { |m| puts "  - #{m}" }',
                '',
                '# Match with groups',
                'if match = pattern.match(text)',
                '  puts "First match: #{match[0]}"',
                '  puts "Groups: #{match.captures}"',
                'end',
            ])
        else:
            lines.extend([
                '# Usage examples:',
                '# matches = text.scan(pattern)',
                '# if match = pattern.match(text) ...',
            ])
        
        return GeneratedCode(
            language="Ruby",
            code="\n".join(lines),
            description="Ruby Regexp usage"
        )
