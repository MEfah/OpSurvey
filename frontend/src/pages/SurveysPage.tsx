import { useEffect, useState } from "react";
import SurveyList from "../components/SurveyLists/SurveyList";
import SurveyInfo from "../schemas/SurveyInfo";
import { GetSurveys } from "../http/APIs/SurveysAPI";

function SurveysPage() {

  const [surveys, setSurveys] = useState<Array<SurveyInfo>>([]);

  useEffect(() => {
    const getSurveys = async () => {
      const response = await GetSurveys();
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

export default SurveysPage;
