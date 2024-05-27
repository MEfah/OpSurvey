import React, { FC, ReactElement } from 'react';
import classes from '../../styles/MiniSurvey.module.css';
import SurveyInfo from '../../schemas/SurveyInfo';
import ViewsIcon from '../UI/ViewsIcon/ViewsIcon';

interface MiniSurveyProps {
  surveyInfo: SurveyInfo;
}

const MiniSurvey: FC<MiniSurveyProps> = (props): ReactElement => {
  
  return (
    <div className={classes.body}>
      <div>
        <div className={classes.creator}>{props.surveyInfo.creatorName}</div>
      </div>
      <div className={classes.name}>{props.surveyInfo.name}</div>
      <div className={classes.otherInfo}>
        <div>
          <div className={classes.time}>{props.surveyInfo.completionTime} мин.</div>
          <div className={classes.questionCount}>? {props.surveyInfo.questionCount}/{props.surveyInfo.requiredCount}</div>
          <div className={classes.completionsInfo}>
            <div className={classes.completionsIcon}>
              <ViewsIcon/>
            </div>
            <div>{props.surveyInfo.completionCount}</div>
          </div>
        </div>
        <div className={classes.date}>{props.surveyInfo.creationDate.toLocaleString()}</div>
      </div>
      
    </div>
  )
}

export default MiniSurvey