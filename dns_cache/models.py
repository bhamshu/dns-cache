from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Optional


@dataclass(order=True, frozen=True)
class BSTKey:
    """Expiry index key stored in the SortedList.

    Ordered by (expires_at, domain).
    """
    expires_at: float
    domain: str


@dataclass
class CacheEntry:
    domain_name: str
    ipv4: str
    ttl_secs: int
    created_at: float = field(init=False, repr=False, compare=False)

    def __post_init__(self) -> None:
        self.created_at = time.time()

    @property
    def expires_at(self) -> float:
        return self.created_at + max(0, self.ttl_secs)

    def is_expired(self, now: Optional[float] = None) -> bool:
        if now is None:
            now = time.time()
        return now >= self.expires_at


@dataclass
class KVRecord:
    """Value we store in the kv dict of Store."""
    node: object  # dns_cache.lru.Node
    entry: CacheEntry
    bst_key: BSTKey
