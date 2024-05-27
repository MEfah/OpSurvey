import * as React from 'react';
import classes from '../styles/Email.module.css'
import TextField from '@mui/material/TextField';
import Link from '@mui/material/Link';
import Button from '@mui/material/Button';
import Modal from '@mui/material/Modal';
import { useFetch } from '../hooks/useFetch';
import { sendEmails } from '../http/APIs/EmailAPI';


export interface EmailModalProps {
  open: boolean;
  onClose: () => void;
}

export default function EmailModal (props: EmailModalProps) {
  const [text, setText] = React.useState('');
  const [emails, setEmails] = React.useState('');
  const handleClose = () => props.onClose();
  const [sendEmail, isSendingEmail] = useFetch(async () => {
    return await sendEmails(text, emails.replace(' ', '').replace(',', '\n').split('\n'))
  });

  function canSendEmail() {
    return true;
  }

  async function handleSendEmail() {
    const [response, error] = await sendEmail();

    if (error) {

    } else {
      handleClose();
    }
  }

  return (
    <Modal open={props.open} onClose={handleClose}>
      <div className={`panel ${classes.emailBody}`} style={{width: 600, height: '80%'}}>
        <div className={classes.inputArea}>
          <h2>Email-рассылка</h2>

          <h6 style={{marginTop: 25, marginBottom: -10}}>Введите текст письма:</h6>
          <TextField fullWidth multiline size='small' margin='normal' variant="outlined" InputLabelProps={{ shrink: true, }}
              value={text} onChange={(e) => setText(e.currentTarget.value)} inputProps={{rows: 15}}/>

          <h6 style={{marginTop: 25, marginBottom: -10}}>Введите получателей:</h6>
          <TextField fullWidth multiline size='small' margin='normal' variant="outlined" InputLabelProps={{ shrink: true, }}
              value={emails} onChange={(e) => setEmails(e.currentTarget.value)} inputProps={{rows: 15}}
              helperText={'Перечисляйте адреса электронной почты через запятые или переносом на новую строку'}/>
        </div>

        <div className={classes.actionArea}>
          <Link onClick={handleClose}>Закрыть</Link>
          <Button size='large' variant='contained' disabled={!canSendEmail()} onClick={handleSendEmail}>Отправить</Button>
        </div>
      </div>
    </Modal>
  );
}
