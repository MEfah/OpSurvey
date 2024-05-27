import React from 'react';
import PopularSurveys from '../components/SidePanels/PopularSurveys';
import { Outlet } from 'react-router-dom';
import LatestSurveys from '../components/SidePanels/LatestSurveys';

export default function BodyTemplate () {
  return (
    <div className="body-columns">
      <div className="body-column-left">
        <Outlet/>
      </div>
      <div className="body-column-right">
        <PopularSurveys/>
        <LatestSurveys/>
      </div>
    </div>
  );
}
