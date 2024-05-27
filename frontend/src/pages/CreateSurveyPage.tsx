import { useBeforeUnload, useBlocker, useLocation, useNavigation } from 'react-router-dom';
import { useAppDispatch } from '../hooks/redux';
import React, { useState, useRef, useEffect, useCallback } from 'react';
import classes from '../styles/CreateSurvey.module.css';
import TextField from '@mui/material/TextField';
import Button from '@mui/material/Button';
import InsertPhotoOutlinedIcon from '@mui/icons-material/InsertPhotoOutlined';
import {CreateQuestion} from '../components/CreateSurvey/CreateQuestion';
import MoreVertIcon from '@mui/icons-material/MoreVert';
import IconButton from '@mui/material/IconButton';
import { QuestionInfo, QuestionType } from '../schemas/QuestionInfo';
import { arrayMove } from 'react-movable';
import Menu from '@mui/material/Menu';
import MenuItem from '@mui/material/MenuItem';
import Link from '@mui/material/Link';
import Tooltip from '@mui/material/Tooltip';
import CloseIcon from '@mui/icons-material/Close';
import { CreateSurveyInfo } from '../schemas/FullSurveyInfo';
import { useAppSelector } from '../hooks/redux';
import { useFetch } from '../hooks/useFetch';
import { GetSurveys, PostSurvey, SaveUnfinishedSurvey, UpdateUnfinishedSurvey } from '../http/APIs/SurveysAPI';
import { useNavigate } from 'react-router-dom';
import { UnfinishedSurveyInfo } from '../schemas/UnfinishedSurvey';
import { createdSurveySlice } from '../store/reducers/CreatedSurveySlice';
import { MEDIA_URL } from '../http/api';
import dayjs from 'dayjs';
import { AccessResults, AccessResultsType, AccessSurvey, AccessSurveyType } from '../schemas/SurveyAccessInfo';
import SurveyAccessModal from '../modals/SurveyAccessModal';

// TODO: перенести все создание на контекст
// TODO: и использовать редюсер!!!

function getNewQuestion(): QuestionInfo {
  return {
    id: Date.now(),
    name: '',
    description: ' ',
    shuffleOptions: false,
    required: false,
    questionType: QuestionType.SingleSelect,
    options: [{
      id: 0,
      name: 'Вариант 1'
    },{
      id: 1,
      name: 'Вариант 2'
    }]
  }
}

