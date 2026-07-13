import unittest
import time
from cache import MemoryLRUCache

class TestMemoryLRUCache(unittest.TestCase):
    def test_set_and_get(self):
        cache = MemoryLRUCache(capacity=2)
        cache.set("a", 1)
        self.assertEqual(cache.get("a"), 1)
        self.assertIsNone(cache.get("b"))

    def test_lru_eviction(self):
        cache = MemoryLRUCache(capacity=2)
        cache.set("a", 1)
        cache.set("b", 2)
        cache.set("c", 3)
        
        # 'a' should be evicted
        self.assertIsNone(cache.get("a"))
        self.assertEqual(cache.get("b"), 2)
        self.assertEqual(cache.get("c"), 3)

    def test_lru_refresh(self):
        cache = MemoryLRUCache(capacity=2)
        cache.set("a", 1)
        cache.set("b", 2)
        
        # Access 'a' to make it recently used
        cache.get("a")
        
        # Add 'c', this should evict 'b' instead of 'a'
        cache.set("c", 3)
        self.assertIsNone(cache.get("b"))
        self.assertEqual(cache.get("a"), 1)
        self.assertEqual(cache.get("c"), 3)

    def test_ttl_expiration(self):
        cache = MemoryLRUCache(capacity=2)
        # Set TTL to a very small amount
        cache.set("a", 1, ttl=0.1)
        self.assertEqual(cache.get("a"), 1)
        
        # Wait for expiration
        time.sleep(0.2)
        self.assertIsNone(cache.get("a"))

    def test_invalidate(self):
        cache = MemoryLRUCache(capacity=2)
        cache.set("a", 1)
        cache.invalidate("a")
        self.assertIsNone(cache.get("a"))

if __name__ == '__main__':
    unittest.main()
