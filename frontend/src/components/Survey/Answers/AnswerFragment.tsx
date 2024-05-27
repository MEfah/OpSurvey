import classes from '../../../styles/Survey.module.css';
import Button from '@mui/material/Button';
import Link from '@mui/material/Link';
import FullSurveyInfo from '../../../schemas/FullSurveyInfo';
import { Question } from './Question';
import { SurveyAnswerInfo } from '../../../schemas/SurveyAnswerInfo';
import { useAnswer } from '../AnswerContext';
import { QuestionType } from '../../../schemas/QuestionInfo';


interface AnswerFragmentProps {
  survey: FullSurveyInfo;
  answer?: SurveyAnswerInfo;
  answerExisted?: boolean;
  onCommitAnswer?: (answer: SurveyAnswerInfo | null) => void;
  onSaveAnswer?: (answer: SurveyAnswerInfo | null) => void;
  onViewResults?: () => void;
  onEditAnswer?: () => void;
  onDeleteAnswer?: () => void;
  onCancelAnswer?: () => void;
}


export default function AnswerFragment (props: AnswerFragmentProps) {
  const answer = useAnswer();

  function handleCommitAnswer() {
    props.onCommitAnswer?.(answer);
  }

  function handleSaveAnswer() {
    props.onSaveAnswer?.(answer);
  }

  function handleViewResults() {
    props.onViewResults?.();
  }

  function handleEditAnswer() {
    props.onEditAnswer?.();
  }

  function handleDeleteAnswer() {
    props.onDeleteAnswer?.();
  }

  function handleCancelAnswer() {
    props.onCancelAnswer?.();
  }

  function answerIsValid() {
    if (answer?.questionAnswers) {
      const wrong = answer?.questionAnswers.find((v, index) => {
        const question = props.survey.questions.find((q) => q.id === v.id);
        console.log(v.options?.includes(-1) && question?.questionType === QuestionType.DropDown);
        return (!v.options || v.options.length === 0 || (v.options?.includes(-1) && question?.questionType === QuestionType.DropDown))
          && !v.value && question?.required;
      });
      return wrong ? false : true;
    }
    return false;
  }

  return (
    <>
      {props.survey.questions.map((val, index) => 
        <Question question={val} key={val.id} answer={answer?.questionAnswers[index]} canAnswer={!answer?.isFinished}/>
      )}

      {
        !answer?.isFinished ?
          <div className={classes.actionArea}>
            <Link onClick={handleViewResults}>Просмотреть результаты</Link>

            <div>
              { props.answerExisted?
                <Link onClick={handleCancelAnswer}>Отменить</Link>
              :
                <Link onClick={handleSaveAnswer}>Сохранить ответ</Link>
              }

              <Button size='large' variant='contained' onClick={handleCommitAnswer} disabled={!answerIsValid()}>Отправить ответ</Button>
            </div>

          </div>
        :
          <div className={classes.actionArea}>
            <Link onClick={handleViewResults}>Просмотреть результаты</Link>
            <div>
              <Link onClick={handleDeleteAnswer}>Удалить ответ</Link>
              <Button size='large' variant='contained' onClick={handleEditAnswer}>Изменить ответ</Button>
            </div>

          </div>
      }
    </>
  );
}
