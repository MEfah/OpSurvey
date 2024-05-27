import React, { useEffect, useState } from 'react';
import HidePanel from '../UI/HidePanel/HidePanel';
import MiniSurveyList from '../SurveyLists/MiniSurveyList';
import { GetSurveys } from '../../http/APIs/SurveysAPI';
import { SortParameterType } from '../../schemas/SurveySearchParams';
import SurveyInfo from '../../schemas/SurveyInfo';

function LatestSurveys() {

  const [surveys, setSurveys] = useState<Array<SurveyInfo>>([]);

  useEffect(() => {
    const getSurveys = async () => {
      const response = await GetSurveys({limit: 5}, {sortAscending: false, sortType: SortParameterType.CREATION_DATE});
      let surveys: SurveyInfo[] = response.data.surveys ?? [];
      surveys = surveys.map((v) => {return {...v, creationDate: new Date(v.creationDate)}})
      setSurveys(surveys);
    };
    getSurveys();
  }, []);

  return(
    <HidePanel header={"Недавнее"} hidden={false}>
      <MiniSurveyList surveyInfoList={surveys}/>
    </HidePanel>
  )
}

export default LatestSurveys;