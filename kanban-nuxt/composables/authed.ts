import { useMyFetch } from "./myFetch"
import type { FetchError } from 'ohmyfetch';
import type { FetchOptions } from 'ohmyfetch';

export const useAuthedFetch = (name: string, url: string, opts?: FetchOptions) => {
  const headers = useRequestHeaders(['cookie']);
  const baseURL = 'http://127.0.0.1:8000/api/';

  return useAsyncData(name, () => {
    return $fetch(url, {
      baseURL,
      credentials: 'include',
      headers: {
        Cookie: headers.cookie!
      },
      ...(opts && {...opts})
    })
  }).catch((error: FetchError) => {
    // Check if error is Unauthed
    if (error.statusCode === 401) {
      // Retry the request
      return useAsyncData(name, () => {
        return $fetch(url, {
          credentials: 'include',
          ...(opts && { ...opts }),
          async onResponseError({ response }) {
            // Intercept when the refresh token has expired
            if (response.status === 401) {
              console.log('You are logged out');
              // Push to Login page
              
              // Set the user to none
            }
          }
        })
      })
    }
  })
}
