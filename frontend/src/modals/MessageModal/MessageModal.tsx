import * as React from 'react';
import classes from '../styles/Email.module.css'
import TextField from '@mui/material/TextField';
import Link from '@mui/material/Link';
import Button from '@mui/material/Button';
import Modal from '@mui/material/Modal';
import { useFetch } from '../../hooks/useFetch';
import { sendEmails } from '../../http/APIs/EmailAPI';
import { useMessages } from './MessageProvider';


export default function MessageMoodal () {
  const messagesParams = useMessages();

  return (
    <Modal open={messagesParams?.open ?? false} onClose={messagesParams?.onCancel}>
      <div className={`panel`}>
        {
          messagesParams?.header ?
            <h2>{messagesParams?.header}</h2>
          :
            ''
        }

        <div>
          {messagesParams?.message}
        </div>

        <div className={classes.actionArea}>
          <Link onClick={messagesParams?.onCancel}>{messagesParams?.cancelText ?? 'Отмена'}</Link>
          <Button size='large' variant='contained' onClick={messagesParams?.onAccept}>{messagesParams?.acceptText ?? 'Подтвердить'}</Button>
        </div>
      </div>
    </Modal>
  );
}
