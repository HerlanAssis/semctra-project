import request from '@/utils/request'

export function login(data) {
  return request({
    url: 'users/auth/login/',
    method: 'post',
    data
  })
}

export function getInfo(token) {
  const config = {
    headers: { Authorization: token }
  }

  return request({
    url: 'users/auth/info/',
    method: 'post',
    config
  })
}

export function logout() {
  return request({
    url: 'users/auth/logout/',
    method: 'post'
  })
}