export default function CreateSurveyPage () {
  const fileInputRef = useRef<HTMLInputElement>(null);
  const userInfo = useAppSelector(state => state.user);
  const survey = useAppSelector(state => state.survey);
  useEffect(() => {
    setName(survey.name);
    setDescription(survey.description);
    setImgSrc(survey.imgSrc ?? null);
    setImgLoaded(false);
    setQuestions(survey.questions ?? [getNewQuestion()])
  }, [survey])

  const navigate = useNavigate();
  const dispatch = useAppDispatch();

  const [name, setName] = useState(survey.name);
  const [description, setDescription] = useState(survey.description);
  const [imgSrc, setImgSrc] = useState<string | ArrayBuffer | null>(survey.imgSrc ?? null);
  const [questions, setQuestions] = useState(survey.questions ?? [getNewQuestion()]);
  const accessSurvey = useRef<AccessSurvey>({accessTypeSurvey: AccessSurveyType.ALL});
  const accessResults = useRef<AccessResults>({accessTypeResults: AccessResultsType.ALL});

  const [imgLoaded, setImgLoaded] = useState(false);
  const [editingAccess, setEditingAccess] = useState(false);

  const [anchorEl, setAnchorEl] = React.useState<null | HTMLElement>(null);
  const open = Boolean(anchorEl);
  const handleClick = (event: React.MouseEvent<HTMLButtonElement>) => {
    setAnchorEl(event.currentTarget);
  };
  const closeSurveyMenu = () => {
    setAnchorEl(null);
  };


  const surveyInfo = useRef<UnfinishedSurveyInfo>({id: survey.id, name, description, imgSrc: survey.imgSrc, questions, shuffleQuestions: survey.shuffleQuestions});
  useEffect(() => {
    surveyInfo.current.questions = questions;
  }, [questions]);
  useEffect(() => {
    surveyInfo.current.name = name;
  }, [name]);
  useEffect(() => {
    surveyInfo.current.description = description
  }, [description]);
  useEffect(() => {
    if (!imgLoaded)
      surveyInfo.current.imgSrc = imgSrc ? imgSrc as string : undefined
  }, [imgSrc, imgLoaded])


  const [createSurvey, creatingSurvey] = useFetch(async () => {
    const formData = new FormData();
    formData.append('create_survey', JSON.stringify(getSurveyInfo()));
    if (fileInputRef.current?.files?.[0])
      formData.append('file', fileInputRef.current.files[0]);
    return await PostSurvey(formData);
  });

  const [saveSurvey, savingSurvey] = useFetch(async () => {
    const formData = new FormData();
    formData.append('unfinished_create', JSON.stringify(getUnfinishedSurveyInfo()));
    if (fileInputRef.current?.files?.[0])
      formData.append('file', fileInputRef.current.files[0]);
    if (survey.id) {
      return UpdateUnfinishedSurvey(survey.id, formData);
    } else {
      return SaveUnfinishedSurvey(formData);
    }
  });


  // Блокировать переход на другую страницу
  let blocker = useBlocker(
    ({ currentLocation, nextLocation }) =>
      currentLocation.pathname !== nextLocation.pathname
  );

  // Когда переход на страницу заблокирован
  // Автоматически продолжить переход, но при этом сохранить данные
  // TODO найти способ сохранения без костылей
  useEffect(() => {
    blocker.proceed?.();
    dispatch(createdSurveySlice.actions.setSurvey(surveyInfo.current));
  }, [blocker, dispatch])

  // Также сохранить когда страница закрывается
  useEffect(() => {
    window.addEventListener("beforeunload", handleUnload);
    return () => {
      window.removeEventListener("beforeunload", handleUnload);
    };

    function handleUnload () {
      dispatch(createdSurveySlice.actions.setSurvey(surveyInfo.current));
    };
  }, [dispatch]);


  function handleNameChanged(event: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) {
    setName(event.currentTarget.value);
  }

  function handleDescriptionChanged(event: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) {
    setDescription(event.currentTarget.value);
  }

  function handleImageUpload(event: React.ChangeEvent<HTMLInputElement>) {
    if (event.currentTarget.files && event.currentTarget.files[0]) {
      const reader = new FileReader();
      reader.onload = (e) => {
        if (e.target?.result) 
          setImgSrc(reader.result);
      }
      reader.readAsDataURL(event.currentTarget.files[0]);
      setImgLoaded(true);
    }
  }

  function handleImageDelete() {
    setImgSrc('');
  }

  const handleAddQuestion = useCallback(function handleAddQuestion() {
    setQuestions(questions => [...questions, getNewQuestion()])
  }, []);

  const handleQuestionChanged = useCallback(function handleQuestionChanged(question: Partial<QuestionInfo>) {
    setQuestions(questions => [...questions.map(item => {
      if (item.id === question.id) {
        return {...item, ...question};
      }
      return item;
    })])
  }, []);

  const handleOptionTextchanged = useCallback(function handleOptionTextchanged(questionId: number, optionId: number, text: string) {
    setQuestions(questions => [...questions.map(item => {
      if (item.id === questionId) {
        return {...item, ...{
          options: item.options ? [...item.options.map((val) => {
            if (val.id === optionId)
              return {...val, name: text}
            return val
          })] : undefined
        }};
      }
      return item;
    })])
  }, [])

  const handleOptionDeleted = useCallback(function handleOptionTextchanged(questionId: number, optionId: number) {
    setQuestions(questions => [...questions.map(item => {
      if (item.id === questionId) {
        return {...item, ...{
          options: item.options ? [...item.options.filter((v) => {return v.id !== optionId})] : undefined
        }};
      }
      return item;
    })])
  }, []);

  const handleQuestionDeleted = useCallback(function handleQuestionDeleted(id: number) {
    setQuestions(questions => [...questions.filter((v) => v.id !== id)])
  }, []);

  const handleQuestionMove = useCallback(function handleQuestionMove(oldInd: number, newInd: number ) {
    setQuestions(questions => [...arrayMove(questions, oldInd, newInd)]);
  }, []);

  function canCreateSurvey() {
    return name.length >= 5 && questions.length > 0 && !questions.find((question) => {
      return question.name.length < 5 || (question.questionType < 5 && (!question.options || question.options.length < 2));
    });
  }

  function getProperQuestions() {
    console.log(questions);
    return questions.map((v, index) => {
      const val = v.questionType < 5 ? {...v} : {...v, options: undefined, shuffleOptions: undefined};

      try {
        val.description = val.description && val.description.trim() !== '' ? val.description : undefined;
      } catch (e) {
        console.log(e);
      }

      val.id = index;
      val.options = val.options?.map((opt, optInd) => {return {...opt, id: optInd}});

      return val;
    });
  }

  function getSurveyInfo() {
    const q = getProperQuestions();

    const survey: CreateSurveyInfo = {
      name,
      description: description && description.trim() !== '' ? description : undefined,
      imgSrc: '',
      creatorId: userInfo.id,
      creatorName: userInfo.name,
      creatorImgSrc: userInfo.imgSrc,
      shuffleQuestions: false,
      accessSurvey: accessSurvey.current,
      accessResults: accessResults.current,
      accessApi: {accessTypeApi: 0},
      questions: q
    };
    return survey;
  }

  function getUnfinishedSurveyInfo() {
    const q = getProperQuestions();

    const survey: UnfinishedSurveyInfo = {
      name,
      description: description && description.trim() !== '' ? description : undefined,
      imgSrc: '',
      shuffleQuestions: false,
      questions: q
    };
    return survey;
  }

  async function handleCreate() {
    const [response, error] = await createSurvey();

    if (error) {
      console.log(response);
    } else {
      dispatch(createdSurveySlice.actions.clearSurvey());
      navigate('/');
    }
  }

  async function handleSave() {
    const [response, error] = await saveSurvey();

    if (error) {
      console.log(response);
    } else {
      dispatch(createdSurveySlice.actions.clearSurvey());
      navigate('/');
    }
  }

  function handleClear() {
    console.log('clear');
    dispatch(createdSurveySlice.actions.clearSurvey());
  }

  return (
    <div className={`panel ${classes.surveyBody}`}>
      <SurveyAccessModal open={editingAccess} onAccept={() => setEditingAccess(false)} onClose={() => setEditingAccess(false)}
        accessResults={accessResults} accessSurvey={accessSurvey}/>
      <div className={classes.optionsMenu}>
        <IconButton color='primary' size='large' onClick={handleClick}><MoreVertIcon/></IconButton>
      </div>
      <Menu anchorEl={anchorEl} open={open} onClose={closeSurveyMenu}>
        <MenuItem onClick={() => {setEditingAccess(true); closeSurveyMenu();}}>Настроить доступ</MenuItem>
        <MenuItem>Перемешивать вопросы</MenuItem>
        <MenuItem onClick={handleSave}>Сохранить опрос</MenuItem> 
        <MenuItem onClick={() => navigate('/surveys/unfinished')}>Загрузить опрос</MenuItem>
        <MenuItem onClick={() => handleAddQuestion()}>Добавить вопрос</MenuItem>
        <MenuItem onClick={handleClear}>Очистить</MenuItem>
        <MenuItem onClick={closeSurveyMenu}>Выйти</MenuItem>
      </Menu>
      
      <div className={classes.name}>
        <TextField fullWidth multiline placeholder="Название опроса" size='medium' variant="standard" onKeyDown={
          (event) => {
            if (event.key === 'Enter')
              event.preventDefault();
          }} value={name} onChange={handleNameChanged}/>
      </div>

      {!imgSrc ? 
        <Button fullWidth sx={{border: "2px dashed var(--text-color-secondary)"}} color='secondary' onClick={() => fileInputRef.current?.click()}>
          <InsertPhotoOutlinedIcon/><span style={{marginLeft: "2px"}}> + Добавить изображение</span>
        </Button>
      : ''}
      
      <input
        ref={fileInputRef}
        type="file"
        accept="image/*"
        style={{ display: 'none' }}
        onChange={handleImageUpload}
      />

      { imgSrc ?
        <div style={{position: 'relative'}}>
          <Tooltip title='Изменить изображение'>
            <img className={classes.uploadedImage} src={imgSrc ? (!imgLoaded ? MEDIA_URL + imgSrc as string : imgSrc as string) : ''} alt="Uploaded" 
              onClick={() => fileInputRef.current?.click()}/> 
          </Tooltip>
          <IconButton style={{position: 'absolute', right: 5, top: 5, background: "#fff", padding: 5}} onClick={handleImageDelete}>
            <CloseIcon/>
          </IconButton>
        </div>
      : '' }

      <div className={classes.description}>
        <TextField fullWidth multiline label="Описание" size='medium' margin='normal' variant="standard" InputLabelProps={{ shrink: true, }}
          value={description} onChange={handleDescriptionChanged}/>
      </div>
      
      {questions.map((val, index) => 
        <CreateQuestion question={val} key={val.id} onQuestionChanged={handleQuestionChanged} onOptionTextChanged={handleOptionTextchanged} onQuestionDelete={handleQuestionDeleted}
          onOptionDeleted={handleOptionDeleted} canMoveUp={index > 0} canMoveDown={index < questions.length - 1} onQuestionMove={handleQuestionMove} listIndex={index}/>
      )}

      <Button fullWidth sx={{border: "2px dashed var(--text-color-secondary)"}} color='secondary' onClick={handleAddQuestion}>
        + Добавить вопрос
      </Button>

      <div className={classes.actionArea}>
        <Link onClick={handleSave}>Сохранить и выйти</Link>
        <Button size='large' variant='contained' disabled={!canCreateSurvey()} onClick={handleCreate}>Создать опрос</Button>
      </div>
    </div>
  );
}
