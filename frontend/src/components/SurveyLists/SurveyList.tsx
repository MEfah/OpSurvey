import React from 'react';
import SurveyItem from './SurveyItem';
import SurveyInfo from '../../schemas/SurveyInfo';

interface SurveyListProps {
  surveyInfoList: SurveyInfo[]
}

export default function SurveyList (props: SurveyListProps) {
  return (
    <div className='survey-list-body'>
      {props.surveyInfoList.map((survey) => 
        <SurveyItem {...survey} key={survey.id}></SurveyItem>
      )}
    </div>
  );
}