import React, { useState } from 'react';
import classes from './HideSection.module.css'
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
export interface HideSectionProps {
  header: React.ReactNode | string;
  children: React.ReactNode;
  hidden?: boolean;
}

export default function HideSection (props: HideSectionProps) {
    const [hidden, setHidden] = useState(props.hidden ?? false)

  return (
    <div className={`${classes.body} ${hidden ? classes.hidden : ''}`}>
      <div className={classes.header}>
        <div className={classes.headerButton} onClick={(event) => setHidden(!hidden)}>
          <ExpandMoreIcon className={classes.headerImg} color='primary' sx={{fontSize: 30}}/>
        </div>
        <div className={classes.headerContent}>
          {props.header}
        </div>
      </div>
      <div className={classes.content} >
        {props.children}
      </div>
    </div>
  )
}