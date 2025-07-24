from __future__ import annotations

from typing import Optional

from .store import Store
from .models import CacheEntry
from .validators import valid_domain, valid_ipv4


class DNSCache:
    def __init__(self, store: Store):
        self._store = store

    def get(self, domain_name: str) -> Optional[str]:
        entry = self._store.get(domain_name)
        return entry.ipv4 if entry else None

    def put(self, domain_name: str, ipv4: str, ttl_secs: int) -> None:
        if not valid_domain(domain_name):
            raise ValueError(f"Invalid domain_name: {domain_name}")
        if not valid_ipv4(ipv4):
            raise ValueError(f"Invalid IPv4 address: {ipv4}")
        entry = CacheEntry(domain_name, ipv4, ttl_secs)
        self._store.put(domain_name, entry)

    def delete(self, domain_name: str) -> None:
        self._store.delete(domain_name)
