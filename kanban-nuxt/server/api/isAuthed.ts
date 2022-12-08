export default defineEventHandler((event) => {
  return event.req.headers.cookie?.includes('sessionid');
})