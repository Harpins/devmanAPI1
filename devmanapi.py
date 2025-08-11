from time import sleep
import requests
from environs import Env
import telegram
from telegram import ParseMode
from telegram.ext import Updater, CommandHandler
import logging



def start_long_polling(token, timestamp, timeout=100):
    url = "https://dvmn.org/api/long_polling/"
    response = requests.get(
        url,
        headers={"Authorization": token},
        params={"timestamp": timestamp},
        timeout=timeout,
    )
    response.raise_for_status()
    return response.json()


def make_bot_messages(raw_results):
    messages = []
    for raw_result in raw_results:
        title = raw_result.get("lesson_title")
        is_negative = raw_result.get("is_negative")
        lesson_url = raw_result.get("lesson_url")
        if not all([title, is_negative, lesson_url]):
            raise ValueError("Изменилась форма ответа API")

        lesson_status = "<b>вернулась с проверки</b>" if is_negative else "<b>принята</b>"
        message = f'Работа\n<i>"{title}"</i>\n{lesson_status}\n<a href="{lesson_url}">Cсылка</a>'
        messages.append(message)
    return messages


def start(update, context):
    user = update.message.from_user
    update.message.reply_text(
        f"Добро пожаловать, {user.first_name}!\nБот запущен!"
    )


def main():
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger(__name__)
    logger.info("Бот запускается")

    env = Env()
    env.read_env()
    dvmn_token = env.str("AUTH_TOKEN")
    bot_token = env.str("TG_BOT_TOKEN")
    tg_chat_id = env.int("TG_CHAT_ID")

    bot = telegram.Bot(token=bot_token)
    updater = Updater(bot=bot, use_context=True)
    updater.dispatcher.add_handler(CommandHandler("start", start))
    updater.start_polling()
    logger.info("Бот запущен")
    timestamp = None
    
    while True:
        try:
            response = start_long_polling(dvmn_token, timestamp)
            status = response.get("status")
            if status == "timeout":
                timestamp = response.get("timestamp_to_request")
            if status == "found":
                raw_results = response.get("new_attempts")
                messages = make_bot_messages(raw_results)
                for message in messages:
                    bot.send_message(chat_id=tg_chat_id,
                                     text=message, parse_mode=ParseMode.HTML)
        except requests.exceptions.ReadTimeout:
            continue
        except requests.exceptions.ConnectionError:
            logger.error("Потеряно соединение с интернетом, пробуем переподключиться")
            sleep(10)
            continue
        except telegram.error.TelegramError as err:
            logger.error(f"Ошибка Telegram API: {err.message}")
            continue


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logging.getLogger(__name__).info("Бот остановлен вручную")
    except Exception as e:
        logging.getLogger(__name__).critical(f"Критическая ошибка при запуске: {str(e)}")
        raise
