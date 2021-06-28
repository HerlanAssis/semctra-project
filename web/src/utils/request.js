import axios from 'axios'
// import { MessageBox, Message } from 'element-ui'
import { Message } from 'element-ui'
import store from '@/store'
import { getToken } from '@/utils/auth'

// create an axios instance
const service = axios.create({
  baseURL: process.env.VUE_APP_API_BASE_URL
})

// request interceptor
service.interceptors.request.use(
  config => {
    // do something before request is sent

    if (store.getters.token) {
      // let each request carry token
      // ['X-Token'] is a custom headers key
      // please modify it according to the actual situation
      config.headers.common['Authorization'] = getToken()
    }
    return config
  },
  error => {
    // do something with request error
    console.log(error) // for debug
    return Promise.reject(error)
  }
)

// response interceptor
service.interceptors.response.use(
  response => {
    const res = response
    if (res?.data?.detail) {
      Message({
        message: res?.data?.detail,
        type: 'success',
        duration: 5 * 1000
      })
    }

    return res
  },
  error => {
    console.log('err' + error) // for debug
    Message({
      message: error?.response?.data?.detail || error.message,
      type: 'error',
      duration: 5 * 1000
    })
    return Promise.reject(error)
  })

export default service
