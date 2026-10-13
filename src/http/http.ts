import { useTokenStore } from '@/store/token'

interface IResponse<T> { code: number, msg: string, data: T }
type MyOptions = UniNamespace.RequestOptions & { __retried?: boolean }

const BASE_URL = 'http://127.0.0.1:8000'
const TIMEOUT = 10000

/* ---------- 无感刷新的三个全局状态(整个 app 共享一份) ---------- */
let refreshing = false // 正在刷新中?
// eslint-disable-next-line ts/no-unsafe-function-type
let taskQueue: { resolve: Function, reject: Function, options: MyOptions }[] = [] // 挂起等待重放的请求

/** 刷新 accessToken —— 注意:故意用裸 uni.request 而不用 http() */
function refreshAccessToken(store: ReturnType<typeof useTokenStore>) {
  return new Promise<string>((resolve, reject) => {
    uni.request({
      url: `${BASE_URL}/refresh-token`,
      method: 'POST',
      // 刷新只带 refreshToken,不带过期的 accessToken
      header: { Authorization: `Bearer ${store.refreshToken}` },
      success: (res) => {
        const body = res.data as IResponse<{ accessToken: string }>
        if (res.statusCode === 200 && body.code === 0)
          resolve(body.data.accessToken)
        else reject(res)
      },
      fail: reject,
    })
  })
}

export function http<T>(options: MyOptions) {
  return new Promise<T>((resolve, reject) => {
    const store = useTokenStore()

    uni.request({
      ...options,
      url: BASE_URL + options.url,
      timeout: TIMEOUT,
      header: {
        ...(options.header || {}),
        // 拦截器思想:token 统一注入,调用处零成本
        Authorization: `Bearer ${store.accessToken}`,
      },
      success: async (res) => {
        // ---------- 401 分支:无感刷新的战场 ----------
        if (res.statusCode === 401) {
          // 保险丝:刷新后的重放如果还 401,说明 token 被吊销,停止循环
          if (options.__retried || !store.refreshToken) {
            store.clearToken()
            uni.showToast({ icon: 'none', title: '登录已过期,请重新登录' })
            return reject(res)
          }
          // 1. 把自己挂起进队列(不 reject,让调用方安静等待)
          taskQueue.push({ resolve, reject, options })
          // 2. 只允许第一个撞上 401 的请求去刷新,后来的只排队
          if (!refreshing) {
            refreshing = true
            try {
              const newToken = await refreshAccessToken(store)
              store.setTokenInfo(newToken, store.refreshToken)
              // 3. 刷新成功:重放队列,并用 __retried 标记防止无限循环
              const tasks = [...taskQueue]
              taskQueue = []
              tasks.forEach(t => t.resolve(http<T>({ ...t.options, __retried: true })))
            }
            catch {
              // 4. 刷新也失败: refreshToken 也失效了,真正掉登录
              store.clearToken()
              uni.showToast({ icon: 'none', title: '登录已过期,请重新登录' })
              taskQueue.forEach(t => t.reject())
              taskQueue = []
            }
            finally {
              refreshing = false
            }
          }
          return
        }
        // ---------- 正常分支 ----------
        const body = res.data as IResponse<T>
        if (res.statusCode === 200 && body.code === 0) {
          resolve(body.data)
        }
        else {
          uni.showToast({ icon: 'none', title: body?.msg || (body as any)?.detail?.[0]?.msg || '请求失败' })
          reject(body)
        }
      },
      fail: (err) => {
        uni.showToast({ icon: 'none', title: '网络错误' })
        reject(err)
      },
    })
  })
}

export function httpGet<T>(url: string, query?: Record<string, any>) {
  return http<T>({ url, method: 'GET', data: query })
}

export function httpPost<T>(url: string, data?: Record<string, any>) {
  return http<T>({ url, data, method: 'POST' })
}
