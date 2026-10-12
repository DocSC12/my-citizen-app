<template>
  <view class="demo">
    <text class="title">详情页</text>
    <text class="info">收到参数 id:{{ id }}</text>
    <button @click="goHome">
      reLaunch:清空页面栈,逃回首页
    </button>
  </view>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { onLoad } from '@dcloudio/uni-app'

// definePage:本页面的路由配置(unibest 特色,自动进 pages.json)
definePage({
  style: {
    navigationBarTitleText: '详情页',
  },
})

const id = ref('未收到')

// onLoad:页面加载时触发一次,options 就是跳转链接里 ? 后面的参数
onLoad((options) => {
  id.value = String(options?.id ?? '未传')
  console.log('onLoad 触发,收到的参数:', options)
})

function goHome() {
  uni.reLaunch({ url: '/pages/index/index' })
}
</script>

<style scoped>
.demo {
  padding: 40rpx;
}
.title {
  display: block;
  margin-bottom: 24rpx;
  font-size: 40rpx;
  font-weight: bold;
}
.info {
  display: block;
  margin-bottom: 40rpx;
  font-size: 30rpx;
  color: #64748b;
}
</style>
