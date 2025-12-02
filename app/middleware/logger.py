async def log_requests(request, call_next):
    print("Request:", request.url)
    response = await call_next(request)
    print("Response:", response.status_code)
    return response
