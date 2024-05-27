import { AxiosError, AxiosResponse } from "axios";
import { useState } from "react";

export function useFetch<T>(callback: (arg?: T) => Promise<AxiosResponse<any, any>>): [(arg?: T) => Promise<[AxiosResponse<any, any> | undefined, boolean]>, boolean] {
  const [isFetching, setIsFetching] = useState(false);
  const [response, setResponse] = useState<AxiosResponse<any, any> | undefined>();

  async function fetch(arg?: T): Promise<[AxiosResponse<any, any> | undefined, boolean]> {
    let response = undefined;
    let error = false; 
    try {
      setIsFetching(true);
      response = await callback(arg);
      setResponse(response);
    } catch (e) {
      error = true;
      if (e instanceof AxiosError) {
        response = e.response;
        setResponse(response);
      }
    } finally {
      setIsFetching(false);
    }
    return [response, error];
  }

  return [fetch, isFetching];
}