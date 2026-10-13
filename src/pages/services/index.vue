<template>
  <view class="page">
    <view v-for="s in services" :key="s.id" class="item" @click="goDetail(s.id)">
      <text class="item-icon">{{ s.icon }}</text>
      <view class="item-body">
        <text class="item-title">{{ s.title }}</text>
        <text class="item-desc">{{ s.desc }}</text>
      </view>
      <text class="item-arrow">›</text>
    </view>
    <view v-if="!services.length" class="empty">
      <text>暂无服务:请先启动后端</text>
    </view>
  </view>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { onLoad } from '@dcloudio/uni-app'
import { httpGet } from '@/http/http'

definePage({
  style: { navigationBarTitleText: '全部服务' },
})

interface ServiceItem { id: number, title: string, icon: string, category: string, desc: string }

const services = ref<ServiceItem[]>([])

// onLoad 的 options 就是 URL query 参数,可带分类进来过滤
onLoad(async (options) => {
  const category = String(options?.category ?? '')
  const title = String(options?.title ?? '')
  // 导航栏标题是编译期配置(definePage),运行期动态改用 setNavigationBarTitle
  if (title)
    uni.setNavigationBarTitle({ title })
  try {
    services.value = await httpGet<ServiceItem[]>('/services', category ? { category } : undefined)
  }
  catch {
    /* 失败提示 http 层已 toast */
  }
})

function goDetail(id: number) {
  uni.navigateTo({ url: `/pages/detail/index?id=${id}` })
}
</script>

<style scoped>
.page {
  padding: 24rpx;
}
.item {
  display: flex;
  align-items: center;
  margin-bottom: 20rpx;
  padding: 28rpx;
  border-radius: 20rpx;
  background: #fff;
}
.item-icon {
  margin-right: 20rpx;
  font-size: 56rpx;
}
.item-body {
  flex: 1;
}
.item-title {
  display: block;
  font-size: 30rpx;
  font-weight: bold;
  color: #1e293b;
}
.item-desc {
  display: block;
  margin-top: 8rpx;
  font-size: 24rpx;
  color: #94a3b8;
}
.item-arrow {
  color: #cbd5e1;
  font-size: 36rpx;
}
.empty {
  padding: 60rpx 0;
  text-align: center;
}
.empty text {
  font-size: 26rpx;
  color: #94a3b8;
}
</style>
