import random

ENTERTAINMENT_NUMS = [10, 11, 12, 13, 14, 15, 16, 29, 31, 32]
SCIENCE_NUMS = [17, 18, 19, 30]

CATEGORY = {
    "general knowledge": 9,
    "entertainment": random.choice(ENTERTAINMENT_NUMS),
    "science": random.choice(SCIENCE_NUMS),
    "mythology": 20,
    "sports": 21,
    "geography": 22,
    "history": 23,
    "politics": 24,
    "art": 25,
    "celebrities": 26,
    "animals": 27,
    "vehicles": 28
}

SOUNDS = {
    "welcome": "<audio src='soundbank://soundlibrary/musical/amzn_sfx_drum_and_cymbal_02'/>",
    "positive_response": "<audio src='soundbank://soundlibrary/ui/gameshow/amzn_ui_sfx_gameshow_positive_response_03'/>",
    "negative_response": "<audio src='soundbank://soundlibrary/ui/gameshow/amzn_ui_sfx_gameshow_negative_response_02'/>",
    "winning": "<audio src='soundbank://soundlibrary/human/amzn_sfx_crowd_applause_02'/>",
    "start_question": "<audio src='soundbank://soundlibrary/musical/amzn_sfx_bell_med_chime_02'/>"
}

DIFFICULTY = {
    "easy": "easy",
    "medium": "medium",
    "hard": "hard"
}