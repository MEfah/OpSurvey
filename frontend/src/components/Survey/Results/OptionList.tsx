import React, { memo, useMemo } from 'react';
import { QuestionOptionInfo, QuestionType } from '../../../schemas/QuestionInfo';
import classes from '../../../styles/Survey.module.css';
import {Option} from './Option';
import { QuestionAnswerInfo } from '../../../schemas/SurveyAnswerInfo';
import { OptionsResultsInfo } from '../../../schemas/ResultsInfo';


export interface OptionListProps {
  type: QuestionType;
  options: QuestionOptionInfo[];
  answer?: QuestionAnswerInfo;
  answer_count?: number;
  results?: OptionsResultsInfo;
}


export const OptionList = memo(function OptionList ({type, options, answer, answer_count, results}: OptionListProps) {
  const totalCount = useMemo(() => {
    if (results){
      let count = 0;
      results.options.forEach((v) => {count = count + v.count});
      console.log(count);
      return count;
    }
    return undefined
  }, [results]);
  
  
  function getIsSelected(id: number) {
    return answer?.options ? answer?.options.includes(id) : false;
  }

  function getOptionCount(id: number) {
    if (!results)
      return undefined;

    return results.options.find((v) => v.id === id)?.count;
  }

  return (
    <div className={classes.options} style={type === QuestionType.DropDown ? {marginTop: 10, marginBottom: 20} : {}}>
      {options.map((val, index) => 
        <Option type={type} key={val.id} isSelected={getIsSelected(index)} totalCount={totalCount} count={getOptionCount(val.id)}>{val.name}</Option>)}
      {[QuestionType.SingleSelectOther, QuestionType.MultiSelectOther].includes(type) ? 
        <>
          <Option type={type} key={-1} isSelected={getIsSelected(-1)} totalCount={totalCount} count={getOptionCount(-1)}><i>Свой вариант ответа...</i></Option>
        </>
      : ''}
    </div>
  );
})