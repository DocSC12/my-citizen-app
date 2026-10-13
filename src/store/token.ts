import { defineStore } from 'pinia'
import { ref } from 'vue'

const ACCESS_KEY = 'my_app_access_token'
const REFRESH_KEY = 'my_app_refresh_token'

export const useTokenStore = defineStore('token', () => {
  // 启动时从 storage 恢复:内存会丢(app 重启),磁盘不会
  const accessToken = ref<string>(uni.getStorageSync(ACCESS_KEY) || '')
  const refreshToken = ref<string>(uni.getStorageSync(REFRESH_KEY) || '')

  function setTokenInfo(access: string, refresh: string) {
    accessToken.value = access
    refreshToken.value = refresh
    uni.setStorageSync(ACCESS_KEY, access)
    uni.setStorageSync(REFRESH_KEY, refresh)
  }

  function clearToken() {
    accessToken.value = ''
    refreshToken.value = ''
    uni.removeStorageSync(ACCESS_KEY)
    uni.removeStorageSync(REFRESH_KEY)
  }

  return { accessToken, refreshToken, setTokenInfo, clearToken }
})
