import * as React from 'react';
import { QuestionType } from '../../../schemas/QuestionInfo';
import classes from '../../../styles/Survey.module.css';
import Radio from '@mui/material/Radio';
import Checkbox from '@mui/material/Checkbox';

export interface OptionProps {
  type: QuestionType;
  children: React.ReactNode;
  isSelected?: boolean;
  count?: number;
  totalCount?: number;
}

export const Option = React.memo(function Option (props: OptionProps) {
  function getOptionControl() {
    if ([QuestionType.SingleSelect, QuestionType.SingleSelectOther, QuestionType.DropDown].includes(props.type))
      return (<Radio color='primary' value={props.isSelected} style={{marginTop: -5, marginBottom: -5, marginLeft: -10}} checked={props.isSelected}
      disabled/>);
    else if ([QuestionType.MultiSelect, QuestionType.MultiSelectOther].includes(props.type))
      return (<Checkbox color='primary' value={props.isSelected} style={{marginTop: -5, marginBottom: -5, marginLeft: -10}} checked={props.isSelected}
      disabled/>);
    return '';
  }

  return (
    <>
      <div className={classes.resultOption}>
        {getOptionControl()} 
        <div style={{color: 'var(--text-color-primary)', width: '100%'}}>{props.children}</div>
        {
          props.count && props.totalCount ? 
          <>
            <div className={classes.optionsResultsBar} style={{width: `${props.count / props.totalCount * 100}%`}}></div>
            <div className={classes.optionsResultsValue}>{`${props.count} (${Math.round(props.count / props.totalCount * 100)}%)`}</div>
          </>
          :
            ''
        }

      </div>
    </>
  );
})