import React from 'react';
import classes from '../../styles/SurveyItem.module.css';
import SurveyInfo from '../../schemas/SurveyInfo';
import ViewsIcon from '../UI/ViewsIcon/ViewsIcon';
import { MEDIA_URL } from '../../http/api';
import { useNavigate } from 'react-router-dom';

export interface ISurveyItemProps {
}

export default function SurveyItem (props: SurveyInfo) {
  const navigate = useNavigate();

  return (
    <div className={classes.body + ' panel'} onClick={() => navigate(`/surveys/${props.id}`)}>
      <div>
        <div className={classes.creator}>{props.creatorName}</div>
        <div className={classes.date}>{props.creationDate.toLocaleString()}</div>
      </div>
      
      <div className={classes.name}>{props.name}</div>
      <div className={classes.otherInfo}>
        <div>{props.completionTime} мин.</div>
        <div>Всего вопросов: {props.questionCount} / Обязательных: {props.requiredCount}</div>
        <div className={classes.completionsInfo}>
          <div className={classes.completionsIcon}>
            <ViewsIcon/>
          </div>
          <div>{props.completionCount}</div>
        </div>
      </div>
      {props.imgSrc ? 
        <img className={classes.img} src={props.imgSrc ? MEDIA_URL + props.imgSrc : ''} alt=''></img>
      : 
        ''}

      {props.description ? 
        <div className={classes.desc +( props.description && props.description.length > 500 ? ' fading-text' : '')}>
          {props.description}
        </div>
      : 
        ''}
      
    </div>
  );
}