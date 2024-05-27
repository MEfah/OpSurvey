import { SurveySearchParams, SurveySearchBody } from '../../schemas/SurveySearchParams';
import { apiAuth } from '../api';
import { UnfinishedSurveyInfo } from '../../schemas/UnfinishedSurvey';
import { AccessResults, AccessSurvey } from '../../schemas/SurveyAccessInfo';

export async function GetSurveys(surveySearchParams?: SurveySearchParams, surveySearchBody?: SurveySearchBody) {
  return await apiAuth.get(`/surveys/`, {
    params: {...surveySearchParams, ...surveySearchBody}
  });
}

export async function PostSurvey(formData: FormData) {
  return await apiAuth.post(`/surveys/`, formData, {
    headers: {
        'content-type': 'multipart/form-data'
    }});
}

export async function GetUsersSurveys(userId: string) {
  return await apiAuth.get(`/users/${userId}/surveys`);
}

export async function GetSurvey(surveyId: string) {
  return await apiAuth.get(`/surveys/${surveyId}`);
}

export async function GetUnfinishedSurveys(userId: string) {
  return await apiAuth.get(`/users/${userId}/surveys/unfinished`)
}

export async function GetUnfinishedSurvey(surveyId: string) {
  return await apiAuth.get(`/unfinished/${surveyId}`);
}

export async function SaveUnfinishedSurvey(formData: FormData) {
  return await apiAuth.post(`/unfinished/`, formData);
}

export async function UpdateUnfinishedSurvey(surveyId: string, formData: FormData) {
  return await apiAuth.put(`/unfinished/${surveyId}`, formData);
}

export async function DeleteUnfinishedSurvey(surveyId: string) {
  return await apiAuth.delete(`/unfinished/${surveyId}`);
}

export async function GetSurveyAccess(surveyId: string) {
  return await apiAuth.get(`/surveys/${surveyId}/access`);
}

export async function UpdateSurveyAccess(surveyId: string, accessSurvey: AccessSurvey, accessResults: AccessResults) {
  return await apiAuth.patch(`/surveys/${surveyId}/access`, { accessSurvey, accessResults });
}

export async function DeleteSurvey(surveyId: string) {
  return await apiAuth.delete(`/surveys/${surveyId}`);
}