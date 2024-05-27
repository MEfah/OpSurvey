import React, { memo } from 'react';
import { QuestionOptionInfo, QuestionType } from '../../../schemas/QuestionInfo';
import classes from '../../../styles/Survey.module.css';
import {Option} from './Option';
import { QuestionAnswerInfo } from '../../../schemas/SurveyAnswerInfo';
import FormControl from '@mui/material/FormControl';
import Select from '@mui/material/Select';
import MenuItem from '@mui/material/MenuItem';
import { useAnswerDispatch } from '../AnswerContext';
import { OtherOption } from './OtherOption';

export interface OptionListProps {
  type: QuestionType;
  questionId: number;
  options: QuestionOptionInfo[];
  answer?: QuestionAnswerInfo;
  canAnswer?: boolean;
}

export const OptionList = memo(function OptionList ({type, options, questionId, answer, canAnswer}: OptionListProps) {
  const dispatch = useAnswerDispatch();

  function handleSelect(event: any, child: React.ReactNode) {
    dispatch?.({type: 'selected', optionId: event.target.value, questionId: questionId});
  }

  function getIsSelected(id: number) {
    return answer?.options ? answer?.options.includes(id) : false;
  }

  return (
    <div className={classes.options} style={type === QuestionType.DropDown ? {marginTop: 10, marginBottom: 20} : {}}>

      {type < 4 ? 
        <>
          {options.map((val, index) => 
            <Option type={type} option={val} key={val.id} questionId={questionId} isSelected={getIsSelected(index)} canAnswer={canAnswer}></Option>)}
          {[QuestionType.SingleSelectOther, QuestionType.MultiSelectOther].includes(type) ? 
            <>
              <OtherOption type={type} key={-1} questionId={questionId} isSelected={getIsSelected(-1)} value={answer?.value as string} canAnswer={canAnswer}/>
            </>
          : ''}
        </>
      :
        <FormControl fullWidth size='small' disabled={!canAnswer}>
          <Select sx={{color: 'var(--text-color-primary)'}}
            value={answer?.options?.[0] ?? -1}
            onChange={handleSelect}
          >
            <MenuItem value={-1} key={-1} sx={{color: 'var(--text-color-primary)'}}><i>Без выбора</i></MenuItem>
            {options.map((val, index) => <MenuItem value={val.id} key={val.id} sx={{color: 'var(--text-color-primary)'}}>{val.name}</MenuItem>)}
          </Select>
        </FormControl>
      }
    </div>
  );
})