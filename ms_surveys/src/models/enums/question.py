from enum import IntEnum


class QuestionType(IntEnum):
    """
    Перечисление типов вопросов
    """
    SINGLE_SELECT=0,
    SINGLE_SELECT_OTHER=1
    MULTI_SELECT=2
    MULTI_SELECT_OTHER=3
    DROP_DOWN=4
    INPUT_TEXT=5
    INPUT_NUMBER=6
    INPUT_INTEGER=7
    INPUT_DATE=8
    INPUT_TIME=9