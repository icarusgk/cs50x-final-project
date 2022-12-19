import type { FetchOptions } from 'ohmyfetch';

export const useMyFetch = (url: string, opts?: FetchOptions) => {
  

  return $fetch(url, {
    baseURL: 'http://127.0.0.1:8000/api/',
    headers: {
      'Content-Type': 'application/json'
    },
    ...(opts && { ...opts })
  });
}
