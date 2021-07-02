import request from '@/utils/request'

const baseUrl = 'schedule/event'

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

export function getDays() {
  return request({
    url: `${baseUrl}/week-day-options`,
    method: 'get'
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

export function remove(data) {
  return request({
    url: `${baseUrl}/${data.id}/`,
    method: 'delete'
  })
}
