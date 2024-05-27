export interface SurveySearchParams {
  limit?: number;
  offset?: number;
}

export interface SurveySearchBody {
  filterParams?: FilterParam[];
  searchText?: string;
  sortType?: SortParameterType;
  sortAscending?: boolean;
}

export interface FilterParam {
  parameterType: FilterParameterType;
  value?: FilterRange;
}

export interface FilterRange {
  from?: number | Date;
  to?: number | Date;
}

export enum FilterParameterType {
  COMPLETIONS=0,
  QUESTIONS=1,
  REQUIRED_QUESTIONS=2,
  COMPLETION_TIME=3,
  CREATION_DATE=4,
  RESULTS_ACCESSIBLE=5
}

export enum SortParameterType {
  RECOMMENDED=0,
  POPULARITY=1,
  COMPLETIONS=2,
  QUESTIONS=3,
  REQUIRED_QUESTIONS=4,
  COMPLETION_TIME=5,
  CREATION_DATE=6
}