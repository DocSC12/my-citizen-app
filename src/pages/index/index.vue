<template>
  <view class="page">
    <!-- 顶部:城市 + 搜索入口 -->
    <view class="header">
      <text class="city">📍 临汾</text>
      <view class="search" @click="goAllServices">
        <text class="search-text">🔍 搜索服务 / 事项 / 公告</text>
      </view>
    </view>

    <!-- 轮播图 -->
    <swiper class="banner" indicator-dots circular autoplay :interval="4000">
      <swiper-item v-for="b in banners" :key="b.id">
        <view class="banner-item" :style="{ background: b.bg }">
          <text class="banner-title">{{ b.title }}</text>
          <text class="banner-sub">{{ b.sub }}</text>
        </view>
      </swiper-item>
    </swiper>

    <!-- 服务宫格 -->
    <view class="card">
      <view class="card-head">
        <text class="card-title">便民服务</text>
        <text class="card-more" @click="goAllServices">全部 ›</text>
      </view>
      <view class="grid">
        <view v-for="s in services" :key="s.id" class="grid-item" @click="goDetail(s.id)">
          <text class="grid-icon">{{ s.icon }}</text>
          <text class="grid-text">{{ s.title }}</text>
        </view>
      </view>
      <view v-if="!services.length" class="empty">
        <text>服务加载失败:请先启动后端(uvicorn main:app --port 8000)</text>
      </view>
    </view>

    <!-- 政务公告 -->
    <view class="card">
      <text class="card-title">政务公告</text>
      <view v-for="a in announcements" :key="a.id" class="notice" @click="onNotice(a)">
        <text class="notice-tag">公告</text>
        <text class="notice-title">{{ a.title }}</text>
        <text class="notice-date">{{ a.date }}</text>
      </view>
      <view v-if="!announcements.length" class="empty">
        <text>公告加载失败:请先启动后端</text>
      </view>
    </view>
  </view>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { onLoad } from '@dcloudio/uni-app'
import { httpGet } from '@/http/http'

definePage({
  style: { navigationBarTitleText: '首页' },
})

interface ServiceItem { id: number, title: string, icon: string, category: string, desc: string }
interface Announcement { id: number, title: string, date: string }

// 轮播是纯展示内容,本地写死即可,不必每次从后端拉
const banners = [
  { id: 1, title: '指尖办事', sub: '800+ 事项掌上办', bg: 'linear-gradient(135deg, #018d71, #34d399)' },
  { id: 2, title: '电子证照', sub: '一部手机走全城', bg: 'linear-gradient(135deg, #2563eb, #60a5fa)' },
  { id: 3, title: '生活缴费', sub: '水电气暖一站搞定', bg: 'linear-gradient(135deg, #b45309, #fbbf24)' },
]

const services = ref<ServiceItem[]>([])
const announcements = ref<Announcement[]>([])

// 公开接口不需要登录;数据放 onLoad 而不是 onShow,避免每次切 tab 都重新请求
onLoad(async () => {
  try {
    services.value = await httpGet<ServiceItem[]>('/services')
  }
  catch { /* 失败提示 http 层已 toast,保留空列表触发空状态 */ }
  try {
    announcements.value = await httpGet<Announcement[]>('/announcements')
  }
  catch { /* 同上 */ }
})

function goAllServices() {
  uni.navigateTo({ url: '/pages/services/index' })
}

function goDetail(id: number) {
  uni.navigateTo({ url: `/pages/detail/index?id=${id}` })
}

function onNotice(a: Announcement) {
  uni.showToast({ icon: 'none', title: a.title })
}
</script>

<style scoped>
.page {
  padding: 24rpx;
  /* 给底部自定义 tabbar 留空间 */
  padding-bottom: 140rpx;
}
.header {
  display: flex;
  align-items: center;
  margin-bottom: 24rpx;
}
.city {
  margin-right: 20rpx;
  font-size: 32rpx;
  font-weight: bold;
}
.search {
  flex: 1;
  padding: 16rpx 24rpx;
  border-radius: 40rpx;
  background: #f1f5f9;
}
.search-text {
  font-size: 26rpx;
  color: #94a3b8;
}
.banner {
  height: 220rpx;
  border-radius: 20rpx;
  overflow: hidden;
  margin-bottom: 24rpx;
}
.banner-item {
  display: flex;
  flex-direction: column;
  justify-content: center;
  height: 100%;
  padding-left: 40rpx;
  color: #fff;
}
.banner-title {
  font-size: 40rpx;
  font-weight: bold;
}
.banner-sub {
  margin-top: 8rpx;
  font-size: 26rpx;
  opacity: 0.9;
}
.card {
  margin-bottom: 24rpx;
  padding: 24rpx;
  border-radius: 20rpx;
  background: #fff;
}
.card-head {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.card-title {
  display: block;
  margin-bottom: 20rpx;
  font-size: 32rpx;
  font-weight: bold;
}
.card-more {
  font-size: 26rpx;
  color: #94a3b8;
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
  margin-bottom: 28rpx;
}
.grid-icon {
  margin-bottom: 8rpx;
  font-size: 52rpx;
}
.grid-text {
  font-size: 26rpx;
  color: #334155;
}
.empty {
  padding: 20rpx 0;
}
.empty text {
  font-size: 24rpx;
  color: #94a3b8;
}
.notice {
  display: flex;
  align-items: center;
  padding: 16rpx 0;
  border-bottom: 1rpx solid #f1f5f9;
}
.notice:last-child {
  border-bottom: none;
}
.notice-tag {
  flex-shrink: 0;
  margin-right: 12rpx;
  padding: 2rpx 12rpx;
  border-radius: 8rpx;
  background: #ecfdf5;
  color: #018d71;
  font-size: 20rpx;
}
.notice-title {
  flex: 1;
  overflow: hidden;
  white-space: nowrap;
  text-overflow: ellipsis;
  font-size: 28rpx;
  color: #334155;
}
.notice-date {
  flex-shrink: 0;
  margin-left: 12rpx;
  font-size: 24rpx;
  color: #94a3b8;
}
</style>
