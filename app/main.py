import time
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import auth, orders, users

app = FastAPI()

origins = ["https://www.google.com"] #lista di domini che possono parlare all'api

#CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#ROUTERS
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(orders.router)

#HOME
@app.get("/home")
def home():
    return {"message": "Benvenuto nel backend Sincrono"}
