from integrations.db.session import get_session
from schemas.auth import AuthInfo
from schemas.survey import SurveyCreated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from integrations.db.session import get_session
from repositories.recommendations import RecommendationsRepository
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.corpus import stopwords
from services.tf_idf import TfIdfMatrix
import numpy as np



class RecommendationsService():
    """
    Сервис для работы с опросами
    """
    
    def __init__(self, session: AsyncSession = Depends(get_session)):
        self.session = session
        self.repository = RecommendationsRepository(session)
        self.matrix = TfIdfMatrix()
        
    
    async def get_recommended_surveys(self, user_info: AuthInfo, limit: int, offset: int) -> list[str]:
        """Получить список идентификаторов рекомендуемых опросов"""
        user_surveys_bow = self.repository.get_user_surveys(user_info.user_id)
        user_surveys_tfidf = self.matrix.get_tfidf_from_bow(user_surveys_bow)
        similarities = cosine_similarity(user_surveys_tfidf, await self.matrix.get_matrix())
        indices = np.argpartition(similarities, len(similarities)-(limit+offset))[-offset-limit:-offset]
        return indices.tolist()
        
        
    async def add_survey_bow(self, doc_id: int, survey: SurveyCreated):
        """Добавить bag of words опроса в базу данных"""
        
        #doc_id = await self.repository.get_survey_doc_id(survey_id=survey.id)
        
        # Объединить весь текст опроса в единую строку
        document = ' '.join(
            [survey.name]
            + ([survey.description] if survey.description else [])
            + [q.name + (' ' + q.description if q.description else '') for q in survey.questions])
        
        # Получить bag of words опроса
        russian_stopwords = stopwords.words("russian")
        count_vectorizer = CountVectorizer(stop_words=russian_stopwords)
        bow_matrix = count_vectorizer.fit_transform([document])
        
        # Получить список слов, добавить в бд новые и получить для всех слов идентификаторы
        # word_map - словарь вида: слово - идентификатор
        words = count_vectorizer.get_feature_names_out()
        word_map = await self.repository.insert_and_get_words(words.tolist()) 
        
        # Подготовить данные для добавления в бд
        # Получаем список кортежей вида: ид документа - ид слова - количество вхождений
        word_counts = bow_matrix.toarray()[0]
        survey_bow = [(doc_id, word_map[word], word_counts[index]) for index, word in enumerate(words)]
        
        self.repository.insert_bow(survey_bow)