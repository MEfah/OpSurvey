import { Dayjs } from "dayjs";

export interface SurveyAnswerInfo {
  surveyId: string;
  userId: string;
  isFinished: boolean;
  questionAnswers: QuestionAnswerInfo[];
}

export interface CreateAnswerInfo extends Omit<SurveyAnswerInfo, 'surveyId' | 'userId'> {

}

export interface QuestionAnswerInfo {
  id: number;
  value: string | Dayjs | number | undefined
  options?: number[]
}