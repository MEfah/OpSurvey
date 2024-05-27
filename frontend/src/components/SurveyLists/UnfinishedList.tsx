import React from 'react';
import SurveyItem from './SurveyItem';
import SurveyInfo from '../../schemas/SurveyInfo';
import UnfinishedItem from './UnfinishedItem';
import { UnfinishedSurveyInfo, UnfinishedSurveyItemInfo } from '../../schemas/UnfinishedSurvey';

interface SurveyListProps {
  surveyInfoList: UnfinishedSurveyItemInfo[]
}

export default function UnfinishedList (props: SurveyListProps) {
  return (
    <div className='survey-list-body'>
      {props.surveyInfoList.map((survey) => 
        <UnfinishedItem survey={survey} key={survey.id}></UnfinishedItem>
      )}
    </div>
  );
}