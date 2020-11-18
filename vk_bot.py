import json
import logging
import os
import random

import redis
import vk_api
from dotenv import load_dotenv
from redis import ConnectionError
from telegram.ext import Updater
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.longpoll import VkLongPoll, VkEventType

from open_file_quiz import get_questions
from telegram_logger import TelegramLogsHandler

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)

logger = logging.getLogger('vk_bot')

keyboard = VkKeyboard(one_time=True)

keyboard.add_button('Новый вопрос', color=VkKeyboardColor.PRIMARY)
keyboard.add_button('Сдаться', color=VkKeyboardColor.NEGATIVE)

keyboard.add_line()  # Переход на вторую строку
keyboard.add_button('Мой счёт', color=VkKeyboardColor.SECONDARY)
questions = get_questions()


def handler(event, vk_api):
    user_active_question = r.get(event.user_id)
    if not user_active_question and event.text == 'Новый вопрос':
        question = questions[random.randint(0, len(questions) - 1)]
        r.set(event.user_id, json.dumps(question))
        send_message(event, vk_api, question['question'])
    elif user_active_question and event.text == 'Сдаться':
        answer = json.loads(user_active_question.decode()).get('answer')
        send_message(event, vk_api,
                     (f'Правильный ответ: {answer} \n'
                      f'Для следующего вопроса нажми «Новый вопрос»'))
        r.delete(event.user_id)
    elif event.text == 'Мой счёт':
        send_message(event, vk_api, f"Ваш счёт {None}")
    elif user_active_question:
        answer = json.loads(user_active_question.decode()).get('answer')
        if answer.split('.')[0].lower() == event.text.lower():
            send_message(event, vk_api,
                         ('Правильно! Поздравляю!\n'
                          'Для следующего вопроса нажми «Новый вопрос»'))
            r.delete(event.user_id)
        else:
            send_message(event, vk_api, 'Неправильно... Попробуешь ещё раз?')
    else:
        send_message(event, vk_api,
                     'Для начала викторины нажмите "Новый вопрос"')


def send_message(event, vk_api, message):
    return vk_api.messages.send(
        user_id=event.user_id,
        random_id=random.randint(1, 1000),
        keyboard=keyboard.get_keyboard(),
        message=message
    )


if __name__ == "__main__":
    load_dotenv()
    logger.setLevel(logging.INFO)
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    updater = Updater(token=os.getenv('TELEGRAM_TOKEN'))
    logger.addHandler(TelegramLogsHandler(updater.bot))
    logger.info('\u2705 Бот запущен')
    try:
        r = redis.Redis(host=os.getenv('REDIS_URL'),
                        port=os.getenv('REDIS_PORT'),
                        db=0, password=os.getenv('REDIS_PASSWORD'))
        r.client()
    except ConnectionError as e:
        logger.error(e)
        raise e
    vk_session = vk_api.VkApi(token=os.getenv('VK_TOKEN'))
    vk_api = vk_session.get_api()

    longpoll = VkLongPoll(vk_session)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            handler(event, vk_api)
