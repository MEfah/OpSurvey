export interface UserInfo {
  id: string;
  name: string;
  description?: string;
  imgSrc?: string;
}

export interface UserSignInInfo {
  email: string;
  password: string;
}

export interface UserSignUpInfo {
  email: string;
  password: string;
  name: string;
}

export interface UpdateUserInfo {
  name?: string;
  description?: string;
  imgSrc?: string;
}