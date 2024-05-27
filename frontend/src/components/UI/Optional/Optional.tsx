import React from 'react';
import Checkbox from '@mui/material/Checkbox';
import classes from './Optional.module.css'

export interface OptionalProps {
  children: React.ReactNode;
  value?: boolean;
  onChange?: () => void;
}

export default function Optional (props: OptionalProps) {
  return (
    <div className={classes.body}>
      {props.children}
      <Checkbox value={props.value} onChange={props.onChange}/>
    </div>
  )
}