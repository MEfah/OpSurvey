import React from 'react';
import SearchInput from '../UI/SearchInput/SearchInput';
import classes from '../../styles/SearchPanel.module.css';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import Select from '@mui/material/Select';
import Switch from '@mui/material/Switch';
import { SortParameterType } from '../../schemas/SurveySearchParams';

export interface SearchPanelProps {
  onSearch?: (search?: string, sortType?: SortParameterType, sortAscending?: boolean) => void;
}

export default function SearchPanel (props: SearchPanelProps) {
  const [sortType, setSortType] = React.useState<SortParameterType | undefined>(undefined);
  const [sortAscending, setSortAscending] = React.useState<boolean>(false);

  const handleSortChange = (event: any, child: React.ReactNode) => {
    setSortType(event.target.value);
  };

  const handleSearch = (text?: string) => {
    props.onSearch?.(text, sortType, sortType ? sortAscending : undefined);
  }

  return (
    <div className='panel stick-top'>
      <SearchInput onSearch={handleSearch}/>
      <div className={classes.options}>
        <div className={classes.optionsLabel}>Сортировка: </div>
        <FormControl variant="standard" sx={{ m: 1, minWidth: 120}}>
          <Select value={sortType} onChange={handleSortChange}>
            <MenuItem value={undefined}>
              <em>Нет</em>
            </MenuItem>
            <MenuItem value={SortParameterType.COMPLETIONS}>Количество прохождений</MenuItem>
            <MenuItem value={SortParameterType.QUESTIONS}>Количество вопросов</MenuItem>
            <MenuItem value={SortParameterType.REQUIRED_QUESTIONS}>Количество обязательных</MenuItem>
            <MenuItem value={SortParameterType.COMPLETION_TIME}>Время прохождения</MenuItem>
            <MenuItem value={SortParameterType.CREATION_DATE}>Дата создания</MenuItem>
          </Select>
        </FormControl>
        <div className={classes.optionsLabel}>По убыванию: </div>
        <Switch value={sortAscending} onChange={(e, c) => setSortAscending(c)}/>
        {/* <div className={classes['options-label']}>Искать в вопросах: </div>
        <Switch/> */}
      </div>
    </div>
  )
}