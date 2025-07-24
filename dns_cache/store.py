from __future__ import annotations

import time
import threading
from typing import Dict, Optional

from sortedcontainers import SortedList

from .lru import DLL, Node
from .models import CacheEntry, KVRecord, BSTKey


class Store:
    """TTL + LRU store.

    - LRU: DLL (head = LRU, tail = MRU)
    - Expiry index: SortedList holding BSTKey(expires_at, domain)
    - kv: key -> KVRecord(node, entry, bst_key)
    """

    def __init__(self, max_capacity: int):
        if max_capacity < 0:
            raise ValueError("max_capacity cannot be negative")
        self.max_capacity = max_capacity
        self.dll = DLL()
        self.bst: SortedList[BSTKey] = SortedList()
        self.kv: Dict[str, KVRecord] = {}
        self._lock = threading.RLock()

    @property
    def used(self) -> int:
        return len(self.kv)

    def put(self, domain_name: str, entry: CacheEntry) -> None:
        now = time.time()
        if entry.ttl_secs <= 0:
            with self._lock:
                self._remove_key(domain_name)
            return

        with self._lock:
            self._evict_expired(now)

            expires_at = entry.expires_at
            new_bst_key = BSTKey(expires_at=expires_at, domain=domain_name)

            if domain_name in self.kv:
                kv_rec = self.kv[domain_name]
                # Remove old
                self.bst.discard(kv_rec.bst_key)
                # Insert new
                self.bst.add(new_bst_key)
                kv_rec.entry = entry
                kv_rec.bst_key = new_bst_key
                # Touch LRU
                self.dll.move_to_tail(kv_rec.node)
                return

            if self.max_capacity == 0:
                return

            self._ensure_capacity(now)
            if self.used >= self.max_capacity:
                return

            node = Node(domain_name)
            self.dll.append(node)
            self.bst.add(new_bst_key)
            self.kv[domain_name] = KVRecord(node=node, entry=entry, bst_key=new_bst_key)

    def get(self, domain_name: str) -> Optional[CacheEntry]:
        now = time.time()
        with self._lock:
            kv_rec = self.kv.get(domain_name)
            if not kv_rec:
                self._evict_expired(now)
                return None

            if kv_rec.entry.is_expired(now):
                self._remove_key(domain_name)
                return None

            self.dll.move_to_tail(kv_rec.node)
            return kv_rec.entry

    def delete(self, domain_name: str) -> None:
        with self._lock:
            self._remove_key(domain_name)

    def _ensure_capacity(self, now: float) -> None:
        self._evict_expired(now)
        while self.used > 0 and self.used >= self.max_capacity:
            lru = self.dll.pop_head()
            if not lru:
                break
            self._remove_key(lru.val, already_popped_from_dll=True)

    def _evict_expired(self, now: float) -> None:
        while self.bst and self.bst[0].expires_at <= now:
            key = self.bst.pop(0)
            kv_rec = self.kv.pop(key.domain, None)
            if not kv_rec:
                continue
            self.dll.remove_node(kv_rec.node)

    def _remove_key(self, domain_name: str, already_popped_from_dll: bool = False) -> None:
        kv_rec = self.kv.pop(domain_name, None)
        if not kv_rec:
            return
        self.bst.discard(kv_rec.bst_key)
        if not already_popped_from_dll:
            self.dll.remove_node(kv_rec.node)
