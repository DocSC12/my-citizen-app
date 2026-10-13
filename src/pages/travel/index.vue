<template>
  <view class="page">
    <!-- 天气卡片(教学 mock,真实天气需要和风天气等三方 API) -->
    <view class="weather">
      <view class="weather-left">
        <text class="temp">18°</text>
        <view class="weather-desc">
          <text class="city">临汾 · 晴</text>
          <text class="air">空气质量 优 · 适宜出行</text>
        </view>
      </view>
      <text class="weather-icon">☀️</text>
    </view>

    <!-- 公交查询 -->
    <view class="card">
      <text class="card-title">公交查询</text>
      <view class="query">
        <input v-model="form.line" class="input" placeholder="输入线路,如:1路 / 10路" :maxlength="10">
        <button class="btn" type="primary" size="mini" :disabled="loading" @click="queryBus">
          {{ loading ? '查询中' : '查询' }}
        </button>
      </view>

      <view v-if="bus" class="bus">
        <view class="bus-head">
          <text class="bus-line">{{ bus.line }} 路</text>
          <text class="bus-direction">{{ bus.direction }}</text>
        </view>
        <view class="bus-row">
          <text class="bus-label">即将到站</text>
          <text class="bus-value">{{ bus.nextBuses.join(' / ') }}</text>
        </view>
        <view class="bus-row">
          <text class="bus-label">首末班</text>
          <text class="bus-value">{{ bus.firstBus }} - {{ bus.lastBus }}</text>
        </view>
        <view class="bus-row">
          <text class="bus-label">票价</text>
          <text class="bus-value">{{ bus.fare }}</text>
        </view>
        <view class="stations">
          <text v-for="(s, i) in bus.stations" :key="i" class="station">{{ s }}</text>
        </view>
      </view>
    </view>

    <!-- 出行提示 -->
    <view class="card">
      <text class="card-title">出行提示</text>
      <view v-for="t in tips" :key="t" class="tip-row">
        <text class="tip-dot">•</text>
        <text class="tip-text">{{ t }}</text>
      </view>
    </view>
  </view>
</template>

<script setup lang="ts">
import { reactive, ref } from 'vue'
import { httpGet } from '@/http/http'

definePage({
  style: { navigationBarTitleText: '出行' },
})

interface BusInfo {
  line: string
  direction: string
  nextBuses: string[]
  firstBus: string
  lastBus: string
  stations: string[]
  fare: string
}

const form = reactive({ line: '' })
const loading = ref(false)
const bus = ref<BusInfo | null>(null)

const tips = [
  '高峰时段(7:00-9:00 / 17:30-19:30)公交拥挤,请提前出门',
  '支持电子公交卡刷码乘车,享 9 折优惠',
  '夜间出行请选择正规出租车或网约车',
]

async function queryBus() {
  if (loading.value)
    return
  const line = form.line.trim()
  if (!line) {
    uni.showToast({ icon: 'none', title: '请输入公交线路' })
    return
  }
  loading.value = true
  try {
    bus.value = await httpGet<BusInfo>('/bus-line', { line })
  }
  catch {
    /* 失败提示 http 层已 toast */
  }
  finally {
    loading.value = false
  }
}
</script>

<style scoped>
.page {
  padding: 24rpx;
  padding-bottom: 140rpx;
}
.weather {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 32rpx;
  margin-bottom: 24rpx;
  border-radius: 24rpx;
  background: linear-gradient(135deg, #2563eb, #60a5fa);
}
.weather-left {
  display: flex;
  align-items: center;
}
.temp {
  margin-right: 20rpx;
  color: #fff;
  font-size: 80rpx;
  font-weight: bold;
}
.weather-desc {
  display: flex;
  flex-direction: column;
}
.city {
  color: #fff;
  font-size: 32rpx;
  font-weight: bold;
}
.air {
  margin-top: 8rpx;
  color: rgba(255, 255, 255, 0.85);
  font-size: 24rpx;
}
.weather-icon {
  font-size: 80rpx;
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
.query {
  display: flex;
  align-items: center;
}
.input {
  flex: 1;
  margin-right: 16rpx;
  padding: 16rpx 24rpx;
  border: 1rpx solid #e2e8f0;
  border-radius: 12rpx;
  background: #f8fafc;
  font-size: 28rpx;
}
.bus {
  margin-top: 24rpx;
}
.bus-head {
  display: flex;
  align-items: center;
  margin-bottom: 16rpx;
}
.bus-line {
  margin-right: 12rpx;
  padding: 4rpx 16rpx;
  border-radius: 8rpx;
  background: #018d71;
  color: #fff;
  font-size: 26rpx;
}
.bus-direction {
  font-size: 26rpx;
  color: #64748b;
}
.bus-row {
  display: flex;
  padding: 12rpx 0;
}
.bus-label {
  width: 140rpx;
  color: #94a3b8;
  font-size: 26rpx;
}
.bus-value {
  flex: 1;
  color: #334155;
  font-size: 26rpx;
}
.stations {
  display: flex;
  flex-wrap: wrap;
  margin-top: 12rpx;
}
.station {
  margin: 8rpx 8rpx 0 0;
  padding: 4rpx 16rpx;
  border-radius: 20rpx;
  background: #f1f5f9;
  color: #475569;
  font-size: 24rpx;
}
.tip-row {
  display: flex;
  padding: 8rpx 0;
}
.tip-dot {
  margin-right: 8rpx;
  color: #018d71;
}
.tip-text {
  flex: 1;
  color: #475569;
  font-size: 26rpx;
}
</style>
