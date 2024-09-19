from fastapi import FastAPI
from . import models
from .database import engine
from .routers import order, user, authentication, payment, ordertrackingupdate
from fastapi.staticfiles import StaticFiles


app = FastAPI()


models.Base.metadata.create_all(engine)

app.include_router(authentication.router)
app.include_router(order.router)
app.include_router(user.router)
app.include_router(payment.router)
app.include_router(ordertrackingupdate.router)

app.mount("/payment_screenshots", StaticFiles(directory="payment_screenshots"), name="payment_screenshots")
