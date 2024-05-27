import * as React from 'react';
import RemoveRedEyeIcon from '@mui/icons-material/RemoveRedEye';
import { useTheme } from '@mui/material/styles';

export interface ViewsIconProps {
}

export default function ViewsIcon (props: ViewsIconProps) {
  const theme = useTheme();

  return (
    <RemoveRedEyeIcon fontSize='inherit' sx={{color: theme.palette.text.secondary}}/>
  );
}
