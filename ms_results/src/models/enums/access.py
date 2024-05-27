from enum import IntEnum


class AccessSurveyType(IntEnum):
    """
    Перечисление типов доступа к опросу
    """
    ALL=0
    ONLY_AUTHORIZED=1
    ONLY_URL=2
    ONLY_LIST=3
    ONLY_KEYS=4
    ONLY_LIST_AND_KEYS=5
    NONE=6
    
    
class AccessResultsType(IntEnum):
    """
    Перечисление типов доступа к результатам опроса
    """
    ALL=0
    ONLY_LIST=1
    NONE=2
    
    
class AccessApiType(IntEnum):
    """
    Перечисление типов доступа к API опроса
    """
    ALL=0
    ONLY_LIST=1
    NONE=2