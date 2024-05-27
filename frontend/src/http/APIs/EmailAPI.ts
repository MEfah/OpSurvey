import { apiAuth } from '../api';


export async function sendEmails(text: string, to: string[]) {
  return await apiAuth.post(`/mail/`, {text, to});
}