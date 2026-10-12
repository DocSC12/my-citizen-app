<template>
  <view class="demo">
    <text class="title">{{ title }}</text>
    <button @click="count++">点了 {{ count }} 次</button>
  </view>
</template>

<script setup lang="ts">
import { ref } from 'vue'

// ref() 包装的变量是"响应式"的:值一变,界面自动跟着变
const title = ref('我的第一个小程序')
const count = ref(0)
</script>

<style scoped>
/* scoped:样式只作用于当前页面,不会污染别的页面 */
.demo { padding: 40rpx; }
.title { display: block; margin-bottom: 24rpx; font-size: 40rpx; font-weight: bold; }
</style>