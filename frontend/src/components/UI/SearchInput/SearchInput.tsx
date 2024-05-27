import React, { useState } from 'react';
import { Button } from '@mui/material';
import classes from './SearchInput.module.css';
;

export interface SearchInputProps {
  onSearch?: (text?: string) => void;
}

export default function SearchInput (props: SearchInputProps) {
  const [searchText, setSearchText] = useState('');

  function handleSearch() {
    props.onSearch?.(searchText.trim() === '' ? undefined : searchText);
  }

  return (
    <div className={classes.body}>
        <input className={classes.search} value={searchText} onChange={(e) => setSearchText(e.currentTarget.value)}/>
      
      <Button variant="contained" sx={{boxShadow: 0}} style={{
        borderTopLeftRadius: '0',
        borderBottomLeftRadius: '0',
        borderTopRightRadius: '4px',
        borderBottomRightRadius: '4px',
      }} onClick={handleSearch}>Искать</Button>
    </div>
  )
}