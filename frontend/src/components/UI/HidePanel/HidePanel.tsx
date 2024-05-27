import React, { useState } from 'react';
import ArrowDropDownRoundedIcon from '@mui/icons-material/ArrowDropDownRounded';
import classes from './HidePanel.module.css';

export interface HidePanelProps {
  header: React.ReactNode | string;
  hidden?: boolean;
  children: React.ReactNode;
}

export default function HidePanel (props: HidePanelProps) {
  const [hidden, setHidden] = useState(props.hidden ?? false)

  return (
    <div className={`panel hide-panel ${hidden ? classes.hidden : ''}`}>
      <div onClick={(event) => setHidden(!hidden)} className={classes.header}>
        <div className={classes.headerText}>
          {props.header}
        </div>
        <div className={classes.headerImg}>
          <ArrowDropDownRoundedIcon fontSize='inherit' color='primary'/>
        </div>
        
      </div>
      <div className={classes.content} >
        {props.children}
      </div>
    </div>
  )
}