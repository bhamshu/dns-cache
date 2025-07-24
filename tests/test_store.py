import time

from dns_cache.store import Store
from dns_cache.models import CacheEntry


def test_put_get_basic():
    s = Store(max_capacity=2)
    e = CacheEntry("example.com", "1.1.1.1", ttl_secs=10)
    s.put("example.com", e)

    got = s.get("example.com")
    assert got is not None
    assert got.ipv4 == "1.1.1.1"


def test_expiry():
    s = Store(max_capacity=2)
    e = CacheEntry("foo.com", "2.2.2.2", ttl_secs=0)
    s.put("foo.com", e)  # should not be stored
    assert s.get("foo.com") is None

    e2 = CacheEntry("bar.com", "3.3.3.3", ttl_secs=1)
    s.put("bar.com", e2)
    assert s.get("bar.com") is not None
    time.sleep(1.1)
    assert s.get("bar.com") is None


def test_lru_eviction():
    s = Store(max_capacity=2)
    s.put("a.com", CacheEntry("a.com", "1.1.1.1", ttl_secs=100))
    s.put("b.com", CacheEntry("b.com", "2.2.2.2", ttl_secs=100))
    # Access a.com to make it MRU
    assert s.get("a.com") is not None

    # Inserting c.com should evict b.com (the LRU)
    s.put("c.com", CacheEntry("c.com", "3.3.3.3", ttl_secs=100))

    assert s.get("b.com") is None
    assert s.get("a.com") is not None
    assert s.get("c.com") is not None


def test_overwrite_updates_ttl_and_mru():
    s = Store(max_capacity=2)
    s.put("a.com", CacheEntry("a.com", "1.1.1.1", ttl_secs=1))
    first = s.get("a.com")
    assert first is not None
    # Overwrite with long ttl
    s.put("a.com", CacheEntry("a.com", "1.1.1.1", ttl_secs=100))
    time.sleep(1.1)
    # Should still exist because overwritten with longer TTL
    assert s.get("a.com") is not None


def test_delete():
    s = Store(max_capacity=1)
    s.put("a.com", CacheEntry("a.com", "1.1.1.1", ttl_secs=100))
    assert s.get("a.com") is not None
    s.delete("a.com")
    assert s.get("a.com") is None


def test_zero_capacity():
    s = Store(max_capacity=0)
    s.put("a.com", CacheEntry("a.com", "1.1.1.1", ttl_secs=100))
    assert s.get("a.com") is None
