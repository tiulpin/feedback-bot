import logging
import os

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters


# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.WARNING
)
logger = logging.getLogger(__name__)

fb_group_id = int(os.environ["ADMIN_GROUP_ID"])
users = list(map(int, os.environ["USERS"].split()))
issues = {}


# Define a few command handlers
def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def start(update, context):
    update.message.reply_text(f"{os.environ['START_TEXT']}")


def echo(update, context):
    if update.message.chat_id in users:
        sent_message = context.bot.send_message(
            chat_id=fb_group_id, text=update.message.text
        )
        issues[sent_message.message_id] = update.message.chat_id

    elif (
        update.message.reply_to_message is not None
        and update.message.chat_id == fb_group_id
    ):
        issue_id = update.message.reply_to_message.message_id
        context.bot.send_message(chat_id=issues[issue_id], text=update.message.text)


def main():
    updater = Updater(os.environ["TELEGRAM_TOKEN"], use_context=True)
    dp = updater.dispatcher

    dp.add_error_handler(error)
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(MessageHandler(Filters.text, echo))

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
