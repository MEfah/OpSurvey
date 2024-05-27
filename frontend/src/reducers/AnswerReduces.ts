import { QuestionAnswerInfo, SurveyAnswerInfo } from "../schemas/SurveyAnswerInfo";


export function answerReducer(answer: SurveyAnswerInfo, action: AnswerAction): SurveyAnswerInfo {
  switch (action.type) {
    case 'changed': {
      return action.answer;
    }
    case 'questionChanged': {
      return { 
        ...answer,
        questionAnswers: answer.questionAnswers.map(a => {
          if (a.id === action.answer.id) {
            return action.answer;
          } else {
            return a;
          }
        }
      )};
    }
    case 'selected': {
      return { 
        ...answer,
        questionAnswers: answer.questionAnswers.map(a => {
          if (a.id === action.questionId) {
            // TODO Сделать более эффективно
            let newOptions = a.options;

            if (newOptions) {
              const ind = newOptions.indexOf(action.optionId)
              if (ind > -1) {
                newOptions.splice(ind, 1);
              } else {
                newOptions = [action.optionId];
              }
            } else {
              newOptions = [action.optionId];
            }
            return {
              ...a, options: newOptions
            };
          } else {
            return a;
          }
        }
      )};
    }
    case 'checked': {
      return { 
        ...answer,
        questionAnswers: answer.questionAnswers.map(a => {
          if (a.id === action.questionId) {
            // TODO Сделать более эффективно
            let newOptions = a.options;

            if (newOptions) {
              const ind = newOptions.indexOf(action.optionId);
              if (ind > -1) {
                newOptions.splice(ind, 1);
              } else {
                newOptions.push(action.optionId);
              }
            } else {
              newOptions = [action.optionId];
            }
            return {
              ...a, options: newOptions
            };
          } else {
            return a;
          }
        }
      )};
    }
    case 'otherChanged': {
      return { 
        ...answer,
        questionAnswers: answer.questionAnswers.map(a => {
          if (a.id === action.questionId) {
            return {
              ...a, value: action.value
            }
          } else {
            return a;
          }
        }
      )};
    }
    default: {
      throw Error('Unknown action');
    }
  }
}

export type AnswerAction = 
  | {type: 'changed', answer: SurveyAnswerInfo}
  | {type: 'questionChanged', answer: QuestionAnswerInfo}
  | {type: 'selected', questionId: number, optionId: number}
  | {type: 'checked', questionId: number, optionId: number}
  | {type: 'otherChanged', questionId: number, value: string | undefined}