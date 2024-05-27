import React, {useState} from 'react';
import { useAppDispatch, useAppSelector } from '../hooks/redux';
import classes from '../styles/User.module.css';
import TextField from '@mui/material/TextField';
import Button from '@mui/material/Button';
import Tooltip from '@mui/material/Tooltip';
import Avatar from '@mui/material/Avatar';
import { userSlice } from '../store/reducers/UserSlice';
import { useNavigate } from 'react-router-dom';
import { useFetch } from '../hooks/useFetch';
import { UpdateUser } from '../http/APIs/UserAPI';
import { UserInfo } from '../schemas/UserInfo';
import { MEDIA_URL } from '../http/api';


export default function UserPage () {
  const fileInputRef = React.useRef<HTMLInputElement>(null);

  const userInfo = useAppSelector(state => state.user);
  const [name, setName] = useState(userInfo.name);
  const [description, setDescription] = useState(userInfo.description ?? '');
  const [imgSrc, setImgSrc] = useState<string | ArrayBuffer | null>(userInfo.imgSrc ?? '');
  const [nameTaken, setNameTaken] = useState(false);
  const [imgCounter, setImgCounter] = useState(0);
  const dispatch = useAppDispatch();
  const navigate = useNavigate();
  const [updateUser, isUpdatingUser] = useFetch(async () => {
    const formData = new FormData();
    if (fileInputRef.current?.files?.[0]){
      formData.append('file', fileInputRef.current.files[0]);

      return await UpdateUser(userInfo.id, {
        name: name === userInfo.name ? undefined : name,
        description: description === userInfo.description ? undefined : description
      }, formData);
    }
    console.log(description === userInfo.description ? undefined : description);
    return await UpdateUser(userInfo.id, {
      name: name === userInfo.name ? undefined : name,
      description: description === userInfo.description ? undefined : description
    }, formData);
  });

  function handleNameChanged(event: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) {
    setName(event.currentTarget.value);
    setNameTaken(false);
  }

  function handleDescriptionChanged(event: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) {
    setDescription(event.currentTarget.value);
  }

  function handleImageUpload(event: React.ChangeEvent<HTMLInputElement>) {
    if (event.currentTarget.files && event.currentTarget.files[0]) {
      const reader = new FileReader();
      reader.onload = (e) => {
        if (e.target?.result) 
          setImgSrc(reader.result);
      }
      reader.readAsDataURL(event.currentTarget.files[0]);
    }
  }

  function determineCanSave() {
    console.log()
    return name.length >= 5 && (name !== userInfo.name || description !== (userInfo.description ?? '') || imgSrc !== (userInfo.imgSrc ?? ''));
  }

  async function handleAccept() {
    const [response, error] = await updateUser();
    
    if (error) {
      if (response?.status === 409) {
        setNameTaken(true);
      } else {

      }
    } else {
      const user: UserInfo = response?.data;
      dispatch(userSlice.actions.setUser(user));
      navigate('/');
    }
  }

  function getImgSrc() {
    if(imgSrc) {
      if (typeof imgSrc === 'string') {
        if (imgSrc === userInfo.imgSrc)
          return MEDIA_URL + imgSrc;
        return imgSrc;
      }
      return (imgSrc as unknown) as string;
    }
    return '';
  }
  
  return (
    <div className={`panel`}>
      <div className={classes.nameImage}>
        <div className={classes.uploadedImage} onClick={() => fileInputRef.current?.click()}>
          { imgSrc ?
            <Tooltip title='Изменить изображение'>
              <img key={imgCounter} style={{height: "100%", width: "100%"}} src={getImgSrc()} alt="Uploaded"/> 
            </Tooltip>
          : <Avatar style={{height: "100%", width: "100%", fontSize: "20pt"}}>{userInfo.name[0]}</Avatar> }
        </div>
        <div className={classes.name}>
          <TextField fullWidth multiline placeholder="Имя" size='medium' variant="standard" onKeyDown={
            (event) => {
              if (event.key === 'Enter')
                event.preventDefault();
            }} value={name} onChange={handleNameChanged} helperText={nameTaken ? 'Имя занято' : ' '} error={nameTaken}/>
        </div>
      </div>
      
      <input
        ref={fileInputRef}
        type="file"
        accept="image/*"
        style={{ display: 'none' }}
        onChange={handleImageUpload}
      />

      <div className={classes.description}>
        <TextField fullWidth multiline label="Дополнительная информация" size='medium' margin='normal' variant="outlined" InputLabelProps={{ shrink: true, }}
          value={description} onChange={handleDescriptionChanged} style={{}} InputProps={{rows: 15}}/>
      </div>
      
      <div className={classes.actionArea}>
        <Button size='large' variant='contained' disabled={!determineCanSave() || nameTaken} onClick={handleAccept}>Сохранить</Button>
      </div>
    </div>
  );
}
