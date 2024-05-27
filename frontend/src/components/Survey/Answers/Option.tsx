import * as React from 'react';
import { QuestionOptionInfo, QuestionType } from '../../../schemas/QuestionInfo';
import classes from '../../../styles/Survey.module.css';
import Radio from '@mui/material/Radio';
import Checkbox from '@mui/material/Checkbox';
import { useAnswerDispatch } from '../AnswerContext';
import Button from '@mui/material/Button';

export interface OptionProps {
  type: QuestionType;
  option: QuestionOptionInfo;
  questionId: number;
  canAnswer?: boolean;
  isSelected?: boolean;
}

export const Option = React.memo(function Option (props: OptionProps) {
  const dispatch = useAnswerDispatch();
  const elementRef = React.useRef<HTMLButtonElement>(null);

  function getOptionControl() {
    if ([QuestionType.SingleSelect, QuestionType.SingleSelectOther].includes(props.type))
      return (<Radio ref={elementRef} color='primary' value={props.isSelected} style={{marginTop: -5, marginBottom: -5, marginLeft: -10}} checked={props.isSelected}
      onClick={(e) => {e.stopPropagation(); e.preventDefault(); handleSelect(); }} disabled={!props.canAnswer}/>);
    else if ([QuestionType.MultiSelect, QuestionType.MultiSelectOther].includes(props.type))
      return (<Checkbox ref={elementRef} color='primary' value={props.isSelected} style={{marginTop: -5, marginBottom: -5, marginLeft: -10}} checked={props.isSelected}
      onClick={(e) => {e.stopPropagation(); e.preventDefault(); handleSelect(); }} disabled={!props.canAnswer}/>);
    return '';
  }

  function handleSelect() {
    if ([QuestionType.SingleSelect, QuestionType.SingleSelectOther].includes(props.type))
      dispatch?.({type: 'selected', optionId: props.option.id, questionId: props.questionId});
    else
      dispatch?.({type: 'checked', optionId: props.option.id, questionId: props.questionId});
  }

  function onRender() {
    console.log('option rendered');
    return '';
  }

  return (
    <>
      {onRender()}
      <Button sx={{padding: 0, textTransform: 'none', marginTop: 1, marginBottom: 1}} fullWidth onClick={(e) => { elementRef?.current?.click();}} disabled={!props.canAnswer}>
        <div className={classes.option}>
          {getOptionControl()} <div style={{color: 'var(--text-color-primary)', width: '100%'}}>{props.option.name}</div>
        </div>
      </Button>

    </>
  );
})