from fastapi import FastAPI
from database import engine, Base
from routers import users, items, add_to_cart
import auth

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(users.router)
app.include_router(auth.router)
app.include_router(items.router)
app.include_router(add_to_cart.router)
