import { AxiosError } from "axios";
import { getCookieId, Refresh } from "../APIs/UserAPI";


export async function initCookieId() {
  await getCookieId();
}


export async function CheckAuth() {
  let response = undefined;
  let error = false;
  try {
    response = await Refresh();
  } catch (e) {
    if (e instanceof AxiosError) {
      response = e.response;
      error = true;
    }
  }

  if (!error) {
    localStorage.setItem('access-token', response?.data.accessToken);
  }

  return !error;
}