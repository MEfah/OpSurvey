import { apiAuth } from '../api';
import { CreateAnswerInfo } from '../../schemas/SurveyAnswerInfo';


export async function GetAnswer(surveyId: string, userId: string) {
  return await apiAuth.get(`/surveys/${surveyId}/answers/${userId}`);
}

export async function GetUsersAnswer(surveyId: string) {
  return await apiAuth.get(`/surveys/${surveyId}/answers/my`);
}

export async function PostAnswer(surveyId: string, info: CreateAnswerInfo) {
  return await apiAuth.post(`/surveys/${surveyId}/answers`, info);
}

export async function UpdateAnswer(surveyId: string, userId: string, info: CreateAnswerInfo) {
  return await apiAuth.put(`/surveys/${surveyId}/answers/${userId}`, info);
}

export async function DeleteAnswer(surveyId: string, userId: string) {
  return await apiAuth.delete(`/surveys/${surveyId}/answers/${userId}`);
}

export async function GetAnswers(surveyId: string) {
  return await apiAuth.get(`/surveys/${surveyId}/answers`);
}

export async function GetResults(surveyId: string) {
  return await apiAuth.get(`/surveys/${surveyId}/results`);
}