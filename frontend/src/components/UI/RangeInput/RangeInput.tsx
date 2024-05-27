import React, { ChangeEvent, FC, useState } from 'react'
import Slider from '@mui/material/Slider';
import TextField from '@mui/material/TextField';
import Grid from '@mui/material/Grid';
import classes from './RangeInput.module.css'


function valuetext(value: number): string {
  return `${value}`;
}


export interface RangeInputProps {
  min: number;
  max: number;
  from?: number;
  to?: number;
  rangeMin?: number;
  rangeMax?: number;
  disabled?: boolean;
  onChange?: (from: number, to: number) => void;
}

const RangeInput: FC<RangeInputProps> = (props) => {
  const min = props.min ?? 0;
  const max = props.max ?? 100;
  const rangeMin = props.rangeMin ? Math.max(props.rangeMin, min) : min;
  const rangeMax = props.rangeMax ? Math.min(props.rangeMax, max) : max;
  const [value, setValue] = useState<number[]>([props.from ?? min, props.to ?? max]);

  const marks = [{
      value: rangeMin,
      label: valuetext(rangeMin),
    },{
      value: rangeMax,
      label: valuetext(rangeMax),
    }];

  const handleSliderChange = (event: Event, newValue: number | number[]) => {
    if (typeof newValue === "number"){
      setValue([newValue, newValue]);
    }
    else {
      setValue(newValue);
    }
  };

  const handleSliderCommit = (event: Event | React.SyntheticEvent, newValue: number | number[]) => {
    if (typeof newValue === "number"){
      props.onChange?.(newValue, newValue);
    }
    else {
      props.onChange?.(newValue[0], newValue[1]);
    }
  }

  const handleFromChange = (event: ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    let from = event.currentTarget.value ?? event.currentTarget.value === "" ? parseInt(event.currentTarget.value) : 0;
    let to = value[1];
    if (from < min) 
      from = min;
    else if (from > to) {
      from = to;
    }
    setValue([from, to])
    props.onChange?.(from, to);
  }

  const handleToChange = (event: ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    let from = value[0];
    let to = event.currentTarget.value ?? event.currentTarget.value === "" ? parseInt(event.currentTarget.value) : 0;
    if (to > max) 
      to = max;
    else if (from > to) {
      from = to;
    }
    setValue([from, to])
    props.onChange?.(from, to);
  }

  return (
    <div>
      <Grid container spacing={0}>
        <Grid item xs={3}>
          <TextField label="От" size="small" margin="dense" className='hide-number-arrows' type='number' 
          value={value?.[0]} onChange={handleFromChange} disabled={props.disabled}
            InputLabelProps={{ shrink: true, }} inputProps={{ style: { padding: 5 }}}
          />
        </Grid>
        <Grid item xs={6}></Grid>
        <Grid item xs={3}>
          <TextField label="До" size="small" margin="dense" className='hide-number-arrows' type='number'
          value={value?.[1]} onChange={handleToChange} disabled={props.disabled}
            InputLabelProps={{ shrink: true, }} inputProps={{ style: { padding: 5 }}}
          />
        </Grid>
      </Grid>
      <div className={classes.slider}>
        <Slider value={value} onChange={handleSliderChange} valueLabelDisplay="auto" getAriaValueText={valuetext}
          min={rangeMin} max={rangeMax} marks={marks} disabled={props.disabled} onChangeCommitted={handleSliderCommit}
        />
      </div>
      
    </div>
  )
}

export default RangeInput;