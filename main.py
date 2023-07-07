from fastapi import FastAPI
import uvicorn

from src.routes import contacts, users


app = FastAPI()

app.include_router(contacts.router)
app.include_router(users.router)


if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)