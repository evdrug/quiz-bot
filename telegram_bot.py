import json
import logging
import os
from enum import Enum, auto
from random import randint

import redis
from dotenv import load_dotenv
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, \
    ConversationHandler, RegexHandler

# Enable logging
from open_file_quiz import get_questions
from telegram_logger import TelegramLogsHandler


class StepQuiz(Enum):
    NEW_QUESTION = auto()
    ANSWER = auto()
    GIVE_UP = auto()
    MY_SCORE = auto()


questions = get_questions()

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)

logger = logging.getLogger('telegram_bot')


def start(bot, update):
    start_keyboard = [['Новый вопрос', 'Сдаться'], ['Мой счёт']]
    update.message.reply_text(
        text=("Приветствую!\n Нажмите «Новый вопрос», для начала викторины.\n"
              "/cancel - для отмены."),
        reply_markup=ReplyKeyboardMarkup(start_keyboard))
    return StepQuiz.NEW_QUESTION.value


def check_answer(bot, update):
    user_active_question = r.get(update.message.chat_id)
    answer = json.loads(user_active_question.decode()).get('answer')
    if answer.split('.')[0].lower() == update.message.text.lower():
        update.message.reply_text(
            ('Правильно! Поздравляю!\n'
             'Для следующего вопроса нажми «Новый вопрос»'))
    else:
        update.message.reply_text('Неправильно... Попробуешь ещё раз?')


def my_score(bot, update):
    update.message.reply_text(f"Ваш счёт {None}")


def new_question(bot, update):
    question = questions[randint(0, len(questions) - 1)]
    r.set(update.message.chat_id, json.dumps(question))
    update.message.reply_text(question['question'])
    return StepQuiz.ANSWER.value


def give_up(bot, update):
    user_active_question = r.get(update.message.chat_id)
    answer = json.loads(user_active_question.decode()).get('answer')
    update.message.reply_text(
        f'Правильный ответ: {answer} \n Для следующего вопроса нажми «Новый вопрос»')
    return StepQuiz.NEW_QUESTION.value


def error(bot, update, error):
    logger.warning('Update "%s" caused error "%s"', update, error)


def cancel(bot, update):
    update.message.reply_text(text="Векторина окончена.",
                              reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END


def main():
    logger.setLevel(logging.INFO)
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    updater = Updater(token=os.getenv('TELEGRAM_TOKEN'))
    logger.addHandler(TelegramLogsHandler(updater.bot))
    logger.info('\u2705 Бот запущен')

    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            StepQuiz.NEW_QUESTION.value: [
                RegexHandler('^Новый вопрос$', new_question),
                RegexHandler('^Мой счёт$', my_score),
            ],
            StepQuiz.ANSWER.value: [
                RegexHandler('^Сдаться$', give_up),
                RegexHandler('^Мой счёт$', my_score),
                MessageHandler(Filters.text, check_answer),
            ]

        },

        fallbacks=[CommandHandler('cancel', cancel)]
    )

    dp.add_handler(conv_handler)
    dp.add_error_handler(error)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    load_dotenv()
    try:
        r = redis.Redis(host=os.getenv('REDIS_URL'),
                        port=os.getenv('REDIS_PORT'),
                        db=0, password=os.getenv('REDIS_PASSWORD'))
        r.client()
    except ConnectionError as e:
        logger.error(e)
        raise e
    main()
