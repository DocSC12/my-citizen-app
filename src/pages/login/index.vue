<template>
  <view class="page">
    <view class="logo-card">
      <text class="logo">🏛️</text>
      <text class="app-name">临汾公众服务</text>
      <text class="app-sub">一站式城市服务平台</text>
    </view>

    <view class="form-card">
      <view class="field">
        <text class="label">用户名</text>
        <input v-model="form.username" class="input" placeholder="3-20 个字符" :maxlength="20">
      </view>
      <view class="field">
        <text class="label">密码</text>
        <input v-model="form.password" class="input" password placeholder="6-20 个字符" :maxlength="20">
      </view>
      <button class="btn" type="primary" :loading="loading" :disabled="loading" @click="doLogin">
        {{ loading ? '登录中...' : '登 录' }}
      </button>
      <text class="tip">测试账号:admin / 123456</text>
    </view>
  </view>
</template>

<script setup lang="ts">
import { reactive, ref } from 'vue'
import { useTokenStore } from '@/store/token'
import { httpPost } from '@/http/http'

definePage({
  style: { navigationBarTitleText: '登录' },
})

const tokenStore = useTokenStore()
const form = reactive({ username: '', password: '' })
// 防连点锁:请求进行中再点也发不出第二次请求
const loading = ref(false)

async function doLogin() {
  if (loading.value)
    return

  // 前端校验是"体验",后端校验才是"安全"——两端都要有
  if (form.username.trim().length < 3) {
    uni.showToast({ icon: 'none', title: '用户名至少 3 个字符' })
    return
  }
  if (form.password.length < 6) {
    uni.showToast({ icon: 'none', title: '密码至少 6 位' })
    return
  }

  loading.value = true
  try {
    const data = await httpPost<{ accessToken: string, refreshToken: string }>('/login', {
      username: form.username.trim(),
      password: form.password,
    })
    tokenStore.setTokenInfo(data.accessToken, data.refreshToken)
    uni.showToast({ title: '登录成功', icon: 'success' })
    setTimeout(backToList, 600)
  }
  catch {
    // 失败提示(密码错/锁定/422)http 层已统一 toast,这里只负责收尾
  }
  finally {
    loading.value = false
  }
}

// 返回策略:有上级页就返回(触发上级页 onShow 刷新);没有就去首页
function backToList() {
  const pages = getCurrentPages()
  if (pages.length > 1)
    uni.navigateBack()
  else
    uni.switchTab({ url: '/pages/index/index' })
}
</script>

<style scoped>
.page {
  padding: 40rpx;
}
.logo-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin: 40rpx 0 60rpx;
}
.logo {
  font-size: 100rpx;
}
.app-name {
  margin-top: 16rpx;
  font-size: 40rpx;
  font-weight: bold;
}
.app-sub {
  margin-top: 8rpx;
  font-size: 26rpx;
  color: #94a3b8;
}
.form-card {
  padding: 40rpx 32rpx;
  border-radius: 24rpx;
  background: #fff;
}
.field {
  margin-bottom: 32rpx;
}
.label {
  display: block;
  margin-bottom: 12rpx;
  font-size: 28rpx;
  color: #334155;
}
.input {
  padding: 20rpx 24rpx;
  border: 1rpx solid #e2e8f0;
  border-radius: 16rpx;
  background: #f8fafc;
}
.btn {
  margin-top: 16rpx;
}
.tip {
  display: block;
  margin-top: 24rpx;
  text-align: center;
  font-size: 24rpx;
  color: #94a3b8;
}
</style>
