from fastapi import FastAPI
from src.api import contacts

app = FastAPI()

# Підключаємо маршрути з файлу contacts.py
app.include_router(contacts.router, prefix="/contacts", tags=["contacts"])

@app.get("/")
async def root():
    return {"message": "Welcome to the Contact API!"}
