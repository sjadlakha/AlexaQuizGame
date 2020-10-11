# quiz_data = {
#     " The World Largest desert is ? A. Thar B. Kalahari C. Sahara D. Sonoran" : {"option c": "Sahara"},
#      " Country that has the highest in Barley Production ? \
#         A. China B. India C. Russia D. France": { "option c": "Russia"},
#     " The Central Rice Research Station is situated in ? \
#         A. Chennai B. Cuttack C. Bangalore D. Quilon": {"option b": "Cuttack"},
#     " Mount Everest is located in ? A. India B. Nepal C. Tibet D. China": {"option b": "Nepal"},
#     " Gate way of India is ? A. Chennai B. Mumbai C. Kolkata D. New Delhi": {"option b": "Mumbai"},
#     " World Largest desert is ? A. Thar B. Kalahari C. Sahara D. Sonoran" : {"option c": "Sahara"}
# }

import requests
import random
import pdb
# from constants import CATEGORY
def middleware(question_amount, category):
    # pdb.set_trace()

    url = "https://opentdb.com/api.php?amount={ques}&category={category}&type=multiple".format(
        ques=question_amount, category=category)

    print('question middleware is called')
    data = requests.get(url).json()
    quiz_data = {}
    val = {0:'a', 1:'b', 2:'c', 3:'d'}

    if data['response_code'] == 0:
        for res in data['results']:
            res['incorrect_answers'].insert(random.randrange(0, 3), res['correct_answer'])
            opt = res['incorrect_answers']
            options = f'A. {opt[0]}, B. {opt[1]}, C. {opt[2]}, D.{opt[3]}'
            correct_opt = res['incorrect_answers'].index(res['correct_answer'])
            answer = "option "+val[correct_opt]
            quiz_data[res['question']+' '+options] = {answer: res['correct_answer']}
        print(quiz_data)
        return quiz_data 
    else:
        print('There are no more quetsion for this category!!')
