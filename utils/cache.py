import time

# Cache storage: { key: (value, expire_time) }
cache = {}

def set_cache(key: str, value: any, ttl: int = 300):
    expire_time = time.time() + ttl
    cache[key] = (value, expire_time)

def get_cache(key: str):
    if key in cache:
        value, expire_time = cache[key]
        if time.time() < expire_time:
            print(f"[CACHE HIT] {key}") # Remove when testing is complete
            return value
        else:
            # Cache expired
            print(f"[CACHE EXPIRED] {key}")# Remove when testing is complete
            del cache[key]
    print(f"[CACHE EXPIRED] {key}")# Remove when testing is complete
    return None

def clear_cache(key: str):
    if key in cache:
        del cache[key]
