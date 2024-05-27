import * as React from 'react';
import { QuestionType } from '../../../schemas/QuestionInfo';
import classes from '../../../styles/Survey.module.css';
import TextField from '@mui/material/TextField';
import Radio from '@mui/material/Radio';
import Checkbox from '@mui/material/Checkbox';
import { useAnswerDispatch } from '../AnswerContext';
import Button from '@mui/material/Button';

export interface OptionProps {
  type: QuestionType;
  questionId: number;
  canAnswer?: boolean;
  isSelected?: boolean;
  value?: string;
}

export const OtherOption = React.memo(function OtherOption (props: OptionProps) {
  const dispatch = useAnswerDispatch();
  const elementRef = React.useRef<HTMLButtonElement>(null);
  const [canRipple, setCanRipple] = React.useState(true);

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
    // TODO добиться корректной работе при спаме кликом
    if (!props.isSelected) {
      setTimeout(() => {setCanRipple(false)}, 400);
    } else {
      setCanRipple(true);
    }
    if ([QuestionType.SingleSelect, QuestionType.SingleSelectOther].includes(props.type))
      dispatch?.({type: 'selected', optionId: -1, questionId: props.questionId});
    else
      dispatch?.({type: 'checked', optionId: -1, questionId: props.questionId});
  }

  function handleAnswerChanged(value: string | undefined) {
    dispatch?.({type: 'otherChanged', questionId: props.questionId, value: value});
  }

  return (
    <>
      <Button sx={{padding: 0, textTransform: 'none', marginTop: 1, marginBottom: 1}} fullWidth disabled={!props.canAnswer}
        onClick={(e) => { if (!props.isSelected) elementRef?.current?.click();}}
        disableRipple={!canRipple} type='button'>
        <div className={classes.option}>
          {getOptionControl()} 
          {props.isSelected ? 
            <TextField variant='standard' placeholder='Свой вариант ответа...' fullWidth multiline onClick={(e) => e.stopPropagation()}
              value={props.value} onChange={(e) => handleAnswerChanged(e.currentTarget.value)} disabled={!props.canAnswer}/> 
          : 
            <div style={{color: 'var(--text-color-primary)', width: '100%'}}><i>Свой вариант ответа...</i></div>}
        </div>
      </Button>
    </>
  );
})