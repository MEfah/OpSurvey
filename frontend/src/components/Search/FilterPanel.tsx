import React, { useState } from 'react';
import HideSection from '../UI/HideSection/HideSection';
import Optional from '../UI/Optional/Optional';
import RangeInput from '../UI/RangeInput/RangeInput';
import classes from '../../styles/FilterPanel.module.css';
import { FilterParameterType } from '../../schemas/SurveySearchParams';
import { FilterInfo } from '../../schemas/FilterInfo';

export interface FilterPanelProps {
  filterParams: Partial<Record<FilterParameterType, FilterInfo>>;
  onChange?: (paramType: FilterParameterType, newInfo: FilterInfo) => void;
}

export default function FilterPanel (props: FilterPanelProps) {
  function getUseFilter(filterParameterType: FilterParameterType): boolean{
    return props.filterParams[filterParameterType]?.useFilter ?? false;
  }

  function toggleUseFilter(filterParameterType: FilterParameterType) {
    let filterInfo = props.filterParams[filterParameterType];
    if (filterInfo)
      props.onChange?.(filterParameterType, {...filterInfo, useFilter: !filterInfo.useFilter});
    else
      props.onChange?.(filterParameterType, {useFilter: true});
  }

  function setRange(filterParameterType: FilterParameterType, from: number, to: number) {
    let filterInfo = props.filterParams[filterParameterType];
    if (filterInfo)
      props.onChange?.(filterParameterType, {...filterInfo, range: {from: from, to: to}});
    else
      props.onChange?.(filterParameterType, {useFilter: true, range: {from: from, to: to}});
  }

  return (
    <div>
      <HideSection hidden={true} header={
        <Optional value={getUseFilter(FilterParameterType.COMPLETIONS)} onChange={() => toggleUseFilter(FilterParameterType.COMPLETIONS)}>
          <div className={classes.sectionHeader}>Количество прохождений</div>
        </Optional>}>
        <RangeInput min={0} max={1000} from={0} to={1000} 
          disabled={!getUseFilter(FilterParameterType.COMPLETIONS)} onChange={(from, to) => setRange(FilterParameterType.COMPLETIONS, from, to)}/>
      </HideSection>
      <HideSection hidden={true} header={
        <Optional value={getUseFilter(FilterParameterType.QUESTIONS)} onChange={() => toggleUseFilter(FilterParameterType.QUESTIONS)}>
            <div className={classes.sectionHeader}>Количество вопросов</div>
        </Optional>}>
        <RangeInput min={0} max={1000} rangeMax={100} from={0} to={100} 
          disabled={!getUseFilter(FilterParameterType.QUESTIONS)} onChange={(from, to) => setRange(FilterParameterType.QUESTIONS, from, to)}/>
      </HideSection>
      <HideSection hidden={true} header={
        <Optional value={getUseFilter(FilterParameterType.REQUIRED_QUESTIONS)} onChange={() => toggleUseFilter(FilterParameterType.REQUIRED_QUESTIONS)}>
          <div className={classes.sectionHeader}>Количество обязательных</div>
        </Optional>}>
        <RangeInput min={0} max={1000} rangeMax={100} from={0} to={100} 
          disabled={!getUseFilter(FilterParameterType.REQUIRED_QUESTIONS)} onChange={(from, to) => setRange(FilterParameterType.REQUIRED_QUESTIONS, from, to)}/>
      </HideSection>
      <HideSection hidden={true} header={
        <Optional value={getUseFilter(FilterParameterType.COMPLETION_TIME)} onChange={() => toggleUseFilter(FilterParameterType.COMPLETION_TIME)}>
          <div className={classes.sectionHeader}>Время прохождения</div>
        </Optional>}>
        <RangeInput min={0} max={1000} rangeMax={100} from={0} to={100} 
          disabled={!getUseFilter(FilterParameterType.COMPLETION_TIME)} onChange={(from, to) => setRange(FilterParameterType.COMPLETION_TIME, from, to)}/>
      </HideSection>
      <HideSection hidden={true} header={
        <Optional value={getUseFilter(FilterParameterType.CREATION_DATE)} onChange={() => toggleUseFilter(FilterParameterType.CREATION_DATE)}>
          <div className={classes.sectionHeader}>Дата создания</div>
        </Optional>}>
        <RangeInput min={0} max={1000} rangeMax={100} from={0} to={100} 
          disabled={!getUseFilter(FilterParameterType.CREATION_DATE)} onChange={(from, to) => setRange(FilterParameterType.CREATION_DATE, from, to)}/>
      </HideSection>
      <Optional value={getUseFilter(FilterParameterType.RESULTS_ACCESSIBLE)} onChange={() => toggleUseFilter(FilterParameterType.RESULTS_ACCESSIBLE)}>
        <div className={classes.sectionHeader}>Доступны результаты</div>
      </Optional>
    </div>
  );
}
