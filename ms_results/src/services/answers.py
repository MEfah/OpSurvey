from bson import ObjectId
from pydantic import TypeAdapter
from exceptions import ConflictException
import pymongo.errors
from integrations.db.session import get_collection
from schemas.answer import SurveyAnswerCreate
from models.survey import Survey
from models.answer import SurveyAnswer, QuestionAnswer
from models.enums.access import AccessSurveyType, AccessResultsType
from models.enums.question import QuestionType
from schemas.enums.filter import FilterParameterType
from schemas.enums.sort import SortType
from schemas.auth import AuthInfo
from schemas.answer import SurveyAnswerResponse, SurveyAnswerList
from schemas.results import QuestionResults, OptionsResults, ValueResults, SurveyResults
from datetime import datetime, timezone
from exceptions import UnauthorizedException, ForbiddenException, UnprocessableEntityException
from services.pipelines.results import get_result_pipeline
import pymongo


class AnswersService():
    """
    Сервис для работы с результатами
    """
    
    def __init__(self):
        self.collection = get_collection('answers')
        self.collection.list_indexes()
        
        
    def _get_typed_question_answer(self, answer: QuestionAnswer, question_type: QuestionType) -> QuestionAnswer:
        """Преобразовать ответ в ответ с корректными типами значений, убрать мусор"""
        if not answer.value and (not answer.options or len(answer.options) == 0):
            return None
        
        try:
            match question_type:
                case QuestionType.INPUT_INTEGER:
                    return QuestionAnswer(id=answer.id, value=int(answer.value))
                case QuestionType.INPUT_NUMBER:
                    return QuestionAnswer(id=answer.id, value=float(answer.value))
                case QuestionType.INPUT_DATE:
                    return QuestionAnswer(id=answer.id, value=datetime.fromisoformat(answer.value.replace('Z', '+00:00'))) #2024-05-21T14:15:00.000Z
                case QuestionType.INPUT_TIME:
                    dt=datetime.fromisoformat(answer.value.replace('Z', '+00:00')) #2024-05-21T14:15:00.000Z
                    return QuestionAnswer(id=answer.id, value=datetime(1900, 1, 1, dt.hour, dt.minute, dt.second))
                case QuestionType.DROP_DOWN:
                    if len(answer.options) > 0 and answer.options[0] == -1:
                        return None
                    return QuestionAnswer(id=answer.id, options=answer.options)
                case QuestionType.MULTI_SELECT_OTHER | QuestionType.SINGLE_SELECT_OTHER:
                    if not answer.options or len(answer.options) == 0:
                        return None
                    else:
                        try:
                            ind = answer.options.index(-1)
                        except: ind = -1
                        if ind >= 0 and (not answer.value or answer.value == ''):
                            answer.options.pop(ind)
                            if len(answer.options) == 0:
                                return None
                            return QuestionAnswer(id=answer.id, options=answer.options)
                        return answer
                case QuestionType.SINGLE_SELECT | QuestionType.MULTI_SELECT:
                    if not answer.options or len(answer.options) == 0:
                        return None
                    else:
                        try:
                            ind = answer.options.index(-1)
                        except: ind = -1
                        if ind >= 0:
                            answer.options.pop(ind)
                        return QuestionAnswer(id=answer.id, options=answer.options)
                case _:
                    return answer
        except Exception as e:
            print(e)
            raise UnprocessableEntityException('Указан некорректный тип значения для ответа')

        
    def fix_question_answer_types(self, answer_info: SurveyAnswerCreate, survey: Survey):
        """Преобразует строковые значения в значения нужного типа"""
        # TODO придумать более оптимальный способ
        answers: list[QuestionAnswer] = []
        for item, index in enumerate(survey.question_types):
            for q in answer_info.question_answers:
                if q.id == index:
                    answer = self._get_typed_question_answer(q, item)
                    if answer:
                        answers.append(answer)
                    break
        answer_info.question_answers = answers


    async def add_survey_answer(self, survey_id: str, user_id: str, answer_info: SurveyAnswerCreate) -> SurveyAnswerResponse:
        """Добавить ответ на опрос"""
        
        answer = SurveyAnswer(survey_id=survey_id, user_id=user_id, is_finished=answer_info.is_finished,
                              question_answers=[QuestionAnswer(**q.model_dump()) for q in answer_info.question_answers])
        answer_dump = answer.model_dump(exclude_none=True)

        try:
            result = await self.collection.insert_one(answer_dump)
        except pymongo.errors.DuplicateKeyError:
            raise ConflictException(location=['survey_id', 'user_id'], description='Ответ пользователя на опрос уже существует')
        
        return SurveyAnswerResponse(**answer_dump) if result else None
        
        
    async def get_survey_answers(self, survey_id: str, limit: int, offset: int) -> SurveyAnswerList:
        """Получить список ответов на опрос"""
        return SurveyAnswerList(answers = await self.collection.find({"survey_id": survey_id}).skip(offset).limit(limit).to_list(limit))
        
        
    async def get_survey_results(self, survey_id: str):
        """Получить агрегированные результаты опроса"""
        res = await self.collection.aggregate(get_result_pipeline(survey_id)).to_list(1)
        if res:
            val, opt = res[0]['value_results'], res[0]['options_results']
            question_results: list[QuestionResults] = []
            for v in val:
                question_results.append(QuestionResults(id=v['_id'], answers_count=v['answer_count'], result=ValueResults(**v) if len(v) > 2 else None))
            for o in opt:
                question_results.append(QuestionResults(id=o['_id'], answers_count=o['answer_count'], result=OptionsResults(**o)))
            return SurveyResults(survey_id=survey_id, results=question_results)

        
    async def get_user_answer(self, survey_id: str, user_id: str) -> SurveyAnswerResponse:
        """Получить ответ пользователя"""
        answer = await self.collection.find_one({'survey_id': survey_id, 'user_id': user_id})
        return SurveyAnswerResponse(**answer) if answer else None
         
    
    async def update_survey_answer(self, survey_id: str, user_id: str, answer_info: SurveyAnswerCreate) -> SurveyAnswerResponse:
        """Изменить ответ на опрос"""
        answer = SurveyAnswer(survey_id=survey_id, user_id=user_id, is_finished=answer_info.is_finished,
                              question_answers=[QuestionAnswer(**q.model_dump()) for q in answer_info.question_answers])
        answer_dump = answer.model_dump(by_alias=True, exclude_none=True)
        result = await self.collection.find_one_and_update(
            {'survey_id': survey_id, 'user_id': user_id},
            {'$set': answer_dump},
        )
        return SurveyAnswerResponse(**answer_dump) if result else None
        
    async def delete_survey_answer(self, survey_id: str, user_id: str) -> bool:
        """Удалить ответ на опрос"""
        delete_result = await self.collection.delete_one({"survey_id": survey_id, "user_id": user_id})

        if delete_result.deleted_count == 1:
            return True
        
        return False