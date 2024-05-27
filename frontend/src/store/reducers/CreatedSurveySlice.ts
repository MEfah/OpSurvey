import { createSlice, PayloadAction } from "@reduxjs/toolkit";
import { UserInfo } from "../../schemas/UserInfo";
import FullSurveyInfo, { CreateSurveyInfo } from "../../schemas/FullSurveyInfo";
import { UnfinishedSurveyInfo } from "../../schemas/UnfinishedSurvey";
import { QuestionType } from "../../schemas/QuestionInfo";

const initialState: UnfinishedSurveyInfo = {
  name: '',
  description: '',
  shuffleQuestions: false,
  questions: undefined
}

export const createdSurveySlice = createSlice({
  name: 'createdSurvey',
  initialState: initialState,
  reducers: {
    setSurvey(state, action: PayloadAction<UnfinishedSurveyInfo>): UnfinishedSurveyInfo {
      return {...action.payload};
    },
    clearSurvey(state): UnfinishedSurveyInfo {
      return {...initialState};
    }
  }
});

export default createdSurveySlice.reducer;