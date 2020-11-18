import os

from dotenv import load_dotenv


def serialize_quiz(quiz_file):
    quiz_questions = []
    try:
        with open(quiz_file, 'r',
                  encoding='KOI8-R') as file:
            sections = file.read().split("\n\n")
    except FileNotFoundError:
        return quiz_questions
    question = ''
    answer = ''
    for section in sections:
        if section.startswith('Вопрос'):
            question_tmp = section.split('\n')[1:]
            question = '\n'.join(question_tmp)
        if section.startswith('Ответ'):
            answer_tmp = section.split('\n')[1:]
            answer = '\n'.join(answer_tmp)
        if question and answer:
            quiz_questions.append(
                {'question': question, 'answer': answer})
            question = ''
            answer = ''

    return quiz_questions


def get_questions():
    load_dotenv()
    path = os.getenv('QUIZ_FOLDER', 'quizes')
    questions = []
    for file_quiz in os.listdir(path):
        questions.extend(serialize_quiz('{}/{}'.format(path, file_quiz)))
    return questions
