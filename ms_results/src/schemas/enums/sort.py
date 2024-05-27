from enum import IntEnum


class SortType(IntEnum):
    """
    Перечисление параметров сортировки
    """
    
    RECOMMENDED=0
    POPULARITY=1
    COMPLETIONS=2
    QUESTIONS=3
    REQUIRED_QUESTIONS=4
    COMPLETION_TIME=5
    CREATION_DATE=6