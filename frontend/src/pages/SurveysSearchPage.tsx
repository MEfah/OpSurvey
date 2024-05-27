import { useEffect, useState } from "react";
import SurveyList from "../components/SurveyLists/SurveyList";
import PopularSurveys from "../components/SidePanels/PopularSurveys";
import FilterPanel from "../components/Search/FilterPanel";
import SearchPanel from "../components/Search/SearchPanel";
import HidePanel from "../components/UI/HidePanel/HidePanel";
import SurveyInfo from "../schemas/SurveyInfo";
import { GetSurveys } from "../http/APIs/SurveysAPI";
import { FilterParam, FilterParameterType, SortParameterType, SurveySearchBody } from '../schemas/SurveySearchParams';
import { FilterInfo } from '../schemas/FilterInfo';
import LatestSurveys from "../components/SidePanels/LatestSurveys";


export function SurveysSearchPage() {

  const [surveys, setSurveys] = useState<Array<SurveyInfo>>([]);
  const [filterInfo, setFilterInfo] = useState<Partial<Record<FilterParameterType, FilterInfo>>>({});

  useEffect(() => {
    const getSurveys = async () => {
      const response = await GetSurveys(undefined);
      let surveys: SurveyInfo[] = response.data?.surveys ?? [];
      surveys = surveys.map((v) => {return {...v, creationDate: new Date(v.creationDate)}});
      setSurveys(surveys);
    };
    getSurveys();
  }, []);

  function handleFilterInfoChanged(filterParameterType: FilterParameterType, newInfo: FilterInfo) {
    setFilterInfo({...filterInfo, [filterParameterType]: newInfo})
  }

  async function handleSearch(text?: string, sortType?: SortParameterType, sortAscending?: boolean) {
    let filterParams: FilterParam[] | undefined = [];
    for (const ft in filterInfo) {
      const enumKey = parseInt(ft) as FilterParameterType;
      if (enumKey !== FilterParameterType.RESULTS_ACCESSIBLE){
        if (filterInfo[enumKey]?.useFilter)
          filterParams.push({
            parameterType: enumKey,
            value: {
              from: filterInfo[enumKey]?.range?.from,
              to: filterInfo[enumKey]?.range?.to
            }
          })
      }
    }

    if(filterParams.length === 0)
      filterParams = undefined;

    const response = await GetSurveys(undefined, {
      searchText: text,
      sortType: sortType,
      sortAscending: sortAscending,
      filterParams: filterParams
    });
    let surveys: SurveyInfo[] = response.data?.surveys ?? [];
    surveys = surveys.map((v) => {return {...v, creationDate: new Date(v.creationDate)}});
    setSurveys(surveys);
  }

  return (
    <div className="body-columns">
      <div className="body-column-left">
        <SearchPanel onSearch={handleSearch}/>
        <SurveyList surveyInfoList={surveys}/>
      </div>
      <div className="body-column-right">
        <HidePanel header={"Фильтры"} hidden={true}>
          <FilterPanel filterParams={filterInfo} onChange={handleFilterInfoChanged}/>
        </HidePanel>
        <PopularSurveys/>
        <LatestSurveys/>
      </div>
    </div>
  );
}
