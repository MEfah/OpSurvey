import dayjs from "dayjs";
import { CreateSurveyInfo } from "./FullSurveyInfo";
import { QuestionInfo, QuestionType } from "./QuestionInfo";

export interface UnfinishedSurveyInfo extends 
  Omit<CreateSurveyInfo, 'questions' | 'creatorId' | 'creatorName' | 'creatorImgSrc' | 'accessSurvey' | 'accessResults' | 'accessApi'>, 
  Partial<Pick<CreateSurveyInfo, 'questions'>> { 
  id?: string;
}

export interface FullUnfinishedSurveyInfo extends UnfinishedSurveyInfo {
  id: string;
  updatedDate: dayjs.Dayjs;
}

export interface UnfinishedSurveyItemInfo extends Omit<FullUnfinishedSurveyInfo, 'questions' | 'shuffleQuestions'> {

}