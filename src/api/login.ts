import type { IAuthLoginRes, ICaptcha, IDoubleTokenRes, IUpdateInfo, IUpdatePassword, IUserInfoRes } from './types/login'
import { httpGet, httpPost } from '@/http/http'

/**
 * 登录表单
 */
export interface ILoginForm {
  username: string
  password: string
}

/**
 * 获取验证码
 * @returns ICaptcha 验证码
 */
export function getCode() {
  return httpGet<ICaptcha>('/user/getCode')
}

/**
 * 用户登录
 * @param loginForm 登录表单
 */
export function login(loginForm: ILoginForm) {
  return httpPost<IAuthLoginRes>('/auth/login', loginForm)
}

/**
 * 刷新token
 * @param refreshToken 刷新token
 */
export function refreshToken(refreshToken: string) {
  return httpPost<IDoubleTokenRes>('/auth/refreshToken', { refreshToken })
}

/**
 * 获取用户信息
 */
export function getUserInfo() {
  return httpGet<IUserInfoRes>('/user/info')
}

/**
 * 退出登录
 */
export function logout() {
  return httpGet<void>('/auth/logout')
}

/**
 * 修改用户信息
 */
export function updateInfo(data: IUpdateInfo) {
  return httpPost('/user/updateInfo', data)
}

/**
 * 修改用户密码
 */
export function updateUserPassword(data: IUpdatePassword) {
  return httpPost('/user/updatePassword', data)
}

/**
 * 获取微信登录凭证
 * @returns Promise 包含微信登录凭证(code)
 */
export function getWxCode() {
  return new Promise<UniApp.LoginRes>((resolve, reject) => {
    uni.login({
      provider: 'weixin',
      success: res => resolve(res),
      fail: err => reject(new Error(err)),
    })
  })
}

/**
 * 微信登录
 * @param params 微信登录参数，包含code
 * @returns Promise 包含登录结果
 */
export function wxLogin(data: { code: string }) {
  return httpPost<IAuthLoginRes>('/auth/wxLogin', data)
}
