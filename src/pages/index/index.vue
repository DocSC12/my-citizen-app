<template>
  <view class="demo">
    <text class="title">{{ title }}</text>
    <text class="info">onShow 已触发:{{ showCount }} 次</text>
    <button class="mb" @click="count++">
      点了 {{ count }} 次
    </button>

    <button class="mb" type="primary" @click="goDetail">
      navigateTo:进详情页(能返回)
    </button>
    <button class="mb" type="warn" @click="goRedirect">
      redirectTo:替换当前页(回不来)
    </button>
    <button class="mb" @click="showStack">
      打印页面栈(看控制台)
    </button>
  </view>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { onShow } from '@dcloudio/uni-app'

const title = ref('我的第一个小程序')
const count = ref(0)
const showCount = ref(0)

// onShow:每次页面"变得可见"都触发——包括从详情页返回来
onShow(() => {
  showCount.value++
  console.log('首页 onShow 第', showCount.value, '次')
})

function goDetail() {
  uni.navigateTo({ url: '/pages/detail/index?id=42' })
  // 跳转是异步的,半秒后打印,能"抓拍"到栈变长
  setTimeout(() => {
    console.log('跳转后页面栈:', getCurrentPages().map(p => p.route))
  }, 500)
}

function goRedirect() {
  uni.redirectTo({ url: '/pages/detail/index?id=99' })
}

function showStack() {
  const stack = getCurrentPages()
  console.log('当前页面栈:', stack.map(p => p.route))
  uni.showToast({ title: `栈长度 ${stack.length}`, icon: 'none' })
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
  margin-bottom: 40rpx;
  font-size: 28rpx;
  color: #64748b;
}
.mb {
  margin-bottom: 24rpx;
}
</style>
