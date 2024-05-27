from enum import IntEnum


class FilterParameterType(IntEnum):
    """
    Перечисление параметров фильтрации
    """
    
    COMPLETIONS=0
    QUESTIONS=1
    REQUIRED_QUESTIONS=2
    COMPLETION_TIME=3
    CREATION_DATE=4
    RESULTS_ACCESSIBLE=5