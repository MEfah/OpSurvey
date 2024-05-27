import ErrorPage from './pages/ErrorPage';
import SurveysPage from './pages/SurveysPage';
import CreateSurveyPage from './pages/CreateSurveyPage';
import SignInPage from './pages/SignInPage';
import SignUpPage from './pages/SignUpPage';
import BodyTemplate from './pages/BodyTemplate';
import { SurveysSearchPage } from './pages/SurveysSearchPage';
import UserPage from './pages/UserPage';
import { createBrowserRouter } from 'react-router-dom';
import App from './App';
import MySurveysPage from './pages/MySurveysPage';
import LatestSurveysPage from './pages/LatestSurveysPage';
import SurveyPageWithContext from './pages/SurveyPageContext';
import UnfinishedSurveysPage from './pages/UnfinishedSurveysPage';
import RecommendedPage from './pages/RecommendedPage';
import PopularSurveysPage from './pages/PopularSurveysPage';

export const router = createBrowserRouter([
  {
    path: "/",
    element: <App></App>,
    errorElement: <ErrorPage></ErrorPage>,
    children: [{
        path: "/",
        element: <BodyTemplate/>,
        children: [{
            path: "/",
            element: <SurveysPage/>
          },{
            path: "/surveys",
            element: <SurveysPage/>
          },{
            path: '/surveys/:surveyId',
            element: <SurveyPageWithContext/>
          },{
            path: "/surveys/create",
            element: <CreateSurveyPage/>
          },{
            path: "/user",
            element: <UserPage/>
          },{
            path: '/surveys/my',
            element: <MySurveysPage/>
          },{
            path: '/surveys/latest',
            element: <LatestSurveysPage/>
          },{
            path: '/surveys/popular',
            element: <PopularSurveysPage/>
          },{
            path: '/surveys/unfinished',
            element: <UnfinishedSurveysPage/>
          },{
            path: '/surveys/recommended',
            element: <RecommendedPage/>
          }]
      },{
        path: "/surveys/search",
        element: <SurveysSearchPage/>
      }]
  },{
    path: "/signin",
    element: <SignInPage/>
  },{
    path: "/signup",
    element: <SignUpPage/>
  }
]);