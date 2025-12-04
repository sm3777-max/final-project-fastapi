from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.database import engine, Base
# Import models so tables are created by SQLAlchemy
from app import models 
from app.routers import user_routes, calc_routes

# Create database tables on startup
Base.metadata.create_all(bind=engine)

app = FastAPI()

# --- MOUNT STATIC FILES ---
# This allows the API to serve your HTML/CSS/JS files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# --- REGISTER ROUTERS ---
app.include_router(user_routes.router)
app.include_router(calc_routes.router)

@app.get("/")
def read_root():
    # Redirect hint pointing to the new Dashboard
    return {"message": "Go to /static/dashboard.html"}