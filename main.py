from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .auth.views import router as auth_router
from .main.views import router as main_router

app = FastAPI()

origins = [
    "http://localhost:5173",
    "http://localhost:5173/api/login/",
    "http://localhost:5173/api/register/",
    "http://localhost:5173/api/main/user/me",
    "http://localhost:5173/api/main/user/storage",
    "http://localhost:5173/api/main/response",
    "http://localhost:5173/api/main/user/delete",
    "http://localhost:5173/api/main/user/info"

]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(main_router)
