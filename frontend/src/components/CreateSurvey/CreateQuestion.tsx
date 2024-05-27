import * as React from 'react';
import TextField from '@mui/material/TextField';
import Button from '@mui/material/Button';
import classes from '../../styles/CreateSurvey.module.css';
import MoreVertIcon from '@mui/icons-material/MoreVert';
import IconButton from '@mui/material/IconButton';
import { QuestionInfo, QuestionType } from '../../schemas/QuestionInfo';
import {CreateOptionList} from './CreateOptionList';
import Menu from '@mui/material/Menu';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import Select from '@mui/material/Select';
import Switch from '@mui/material/Switch';
import {SelectChangeEvent} from '@mui/material';
import { arrayMove } from 'react-movable';


interface CreateQuestionProps {
  question: QuestionInfo;
  canMoveUp: boolean;
  canMoveDown: boolean;
  listIndex: number;
  onQuestionChanged?: (question: Partial<QuestionInfo>) => void;
  onOptionTextChanged?: (questionId: number, optionId: number, text: string) => void;
  onOptionDeleted?: (questionId: number, optionId: number) => void;
  onQuestionMove?: (oldInd: number, newInd: number) => void;
  onQuestionDelete?: (id: number) => void;
}


export const CreateQuestion = React.memo(function CreateQuestion (
    { question, onQuestionChanged, onOptionTextChanged, onOptionDeleted, 
      onQuestionDelete, onQuestionMove, canMoveUp, canMoveDown, listIndex }: CreateQuestionProps) {
  const questionId = question.id;
  const options = question.options;
  const [anchorEl, setAnchorEl] = React.useState<null | HTMLElement>(null);
  const open = Boolean(anchorEl);
  const handleClick = (event: React.MouseEvent<HTMLButtonElement>) => {
    setAnchorEl(event.currentTarget);
  };
  const handleClose = () => {
    setAnchorEl(null);
  };

  function handleNameChanged(event: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) {
    onQuestionChanged?.(
      {...question, name: event.currentTarget.value}
    );
  }

  function handleDescriptionChanged(event: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) {
    onQuestionChanged?.(
      {...question, description: event.currentTarget.value}
    );
  }

  function handleTypeChange(event: SelectChangeEvent<QuestionType>, child: React.ReactNode) {
    onQuestionChanged?.(
      {...question, questionType: event.target.value as QuestionType}
    );
  };

  function handleRequiredChange(event: React.ChangeEvent<HTMLInputElement>, checked: boolean) {
    onQuestionChanged?.(
      {...question, required: checked}
    );
  }

  function handleShuffleOptionsChange(event: React.ChangeEvent<HTMLInputElement>, checked: boolean) {
    onQuestionChanged?.(
      {...question, shuffleOptions: checked}
    );
  }


  function handleOptionAdd() {
    if (question.options)
      onQuestionChanged?.(
        {...question, options: [...question.options, {id: Date.now(), name: 'Вариант ' + (question.options.length + 1)}]}
      )
    else
      onQuestionChanged?.(
        {...question, options: [{id: Date.now(), name: 'Вариант 1'}]}
      )
  }

  const handleOptionTextChanged = React.useCallback(function handleOptionTextChanged(id: number, text: string) {
    onOptionTextChanged?.(questionId, id, text);
  }, [questionId, onOptionTextChanged]);
  
  const handleOptionDelete = React.useCallback(function handleOptionDelete(id: number) {
    onOptionDeleted?.(questionId, id);
  }, [questionId, onOptionDeleted]);
  
  const handleOptionMoved = React.useCallback(function handleOptionMoved(oldInd: number, newInd: number) {
    onQuestionChanged?.(
      {id: questionId, options: arrayMove(options!, oldInd, newInd)}
    );
  }, [questionId, options, onQuestionChanged]);

  

  return (
    <div className={`panel ${classes.questionBody}`}>

      <div className={`${classes.questionSettings}`}>
        <FormControl variant="standard" sx={{ m: 0, minWidth: 120}}>
          <Select value={question.questionType} onChange={handleTypeChange}>
            <MenuItem value={0}>Единичный выбор</MenuItem>
            <MenuItem value={1}>Ед. выбор с прочим</MenuItem>
            <MenuItem value={2}>Множественный выбор</MenuItem>
            <MenuItem value={3}>Мн. выбор с прочим</MenuItem>
            <MenuItem value={4}>Выпадающий список</MenuItem>
            <MenuItem value={5}>Ввод строки</MenuItem>
            <MenuItem value={6}>Ввод вещ. числа</MenuItem>
            <MenuItem value={7}>Ввод цел. числа</MenuItem>
            <MenuItem value={8}>Ввод даты</MenuItem>
            <MenuItem value={9}>Ввод времени</MenuItem>
          </Select>
        </FormControl>
        <div className={classes.switchGroup}>
          <div className={classes.optionsLabel}>Обязательный: </div>
          <Switch checked={question.required} onChange={handleRequiredChange}/>
        </div>
        
        {question.questionType < 5 ? 
          <div className={classes.switchGroup}>
            <div className={classes.optionsLabel}>Перемешивать варианты: </div>
            <Switch checked={question.shuffleOptions} onChange={handleShuffleOptionsChange}/>
          </div>
        : ''}
      </div>

      <div className={classes.optionsMenu}>
        <IconButton color='primary' size='large' onClick={handleClick}><MoreVertIcon/></IconButton>
      </div>
      <Menu anchorEl={anchorEl} open={open} onClose={handleClose}>
        {question.questionType < 5 ? 
          <MenuItem onClick={handleOptionAdd}>Добавить вариант</MenuItem> 
        : ''}  
        <MenuItem onClick={() => { onQuestionMove?.(listIndex, listIndex - 1); handleClose()}} disabled={!canMoveUp}>Вверх</MenuItem>
        <MenuItem onClick={() => { onQuestionMove?.(listIndex, listIndex + 1); handleClose()}} disabled={!canMoveDown}>Вниз</MenuItem>
        <MenuItem onClick={() => onQuestionDelete?.(question.id)}>Удалить</MenuItem>
      </Menu>

      <div className={classes.questionName}>
        <TextField fullWidth multiline placeholder="Заголовок вопроса" size='medium' variant="standard" onKeyDown={
          (event) => {
            if (event.key === 'Enter')
              event.preventDefault();
          }} value={question.name} onChange={handleNameChanged}/>
      </div>

      {typeof question.description === 'string' ? 
        <div className={classes.questionDescription}>
          <TextField fullWidth multiline label="Описание" size='medium' margin='normal' variant="standard" InputLabelProps={{ shrink: true, }}
             value={question.description} onChange={handleDescriptionChanged}/>
        </div>
      : ''}

      {question.questionType < 5 ?
        <div>
          <CreateOptionList type={question.questionType} options={question.options!} 
            onOptionTextChange={handleOptionTextChanged} onOptionDelete={handleOptionDelete} onOptionMove={handleOptionMoved}/>

          <Button className={classes.addQuestion} fullWidth sx={{border: "2px dashed var(--text-color-secondary)"}} color='secondary' onClick={handleOptionAdd}>
            + Добавить вариант ответа
          </Button>
        </div>

      : ''}
      
    </div>
  );
}/*, (oldProps, newProps) => {
  console.log(Object.is(oldProps.onOptionTextChanged, newProps.onOptionTextChanged))
  return false;
}*/)
