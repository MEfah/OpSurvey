import React, { memo } from 'react';
import classes from '../../../styles/Survey.module.css';
import { QuestionInfo, QuestionType } from '../../../schemas/QuestionInfo';
import {OptionList} from './OptionList';
import TextField from '@mui/material/TextField';
import { QuestionAnswerInfo } from '../../../schemas/SurveyAnswerInfo';
import { useAnswerDispatch } from '../AnswerContext';
import { DatePicker } from '@mui/x-date-pickers/DatePicker';
import { TimePicker } from '@mui/x-date-pickers/TimePicker';
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import dayjs, {Dayjs} from 'dayjs'


interface QuestionProps {
  question: QuestionInfo;
  answer?: QuestionAnswerInfo;
  canAnswer?: boolean;
}


export const Question = memo(function Question ({answer, question, canAnswer}: QuestionProps) {
  const dispatch = useAnswerDispatch();

  function handleAnswerChanged(value: Dayjs | string | number | undefined) {
    dispatch?.({type: 'questionChanged', answer: {
      id: question.id, value: value
    }});
  }
  
  function onRender() {
    console.log('question rendered');
    return '';
  }

  return (
    <div className={classes.questionBody}>
      {onRender()}
      <div className={classes.questionName}>
        {question.name} {question.required ? <span className={classes.requiredLabel} 
          style={{color: answer?.options || answer?.value ? 'green' : 'red'}}>*Обязательный</span> : ''}
      </div>

      {typeof question.description === 'string' ? 
        <div className={classes.questionDescription}>
          {question.description}
        </div>
      : ''}

      {question.questionType < 5 ?
        <div>
          <OptionList type={question.questionType} options={question.options!} questionId={question.id} answer={answer} canAnswer={canAnswer}/>
        </div>

      : question.questionType === QuestionType.InputText ?
        <TextField size='small' value={answer?.value ?? ''} multiline fullWidth onChange={(e) => handleAnswerChanged(e.currentTarget.value)}
          style={{marginTop: 10, marginBottom: 10}} color='primary' disabled={!canAnswer}/>
      : question.questionType === QuestionType.InputNumber ?
        <TextField size='small' value={answer?.value ?? ''} onChange={(e) => handleAnswerChanged(e.currentTarget.value)} type='number'
          style={{marginTop: 10, marginBottom: 10}} disabled={!canAnswer}/>
      : question.questionType === QuestionType.InputInteger ?
        <TextField size='small' value={answer?.value ?? ''} onChange={(e) => handleAnswerChanged(e.currentTarget.value)} type='number'
          style={{marginTop: 10, marginBottom: 10}} disabled={!canAnswer}/>
      : question.questionType === QuestionType.InputDate ?
        <LocalizationProvider dateAdapter={AdapterDayjs}>
          <DatePicker className={classes.overrideDatetime} sx={{marginTop: 1, marginBottom: 1}} disabled={!canAnswer}
            value={dayjs.isDayjs(answer?.value) ? answer?.value : null} onChange={(val) => {handleAnswerChanged(val ?? undefined)}}/>
        </LocalizationProvider>
      : question.questionType === QuestionType.InputTime ?
        <LocalizationProvider dateAdapter={AdapterDayjs}>
          <TimePicker className={classes.overrideDatetime} sx={{marginTop: 1, marginBottom: 1}} disabled={!canAnswer}
            value={dayjs.isDayjs(answer?.value) ? answer?.value : null} ampm={false} onChange={(val) => {handleAnswerChanged(val ?? undefined)}}/>
        </LocalizationProvider>
      : ''}
      
    </div>
  );
})