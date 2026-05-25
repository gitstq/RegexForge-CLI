"""
RegexForge History Manager
历史记录管理器

Manages regex test history with local file storage.
"""

import json
import os
from datetime import datetime
from typing import List, Dict, Optional
from dataclasses import dataclass, asdict
import hashlib


@dataclass
class HistoryEntry:
    """A history entry for a regex test"""
    pattern: str
    test_text: str
    flags: str
    timestamp: str
    match_count: int
    success: bool
    
    def to_dict(self) -> Dict:
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'HistoryEntry':
        return cls(**data)


class HistoryManager:
    """
    Manages regex test history
    
    Features:
    - Local JSON file storage
    - Pattern deduplication
    - Search history
    - Export/Import
    """
    
    DEFAULT_MAX_ENTRIES = 100
    HISTORY_DIR = os.path.expanduser("~/.regexforge")
    HISTORY_FILE = os.path.join(HISTORY_DIR, "history.json")
    
    def __init__(self, max_entries: int = DEFAULT_MAX_ENTRIES):
        self.max_entries = max_entries
        self._ensure_dir()
        self._entries: List[HistoryEntry] = self._load()
    
    def _ensure_dir(self) -> None:
        """Ensure history directory exists"""
        os.makedirs(self.HISTORY_DIR, exist_ok=True)
    
    def _load(self) -> List[HistoryEntry]:
        """Load history from file"""
        if not os.path.exists(self.HISTORY_FILE):
            return []
        
        try:
            with open(self.HISTORY_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return [HistoryEntry.from_dict(e) for e in data]
        except (json.JSONDecodeError, KeyError):
            return []
    
    def _save(self) -> None:
        """Save history to file"""
        with open(self.HISTORY_FILE, 'w', encoding='utf-8') as f:
            json.dump([e.to_dict() for e in self._entries], f, indent=2, ensure_ascii=False)
    
    def add(
        self, 
        pattern: str, 
        test_text: str, 
        flags: str, 
        match_count: int, 
        success: bool
    ) -> HistoryEntry:
        """Add a new history entry"""
        entry = HistoryEntry(
            pattern=pattern,
            test_text=test_text[:500],  # Limit text length
            flags=flags,
            timestamp=datetime.now().isoformat(),
            match_count=match_count,
            success=success,
        )
        
        # Check for duplicate pattern
        existing_idx = None
        for i, e in enumerate(self._entries):
            if e.pattern == pattern and e.flags == flags:
                existing_idx = i
                break
        
        # Remove existing entry if found
        if existing_idx is not None:
            self._entries.pop(existing_idx)
        
        # Add new entry at the beginning
        self._entries.insert(0, entry)
        
        # Trim to max entries
        if len(self._entries) > self.max_entries:
            self._entries = self._entries[:self.max_entries]
        
        self._save()
        return entry
    
    def get_all(self) -> List[HistoryEntry]:
        """Get all history entries"""
        return self._entries.copy()
    
    def get_recent(self, count: int = 10) -> List[HistoryEntry]:
        """Get recent history entries"""
        return self._entries[:count]
    
    def search(self, query: str) -> List[HistoryEntry]:
        """Search history by pattern"""
        query = query.lower()
        return [
            e for e in self._entries
            if query in e.pattern.lower() or query in e.test_text.lower()
        ]
    
    def clear(self) -> None:
        """Clear all history"""
        self._entries = []
        self._save()
    
    def export_to_file(self, filepath: str) -> None:
        """Export history to a file"""
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump([e.to_dict() for e in self._entries], f, indent=2, ensure_ascii=False)
    
    def import_from_file(self, filepath: str) -> int:
        """Import history from a file"""
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
            imported = [HistoryEntry.from_dict(e) for e in data]
            self._entries.extend(imported)
            self._entries = self._entries[:self.max_entries]
            self._save()
            return len(imported)
    
    def get_patterns(self) -> List[str]:
        """Get unique patterns from history"""
        seen = set()
        patterns = []
        for e in self._entries:
            if e.pattern not in seen:
                seen.add(e.pattern)
                patterns.append(e.pattern)
        return patterns
    
    def get_stats(self) -> Dict:
        """Get history statistics"""
        if not self._entries:
            return {
                "total_tests": 0,
                "successful_tests": 0,
                "failed_tests": 0,
                "unique_patterns": 0,
                "total_matches": 0,
            }
        
        return {
            "total_tests": len(self._entries),
            "successful_tests": sum(1 for e in self._entries if e.success),
            "failed_tests": sum(1 for e in self._entries if not e.success),
            "unique_patterns": len(set(e.pattern for e in self._entries)),
            "total_matches": sum(e.match_count for e in self._entries),
        }
