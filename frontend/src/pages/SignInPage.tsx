import React, { ChangeEvent, useState } from 'react';
import classes from '../styles/Auth.module.css';
import TextField from '@mui/material/TextField';
import Button from '@mui/material/Button';
import Link from '@mui/material/Link';
import HidePassword from '../components/UI/HidePassword/HidePassword';
import { useFetch } from '../hooks/useFetch';
import { SignIn as SignInApi } from '../http/APIs/UserAPI';
import CircularProgress from '@mui/material/CircularProgress';
import { useNavigate } from 'react-router-dom';
import { useAppDispatch } from '../hooks/redux';
import { userSlice } from '../store/reducers/UserSlice';
import { UserInfo } from '../schemas/UserInfo';

export default function SignInPage() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [userNotFound, setUserNotFound] = useState(false);
  const [wrongPwd, setWrongPwd] = useState(false);
  const [signIn, isSigningIn] = useFetch(async () => {
    return await SignInApi({email, password});
  });
  const navigate = useNavigate();
  const dispatch = useAppDispatch();

  function handleEmailChanged(event: ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) {
    setEmail(event.currentTarget.value);
    setUserNotFound(false);
  }

  function validateEmail() {
    const match = String(email)
    .toLowerCase()
    .match(
      /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|.(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
    );

    if (match)
      return true;
    return false;
  }

  function handlePwdChanged(event: ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) {
    setPassword(event.currentTarget.value);
    setWrongPwd(false);
  }

  async function handleAccept() {
    const [response, error] = await signIn();
    console.log(response);
    if (error) {
      if (response?.status === 404) {
        setUserNotFound(true);
      } else if (response?.status === 401) {
        setWrongPwd(true);
      }
    } else {
      const userInfo: UserInfo = response?.data.user;
      localStorage.setItem('access-token', response?.data.accessToken);
      dispatch(userSlice.actions.setUser(userInfo));
      navigate('/');
    }
  }

  return (
  <div className={classes.screen}>
    <div className={`panel ${classes.authPanel}`}>
      <div className={classes.headerFrea}>
        <div className={classes.siteName}>OpSurvey</div>
        <div className={classes.authHeader}>Вход</div>
      </div>
      <div className={classes.inputArea}>
        <div className={classes.textField}>
          <TextField label="Email" margin="dense" type='email' helperText={userNotFound ? 'Пользователь не найден' : ' '} value={email} onChange={handleEmailChanged}
            InputLabelProps={{ shrink: true, }} inputProps={{ style: { padding: 10 }}} error={!validateEmail() || userNotFound}/>
        </div>
        <div className={classes.textField}>
          <HidePassword label="Пароль" margin="dense" helperText={password.length < 5 ? 'Пароль слишком короткий' : (wrongPwd ? 'Неверный пароль' : ' ') }
            value={password} onChange={handlePwdChanged} error={password.length < 5 || wrongPwd}
            InputLabelProps={{ shrink: true, }} inputProps={{ style: { padding: 10 }}}/>
        </div>
      </div>
      
      <div className={classes.actionArea}>
        {
          isSigningIn ?
          <div>
            <CircularProgress/>
          </div>
          :
          <Button size='large' variant='contained' onClick={handleAccept} disabled={!validateEmail() || wrongPwd || userNotFound}>Войти</Button>
        }
        <Link href='/'>Продолжить без аккаунта</Link>
        <Link href='/signup'>Зарегистрироваться</Link>
      </div>
    </div>
  </div>
)}