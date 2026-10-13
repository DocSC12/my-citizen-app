<template>
  <view class="page">
    <view v-if="detail" class="wrap">
      <!-- 服务头部 -->
      <view class="head">
        <text class="head-icon">{{ detail.icon }}</text>
        <view class="head-body">
          <text class="head-title">{{ detail.title }}</text>
          <text class="head-desc">{{ detail.desc }}</text>
        </view>
      </view>

      <!-- 办理材料 -->
      <view class="card">
        <text class="card-title">所需材料</text>
        <view v-for="m in detail.materials" :key="m" class="line">
          <text class="line-dot">•</text>
          <text class="line-text">{{ m }}</text>
        </view>
      </view>

      <!-- 办理流程 -->
      <view class="card">
        <text class="card-title">办理流程</text>
        <view v-for="(step, i) in detail.steps" :key="step" class="step">
          <view class="step-no">
            <text>{{ i + 1 }}</text>
          </view>
          <text class="step-text">{{ step }}</text>
        </view>
      </view>

      <!-- 咨询热线 -->
      <view class="card hotline" @click="call(detail.hotline)">
        <text class="card-title">咨询热线</text>
        <text class="hotline-text">📞 {{ detail.hotline }}</text>
      </view>

      <button class="btn" type="primary" @click="apply">
        开始办理
      </button>
    </view>
    <view v-else class="empty">
      <text>加载中...</text>
    </view>
  </view>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { onLoad } from '@dcloudio/uni-app'
import { httpGet } from '@/http/http'

definePage({
  style: { navigationBarTitleText: '服务详情' },
})

interface ServiceDetail {
  id: number
  title: string
  icon: string
  desc: string
  steps: string[]
  materials: string[]
  hotline: string
}

const detail = ref<ServiceDetail | null>(null)

onLoad(async (options) => {
  const id = Number(options?.id ?? 0)
  try {
    detail.value = await httpGet<ServiceDetail>('/service-detail', { id })
  }
  catch {
    /* 失败提示 http 层已 toast */
  }
})

function call(hotline: string) {
  // 拨打电话:小程序原生能力,无需任何权限声明
  uni.makePhoneCall({
    phoneNumber: hotline,
    fail: () => {},
  })
}

function apply() {
  uni.showToast({ icon: 'none', title: '教学演示:办理流程待接入' })
}
</script>

<style scoped>
.page {
  padding: 24rpx;
}
.wrap {
  padding-bottom: 60rpx;
}
.head {
  display: flex;
  align-items: center;
  padding: 32rpx;
  margin-bottom: 24rpx;
  border-radius: 24rpx;
  background: linear-gradient(135deg, #018d71, #34d399);
}
.head-icon {
  margin-right: 24rpx;
  font-size: 72rpx;
}
.head-body {
  flex: 1;
}
.head-title {
  display: block;
  color: #fff;
  font-size: 38rpx;
  font-weight: bold;
}
.head-desc {
  display: block;
  margin-top: 8rpx;
  color: rgba(255, 255, 255, 0.85);
  font-size: 26rpx;
}
.card {
  margin-bottom: 24rpx;
  padding: 24rpx;
  border-radius: 20rpx;
  background: #fff;
}
.card-title {
  display: block;
  margin-bottom: 16rpx;
  font-size: 30rpx;
  font-weight: bold;
}
.line {
  display: flex;
  padding: 8rpx 0;
}
.line-dot {
  margin-right: 12rpx;
  color: #018d71;
}
.line-text {
  font-size: 28rpx;
  color: #475569;
}
.step {
  display: flex;
  align-items: center;
  padding: 12rpx 0;
}
.step-no {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 44rpx;
  height: 44rpx;
  margin-right: 16rpx;
  border-radius: 50%;
  background: #ecfdf5;
  color: #018d71;
  font-size: 26rpx;
  font-weight: bold;
}
.step-text {
  font-size: 28rpx;
  color: #475569;
}
.hotline {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.hotline .card-title {
  margin-bottom: 0;
}
.hotline-text {
  font-size: 32rpx;
  color: #018d71;
  font-weight: bold;
}
.btn {
  margin-top: 16rpx;
}
.empty {
  padding: 100rpx 0;
  text-align: center;
}
.empty text {
  font-size: 26rpx;
  color: #94a3b8;
}
</style>
