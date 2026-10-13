<template>
  <view class="demo">
    <text class="title">双 token 实验台</text>
    <text class="info">昵称:{{ nickname || '(未获取)' }}</text>
    <text class="info">accessToken:{{ tokenStore.accessToken || '(无)' }}</text>
    <button class="mb" type="primary" @click="doLogin">
      1. 登录
    </button>
    <button class="mb" @click="fetchUserInfo">
      2. 获取用户信息
    </button>
    <button class="mb" @click="fetchUserInfo3">
      3. 并发获取三次(测刷新队列)
    </button>
    <button class="mb" @click="clearAll">
      清除全部 token
    </button>
  </view>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useTokenStore } from '@/store/token'
import { httpGet, httpPost } from '@/http/http'

definePage({ style: { navigationBarTitleText: '实验台' } })

const tokenStore = useTokenStore()
const nickname = ref('')

async function doLogin() {
  const data = await httpPost<{ accessToken: string, refreshToken: string }>('/login', {
    username: 'admin',
    password: '123456',
  })
  tokenStore.setTokenInfo(data.accessToken, data.refreshToken)
  uni.showToast({ title: '登录成功', icon: 'success' })
}

async function fetchUserInfo() {
  const data = await httpGet<{ nickname: string }>('/user-info')
  nickname.value = data.nickname
}

async function fetchUserInfo3() {
  const [a] = await Promise.all([
    httpGet<{ nickname: string }>('/user-info'),
    httpGet<{ nickname: string }>('/user-info'),
    httpGet<{ nickname: string }>('/user-info'),
  ])
  nickname.value = `${a.nickname}(3 个并发全成功)`
}

function clearAll() {
  tokenStore.clearToken()
  nickname.value = ''
}
</script>

<style scoped>
.demo {
  padding: 40rpx;
}
.title {
  display: block;
  margin-bottom: 16rpx;
  font-size: 40rpx;
  font-weight: bold;
}
.info {
  display: block;
  margin-bottom: 16rpx;
  font-size: 28rpx;
  color: #64748b;
}
.mb {
  margin-bottom: 24rpx;
}
</style>
