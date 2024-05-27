import { useEffect, useState } from "react";
import SurveyList from "../components/SurveyLists/SurveyList";
import SurveyInfo from "../schemas/SurveyInfo";
import { GetSurveys, GetUnfinishedSurveys } from "../http/APIs/SurveysAPI";
import UnfinishedList from "../components/SurveyLists/UnfinishedList";
import { UnfinishedSurveyItemInfo } from "../schemas/UnfinishedSurvey";
import { useAppSelector } from "../hooks/redux";
import dayjs from "dayjs";

function UnfinishedSurveysPage() {
  const userInfo = useAppSelector(state => state.user);
  const [surveys, setSurveys] = useState<Array<UnfinishedSurveyItemInfo>>([]);

  useEffect(() => {
    const getSurveys = async () => {
      const response = await GetUnfinishedSurveys(userInfo.id);
      let surveys: UnfinishedSurveyItemInfo[] = response.data?.surveys ?? [];
      surveys = surveys.map((v) => {return {...v, updatedDate: dayjs(v.updatedDate)}})
      setSurveys(surveys);
    };
    getSurveys();
  }, []);

  return (
    <UnfinishedList surveyInfoList={surveys}/>
  );
}

export default UnfinishedSurveysPage;
