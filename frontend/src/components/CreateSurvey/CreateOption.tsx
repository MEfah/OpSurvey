import React, { memo } from 'react';
import { QuestionOptionInfo, QuestionType } from '../../schemas/QuestionInfo';
import TextField from '@mui/material/TextField';
import RadioButtonUncheckedIcon from '@mui/icons-material/RadioButtonUnchecked';
import CheckBoxOutlineBlankIcon from '@mui/icons-material/CheckBoxOutlineBlank';
import IconButton from '@mui/material/IconButton';
import DeleteIcon from '@mui/icons-material/Delete';

export interface CreateOptionProps {
  type: QuestionType;
  option: QuestionOptionInfo;
  isDragged: boolean;
  onOptionDelete?: (id: number) => void;
  onOptionTextChange?: (id: number, text: string) => void;
}

export const CreateOption = memo(function CreateOption (props: CreateOptionProps) {

  function handleOptionTextChange(id: number, event: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>){
    props.onOptionTextChange?.(id, event.currentTarget.value);
  }

  function handleOptionDelete(id: number) {
    props.onOptionDelete?.(id);
  }

  function getOptionIcon() {
    if ([QuestionType.SingleSelect, QuestionType.SingleSelectOther].includes(props.type))
      return (<RadioButtonUncheckedIcon color='secondary' sx={{marginLeft: "5px", marginRight: "15px"}}/>)
    else if ([QuestionType.MultiSelect, QuestionType.MultiSelectOther].includes(props.type))
      return (<CheckBoxOutlineBlankIcon color='secondary' sx={{marginLeft: "5px", marginRight: "15px"}}/>)
    return '';
  }

  function getOptionStyle(isDragged: boolean) {
    const style: any = {
      marginTop: 5, marginBottom: 5
    };
    if (props.type === QuestionType.DropDown){
      style.padding = 0;
    } else {
      style.padding = 5;
    }

    if (isDragged)
      style.cursor = 'grabbing';
    else
      style.cursor = 'grab';
    return style
  }

  return (
    <TextField fullWidth key={props.option.id} size='small' multiline variant={props.type === QuestionType.DropDown ? 'standard' : 'outlined'}
      onKeyDown={
        (event) => {
          if (event.key === 'Enter')
            event.preventDefault();
        }}
      InputProps={{style: { ...getOptionStyle(props?.isDragged ?? false) }, startAdornment: getOptionIcon(), endAdornment:
      <IconButton onClick={() => handleOptionDelete(props.option.id)}>
        <DeleteIcon/>
      </IconButton>
      }} value={props.option.name} onChange={(e) => handleOptionTextChange(props.option.id, e)}>
    </TextField>
  );
})