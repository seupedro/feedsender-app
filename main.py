import telegram
from fastapi import FastAPI
from mybot import mybot, TOKEN
from models import Message

app = FastAPI()
bot: telegram.Bot = mybot()


@app.get("/ping")
async def read_root():
    return {"Async": "World"}


@app.post(f'/{TOKEN}/send')
async def send(msg: Message):
    bot.send_message(msg.chat_id, msg.text)
    return {"message": "send", "status": 200}
