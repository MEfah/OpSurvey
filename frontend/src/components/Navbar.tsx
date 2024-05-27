import React, { useState } from 'react';
import SearchInput from './UI/SearchInput/SearchInput';
import { Link } from '@mui/material';
import classes from '../styles/Navbar.module.css';
import Button from '@mui/material/Button';
import { useTheme } from '@mui/material/styles';
import { useAppDispatch, useAppSelector } from '../hooks/redux';
import Avatar from '@mui/material/Avatar';
import Menu from '@mui/material/Menu';
import MenuItem from '@mui/material/MenuItem';
import Logout from '@mui/icons-material/Logout';
import ArrowDropDownRoundedIcon from '@mui/icons-material/ArrowDropDownRounded';
import { userSlice } from '../store/reducers/UserSlice';
import { useNavigate } from 'react-router-dom';
import { SignOut } from '../http/APIs/UserAPI';
import { useFetch } from '../hooks/useFetch';
import { MEDIA_URL } from '../http/api';
import EmailIcon from '@mui/icons-material/Email';
import EmailModal from '../modals/EmailModal';


export interface NavbarProps {
}

export default function Navbar (props: NavbarProps) {
  const [emailOpen, setEmailOpen] = useState(false);
  const theme = useTheme();
  const {name, imgSrc} = useAppSelector(state => state.user);
  const dispatch = useAppDispatch();
  const navigate = useNavigate();
  const [signOut] = useFetch(async () => {
    return await SignOut();
  });
  const [anchorEl, setAnchorEl] = React.useState<null | HTMLElement>(null);
  const open = Boolean(anchorEl);
  const handleClick = (event: React.MouseEvent<HTMLElement>) => {
    setAnchorEl(event.currentTarget);
  };
  const handleClose = () => {
    setAnchorEl(null);
  };
  async function handleSignOut() {
    const [response, error] = await signOut();
    if (error) {

    } else {
      dispatch(userSlice.actions.clearUser());
      handleClose();
      navigate('/');
    }
  }
  
  return (
      <nav>
          <EmailModal open={emailOpen} onClose={() => setEmailOpen(false)}/>
          <div className={classes.siteName}>
              <a href="/">OpSurvey</a>
          </div>

          <div className={classes.navigation}>
            <Link href="/surveys/search">Поиск</Link>
            <Link href="/surveys/recommended">Моя лента</Link>
            <Link href="/surveys/popular">Популярное</Link>
            <Link href="/surveys/latest">Недавнее</Link>
            {
              name ? 
                <>
                  <Link href="/surveys/my">Мои опросы</Link>
                  {/* <Link href="/surveys/unfinished">Незак. опросы</Link> */}
                  <Link href="/surveys/create">Создать опрос</Link>
                </>
                : ''
            }
          </div>

          <div className={classes.searchInput}>
            <SearchInput/>
          </div>
          
          {
            name ? 
            <>
              <Button onClick={handleClick}>
                {imgSrc ? 
                  <div style={{width: 48, height: 48, borderRadius: 16, borderWidth: 5, borderColor: "black"}}>
                    <img style={{width: 48, height: 48, borderRadius: 16, borderWidth: 5, borderColor: "black"}} src={MEDIA_URL + imgSrc} alt=''></img>
                  </div>
                  
                : <Avatar sx={{ width: 32, height: 32 }}>{name[0]}</Avatar>}
                <div className={classes.userName}>
                  {name}
                </div>
                <ArrowDropDownRoundedIcon className={`${classes.userDropdownIcon} ${anchorEl ? classes.open : ''}`}/>
                
              </Button>
              <Menu anchorEl={anchorEl} open={open} onClose={handleClose}>
                <MenuItem onClick={() => {navigate('/user');handleClose();}}>
                  <Avatar sx={{ width: 24, height: 24, marginRight: 1, background: theme.palette.primary.main }}/> Мой аккаунт
                </MenuItem> 
                <MenuItem onClick={() => {setEmailOpen(true); handleClose();}}><EmailIcon sx={{marginRight: 1}}/>Рассылка</MenuItem>
                <MenuItem onClick={handleSignOut}><Logout sx={{marginRight: 1}}/>Выйти</MenuItem>
              </Menu>
            </>
            
            :
            <div className={classes.authFragment}>
              <Link href="/signin">Войти</Link>
              <Button href="/signup" variant="contained">Зарегистрироваться</Button>
            </div>
          }
          
      </nav>
  );
}