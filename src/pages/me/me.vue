<template>
  <view class="page">
    <!-- 用户卡片 -->
    <view class="user-card" @click="!isLogin && goLogin()">
      <view class="avatar">
        <text>{{ isLogin && userInfo ? userInfo.nickname[0] : '?' }}</text>
      </view>
      <view class="user-info">
        <template v-if="isLogin && userInfo">
          <text class="nickname">{{ userInfo.nickname }}</text>
          <text class="role">角色:{{ userInfo.role === 'admin' ? '管理员' : userInfo.role }}</text>
        </template>
        <template v-else-if="isLogin">
          <text class="nickname">加载中...</text>
          <text class="role">正在获取用户信息</text>
        </template>
        <template v-else>
          <text class="nickname">点击登录</text>
          <text class="role">登录后享受更多服务</text>
        </template>
      </view>
    </view>

    <!-- 我的服务 -->
    <view class="card">
      <text class="card-title">我的服务</text>
      <view class="grid">
        <view class="grid-item" @click="todo">
          <text class="grid-icon">📅</text>
          <text class="grid-text">我的预约</text>
        </view>
        <view class="grid-item" @click="todo">
          <text class="grid-icon">🧾</text>
          <text class="grid-text">我的缴费</text>
        </view>
        <view class="grid-item" @click="todo">
          <text class="grid-icon">🪪</text>
          <text class="grid-text">我的证照</text>
        </view>
        <view class="grid-item" @click="todo">
          <text class="grid-icon">📝</text>
          <text class="grid-text">我的诉求</text>
        </view>
      </view>
    </view>

    <!-- 通用菜单 -->
    <view class="card">
      <view class="menu" @click="goAbout">
        <text class="menu-text">关于应用</text>
        <text class="menu-arrow">›</text>
      </view>
      <view class="menu" @click="todo">
        <text class="menu-text">隐私政策</text>
        <text class="menu-arrow">›</text>
      </view>
      <view v-if="isLogin" class="menu" @click="logout">
        <text class="menu-text logout">退出登录</text>
        <text class="menu-arrow">›</text>
      </view>
    </view>
  </view>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'
import { onShow } from '@dcloudio/uni-app'
import { useTokenStore } from '@/store/token'
import { httpGet } from '@/http/http'

definePage({
  style: { navigationBarTitleText: '我的' },
})

const tokenStore = useTokenStore()
const userInfo = ref<{ nickname: string, role: string } | null>(null)
const isLogin = computed(() => !!tokenStore.accessToken)

// tab 页 onLoad 终身只触发一次,onShow 每次切回来都触发
// 登录返回/退出后都要刷新展示 → 放 onShow
onShow(() => {
  if (isLogin.value && !userInfo.value)
    fetchUserInfo()
})

async function fetchUserInfo() {
  try {
    userInfo.value = await httpGet<{ nickname: string, role: string }>('/user-info')
  }
  catch {
    /* token 失效等情况 http 层已处理 */
  }
}

function goLogin() {
  uni.navigateTo({ url: '/pages/login/index' })
}

function logout() {
  uni.showModal({
    title: '提示',
    content: '确定退出登录吗?',
    success: (res) => {
      if (res.confirm) {
        tokenStore.clearToken()
        userInfo.value = null
        uni.showToast({ title: '已退出', icon: 'none' })
      }
    },
  })
}

function goAbout() {
  uni.navigateTo({ url: '/pages/about/about' })
}

function todo() {
  uni.showToast({ icon: 'none', title: '敬请期待' })
}
</script>

<style scoped>
.page {
  padding: 24rpx;
  padding-bottom: 140rpx;
}
.user-card {
  display: flex;
  align-items: center;
  padding: 40rpx 32rpx;
  margin-bottom: 24rpx;
  border-radius: 24rpx;
  background: linear-gradient(135deg, #018d71, #34d399);
}
.avatar {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 110rpx;
  height: 110rpx;
  margin-right: 24rpx;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.3);
  color: #fff;
  font-size: 48rpx;
  font-weight: bold;
}
.user-info {
  flex: 1;
}
.nickname {
  display: block;
  color: #fff;
  font-size: 36rpx;
  font-weight: bold;
}
.role {
  display: block;
  margin-top: 8rpx;
  color: rgba(255, 255, 255, 0.85);
  font-size: 24rpx;
}
.card {
  margin-bottom: 24rpx;
  padding: 24rpx;
  border-radius: 20rpx;
  background: #fff;
}
.card-title {
  display: block;
  margin-bottom: 20rpx;
  font-size: 32rpx;
  font-weight: bold;
}
.grid {
  display: flex;
  flex-wrap: wrap;
}
.grid-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 25%;
  margin-bottom: 20rpx;
}
.grid-icon {
  margin-bottom: 8rpx;
  font-size: 48rpx;
}
.grid-text {
  font-size: 26rpx;
  color: #334155;
}
.menu {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 24rpx 0;
  border-bottom: 1rpx solid #f1f5f9;
}
.menu:last-child {
  border-bottom: none;
}
.menu-text {
  font-size: 28rpx;
  color: #334155;
}
.menu-text.logout {
  color: #ef4444;
}
.menu-arrow {
  color: #cbd5e1;
  font-size: 32rpx;
}
</style>
