import React, { ChangeEvent, useState } from 'react';
import classes from '../../styles/Auth.module.css';
import TextField from '@mui/material/TextField';
import Button from '@mui/material/Button';
import Link from '@mui/material/Link';
import CircularProgress from '@mui/material/CircularProgress';

interface SignUpNamePanelProps {
  onNameChange?: (name: string) => void;
  onAccept?: () => void;
  onCancel?: () => void;
  name: string;
  nameTaken: boolean;
  isSigningUp: boolean;
}

export default function SignUpNamePanel(props: SignUpNamePanelProps) {
  function handleNameChange(event: ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) {
    props.onNameChange?.(event.currentTarget.value);
  }

  function handleAccept() {
    props.onAccept?.();
  }

  function handleCancel() {
    props.onCancel?.();
  }

  function canAccept() {
    return props.name.length >= 5;
  }

  return (
  <div className={classes.screen}>
    <div className={`panel ${classes.authPanel} ${classes.signupName}`}>
      <div className={classes.headerArea}>
        <div className={classes.siteName}>OpSurvey</div>
        <div className={classes.authHeader}>Регистрация</div>
      </div>
      <div className={classes.inputArea}>
        <div className={classes.nameHint}>Введите имя, которое будут видеть другие пользователи</div>
        <div className={classes.textField}>
          <TextField margin="dense" type='text' color='primary' helperText={props.nameTaken ? 'Имя занято' : "Имя можно изменить позже"} 
            value={props.name} onChange={handleNameChange} error={props.nameTaken}
            InputLabelProps={{ shrink: true, }} inputProps={{ style: { padding: 10 }}}/>
        </div>
      </div>
      
      <div className={classes.actionArea}>
        {
          props.isSigningUp ?
          <div>
            <CircularProgress/>
          </div>
          :
          <Button size='large' variant='contained' onClick={handleAccept} disabled={!canAccept()}>Завершить</Button>
        }
        <div onClick={handleCancel}><Link>Отмена</Link> </div>
      </div>
    </div>
  </div>
)}