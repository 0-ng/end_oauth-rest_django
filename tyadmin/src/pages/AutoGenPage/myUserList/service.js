import request from 'umi-request';

import { buildFileFormData } from '@/utils/utils'
export async function querymyUser(params) {
  return request('/api/xadmin/v1/my_user', {
    params,
  });
}
export async function removemyUser(params) {
  return request(`/api/xadmin/v1/my_user/${params}`, {
    method: 'DELETE',
  });
}
export async function addmyUser(params) {
  let fileFieldList = []
  let fileData = buildFileFormData(params, fileFieldList);
  return request('/api/xadmin/v1/my_user', {
    method: 'POST',
    data: fileData,
  });
}
export async function updatemyUser(params, id) {
  let fileFieldList = []
  let fileData = buildFileFormData(params, fileFieldList);
  return request(`/api/xadmin/v1/my_user/${id}`, {
    method: 'PUT',
    data: fileData,
  });
}
export async function querymyUserVerboseName(params) {
  return request('/api/xadmin/v1/my_user/verbose_name', {
    params,
  });
}
export async function querymyUserListDisplay(params) {
  return request('/api/xadmin/v1/my_user/list_display', {
    params,
  });
}
export async function querymyUserDisplayOrder(params) {
  return request('/api/xadmin/v1/my_user/display_order', {
    params,
  });
}


