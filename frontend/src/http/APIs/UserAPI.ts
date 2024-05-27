import { SignUpInfo, SignInInfo } from '../../schemas/AuthInfo';
import { UpdateUserInfo } from "../../schemas/UserInfo";
import { api, apiAuth } from '../api';

export async function GetUsers() {
  return await api.post(`/users/all`);
}

export async function CheckEmail(email: string) {
  return await api.get(`/users/checkemail`, {
    params: {
      email: email
    }
  })
}

export async function SignUp(signUpInfo: SignUpInfo) {
  return await api.post(`/auth/signup`, signUpInfo);
}

export async function SignIn(signInInfo: SignInInfo) {
  return await api.post(`/auth/signin`, signInInfo);
}

export async function UpdateUser(userId: string, updateUserInfo: UpdateUserInfo, formData?: FormData) {
  formData?.append('update_user_info', JSON.stringify(updateUserInfo));
  return await apiAuth.patch(`/users/${userId}`, formData, {
    headers: {
        'content-type': 'multipart/form-data'
    }});
}

export async function SignOut() {
  return await apiAuth.post(`/auth/signout`);
}

export async function Refresh() {
  return await api.get(`/auth/refresh`);
}

export async function getCookieId() {
  return await api.get(`/auth/cookieid`);
}