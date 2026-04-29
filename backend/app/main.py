from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.routers import auth, expense

app = FastAPI(title="Expense API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(expense.router)


@app.get("/")
def root():
    return {"message": "Expense API running"}


@app.get("/health")
def health():
    return {"status": "ok"}