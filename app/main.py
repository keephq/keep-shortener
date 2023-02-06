import os, sys

# Todo: remove this hack
print(os.getcwd())
sys.path.insert(0, os.getcwd())

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.routes import shortener

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(shortener.router, prefix="/s", tags=["shortener"])

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=int(os.environ["PORT"]) or 8080)
