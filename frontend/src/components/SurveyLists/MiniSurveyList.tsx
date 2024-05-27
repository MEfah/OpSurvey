import React from 'react';
import classes from '../../styles/MiniSurvey.module.css'
import MiniSurvey from './MiniSurvey';
import SurveyInfo from '../../schemas/SurveyInfo';

export interface MiniSurveyListProps {
  surveyInfoList: SurveyInfo[];
}

export default function MiniSurveyList (props: MiniSurveyListProps) {
  return (
    <div className={classes.listBody}>
      {props.surveyInfoList.map((survey) => 
        <MiniSurvey surveyInfo={survey} key={survey.id}></MiniSurvey>
      )}
    </div>
  )
}