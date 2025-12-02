from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from .database import Base, engine
from .routers import users, auth, todos
from .middleware.cors import setup_cors

Base.metadata.create_all(bind=engine)

app = FastAPI()

setup_cors(app)

app.middleware("http")
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(todos.router)

@app.exception_handler(HTTPException)
async def http_error_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail, "success": False},
    )

