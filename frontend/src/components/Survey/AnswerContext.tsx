import React from 'react';
import { createContext, useContext} from 'react';
import { SurveyAnswerInfo } from '../../schemas/SurveyAnswerInfo';
import { AnswerAction } from '../../reducers/AnswerReduces';


const AnswerContext = createContext<SurveyAnswerInfo | null>(null);


const AnswerDispatchContext = createContext<React.Dispatch<AnswerAction> | null>(null);


export function useAnswer() {
  return useContext(AnswerContext);
}


export function useAnswerDispatch() {
  return useContext(AnswerDispatchContext);
}


interface AnswerProviderProps {
  children: React.ReactNode;
  answer: SurveyAnswerInfo;
  dispatch: React.Dispatch<AnswerAction>;
}


export function SurveyAnswerProvider(props: AnswerProviderProps) {
  return (
    <AnswerContext.Provider value={props.answer}>
      <AnswerDispatchContext.Provider value={props.dispatch}>
        {props.children}
      </AnswerDispatchContext.Provider>
    </AnswerContext.Provider>
  );
}