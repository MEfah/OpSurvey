import React, { ChangeEvent, useState, useEffect } from 'react';
import classes from '../../styles/Auth.module.css';
import TextField from '@mui/material/TextField';
import Button from '@mui/material/Button';
import Link from '@mui/material/Link';
import HidePassword from '../UI/HidePassword/HidePassword';
import { passwordStrength } from 'check-password-strength';
import { CheckEmail } from '../../http/APIs/UserAPI';
import { useFetch } from '../../hooks/useFetch';
import CircularProgress from '@mui/material/CircularProgress';

interface SignUpPanelProps {
  email: string;
  password: string;
  onEmailChanged?: (email: string) => void;
  onPasswordChanged?: (password: string) => void;
  onContinue?: (email: string, password: string) => void;
}

export default function SignUpPanel(props: SignUpPanelProps) {
  const [password2, setPassword2] = useState('');
  const [passwordStatus, setPasswordStatus] = useState(-1);
  const [emailTaken, setEmailTaken] = useState(false);
  const [checkEmail, isCheckingEmail] = useFetch(async () => {
    const res = await CheckEmail(props.email);
    return res;
  });
  
  function handleEmailChange(event: ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) {
    props.onEmailChanged?.(event.currentTarget.value);
    setEmailTaken(false);
  }

  function validateEmail() {
    const match = String(props.email)
    .toLowerCase()
    .match(
      /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|.(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
    );

    if (match)
      return true;
    return false;
  }

  function handlePasswordChange(event: ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) {
    let pwd = event.currentTarget.value;
    console.log(pwd);
    if (pwd)
      setPasswordStatus(passwordStrength(pwd).id);
    else
      setPasswordStatus(-1);
    props.onPasswordChanged?.(pwd);
  }

  function getPasswordHint() {
    switch(passwordStatus) {
      case -1:
        return "Используйте латиницу, цифры и спец. символы";
      case 0:
        return "Слишком слабый";
      case 1:
        return "Слабый";
      case 2:
        return "Средний";
      case 3:
        return "Сильный";
    }
  }

  function getPasswordClass() {
    switch(passwordStatus) {
      case -1:
        return "";
      case 0:
        return classes.error;
      case 1:
        return classes.weak;
      case 2:
        return classes.medium;
      case 3:
        return classes.strong;
    }
  }

  function handlePassword2Change(event: ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) {
    let pwd = event.currentTarget.value;
    setPassword2(pwd);
  }

  function validateForm() {
    return validateEmail() && passwordStatus > 0 && props.password === password2 && !emailTaken;
  }

  async function handleAccept() {
    const [response, error] = await checkEmail();
    console.log([response, error]);
    if (error) {
      
      if (response?.status === 409){
        setEmailTaken(true);
      } else { }
    } else {
      props.onContinue?.(props.email, props.password);
    }
  }

  return (
  <div className={classes.screen}>
    <div className={`panel ${classes.authPanel} ${classes.signup}`}>
      <div className={classes.headerArea}>
        <div className={classes.siteName}>OpSurvey</div>
        <div className={classes.authHeader}>Регистрация</div>
      </div>
      <div className={classes.inputArea}>
        <div className={classes.textField}>
          <TextField label="Email" margin="dense" type='email' color='primary' helperText={emailTaken ? 'Email занят' : ' '} value={props.email} onChange={handleEmailChange} 
            error={!validateEmail() || emailTaken}
            InputLabelProps={{ shrink: true, }} inputProps={{ style: { padding: 10 }}}/>
        </div>
        <div className={`${classes.textField} ${getPasswordClass()}`}>
          <HidePassword label="Пароль" margin="dense" value={props.password} onChange={handlePasswordChange} error={passwordStatus < 1 ? true : false}
            InputLabelProps={{ shrink: true, }} inputProps={{ style: { padding: 10 }}}
            helperText={getPasswordHint()}/>
        </div>
        <div className={`${classes.textField}`}>
          <HidePassword label="Подтвердите пароль" margin="dense" helperText=" "  onChange={handlePassword2Change} error={props.password !== password2}
            InputLabelProps={{ shrink: true, }} inputProps={{ style: { padding: 10 }}}/>
        </div>
      </div>
      
      <div className={classes.actionArea}>
        {
          isCheckingEmail ?
          <div>
            <CircularProgress/>
          </div>
          :
          <Button size='large' variant='contained' onClick={handleAccept} disabled={!validateForm()}>Продолжить</Button>
        }
        <div>Есть аккаунт? <Link href='/signin'>Войти</Link> </div>
      </div>
    </div>
  </div>
)}