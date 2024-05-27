import React from 'react';
import surveyClasses from '../../styles/SurveyItem.module.css'
import FullSurveyInfo from '../../schemas/FullSurveyInfo';
import { MEDIA_URL } from '../../http/api';
import ViewsIcon from '../UI/ViewsIcon/ViewsIcon';

export interface SurveyInfoProps {
  survey: FullSurveyInfo;
}

export default function SurveyInfo (props: SurveyInfoProps) {
  return (
    <>
      <div>
        <div className={surveyClasses.creator}>{props.survey.creatorName}</div>
        <div className={surveyClasses.date}>{props.survey.creationDate.toLocaleString()}</div>
      </div>
      
      <div className={surveyClasses.name}>{props.survey.name}</div>
      <div className={surveyClasses.otherInfo}>
        <div>{props.survey.completionTime} мин.</div>
        <div>Всего вопросов: {props.survey.questionCount} / Обязательных: {props.survey.requiredCount}</div>
        <div className={surveyClasses.completionsInfo}>
          <div className={surveyClasses.completionsIcon}>
            <ViewsIcon/>
          </div>
          <div>{props.survey.completionCount}</div>
        </div>
      </div>
      <img className={surveyClasses.img} src={props.survey.imgSrc ? MEDIA_URL + props.survey.imgSrc : ''} alt=''></img>
      <div className={surveyClasses.desc}>{props.survey.description}</div>
    </>
  );
}
