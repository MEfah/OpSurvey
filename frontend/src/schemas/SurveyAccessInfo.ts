export interface AccessSurvey {
  accessTypeSurvey: AccessSurveyType;
  accessList?: string[];
  accessKeys?: string[];
}

export interface AccessResults {
  accessTypeResults: AccessResultsType;
  accessList?: string[];
}

export interface AccessApi {
  accessTypeApi: AccessApiType;
  accessList?: string[];
}

export enum AccessSurveyType{
  ALL=0,
  ONLY_AUTHORIZED=1,
  ONLY_URL=2,
  ONLY_LIST=3,
  ONLY_KEYS=4,
  ONLY_LIST_AND_KEYS=5,
  NONE=6
}
    
export enum AccessResultsType{
    ALL=0,
    ONLY_LIST=1,
    NONE=2
  }
  
export enum AccessApiType{
  ALL=0,
  ONLY_LIST=1,
  NONE=2
}

