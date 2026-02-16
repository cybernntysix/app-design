# Data model for Song, Platform, and RoyaltySplit
from dataclasses import dataclass, field
from typing import List, Dict, Optional

@dataclass
class RoyaltySplit:
    publishing: float = 0.0  # percent
    mechanical: float = 0.0  # percent
    other: float = 0.0      # percent

@dataclass
class PlatformStats:
    name: str
    streams: int = 0
    followers: int = 0
    revenue: float = 0.0

@dataclass
class Song:
    title: str
    alias: Optional[str] = None
    ipi: Optional[str] = None
    isrc: Optional[str] = None
    platforms: List[PlatformStats] = field(default_factory=list)
    royalty_split: RoyaltySplit = field(default_factory=RoyaltySplit)
    notes: str = ''

    def total_streams(self):
        return sum(p.streams for p in self.platforms)

    def total_revenue(self):
        return sum(p.revenue for p in self.platforms)

    def quarterly_revenue(self):
        # Placeholder: implement logic to split revenue by quarter
        return {}
