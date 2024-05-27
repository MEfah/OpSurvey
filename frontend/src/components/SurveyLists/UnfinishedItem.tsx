import React from 'react';
import classes from '../../styles/SurveyItem.module.css';
import { MEDIA_URL } from '../../http/api';
import { useNavigate } from 'react-router-dom';
import { useAppDispatch, useAppSelector } from '../../hooks/redux';
import { createdSurveySlice } from '../../store/reducers/CreatedSurveySlice';
import { useFetch } from '../../hooks/useFetch';
import { GetUnfinishedSurvey } from '../../http/APIs/SurveysAPI';
import { UnfinishedSurveyItemInfo } from '../../schemas/UnfinishedSurvey';

export interface SurveyItemProps {
  survey: UnfinishedSurveyItemInfo;
}

export default function UnfinishedItem ({survey}: SurveyItemProps) {
  const userInfo = useAppSelector(state => state.user);
  const navigate = useNavigate();
  const dispatch = useAppDispatch();
  const [getSurvey, isGettingSurvey] = useFetch(async () => {
    return await GetUnfinishedSurvey(survey.id);
  });

  async function handleLoadUnfinished() {
    const [response, error] = await getSurvey();
    
    if (error) {

    } else if (response) {
      navigate(`/surveys/create`);
      console.log(response.data);
      dispatch(createdSurveySlice.actions.setSurvey(response.data))
    }
  }

  return (
    <div className={classes.body + ' panel'} onClick={handleLoadUnfinished}>
      <div>
        <div className={classes.creator}>{userInfo.name}</div>
        <div className={classes.date}>{survey.updatedDate.format('DD.MM.YYYY HH:mm')}</div>
      </div>
      
      <div className={classes.name}>{survey.name}</div>
      {survey.imgSrc ? 
        <img className={classes.img} src={survey.imgSrc ? MEDIA_URL + survey.imgSrc : ''} alt=''></img>
      : 
        ''}

      {survey.description ? 
        <div className={classes.desc +( survey.description && survey.description.length > 500 ? ' fading-text' : '')}>
          {survey.description}
        </div>
      : 
        ''}
      
    </div>
  );
}