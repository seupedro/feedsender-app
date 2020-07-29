import logging
import os

from telegram import Bot, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import messagequeue as mq
from telegram.utils.request import Request

from models import Message

TOKEN = os.getenv('FEEDBOT_TELEGRAM_TOKEN')
keyboards = {'contact_keyboard': InlineKeyboardMarkup([[InlineKeyboardButton("📣 Contato", url='t.me/pedrohartmann')]])}


class MQBot(Bot):
    '''A subclass of Bot which delegates send method handling to MQ'''

    def __init__(self, *args, is_queued_def=True, mqueue=None, **kwargs):
        super(MQBot, self).__init__(*args, **kwargs)
        # below 2 attributes should be provided for decorator usage
        self._is_messages_queued_default = is_queued_def
        self._msg_queue = mqueue or mq.MessageQueue()

    def __del__(self):
        try:
            self._msg_queue.stop()
        except:
            pass
        super(MQBot, self).__del__()

    @mq.queuedmessage
    def send_message(self, *args, **kwargs):
        '''Wrapped method would accept new `queued` and `isgroup`
        OPTIONAL arguments'''
        return super(MQBot, self).send_message(*args, **kwargs)


def mybot():
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

    msg_queue = mq.MessageQueue(all_burst_limit=25, all_time_limit_ms=1050)
    request = Request(con_pool_size=8)
    bot = MQBot(TOKEN, request=request, mqueue=msg_queue)
    return bot


def send_message(bot: Bot, msg: Message):
    bot.send_message(
        msg.chat_id,
        msg.text,
        msg.parse_mode,
        msg.disable_web_page_preview,
        msg.disable_notification,
        msg.reply_to_message_id,
        keyboards.get(msg.reply_markup),
        msg.timeout
    )
