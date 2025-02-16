from typing import Any, Optional
import time
from functools import wraps

class CacheService:
    def __init__(self):
        self._cache = {}
        self._ttl = {}
        self._default_ttl = 300  # 5 Minuten Standard-TTL

    def get(self, key: str) -> Optional[Any]:
        """Holt einen Wert aus dem Cache"""
        if key in self._cache:
            if self._ttl[key] > time.time():
                return self._cache[key]
            else:
                # Cache ist abgelaufen
                del self._cache[key]
                del self._ttl[key]
        return None

    def set(self, key: str, value: Any, ttl: int = None) -> None:
        """Setzt einen Wert in den Cache"""
        self._cache[key] = value
        self._ttl[key] = time.time() + (ttl or self._default_ttl)

    def delete(self, key: str) -> None:
        """Löscht einen Wert aus dem Cache"""
        if key in self._cache:
            del self._cache[key]
            del self._ttl[key]

    def clear(self) -> None:
        """Leert den gesamten Cache"""
        self._cache.clear()
        self._ttl.clear()

    def cached(self, ttl: int = None):
        """Decorator für Caching von Funktionsaufrufen"""
        def decorator(func):
            @wraps(func)
            async def wrapper(*args, **kwargs):
                # Erstelle einen eindeutigen Cache-Key
                key = f"{func.__name__}:{str(args)}:{str(kwargs)}"
                
                # Prüfe Cache
                cached_value = self.get(key)
                if cached_value is not None:
                    return cached_value
                
                # Führe Funktion aus und cache das Ergebnis
                result = await func(*args, **kwargs)
                self.set(key, result, ttl)
                return result
            return wrapper
        return decorator

# Globale Cache-Instanz
cache = CacheService()
