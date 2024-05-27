from typing import AsyncGenerator, List, Tuple
from integrations.db.session import get_session
from repositories.recommendations import RecommendationsRepository
from sklearn.feature_extraction.text import TfidfTransformer
from scipy.sparse import coo_matrix, spmatrix
import numpy as np
from sqlalchemy.ext.asyncio import AsyncSession
from integrations.db.session import get_session, get_async_session
from fastapi import Depends
from sklearn.metrics.pairwise import cosine_similarity
from nltk.corpus import stopwords
import numpy as np

async def initialize():
    await TfIdfMatrix().initialize()


class TfIdfMatrix():
    _instance = None


    def __init__(self):
        self._tfidf_matrix = None
        self._tfidf_transformer = None
        self.doc_ids = set()
        self.bow_len = 0
        self.uncalc_bow_len = 0
        

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @property
    async def _session(self):
        return await get_session().__anext__()
    
    @property
    async def _repository(self):
        return RecommendationsRepository(await self._session)


    async def initialize(self):
        """Загрузить bag of words и сгенерировать tf-idf матрицу"""
        bow = await (await self._repository).get_bow()
        self.bow_len = len(bow)
        coo = np.array(bow).T
        if len(coo) == 0:
            return np.ndarray([])
        coo_matr = coo_matrix(coo[2], (coo[0], coo[1]))
        self._tfidf_transformer = TfidfTransformer()
        self.doc_ids = list(dict.fromkeys(coo[0]))
        self._tfidf_matrix = self._tfidf_transformer.fit_transform(coo_matr)


    def get_tfidf_from_bow(self, bow: List[Tuple[int, int, int]]) -> spmatrix:
        coo = np.array(bow).T
        coo_matr = coo_matrix(coo[2], (coo[0], coo[1]))
        return self._tfidf_transformer.transform(coo_matr)


    def get_matrix(self) -> np.ndarray:
        if self._tfidf_matrix:
            return self._tfidf_matrix
        raise Exception('Matrix was not initialized')
    
    
    async def append_bow(self, bow: List[Tuple[int, int, int]]) -> None:
        """
        Добавить tf/idf для bag of words. Если длина добавленных 
        строк больше 1% всей матрицы, перерасчитывает всю матрицу
        Не добавляет bow в бд.
        """
        self.uncalc_bow_len += len(bow)
        if self.uncalc_bow_len > self.bow_len / 100:
            await self.initialize()
            return
        
        
    async def get_closest(self, bow: List[Tuple[int, int, int]], limit: int, offset: int) -> list[int]:
        user_surveys_tfidf = self.matrix.get_matrix_from_bow(bow)
        similarities = cosine_similarity(user_surveys_tfidf, self.matrix.get_matrix)
        indices = np.argpartition(similarities, len(similarities)-(limit+offset))[-offset-limit:-offset]
        return [self.doc_ids[ind] for ind in indices]