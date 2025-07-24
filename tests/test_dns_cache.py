import pytest

from dns_cache.dns_cache import DNSCache
from dns_cache.store import Store


def test_dns_cache_basic():
    c = DNSCache(Store(max_capacity=2))
    c.put("example.com", "1.1.1.1", ttl_secs=10)
    assert c.get("example.com") == "1.1.1.1"


def test_invalid_domain():
    c = DNSCache(Store(max_capacity=2))
    with pytest.raises(ValueError):
        c.put("not-a-domain", "1.2.3.4", ttl_secs=10)


def test_invalid_ipv4():
    c = DNSCache(Store(max_capacity=2))
    with pytest.raises(ValueError):
        c.put("example.com", "999.999.999.999", ttl_secs=10)
