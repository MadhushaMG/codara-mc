import time
from collections import OrderedDict
from typing import Any, Optional

class CacheInterface:
    def get(self, key: str) -> Optional[Any]:
        raise NotImplementedError

    def set(self, key: str, value: Any, ttl: Optional[float] = None) -> None:
        raise NotImplementedError

    def invalidate(self, key: str) -> None:
        raise NotImplementedError

class MemoryLRUCache(CacheInterface):
    def __init__(self, capacity: int = 100):
        self.capacity = capacity
        self.cache = OrderedDict()
        self.ttl_map = {}

    def get(self, key: str) -> Optional[Any]:
        if key not in self.cache:
            return None
        
        # Check TTL
        if key in self.ttl_map:
            if time.time() > self.ttl_map[key]:
                # Expired
                self.invalidate(key)
                return None
                
        # Move to end to mark as recently used
        self.cache.move_to_end(key)
        return self.cache[key]

    def set(self, key: str, value: Any, ttl: Optional[float] = None) -> None:
        if key in self.cache:
            self.cache.move_to_end(key)
        self.cache[key] = value
        
        if ttl is not None:
            self.ttl_map[key] = time.time() + ttl
        elif key in self.ttl_map:
            del self.ttl_map[key]
            
        if len(self.cache) > self.capacity:
            # Pop the first item (least recently used)
            oldest_key, _ = self.cache.popitem(last=False)
            if oldest_key in self.ttl_map:
                del self.ttl_map[oldest_key]

    def invalidate(self, key: str) -> None:
        if key in self.cache:
            del self.cache[key]
        if key in self.ttl_map:
            del self.ttl_map[key]
