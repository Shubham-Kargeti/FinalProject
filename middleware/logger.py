from fastapi import Request
import time

async def log_requests(request: Request, call_next):
    start_time = time.time()

    print(f"Middleware Request: {request.method} {request.url}")

    response = await call_next(request)

    duration = time.time() - start_time
    print(f"Middleware Response: {response.status_code} in {duration:.2f}s")

    return response
