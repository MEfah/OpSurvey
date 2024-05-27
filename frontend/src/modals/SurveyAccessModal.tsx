import * as React from 'react';
import classes from '../styles/CreateSurvey.module.css'
import TextField from '@mui/material/TextField';
import Link from '@mui/material/Link';
import Button from '@mui/material/Button';
import Modal from '@mui/material/Modal';
import { AccessResults, AccessResultsType, AccessSurvey, AccessSurveyType } from '../schemas/SurveyAccessInfo';
import FormControl from '@mui/material/FormControl';
import Select from '@mui/material/Select';
import MenuItem from '@mui/material/MenuItem';
import {SelectChangeEvent} from '@mui/material';

export interface SurveyAccessModalProps {
  accessSurvey: React.MutableRefObject<AccessSurvey>;
  accessResults: React.MutableRefObject<AccessResults>;
  update?: boolean;
  onUpdate?: () => void;
  open: boolean;
  onClose: () => void;
  onAccept: () => void;
}

export default function SurveyAccessModal (props: SurveyAccessModalProps) {
  const [accessSurvey, setAccessSurvey] = React.useState<AccessSurvey>(props.accessSurvey.current);
  const [accessResults, setAccessResults] = React.useState<AccessResults>(props.accessResults.current);

  React.useEffect(() => {
    setAccessSurvey(props.accessSurvey.current);
    setAccessResults(props.accessResults.current);
  }, [props.update])

  function handleCancel() {
    setAccessSurvey(props.accessSurvey.current);
    setAccessResults(props.accessResults.current);
    props.onClose();
  }

  function handleAccept() {
    props.accessSurvey.current = accessSurvey;
    props.accessResults.current = accessResults;
    props.onAccept();
  }

  function handleAccessSurveyTypeChanged(event: SelectChangeEvent<AccessSurveyType>, child: React.ReactNode) {
    setAccessSurvey(accessSurvey => {return {...accessSurvey, accessTypeSurvey: event.target.value as AccessSurveyType}});
  }

  function handleAccessResultsTypeChanged(event: SelectChangeEvent<AccessResultsType>, child: React.ReactNode) {
    setAccessResults(accessResults => {return {...accessResults, accessTypeResults: event.target.value as AccessResultsType}});
  }

  return (
    <Modal open={props.open} onClose={handleCancel}>
      <div className={`panel modal-body ${classes.modalBody}`} style={{width: 600}}>
        <div className={`${classes.modalInputArea}`}>
          <h2>Настройки доступа опроса</h2>

          <div className={classes.selectPair}>
            <h6>Доступ к опросу:</h6>
            <FormControl variant="standard" sx={{ m: 0, minWidth: 120, flex: 1, marginLeft: 1}}>
              <Select value={accessSurvey.accessTypeSurvey} onChange={handleAccessSurveyTypeChanged}>
                <MenuItem value={AccessSurveyType.ALL}>Доступен всем</MenuItem>
                <MenuItem value={AccessSurveyType.ONLY_AUTHORIZED}>Доступен только авторизованным</MenuItem>
                <MenuItem value={AccessSurveyType.ONLY_URL}>Доступен только по URL</MenuItem>
                <MenuItem value={AccessSurveyType.ONLY_LIST}>Доступен только людям из списка</MenuItem>
                <MenuItem value={AccessSurveyType.NONE}>Не доступен никому</MenuItem>
              </Select>
            </FormControl>
          </div>

          {
            accessSurvey.accessTypeSurvey === AccessSurveyType.ONLY_LIST ?
              <TextField multiline fullWidth size='small' label="Список доступа" margin='normal'/>
            :
              ''
          }

          <div className={classes.selectPair}>
            <h6>Доступ к результатам опроса:</h6>
            <FormControl variant="standard" sx={{ m: 0, minWidth: 120, flex: 1, marginLeft: 1}}>
              <Select value={accessResults.accessTypeResults} onChange={handleAccessResultsTypeChanged}>
                <MenuItem value={AccessResultsType.ALL}>Доступны всем</MenuItem>
                <MenuItem value={AccessResultsType.ONLY_LIST}>Доступны только людям из списка</MenuItem>
                <MenuItem value={AccessResultsType.NONE}>Не доступны никому</MenuItem>
              </Select>
            </FormControl>
          </div>

          {
            accessResults.accessTypeResults === AccessResultsType.ONLY_LIST ?
              <TextField multiline fullWidth size='small' label="Список доступа" margin='normal'/>
            :
              ''
          }
        </div>

        <div className={classes.actionArea}>
          <Link onClick={handleCancel}>Отмена</Link>
          <Button size='large' variant='contained' onClick={handleAccept}>Сохранить</Button>
        </div>
      </div>
    </Modal>
  );
}
