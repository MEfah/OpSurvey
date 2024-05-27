import { QuestionInfo } from "./QuestionInfo";
import { AccessResults, AccessSurvey, AccessApi } from './SurveyAccessInfo';
import SurveyInfo from "./SurveyInfo";

export default interface FullSurveyInfo extends SurveyInfo {
  questions: QuestionInfo[];
  shuffleQuestions: boolean;
}

export interface CreateSurveyInfo {
  name: string;
  creatorId: string;
  creatorName: string;
  creatorImgSrc?: string;
  description?: string;
  imgSrc?: string;
  questions: QuestionInfo[];
  accessSurvey: AccessSurvey;
  accessResults: AccessResults;
  accessApi: AccessApi;
  shuffleQuestions: boolean;
}