import React, { useEffect } from 'react';
import './styles/App.css';
import surveyData from './surveyData';
import SurveyItem from './components/SurveyLists/SurveyItem';
import Navbar from './components/Navbar';
import { Outlet } from 'react-router-dom';
import { CheckAuth, initCookieId } from './http/services/Auth';



function App() {

  useEffect(() => {
    const checkAuth = async () => {
      if (!await CheckAuth())
        throw Error;
    }
    const getCookieId = async () => {
      await initCookieId();
    }

    checkAuth().then(() => {}, getCookieId);
  }, [])

  return (
    <>
      <Navbar/>
      <div className='survey-app'>
        <Outlet/>

      </div>
      <footer>
        
      </footer>
    </>
  );
}

export default App;
