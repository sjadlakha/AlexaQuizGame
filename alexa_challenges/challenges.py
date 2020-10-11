import logging
import os
import random
import pdb

from responses import RESPONSE
from flask import Flask
from flask_ask import Ask, request, session, question, statement, audio, current_stream
from data import middleware
from utils import Quiz, info_logger, error_logger
from constants import CATEGORY, SOUNDS

app = Flask(__name__)
ask = Ask(app, "/")
category_name=''
player_num=0

@ask.launch
def launch():
    info_logger('********* IN LAUNCH INTENT *************')
    info_logger('Welcome to the quiz. Game is started')
    session.attributes['playback_speed'] = 'slow'
    speech_text = '<speak>' + Quiz.response_with_music(SOUNDS['welcome'], RESPONSE['WELCOME_MSG'])+\
        '</speak>'
    info_logger(speech_text)
    return question(speech_text).reprompt(speech_text).simple_card('QUIZ', speech_text)

@ask.intent('CurrentSkillIntent')
def current_skill():
    info_logger('********* IN CURRENT SKILL INTENT *************')
    speech_text = RESPONSE['CURRENT_SKILL']
    return question(speech_text).reprompt(speech_text).simple_card('TRT QUIZ', speech_text)


@ask.intent('CategoryNameIntent')
def select_category(category):
    try:
        info_logger('********* IN CATEGORY INTENT *************')
        info_logger('category name: '+category)
        if category.lower() not in CATEGORY.keys():
            speech_text = RESPONSE['INVALID_CATEGORY']
        else:
            category_name = category
            speech_text = RESPONSE['GET_PLAYER_COUNT']

    except Exception as e:
        error_logger(e)
        speech_text = RESPONSE['ERROR_MSG']
    return question(speech_text).reprompt(speech_text).simple_card('Quiz', speech_text)


@ask.intent('PlayerCountIntent')
def count_players(players_count):
    try:
        info_logger('********* IN PLAYER COUNT INTENT *************')
        info_logger('players count: {}'.format(players_count))
        player_num = players_count
        quiz_instance = Quiz(session.attributes)
        speech_text = quiz_instance.count_players_responses(int(players_count))
    except Exception as e:
        error_logger(e)
        speech_text = RESPONSE['ERROR_MSG']
    return question(speech_text).reprompt(speech_text).simple_card('Quiz', speech_text)

@ask.intent('PlayersNameIntent')
def handle_players_info(name):
    try:
        info_logger('********* IN PLAYER NAME INTENT *************')
        info_logger(request)
        info_logger('players name: '+name)
        quiz_instance = Quiz(session.attributes)
        if quiz_instance.track_player_count():
            return question(quiz_instance.track_player_count())
        elif 'next_intent' in session.attributes.keys():
            return question(RESPONSE['ALEXA_MISSUNDERSTOOD'])
        elif request.intent['confirmationStatus'] == "DENIED":
            return question(RESPONSE['ASK_NAME_AGAIN'])
        speech_text = quiz_instance.players_info(name)
    except Exception as e:
        error_logger(e)
        speech_text = RESPONSE['ERROR_MSG']
    return question(speech_text).reprompt(speech_text).simple_card('Quiz', speech_text)




@ask.intent('QuizBeginIntent')
def quiz_beginning(ready_or_not):
    try:
        info_logger('********* IN QUIZ BEGIN INTENT *************')
        info_logger(request)
        quiz_instance = Quiz(session.attributes)
        if quiz_instance.track_players_name():
            return question(quiz_instance.track_players_name())
        info_logger('user is ready or not: '+ready_or_not)
        # players = int(session.attributes['total_players'])
        quiz_data = middleware(player_num*5, category_name)
        session.attributes['quiz_data'] = quiz_data
        session.attributes['counter'] = 0
        speech_text = quiz_instance.initial_quiz_que()
        session.attributes['next_intent'] = 'QuestionAnswerIntent'
    except Exception as e:
        error_logger(e)
        speech_text = RESPONSE['ERROR_MSG']
    return question(speech_text).reprompt(speech_text).simple_card('Question', speech_text)

@ask.intent('QuestionAnswerIntent')
def quiz_question_answer(answer):
    try:
        info_logger('********* IN QUESTION ANSWER INTENT *************')
        info_logger(request)
        info_logger('user answer is: '+answer)
        quiz_instance = Quiz(session.attributes)
        if quiz_instance.track_players_name():
            return question(quiz_instance.track_players_name())
        quiz_que = session.attributes['question']
        result_text = quiz_instance.check_answer(session.attributes['quiz_data'][quiz_que], answer.lower())
        speech_text = '<speak>'+ quiz_instance.quiz_progress(result_text).replace('&', '')+ '</speak>'
        info_logger(speech_text)
    except Exception as e:
        error_logger(e)
        speech_text = RESPONSE['ERROR_MSG']   
    return question(speech_text).reprompt(speech_text).simple_card('QUIZ', speech_text)

@ask.intent('RepeatQuestionIntent')
def repeat_question():
    try:
        info_logger('********* IN REPEAT QUESTION INTENT *************')
        info_logger('repeat question: '+session.attributes['question'])
        speech_text = session.attributes['question']
    except Exception as e:
        error_logger(e)
        speech_text = RESPONSE['ERROR_MSG']
    return question(speech_text).reprompt(speech_text).simple_card('Question', speech_text)

@ask.intent('AMAZON.NoIntent')
def negative_response():
    try:
        info_logger('********* IN AMAZON NO INTENT *************')
        speech_text = RESPONSE['ASK_READY_MSG']
    except Exception as e:
        error_logger(e)
        speech_text = RESPONSE['ERROR_MSG']
    return question(speech_text).reprompt('now Are you ready?').simple_card('QUIZ', speech_text)

@ask.intent('AMAZON.HelpIntent')
def help():
    info_logger('********* IN AMAZON HELP INTENT *************')
    speech_text = RESPONSE['HELP_MSG']
    return question(speech_text).reprompt(speech_text).simple_card('GUIDE', speech_text)

@ask.intent('AMAZON.FallbackIntent')
def handle_errors():
    info_logger('********* IN AMAZON FALLBACK INTENT *************')
    speech_text = RESPONSE['FALLBACK_MSG']
    if 'question' in session.attributes.keys():
        speech_text += '. '+session.attributes['question']
    return question(speech_text).simple_card('QUIZ', speech_text)

@ask.intent('AMAZON.StopIntent')
def stop():
    info_logger('********* IN AMAZON STOP INTENT *************')
    speech_text = RESPONSE['STOP_MSG']
    return statement(speech_text)

@ask.session_ended
def session_ended():
    return "{}", 200

if __name__ == '__main__':
    app.run(debug=True)
