import React, { memo } from 'react';
import { QuestionOptionInfo, QuestionType } from '../../schemas/QuestionInfo';
import TextField from '@mui/material/TextField';
import RadioButtonUncheckedIcon from '@mui/icons-material/RadioButtonUnchecked';
import CheckBoxOutlineBlankIcon from '@mui/icons-material/CheckBoxOutlineBlank';
import IconButton from '@mui/material/IconButton';
import DeleteIcon from '@mui/icons-material/Delete';
import classes from '../../styles/CreateSurvey.module.css';
import { List, RenderItemParams, RenderListParams } from 'react-movable';
import { CreateOption } from './CreateOption';

export interface CreateOptionListProps {
  type: QuestionType;
  options: QuestionOptionInfo[];
  onOptionDelete?: (id: number) => void;
  onOptionMove?: (oldInd: number, newInd: number) => void;
  onOptionTextChange?: (id: number, text: string) => void;
}

export const CreateOptionList = memo(function CreateOptionList (props: CreateOptionListProps) {

  function handleOptionMove(oldInd: number, newInd: number) {
    props.onOptionMove?.(oldInd, newInd);
  }

  function getOptionIcon() {
    if ([QuestionType.SingleSelect, QuestionType.SingleSelectOther].includes(props.type))
      return (<RadioButtonUncheckedIcon color='secondary' sx={{marginLeft: "5px", marginRight: "15px"}}/>)
    else if ([QuestionType.MultiSelect, QuestionType.MultiSelectOther].includes(props.type))
      return (<CheckBoxOutlineBlankIcon color='secondary' sx={{marginLeft: "5px", marginRight: "15px"}}/>)
    return '';
  }

  function renderList(listProps: RenderListParams) {
    return (
      <div {...listProps.props}>
        {listProps.children}
      </div>);
  }

  function renderItem(itemProps: RenderItemParams<QuestionOptionInfo>) {
    return (
      <div  {...itemProps.props} key={itemProps.value.id}>
        <CreateOption option={itemProps.value} isDragged={itemProps.isDragged} onOptionDelete={props.onOptionDelete} 
          onOptionTextChange={props.onOptionTextChange} type={props.type}/>
      </div>);
  }


  return (
    <div className={classes.options} style={props.type === QuestionType.DropDown ? {marginLeft: 20, marginRight: 20} : {}}>
        <List
          values={props.options} onChange={({ oldIndex, newIndex }) => handleOptionMove(oldIndex, newIndex)}
          renderList={renderList} renderItem={renderItem} lockVertically={true}
        />

        {[QuestionType.MultiSelectOther, QuestionType.SingleSelectOther].includes(props.type) ?
        <TextField fullWidth key={-1} size='small' multiline 
        onKeyDown={
          (event) => {
            if (event.key === 'Enter')
              event.preventDefault();
          }}
        InputProps={{ readOnly: true, style: { padding: 5, marginTop: 5, marginBottom: 5 }, startAdornment: getOptionIcon(), endAdornment:
          <IconButton disabled>
            <DeleteIcon/>
          </IconButton>}} value={'Прочее'}>
        </TextField>
        : ''}
    </div>
  );
})