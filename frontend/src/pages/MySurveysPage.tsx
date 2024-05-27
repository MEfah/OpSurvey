import { useEffect, useState } from "react";
import SurveyList from "../components/SurveyLists/SurveyList";
import SurveyInfo from "../schemas/SurveyInfo";
import { GetUsersSurveys } from "../http/APIs/SurveysAPI";
import { useAppSelector } from "../hooks/redux";

function MySurveysPage() {
  const userInfo = useAppSelector(state => state.user);
  const [surveys, setSurveys] = useState<Array<SurveyInfo>>([]);

  useEffect(() => {
    const getSurveys = async () => {
      const response = await GetUsersSurveys(userInfo.id);
      let surveys: SurveyInfo[] = response.data.surveys ?? [];
      surveys = surveys.map((v) => {return {...v, creationDate: new Date(v.creationDate)}})
      setSurveys(surveys);
    };
    getSurveys();
  }, [userInfo.id]);

  return (
    <SurveyList surveyInfoList={surveys}/>
  );
}

export default MySurveysPage;
