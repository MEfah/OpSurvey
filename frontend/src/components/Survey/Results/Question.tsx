import React, { memo, useMemo } from 'react';
import classes from '../../../styles/Survey.module.css';
import { QuestionInfo, QuestionType } from '../../../schemas/QuestionInfo';
import {OptionList} from './OptionList';
import TextField from '@mui/material/TextField';
import { QuestionAnswerInfo } from '../../../schemas/SurveyAnswerInfo';
import dayjs, {Dayjs} from 'dayjs'
import { DateTimeResultsInfo, NumericResultsInfo, OptionsResultsInfo, QuestionResultsInfo } from '../../../schemas/ResultsInfo';
import Link from '@mui/material/Link';
import { BarChart, barElementClasses, barLabelClasses } from '@mui/x-charts/BarChart';
import { axisClasses } from '@mui/x-charts';


interface QuestionProps {
  question: QuestionInfo;
  answer?: QuestionAnswerInfo;
  result?: QuestionResultsInfo;
}

export const Question = memo(function Question ({answer, question, result}: QuestionProps) {

  const dataset = useMemo(() => {
    if (question.questionType === QuestionType.InputInteger || question.questionType === QuestionType.InputNumber) {
      return (result?.result as NumericResultsInfo).intervals.sort((a, b) => a.from - b.from).map((v) => {
        return {label: v.from.toFixed(2).toString(), count: v.count}
      });
    } else if (question.questionType === QuestionType.InputDate) {
      return (result?.result as DateTimeResultsInfo).intervals.sort((a, b) => a.from.diff(b.from)).map((v) => {
        return {label: v.from.format('DD.MM.YYYY'), count: v.count}
      });
    } else if (question.questionType === QuestionType.InputTime) {
      return (result?.result as DateTimeResultsInfo).intervals.sort((a, b) => a.from.diff(b.from)).map((v) => {
        return {label: v.from.format('HH:mm'), count: v.count}
      });
    }
  }, [question.questionType, result?.result])
  const sx=(theme: any) => ({
    [`.${barElementClasses.root}`]: {
      fill: 'var(--foreground-color-primary)'
    },
    [`.${barLabelClasses.root}`]: {
      fill: 'white'
    },
    [`.${axisClasses.root}`]: {
      [`.${axisClasses.tick}, .${axisClasses.line}`]: {
        stroke: 'var(--text-color-primary)',
      },
      [`.${axisClasses.tickLabel}`]: {
        fill: 'var(--text-color-primary)'
      },
    },
  })

  return (
    <div className={`${classes.questionBody}`}>

      <div className={classes.questionName}>
        {question.name} {question.required ? <span className={classes.requiredLabel} 
          style={{color: 'var(--text-color-secondary)'}}>Обязательный</span> : ''}
      </div>

      {typeof question.description === 'string' ? 
        <div className={classes.questionDescription}>
          {question.description}
        </div>
      : ''}
      <div style={{marginTop: 5}}>Всего ответов: {result?.answersCount ?? 0}</div>

      {
        question.questionType < 5 && question.options ?
          <OptionList options={question.options} type={question.questionType} answer={answer} results={result?.result as OptionsResultsInfo}/>
        : question.questionType === QuestionType.InputText ?
          <div style={{marginTop: 5}}>Ваш ответ: {answer?.value?.toString() ?? '-'}</div>
        : question.questionType === QuestionType.InputInteger || question.questionType === QuestionType.InputNumber ?
          <>
            <div style={{marginTop: 5}}>Ваш ответ: {answer?.value?.toString() ?? '-'}</div>
            <div className={classes.valueResultsInfo}>
              <BarChart
                dataset={dataset} height={300} slotProps={{legend: {hidden: true}}}
                series={[{ dataKey: 'count', label: 'Распределение ответов' }]}
                xAxis={[{ scaleType: 'band', dataKey: 'label', tickPlacement: 'start', tickLabelPlacement: 'tick'}]}
                barLabel={'value'}
                yAxis={[{tickInterval: dataset?.map((v) => v.count)}]}
                sx={sx}
              />
              <div>Минимум: {(result?.result as NumericResultsInfo).min}</div>
              <div>Максимум: {(result?.result as NumericResultsInfo).max}</div>
              <div>Среднее: {(result?.result as NumericResultsInfo).mean}</div>
            </div>
          </>
          
        : question.questionType === QuestionType.InputDate ?

          <>
            <div style={{marginTop: 5}}>Ваш ответ: {answer?.value ? (answer?.value as dayjs.Dayjs).format('DD.MM.YYYY') : '-'}</div>
            <div className={classes.valueResultsInfo}>
              <BarChart
                dataset={dataset} height={300} slotProps={{legend: {hidden: true}}}
                series={[{ dataKey: 'count', label: 'Распределение ответов' }]}
                xAxis={[{ scaleType: 'band', dataKey: 'label', tickPlacement: 'start', tickLabelPlacement: 'tick'}]}
                barLabel={'value'}
                yAxis={[{tickInterval: dataset?.map((v) => v.count)}]}
                sx={sx}
              />

              <div>Минимум: {(result?.result as DateTimeResultsInfo).min.format('DD.MM.YYYY')}</div>
              <div>Максимум: {(result?.result as DateTimeResultsInfo).max.format('DD.MM.YYYY')}</div>
              <div>Среднее: {(result?.result as DateTimeResultsInfo).mean.format('DD.MM.YYYY')}</div>
            </div>
          </>
        :
          <>
            <div style={{marginTop: 5}}>Ваш ответ: {answer?.value ? (answer?.value as dayjs.Dayjs).format('HH:mm') : '-'}</div>
            <div className={classes.valueResultsInfo}>
              <BarChart
                dataset={dataset} height={300} slotProps={{legend: {hidden: true}}}
                series={[{ dataKey: 'count', label: 'Распределение ответов' }]}
                xAxis={[{ scaleType: 'band', dataKey: 'label', tickPlacement: 'start', tickLabelPlacement: 'tick'}]}
                barLabel={'value'}
                yAxis={[{tickInterval: dataset?.map((v) => v.count)}]}
                sx={sx}
              />

              <div>Минимум: {(result?.result as DateTimeResultsInfo).min.format('HH:mm')}</div>
              <div>Максимум: {(result?.result as DateTimeResultsInfo).max.format('HH:mm')}</div>
              <div>Среднее: {(result?.result as DateTimeResultsInfo).mean.format('HH:mm')}</div>
            </div>
          </>
      }
    </div>
  );
})