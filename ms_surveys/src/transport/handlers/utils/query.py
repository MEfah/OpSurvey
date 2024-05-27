from fastapi import Request
from schemas.enums.filter import FilterParameterType
from schemas.filter import FilterParamList
import re

def get_filter_params(req: Request) -> FilterParamList | None:
    """
    Преобразовать параметры запроса в массив параметров фильтрации
    """
    # Пример параметров запроса с объектами:
    # ?filterParams[0][parameterType]=0&filterParams[0][value][from]=48&filterParams[0][value][to]=288
    # Решение на основе: https://github.com/tiangolo/fastapi/issues/1415
    
    filter_params = {
        'filter_params': {
            'filterParams': list([{'parameterType': None, 'value': {'from': None, 'to': None}} for i in range(0, len(FilterParameterType))])
        }}
    
    # Возвращает словарь {"filterParams[0][parameterType]": 0, "filterParams[0][value][from]": 48, "filterParams[0][value][to]": 288}
    _query = dict((k, v) for k, v in req.query_params.items())
    
    # Преобразуем словарь в выражения python и вызываем на словаре filter_params
    for _k in _query.keys():
        parts = [f'[{x}]' if x.isnumeric() else f'["{x}"]' for x in filter(None, re.split(r'\[|\]', _k, ))]
        expr = 'filter_params' + ''.join(parts)
        # Получаем выражение filter_params['filterParams'][0]['parameterType']=0
        _eval_str = f'{expr}="{_query.get(_k)}"'
        exec(_eval_str, filter_params)
        
    filter_params['filter_params']['filterParams'] = list(filter(lambda x: x['parameterType'],filter_params['filter_params']['filterParams']))
    
    if len(filter_params['filter_params']['filterParams']) > 0:
        return(FilterParamList(**filter_params['filter_params']))
    
    return None