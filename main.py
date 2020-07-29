import telegram
from fastapi import FastAPI

from models import Message
from mybot import TOKEN, send_message, mybot

app = FastAPI()
bot: telegram.Bot = mybot()


@app.get("/ping")
async def read_root():
    return {"Async": "World"}


@app.post(f'/{TOKEN}/send')
async def send(message: Message):
    send_message(bot, message)
    return {"message": "send", "status": 200}
