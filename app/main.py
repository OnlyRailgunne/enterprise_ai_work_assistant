from fastapi import FastAPI

from app.api.chat import router as chat_router


app = FastAPI(
    title="Enterprise AI Work Assistant",
)


app.include_router(chat_router)


@app.get("/")
def root():
    return {
        "message": "Enterprise AI Work Assistant is running"
    }