"""
RegexForge Pattern Library
常用正则表达式模板库

A comprehensive collection of commonly used regex patterns
organized by category for quick reference and usage.
"""

from dataclasses import dataclass
from typing import Dict, List, Optional
from enum import Enum


class PatternCategory(Enum):
    """Pattern categories"""
    EMAIL = "Email"
    PHONE = "Phone"
    URL = "URL & Web"
    IP_ADDRESS = "IP Address"
    DATE_TIME = "Date & Time"
    NUMBER = "Number"
    STRING = "String"
    FILE = "File & Path"
    CODE = "Code & Programming"
    NETWORK = "Network"
    IDENTITY = "Identity & ID"
    HTML = "HTML & Markup"
    SECURITY = "Security"


@dataclass
class PatternInfo:
    """Information about a regex pattern"""
    name: str
    pattern: str
    description: str
    examples: List[str]
    flags: str = ""
    category: PatternCategory = PatternCategory.STRING


class PatternLibrary:
    """
    Library of commonly used regex patterns
    
    Features:
    - 50+ pre-built patterns
    - Organized by category
    - Examples and descriptions
    - Ready-to-use patterns
    """

    def __init__(self):
        self._patterns: Dict[str, PatternInfo] = {}
        self._by_category: Dict[PatternCategory, List[str]] = {
            cat: [] for cat in PatternCategory
        }
        self._load_patterns()

    def _add_pattern(self, info: PatternInfo) -> None:
        """Add a pattern to the library"""
        key = info.name.lower().replace(" ", "_")
        self._patterns[key] = info
        self._by_category[info.category].append(key)

    def _load_patterns(self) -> None:
        """Load all patterns into the library"""
        
        # === EMAIL ===
        self._add_pattern(PatternInfo(
            name="Email",
            pattern=r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",
            description="Standard email address format",
            examples=["user@example.com", "test.user+tag@domain.co.uk"],
            category=PatternCategory.EMAIL
        ))
        
        self._add_pattern(PatternInfo(
            name="Email Strict",
            pattern=r"(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|\"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*\")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])",
            description="RFC 5322 compliant email validation",
            examples=["user@example.com"],
            category=PatternCategory.EMAIL
        ))

        # === PHONE ===
        self._add_pattern(PatternInfo(
            name="Phone US",
            pattern=r"(?:\+?1[-.\s]?)?\(?[0-9]{3}\)?[-.\s]?[0-9]{3}[-.\s]?[0-9]{4}",
            description="US phone number format",
            examples=["+1-555-123-4567", "(555) 123-4567", "555.123.4567"],
            category=PatternCategory.PHONE
        ))
        
        self._add_pattern(PatternInfo(
            name="Phone China",
            pattern=r"(?:\+?86[-.\s]?)?1[3-9]\d{9}",
            description="Chinese mobile phone number",
            examples=["+8613812345678", "13812345678"],
            category=PatternCategory.PHONE
        ))
        
        self._add_pattern(PatternInfo(
            name="Phone International",
            pattern=r"\+(?:[0-9] ?){6,14}[0-9]",
            description="International phone number format",
            examples=["+44 20 7123 4567", "+81-3-1234-5678"],
            category=PatternCategory.PHONE
        ))

        # === URL ===
        self._add_pattern(PatternInfo(
            name="URL",
            pattern=r"https?://(?:www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b(?:[-a-zA-Z0-9()@:%_\+.~#?&/=]*)",
            description="HTTP/HTTPS URL format",
            examples=["https://www.example.com/path?query=value", "http://example.org"],
            category=PatternCategory.URL
        ))
        
        self._add_pattern(PatternInfo(
            name="URL Domain",
            pattern=r"(?:https?:\/\/)?(?:www\.)?([a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*\.[a-zA-Z]{2,})",
            description="Extract domain from URL",
            examples=["example.com", "sub.domain.co.uk"],
            category=PatternCategory.URL
        ))
        
        self._add_pattern(PatternInfo(
            name="Slug",
            pattern=r"[a-z0-9]+(?:-[a-z0-9]+)*",
            description="URL-friendly slug format",
            examples=["my-blog-post", "product-123"],
            category=PatternCategory.URL
        ))

        # === IP ADDRESS ===
        self._add_pattern(PatternInfo(
            name="IPv4",
            pattern=r"(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)",
            description="IPv4 address format",
            examples=["192.168.1.1", "10.0.0.1", "255.255.255.0"],
            category=PatternCategory.IP_ADDRESS
        ))
        
        self._add_pattern(PatternInfo(
            name="IPv6",
            pattern=r"(?:[0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}",
            description="IPv6 address format (full notation)",
            examples=["2001:0db8:85a3:0000:0000:8a2e:0370:7334"],
            category=PatternCategory.IP_ADDRESS
        ))
        
        self._add_pattern(PatternInfo(
            name="IPv4 or IPv6",
            pattern=r"(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)|(?:[0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}",
            description="Match either IPv4 or IPv6",
            examples=["192.168.1.1", "2001:db8::1"],
            category=PatternCategory.IP_ADDRESS
        ))

        # === DATE & TIME ===
        self._add_pattern(PatternInfo(
            name="Date ISO",
            pattern=r"\d{4}-\d{2}-\d{2}",
            description="ISO 8601 date format (YYYY-MM-DD)",
            examples=["2024-01-15", "2023-12-31"],
            category=PatternCategory.DATE_TIME
        ))
        
        self._add_pattern(PatternInfo(
            name="Date US",
            pattern=r"(?:0[1-9]|1[0-2])/(?:0[1-9]|[12][0-9]|3[01])/\d{4}",
            description="US date format (MM/DD/YYYY)",
            examples=["01/15/2024", "12/31/2023"],
            category=PatternCategory.DATE_TIME
        ))
        
        self._add_pattern(PatternInfo(
            name="Date EU",
            pattern=r"(?:0[1-9]|[12][0-9]|3[01])/(?:0[1-9]|1[0-2])/\d{4}",
            description="European date format (DD/MM/YYYY)",
            examples=["15/01/2024", "31/12/2023"],
            category=PatternCategory.DATE_TIME
        ))
        
        self._add_pattern(PatternInfo(
            name="Time 24h",
            pattern=r"(?:[01]?[0-9]|2[0-3]):[0-5][0-9](?::[0-5][0-9])?",
            description="24-hour time format",
            examples=["14:30", "23:59:59", "00:00"],
            category=PatternCategory.DATE_TIME
        ))
        
        self._add_pattern(PatternInfo(
            name="Time 12h",
            pattern=r"(?:1[0-2]|0?[1-9]):[0-5][0-9](?::[0-5][0-9])?\s?(?:[AP]M|[ap]m)?",
            description="12-hour time format with optional AM/PM",
            examples=["2:30 PM", "11:59:59 pm", "12:00"],
            category=PatternCategory.DATE_TIME
        ))
        
        self._add_pattern(PatternInfo(
            name="DateTime ISO",
            pattern=r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})?",
            description="ISO 8601 datetime format",
            examples=["2024-01-15T14:30:00Z", "2024-01-15T14:30:00+08:00"],
            category=PatternCategory.DATE_TIME
        ))

        # === NUMBER ===
        self._add_pattern(PatternInfo(
            name="Integer",
            pattern=r"[+-]?\d+",
            description="Integer number",
            examples=["123", "-456", "+789"],
            category=PatternCategory.NUMBER
        ))
        
        self._add_pattern(PatternInfo(
            name="Decimal",
            pattern=r"[+-]?\d+\.\d+",
            description="Decimal number",
            examples=["3.14", "-0.5", "+99.99"],
            category=PatternCategory.NUMBER
        ))
        
        self._add_pattern(PatternInfo(
            name="Scientific Notation",
            pattern=r"[+-]?\d+(?:\.\d+)?[eE][+-]?\d+",
            description="Scientific notation",
            examples=["1.23e10", "5E-3", "-2.5e+5"],
            category=PatternCategory.NUMBER
        ))
        
        self._add_pattern(PatternInfo(
            name="Hex Color",
            pattern=r"#(?:[0-9a-fA-F]{3}){1,2}",
            description="Hexadecimal color code",
            examples=["#FF5733", "#fff", "#00FF00"],
            category=PatternCategory.NUMBER
        ))
        
        self._add_pattern(PatternInfo(
            name="Hex Number",
            pattern=r"0[xX][0-9a-fA-F]+",
            description="Hexadecimal number",
            examples=["0xFF", "0x1A2B", "0XDEADBEEF"],
            category=PatternCategory.NUMBER
        ))
        
        self._add_pattern(PatternInfo(
            name="Binary",
            pattern=r"0[bB][01]+",
            description="Binary number",
            examples=["0b1010", "0B11110000"],
            category=PatternCategory.NUMBER
        ))

        # === STRING ===
        self._add_pattern(PatternInfo(
            name="Username",
            pattern=r"[a-zA-Z][a-zA-Z0-9_-]{2,15}",
            description="Username (letter start, alphanumeric with _ and -)",
            examples=["john_doe", "User123", "my-name"],
            category=PatternCategory.STRING
        ))
        
        self._add_pattern(PatternInfo(
            name="Password Strong",
            pattern=r"(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}",
            description="Strong password (8+ chars, upper, lower, digit, special)",
            examples=["Passw0rd!", "Str0ng@Pass"],
            category=PatternCategory.STRING
        ))
        
        self._add_pattern(PatternInfo(
            name="Whitespace",
            pattern=r"\s+",
            description="Match any whitespace",
            examples=[" ", "\t", "\n", "   "],
            category=PatternCategory.STRING
        ))
        
        self._add_pattern(PatternInfo(
            name="Word",
            pattern=r"\b\w+\b",
            description="Match whole words",
            examples=["hello", "world", "test123"],
            category=PatternCategory.STRING
        ))

        # === FILE & PATH ===
        self._add_pattern(PatternInfo(
            name="File Extension",
            pattern=r"\.([a-zA-Z0-9]+)$",
            description="Extract file extension",
            examples=[".txt", ".py", ".jpg"],
            category=PatternCategory.FILE
        ))
        
        self._add_pattern(PatternInfo(
            name="Filename",
            pattern=r"[^/\\?%*:|\"<>\n]+",
            description="Valid filename (no special chars)",
            examples=["document.pdf", "image (1).jpg"],
            category=PatternCategory.FILE
        ))
        
        self._add_pattern(PatternInfo(
            name="Path Unix",
            pattern=r"(?:/[\w.-]+)+",
            description="Unix-style file path",
            examples=["/home/user/file.txt", "/var/log/app.log"],
            category=PatternCategory.FILE
        ))
        
        self._add_pattern(PatternInfo(
            name="Path Windows",
            pattern=r"[A-Za-z]:\\(?:[\w\s-]+\\)*[\w\s-]+",
            description="Windows-style file path",
            examples=["C:\\Users\\file.txt", "D:\\Projects\\app.py"],
            category=PatternCategory.FILE
        ))

        # === CODE ===
        self._add_pattern(PatternInfo(
            name="Function Name",
            pattern=r"\b[a-z_][a-z0-9_]*(?=\s*\()",
            description="Function name (snake_case)",
            examples=["my_function", "test1", "_private"],
            category=PatternCategory.CODE
        ))
        
        self._add_pattern(PatternInfo(
            name="Class Name",
            pattern=r"\b[A-Z][a-zA-Z0-9]*\b",
            description="Class name (PascalCase)",
            examples=["MyClass", "HttpClient", "UserDTO"],
            category=PatternCategory.CODE
        ))
        
        self._add_pattern(PatternInfo(
            name="Variable Name",
            pattern=r"\b[a-z_][a-zA-Z0-9_]*\b",
            description="Variable name (camelCase or snake_case)",
            examples=["myVar", "user_name", "_count"],
            category=PatternCategory.CODE
        ))
        
        self._add_pattern(PatternInfo(
            name="Comment Single Line",
            pattern=r"//.*$|#.*$",
            description="Single-line comment (// or #)",
            examples=["// This is a comment", "# Python comment"],
            flags="m",
            category=PatternCategory.CODE
        ))
        
        self._add_pattern(PatternInfo(
            name="String Double Quote",
            pattern=r'"(?:[^"\\]|\\.)*"',
            description="Double-quoted string",
            examples=['"hello world"', '"escaped \\"quote\\""'],
            category=PatternCategory.CODE
        ))
        
        self._add_pattern(PatternInfo(
            name="String Single Quote",
            pattern=r"'(?:[^'\\]|\\.)*'",
            description="Single-quoted string",
            examples=["'hello world'", "'escaped \\'quote\\''"],
            category=PatternCategory.CODE
        ))

        # === NETWORK ===
        self._add_pattern(PatternInfo(
            name="MAC Address",
            pattern=r"(?:[0-9A-Fa-f]{2}[:-]){5}[0-9A-Fa-f]{2}",
            description="MAC address format",
            examples=["00:1A:2B:3C:4D:5E", "00-1A-2B-3C-4D-5E"],
            category=PatternCategory.NETWORK
        ))
        
        self._add_pattern(PatternInfo(
            name="Port Number",
            pattern=r":([1-9][0-9]{0,4})",
            description="Port number from URL",
            examples=[":80", ":443", ":8080"],
            category=PatternCategory.NETWORK
        ))
        
        self._add_pattern(PatternInfo(
            name="Subnet Mask",
            pattern=r"(?:255\.){2}(?:255|254|252|248|240|224|192|128|0)\.0",
            description="Subnet mask format",
            examples=["255.255.255.0", "255.255.254.0"],
            category=PatternCategory.NETWORK
        ))

        # === IDENTITY ===
        self._add_pattern(PatternInfo(
            name="UUID",
            pattern=r"[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}",
            description="UUID/GUID format",
            examples=["550e8400-e29b-41d4-a716-446655440000"],
            category=PatternCategory.IDENTITY
        ))
        
        self._add_pattern(PatternInfo(
            name="SSN US",
            pattern=r"\d{3}-\d{2}-\d{4}",
            description="US Social Security Number",
            examples=["123-45-6789"],
            category=PatternCategory.IDENTITY
        ))
        
        self._add_pattern(PatternInfo(
            name="Credit Card",
            pattern=r"\b(?:\d{4}[-\s]?){3}\d{4}\b",
            description="Credit card number format",
            examples=["1234-5678-9012-3456", "1234 5678 9012 3456"],
            category=PatternCategory.IDENTITY
        ))
        
        self._add_pattern(PatternInfo(
            name="ID Card China",
            pattern=r"[1-9]\d{5}(?:19|20)\d{2}(?:0[1-9]|1[0-2])(?:0[1-9]|[12]\d|3[01])\d{3}[\dXx]",
            description="Chinese ID card number (18 digits)",
            examples=["11010519900307233X"],
            category=PatternCategory.IDENTITY
        ))

        # === HTML ===
        self._add_pattern(PatternInfo(
            name="HTML Tag",
            pattern=r"</?[a-zA-Z][a-zA-Z0-9]*[^>]*>",
            description="HTML tag",
            examples=["<div>", "</span>", '<input type="text">'],
            category=PatternCategory.HTML
        ))
        
        self._add_pattern(PatternInfo(
            name="HTML Attribute",
            pattern=r'([a-zA-Z-]+)=["\']([^"\']*)["\']',
            description="HTML attribute with value",
            examples=['class="container"', 'id="main"'],
            category=PatternCategory.HTML
        ))
        
        self._add_pattern(PatternInfo(
            name="HTML Link",
            pattern=r'<a[^>]+href=["\']([^"\']+)["\'][^>]*>([^<]+)</a>',
            description="Extract link URL and text",
            examples=['<a href="https://example.com">Click here</a>'],
            category=PatternCategory.HTML
        ))

        # === SECURITY ===
        self._add_pattern(PatternInfo(
            name="JWT",
            pattern=r"eyJ[a-zA-Z0-9_-]*\.eyJ[a-zA-Z0-9_-]*\.[a-zA-Z0-9_-]*",
            description="JSON Web Token format",
            examples=["eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"],
            category=PatternCategory.SECURITY
        ))
        
        self._add_pattern(PatternInfo(
            name="API Key",
            pattern=r"(?:api[_-]?key|apikey|api[_-]?secret|token|bearer)[\s:=]+['\"]?([a-zA-Z0-9_\-]{20,})['\"]?",
            description="API key pattern",
            examples=["api_key: sk-1234567890abcdef"],
            flags="i",
            category=PatternCategory.SECURITY
        ))
        
        self._add_pattern(PatternInfo(
            name="Base64",
            pattern=r"(?:[A-Za-z0-9+/]{4})*(?:[A-Za-z0-9+/]{2}==|[A-Za-z0-9+/]{3}=)?",
            description="Base64 encoded string",
            examples=["SGVsbG8gV29ybGQ=", "TWFueSBoYW5kcyBtYWtlIGxpZ2h0IHdvcmsu"],
            category=PatternCategory.SECURITY
        ))

    def get(self, name: str) -> Optional[PatternInfo]:
        """Get a pattern by name"""
        key = name.lower().replace(" ", "_")
        return self._patterns.get(key)

    def list_all(self) -> List[PatternInfo]:
        """List all patterns"""
        return list(self._patterns.values())

    def list_by_category(self, category: PatternCategory) -> List[PatternInfo]:
        """List patterns by category"""
        keys = self._by_category.get(category, [])
        return [self._patterns[k] for k in keys]

    def search(self, query: str) -> List[PatternInfo]:
        """Search patterns by name or description"""
        query = query.lower()
        return [
            p for p in self._patterns.values()
            if query in p.name.lower() or query in p.description.lower()
        ]

    def get_categories(self) -> List[PatternCategory]:
        """Get all categories"""
        return list(PatternCategory)
