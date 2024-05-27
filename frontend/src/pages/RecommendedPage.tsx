import { useEffect, useState } from "react";
import SurveyList from "../components/SurveyLists/SurveyList";
import SurveyInfo from "../schemas/SurveyInfo";
import { GetSurveys } from "../http/APIs/SurveysAPI";
import { getRecommendations } from "../http/APIs/RecommendationsAPI";

function RecommendedPage() {

  const [surveys, setSurveys] = useState<Array<SurveyInfo>>([]);

  useEffect(() => {
    const getSurveys = async () => {
      const response = await getRecommendations(20, 0);
      let surveys: SurveyInfo[] = response.data?.surveys ?? [];
      surveys = surveys.map((v) => {return {...v, creationDate: new Date(v.creationDate)}})
      setSurveys(surveys);
    };
    getSurveys();
  }, []);

  return (
    <SurveyList surveyInfoList={surveys}/>
  );
}

export default RecommendedPage;
