import React, { useEffect, useReducer, useRef, useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { useFetch } from '../hooks/useFetch';
import { DeleteSurvey, GetSurvey, GetSurveyAccess, UpdateSurveyAccess } from '../http/APIs/SurveysAPI';
import FullSurveyInfo from '../schemas/FullSurveyInfo';
import CircularProgress from '@mui/material/CircularProgress';
import { SurveyAnswerProvider } from '../components/Survey/AnswerContext';
import { QuestionAnswerInfo, SurveyAnswerInfo, CreateAnswerInfo } from '../schemas/SurveyAnswerInfo';
import { QuestionType } from '../schemas/QuestionInfo';
import { DeleteAnswer, GetAnswer, GetResults, GetUsersAnswer, PostAnswer, UpdateAnswer } from '../http/APIs/ResultsAPI';
import { useAppSelector } from '../hooks/redux';
import { answerReducer } from '../reducers/AnswerReduces';
import dayjs from 'dayjs';
import { AxiosResponse } from 'axios';
import AnswerFragment from '../components/Survey/Answers/AnswerFragment';
import SurveyInfo from '../components/Survey/SurveyInfo';
import classes from '../styles/Survey.module.css';
import ResultsFragment from '../components/Survey/Results/ResultsFragment';
import { DateTimeResultsInfo, SurveyResultsInfo } from '../schemas/ResultsInfo';
import Menu from '@mui/material/Menu';
import MenuItem from '@mui/material/MenuItem';
import MoreVertIcon from '@mui/icons-material/MoreVert';
import IconButton from '@mui/material/IconButton';
import SurveyAccessModal from '../modals/SurveyAccessModal';
import { AccessResults, AccessResultsType, AccessSurvey, AccessSurveyType } from '../schemas/SurveyAccessInfo';


function getAnswerFromResponse(response: AxiosResponse<any, any>, survey: FullSurveyInfo): SurveyAnswerInfo | undefined {
  try {
    let answer = response.data as SurveyAnswerInfo;

    answer.questionAnswers = answer.questionAnswers.map((v, i) => {
      const question = survey.questions.find((q) => q.id === v.id);
      if (question && [QuestionType.InputDate, QuestionType.InputTime].includes(question.questionType))
        return {...v, value: dayjs(v.value)}
      else return v
    });
  
    return answer
  } catch {
    return undefined
  }
}

export default function SurveyPageWithContext() {
  const params = useParams();
  const user = useAppSelector(state => state.user);
  const [surveyInfo, setSurveyInfo] = useState<FullSurveyInfo | undefined>();
  const [answer, dispatch] = useReducer(answerReducer, {surveyId: params.surveyId ?? '', isFinished: false, userId: '', questionAnswers: []});
  const [results, setResults] = useState<SurveyResultsInfo | undefined>();
  const [answerExisted, setAnswerExisted] = useState(false);
  const [viewResults, setViewResults] = useState(false);
  const [update, setUpdate] = useState(false);
  const initial = useRef<SurveyAnswerInfo | undefined>();

  const [editingAccess, setEditingAccess] = useState(false);
  const accessSurvey = useRef<AccessSurvey>({accessTypeSurvey: AccessSurveyType.ALL});
  const accessResults = useRef<AccessResults>({accessTypeResults: AccessResultsType.ALL});

  const navigate = useNavigate();

  const [anchorEl, setAnchorEl] = React.useState<null | HTMLElement>(null);
  const open = Boolean(anchorEl);
  const handleOpenMenu = (event: React.MouseEvent<HTMLButtonElement>) => {
    setAnchorEl(event.currentTarget);
  };
  const handleCloseMenu = () => {
    setAnchorEl(null);
  };

  const [getSurvey, isGettingSurvey] = useFetch(async () => {
    return await GetSurvey(params.surveyId ?? '');
  });
  const [getAnswer, isGettingAnswer] = useFetch(async () => {
    return await GetUsersAnswer(params.surveyId ?? '');
  });
  const [commitAnswer] = useFetch<SurveyAnswerInfo>(async (answer) => {
    return await PostAnswer(answer?.surveyId ?? '', answer as CreateAnswerInfo);
  });
  const [updateAnswer] = useFetch<SurveyAnswerInfo>(async (answer) => {
    return await UpdateAnswer(answer?.surveyId ?? '', answer?.userId ?? '', answer as CreateAnswerInfo);
  });
  const [deleteAnswer] = useFetch<SurveyAnswerInfo>(async () => {
    return await DeleteAnswer(answer?.surveyId ?? '', answer?.userId ?? '');
  });
  const [getResults] = useFetch(async () => {
    return await GetResults(params.surveyId ?? '');
  });
  const [getAccess] = useFetch(async () => {
    return await GetSurveyAccess(params.surveyId ?? '');
  })
  const [updateAccess] = useFetch(async () => {
    return await UpdateSurveyAccess(params.surveyId ?? '', accessSurvey.current, accessResults.current);
  });
  const [deleteSurvey] = useFetch(async () => {
    return await DeleteSurvey(params.surveyId ?? '');
  });


  async function getCurrentAnswer() {
    const [responseSurvey, errorSurvey] = await getSurvey();
    const [responseAnswer, errorAnswer] = await getAnswer();

    if (errorSurvey || !responseSurvey?.data) {
      
    } else {
      const survey = responseSurvey.data as FullSurveyInfo;
      let newAnswer = (errorAnswer || !responseAnswer?.data) ? undefined : getAnswerFromResponse(responseAnswer, survey);
      survey.creationDate = new Date(survey.creationDate);
      setSurveyInfo(survey);

      if (!newAnswer) {
        const answers: QuestionAnswerInfo[] = [];
        survey.questions.forEach((v) => answers.push({id: v.id, value: undefined}));
        newAnswer = {surveyId: params.surveyId ?? '', isFinished: false, userId: user.id ?? '', questionAnswers: answers}
      } else {
        setAnswerExisted(true);
      }

      initial.current = newAnswer;
      dispatch({type: 'changed', answer: newAnswer});

      if (survey.creatorId === user.id) {
        const [responseAccess, errorAccess] = await getAccess();

        if (errorAccess) {

        } else {
          accessSurvey.current = responseAccess?.data.accessSurvey;
          accessResults.current = responseAccess?.data.accessResults;
          setUpdate(update => !update);
        }
      }
    }
  }

  useEffect(() => {
    // TODO сделать красивее
    getCurrentAnswer()
  }, [params.surveyId, user.id]);

  async function sendAnswer(newAnswer: SurveyAnswerInfo) {
    let response, error
    if (answerExisted)
      [response, error] = await updateAnswer(newAnswer);
    else
      [response, error] = await commitAnswer(newAnswer);

    if (error) {
      // TODO: обработать ошибку
    } else {
      if (response?.data && surveyInfo) {
        const returnedAnswer = getAnswerFromResponse(response.data, surveyInfo);
        if (returnedAnswer)
          dispatch({type: 'changed', answer: returnedAnswer});
      }
    }
  }


  async function handleCommitAnswer(newAnswer: SurveyAnswerInfo | null) {
    if (!newAnswer)
      return

    newAnswer.isFinished = true;
    await sendAnswer(newAnswer);
  }

  async function handleSaveAnswer(newAnswer: SurveyAnswerInfo | null) {
    if (!newAnswer)
      return

    newAnswer.isFinished = false;
    await sendAnswer(newAnswer);
  }

  async function handleDeleteAnswer() {
    const [response, error] = await deleteAnswer();

    if (error) {

    } else {
      await getCurrentAnswer();
    }
  }

  async function handleCancelAnswer() {
    if (initial.current)
      dispatch({type: 'changed', answer: initial.current});
  }

  async function handleViewResults() {
    if (results) {
      setViewResults(true);
      window.scrollTo(0,0);
      return;
    }

    const [response, error] = await getResults();
    if (error) {
      // TODO обработать ошибку
    } else {
      let results = undefined;
      if (response?.data) {
        results = response.data as SurveyResultsInfo;
        results.results = results.results.map((v) => {
          const type = surveyInfo?.questions[v.id].questionType;
          if ((type === QuestionType.InputDate || type === QuestionType.InputTime) && v.result) {
            const res = v.result as DateTimeResultsInfo;
            res.max = dayjs(res.max);
            res.min = dayjs(res.min);
            res.mean = dayjs(res.mean);
            res.intervals = res.intervals.map((v) => { return {...v, from: dayjs(v.from)}})
            return v;
          }
          return v
        });

        setResults(results);
        setViewResults(true);
        window.scrollTo(0,0);
      }
    }
  }

  function handleEditAnswer() {
    dispatch({type:'changed', answer:{
      ...answer, isFinished: false
    }})
  }

  function handleViewAnswer() {
    setViewResults(false);
    window.scrollTo(0,0);
  }

  async function handleUpdateAccess() {
    const [response, error] = await updateAccess();

    if (error) {
      // TODO: Обработать ошибку
    } else {
      setEditingAccess(false);
    }
  }

  async function handleDelete() {
    const [response, error] = await deleteSurvey();

    if (error) {
      // TODO: Обработать ошибку
    } else {
      navigate('/surveys/my');
    }
  }

  return (
    isGettingSurvey || isGettingAnswer ? 
      <CircularProgress/> 
    : surveyInfo ? 
      <SurveyAnswerProvider answer={answer} dispatch={dispatch}>
        <div className={`panel ${classes.surveyBody}`}>
          {
            user.id === surveyInfo.creatorId ? 
            <>
              <SurveyAccessModal open={editingAccess} onAccept={handleUpdateAccess} onClose={() => setEditingAccess(false)}
                accessResults={accessResults} accessSurvey={accessSurvey} update={update}/>
              <div className={classes.optionsMenu}>
                <IconButton color='primary' size='large' onClick={handleOpenMenu}><MoreVertIcon/></IconButton>
              </div>
              <Menu anchorEl={anchorEl} open={open} onClose={handleCloseMenu}>
                <MenuItem onClick={() => {setEditingAccess(true); handleCloseMenu()}}>Настроить доступ</MenuItem>
                <MenuItem onClick={() => {handleDelete(); handleCloseMenu()}}>Удалить</MenuItem>
              </Menu>
            </>
          : ''
          }

          <SurveyInfo survey={surveyInfo}/>
          {
            viewResults ? 
            <ResultsFragment survey={surveyInfo} results={results} onViewAnswer={handleViewAnswer}/>
          :
            <AnswerFragment survey={surveyInfo} onCommitAnswer={handleCommitAnswer} onSaveAnswer={handleSaveAnswer} onViewResults={handleViewResults}
            onEditAnswer={handleEditAnswer} answerExisted={answerExisted} onDeleteAnswer={handleDeleteAnswer} onCancelAnswer={handleCancelAnswer}/> 
          }
        </div>

      </SurveyAnswerProvider>
    :
      <></>)
}