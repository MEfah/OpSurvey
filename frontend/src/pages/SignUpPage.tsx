import React, { useEffect, useState } from 'react';
import SignUpPanel from '../components/SignUp/SignUpPanel';
import SignUpNamePanel from '../components/SignUp/SignUpNamePanel';
import { useNavigate } from 'react-router-dom';
import { useAppDispatch, useAppSelector } from '../hooks/redux';
import { userSlice } from '../store/reducers/UserSlice';
import { CheckEmail, SignUp as SignUpApi } from '../http/APIs/UserAPI';
import { useFetch } from '../hooks/useFetch';


export default function SignUpPage() {
  const initUser = useAppSelector(state => state.user);

  const [stage, setStage] = useState(0);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [name, setName] = useState('');
  const [nameTaken, setNameTaken] = useState(false);
  const navigate = useNavigate();
  const dispatch = useAppDispatch();
  const [signUp, isSigningUp] = useFetch(async () => {
    return await SignUpApi({
      email, password, name
    });
  });
  
  function handleEmailChanged(email: string) {
    setEmail(email);
  }

  function handlePasswordChanged(password: string) {
    setPassword(password);
  }

  function handleNameChanged(name: string) {
    setName(name);
    setNameTaken(false);
  }

  function handleContinue(newEmail: string, newPassword: string) {
    setEmail(newEmail);
    setPassword(newPassword);
    setStage(1);
  }

  async function handleAccept() {
    const [response, error] = await signUp();

    if (error) {
      if (response?.status === 409) {
        setNameTaken(true);
      }
    } else {
      const userInfo = response?.data.user;
      localStorage.setItem('access-token', response?.data.accessToken);
      dispatch(userSlice.actions.setUser(userInfo));
      navigate('/');
    }
  }

  function handleCancel() {
    setStage(0);
  }

  if (stage === 0)
    return (
      <SignUpPanel onContinue={handleContinue} email={email} password={password} onEmailChanged={handleEmailChanged} onPasswordChanged={handlePasswordChanged}/>
    )
  else
    return (
      <SignUpNamePanel onAccept={handleAccept} onCancel={handleCancel} name={name} onNameChange={handleNameChanged} isSigningUp={isSigningUp} nameTaken={nameTaken}/>
    )
}