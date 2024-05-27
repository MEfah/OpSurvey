import dayjs from "dayjs";

export interface SurveyResultsInfo {
  surveyId: string;
  results: QuestionResultsInfo[];
}

export interface QuestionResultsInfo {
  id: number;
  answersCount: number;
  result?: NumericResultsInfo | OptionsResultsInfo | DateTimeResultsInfo;
}

export interface DateTimeResultsInfo {
  min: dayjs.Dayjs;
  max: dayjs.Dayjs;
  mean: dayjs.Dayjs;
  intervals: DateTimeInterval[];
}

export interface DateTimeInterval {
  from: dayjs.Dayjs;
  count: number;
}

export interface NumericResultsInfo {
  min: number;
  max: number;
  mean: number;
  intervals: NumericInterval[];
}

export interface NumericInterval {
  from: number;
  count: number;
}

export interface OptionsResultsInfo {
  options: OptionResultInfo[];
}

export interface OptionResultInfo {
  id: number;
  count: number;
}