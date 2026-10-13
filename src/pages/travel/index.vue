<template>
  <view class="demo">
    <text class="title">出行</text>
    <text class="info">onLoad:{{ loadCount }} 次 · onShow:{{ showCount }} 次</text>
    <text class="info">在 tab 间来回切,盯住上面两个数字</text>
  </view>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { onLoad, onShow } from '@dcloudio/uni-app'

definePage({
  style: {
    navigationBarTitleText: '出行',
  },
})

const loadCount = ref(0)
const showCount = ref(0)

onLoad(() => {
  loadCount.value++
  console.log('出行 onLoad 第', loadCount.value, '次')
})

onShow(() => {
  showCount.value++
  console.log('出行 onShow 第', showCount.value, '次')
})
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
</style>
