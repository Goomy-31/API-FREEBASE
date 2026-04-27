from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# from backend.app.routers.auth import router as auth_router
# from backend.app.routers.chat import router as chat_router

from app.routers import auth, expense

# app = FastAPI(title="Mika Backend")

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# app.include_router(auth_router)
# app.include_router(chat_router)

# @app.get("/health")
# def health():
#     return {"status": "ok"}

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Expense API running"}

@app.get("/health")
def health():
    return {"status": "ok"}

app.include_router(auth.router)
app.include_router(expense.router)