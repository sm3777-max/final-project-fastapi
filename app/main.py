from fastapi import FastAPI
from app.database import engine, Base
from app.routers import user_routes, calc_routes

# Create tables on startup
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Register the routers
app.include_router(user_routes.router)
app.include_router(calc_routes.router)

@app.get("/")
def read_root():
    return {"message": "Module 12: Final Backend API is Running"}