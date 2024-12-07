from fastapi import FastAPI
from . import models
from .database import engine
from .routers import order, user, authentication, payment, ordertrackingupdate, profile, notifications
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can set this to a specific domain in production (e.g., ["https://example.com"])
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers (you can specify specific headers if needed)
)




# Create the database tables
models.Base.metadata.create_all(bind=engine)

app.include_router(authentication.router)
app.include_router(order.router)
app.include_router(user.router)
app.include_router(profile.router)
app.include_router(payment.router)
app.include_router(ordertrackingupdate.router)
app.include_router(notifications.router)

# Serve static files
app.mount("/payment_screenshots", StaticFiles(directory="payment_screenshots"), name="payment_screenshots")
