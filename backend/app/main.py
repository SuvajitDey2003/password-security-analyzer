from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.api.routes import router
from backend.app.core.dictionary import load_password_files


app = FastAPI(title="Password Security Analyzer")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup():
    load_password_files(["data/common_passwords.sample.txt"])

@app.get("/")
def health():
    return {"status": "ok"}

app.include_router(router)
