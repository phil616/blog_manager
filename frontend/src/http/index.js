import axios from 'axios';

// Get token from session storage
function getToken(name) {
  return sessionStorage.getItem(name);
}

let api_prefix = process.env.VUE_APP_API || undefined;

let baseURL = null;
if (api_prefix){
  baseURL = api_prefix + "/api";
}else{
  baseURL = "/api";
}
const service = axios.create({
  baseURL: baseURL,
  withCredentials: false,  // This is required to handle cookies
});

service.baseURL = baseURL;


// Request Interceptor
// do something before request is sent
service.interceptors.request.use(
  config => {

    // get token from cookie
    const token = getToken('token');
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`;
    }
    return config;
  },
  error => {
    // do something with request error
    return Promise.reject(error);
  }
);

// response Interceptor
service.interceptors.response.use(
  response => {
    // do something with response data before return to the component
    return response;
  },
  error => {
    // do something with response error
    return Promise.reject(error);
  }
);

export default service;

