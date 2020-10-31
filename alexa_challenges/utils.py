from responses import RESPONSE
from logger import InfoLogger, ErrorLogger
from constants import SOUNDS
import pdb

def info_logger(message):
    logger_instance = InfoLogger(message)
    logger_instance.info_log()

def error_logger(message):
    logger_instance = ErrorLogger(message)
    logger_instance.error_log()

class Quiz():

    def __init__(self, attr):
        '''Here self.attr are intialized'''
        self.attr = attr
        self.speed = attr['playback_speed']

    @staticmethod
    def response_with_music(sound, response):
        speech_text = sound+response
        return speech_text

    def control_playback_speed(self, content):
        result = '''
            <speak>
                <audio src='soundbank://soundlibrary/ui/gameshow/amzn_ui_sfx_gameshow_intro_01'/>
                <prosody volume='''+self.speed+'''>'''+content+'''</prosody>.
            </speak>'''
        return result

    def track_player_count(self):
        speech_text = RESPONSE['TRACK_PLAYERS_COUNT']
        return speech_text if 'total_players' not in self.attr else None

    def track_players_name(self):
        if self.track_player_count():
            speech_text = self.track_player_count()
        elif 'name' not in self.attr['players']['0'].keys():
            speech_text = RESPONSE['TRACK_PLAYER_NAME']
        else:
            speech_text = None
        return speech_text

    def intialize_players(self, players_count):
        self.attr['players'] = {}
        self.attr['total_players'] = int(players_count)
        self.attr['players']['count'] = 0
    
    def count_players_responses(self, players_count):
        if players_count == 0 or players_count < 0:
            speech_text = RESPONSE['NO_PLAYERS_MSG']
        elif players_count == 1:
            self.intialize_players(players_count)
            speech_text = RESPONSE['ONE_PLAYER_MSG'] +' '+RESPONSE['HINT_PLAYER_NAME']
        elif players_count > 5:
            speech_text = RESPONSE['PLAYERS_OUT_OF_RANGE']
        else:
            self.intialize_players(players_count)
            speech_text = RESPONSE['VALID_PLAYERS_MSG'].format(number=players_count) \
                + RESPONSE['HINT_PLAYER_NAME']
        return speech_text

    def players_info(self, name):
        players = self.attr['players']
        if self.attr['total_players'] == 1:
            speech_text = RESPONSE['GET_SINGLE_PLAYER_MSG'].format(name=name)
        elif players['count']+1 < self.attr['total_players']:
            speech_text = RESPONSE['GET_MULTI_PLAYER_MSG'].format(number=str(players['count']+1), 
                name=name)
        elif players['count']+1 == self.attr['total_players']:
            speech_text = RESPONSE['GET_LAST_PLAYER_MSG'].format(number=str(players['count']+1), 
                name=name)
        elif players['count']+1 > self.attr['total_players']:
            speech_text = 'You can\'t add extra player in on going game.'
        players[str(players['count'])] = {}
        players[str(players['count'])]['name'] = name
        players[str(players['count'])]['score'] = 0
        players['count'] += 1
        return speech_text

    def get_question(self):
        '''Get question from quiz data according to counter index.'''
        # pdb.set_trace()
        que = list(self.attr['quiz_data'])[self.attr['counter']+1]
        info_logger(list(self.attr['quiz_data']))
        info_logger(self.attr['counter']+1)
        info_logger(que)
        self.attr['question'] = que
        que_with_sound = self.response_with_music(SOUNDS['start_question'], ' Tell me '+que)
        return que_with_sound

    def initial_quiz_que(self):
        # pdb.set_trace()
        players = self.attr['players']
        if self.attr['total_players'] > 1:
            player_name = players[str(self.attr['counter'])]['name']
            speech_text = 'Here is the question for '+ player_name +','
        else:
            speech_text = 'Okay Here is your question, '
        que = list(self.attr['quiz_data'])[self.attr['counter']]
        info_logger(list(self.attr['quiz_data']))
        info_logger(self.attr['counter']+1)
        info_logger(que)    
        speech_text += que +'. '+ RESPONSE['HINT_ANSWER_PATTERN']
        self.attr['question'] = que
        return speech_text

    def check_answer(self, answer, user_answer):
        '''Check user answer is correct or not and update score accordingly.'''
        correct_option = list(answer.keys())[0]
        if user_answer.lower() in correct_option.lower():
            players = self.attr['players']
            current_player = players[str(self.attr['counter'] % self.attr['total_players'])]
            current_player['score'] += 10
            response = RESPONSE['CORRECT_ANS_MSG'].format(name=current_player['name'],
                score=current_player['score'])
            speech_text = self.response_with_music(SOUNDS['positive_response'], response)
        else:
            response = RESPONSE['WRONG_ANS_MSG'].format(
                ans=correct_option+' '+self.attr['quiz_data'][self.attr['question']][correct_option])
            speech_text = self.response_with_music(SOUNDS['negative_response'], response)
        return speech_text

    def quiz_progress(self, result_text):
        players = self.attr['players']
        question_range = self.check_question_range()
        if question_range:
            new_question = self.get_question() 
            speech_text = result_text + ' okay let\'s move on to the next question for '\
                +players[str((self.attr['counter']+1) % self.attr['total_players'])]['name']+\
                new_question
            print(self.attr.category_name)
        else:
            winners_list, max_score = self.get_winner()
            winner = ' and '.join(winners_list)
            if len(winners_list) == 1 and max_score == 10:
                response = RESPONSE['SINGLE_WIN_MSG1'].format(
                    name=winner, score=max_score, category = self.attr.category_name)
            elif len(winners_list) == 1 and max_score == 20:
                response = RESPONSE['SINGLE_WIN_MSG2'].format(
                    name=winner, score=max_score, category = self.attr.category_name)
            elif len(winners_list) == 1 and max_score == 30:
                response = RESPONSE['SINGLE_WIN_MSG3'].format(
                    name=winner, score=max_score, category = self.attr.category_name)
            elif len(winners_list) == 1 and max_score == 40:
                response = RESPONSE['SINGLE_WIN_MSG4'].format(
                    name=winner, score=max_score, category = self.attr.category_name)
            elif len(winners_list) == 1 and max_score == 50:
                response = RESPONSE['SINGLE_WIN_MSG5'].format(
                    name=winner, score=max_score, category = self.attr.category_name)
            else:
                response = RESPONSE['MULTI_WIN_MSG'].format(
                    name=winner, score=max_score, category = self.attr.category_name)
            #response = RESPONSE['SINGLE_WIN_MSG'].format(name=winner, score=max_score) \
                #if len(winners_list) == 1 else RESPONSE['MULTI_WIN_MSG'].format(name=winner, score=max_score)
            speech_text = self.response_with_music(SOUNDS['winning'], response)
            info_logger('$ Stage one Of quiz is over $')
        self.attr['counter'] += 1    
        return speech_text

    def get_winner(self):
        players = self.attr['players']
        player_score = { value['name']:value['score'] for key,value in players.items() 
            if type(value) != int}
        winners_list = [key for key, value in player_score.items() 
            if value == max(player_score.values())]
        max_score = max(player_score.values())     
        return winners_list, max_score

    def check_question_range(self):
        '''Check que range and give que or end quiz accordingly.'''
        return True if self.attr['counter'] + 1 < len(self.attr['quiz_data']) else False
