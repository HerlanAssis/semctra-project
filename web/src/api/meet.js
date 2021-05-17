import request from '@/utils/request'

const baseUrl = 'telehealth/meet'

export function get(data) {
  return request({
    url: `${baseUrl}/${data.id}`,
    method: 'get'
  })
}

export function getList() {
  return request({
    url: `${baseUrl}/`,
    method: 'get'
  })
}

export function accept(data) {
  return request({
    url: `${baseUrl}/accept/`,
    method: 'post',
    data
  })
}

export function save(data) {
  return data?.id
    ? request({
        url: `${baseUrl}/${data.id}/`,
        method: 'patch',
        data
      })
    : request({
        url: `${baseUrl}/`,
        method: 'post',
        data
      })
}
