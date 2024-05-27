import classes from '../../../styles/Survey.module.css';
import Button from '@mui/material/Button';
import Link from '@mui/material/Link';
import FullSurveyInfo from '../../../schemas/FullSurveyInfo';
import { Question } from './Question';
import { SurveyAnswerInfo } from '../../../schemas/SurveyAnswerInfo';
import { useAnswer } from '../AnswerContext';
import { QuestionType } from '../../../schemas/QuestionInfo';
import { SurveyResultsInfo } from '../../../schemas/ResultsInfo';
import { useFetch } from '../../../hooks/useFetch';
import { GetResults } from '../../../http/APIs/ResultsAPI';


export interface ResultsFragmentProps {
  survey: FullSurveyInfo;
  answer?: SurveyAnswerInfo;
  results?: SurveyResultsInfo;
  answerExisted?: boolean;
  onViewAnswer?: () => void;
}

export default function ResultsFragment (props: ResultsFragmentProps) {
  const answer = useAnswer();

  function handleViewAnswer() {
    props.onViewAnswer?.();
  }

  function answerIsValid() {
    if (answer?.questionAnswers) {
      const wrong = answer?.questionAnswers.find((v, index) => {
        const question = props.survey.questions.find((q) => q.id === v.id);
        return (!v.options || v.options.length === 0 || (v.options?.includes(-1) && question?.questionType === QuestionType.DropDown))
          && !v.value && question?.required;
      });
      return wrong ? false : true;
    }
    return false;
  }

  function getQuestionResult(id: number) {
    if (!props.results)
      return undefined;

    return props.results.results.find((v) => v.id === id);
  }

  return (
    <>
      {props.survey.questions.map((val, index) => 
        <Question question={val} key={val.id} answer={answer?.questionAnswers[index]} result={getQuestionResult(val.id)}/>
      )}

      <div className={classes.resultsActionArea}>
        <div className={classes.downloadArea}>
          Загрузить ответы:
          <Link onClick={handleViewAnswer}>txt</Link>
          <Link onClick={handleViewAnswer}>csv</Link>
          <Link onClick={handleViewAnswer}>xlsx</Link>
        </div>
        <Link onClick={handleViewAnswer}>Вернуться к ответу</Link>
      </div>
    </>
  );
}
