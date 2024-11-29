<template>
  <view class="container">
    <!-- 顶部导航栏 -->
    <view class="navbar">
      <view class="back-button" @click="goBack">＜</view>
      <text class="title">添加行李</text>
    </view>

    <!-- 搜索框 -->
    <view class="search-bar">
      <input class="search-input" placeholder="输入物品名称..." />
    </view>

    <!-- 常用物品分类 -->
    <view class="category-section">
      <text class="section-title">常用物品</text>
      <view class="category-tabs">
        <view 
          class="tab" 
          v-for="(category, index) in categories" 
          :key="index" 
          :class="{ active: currentCategory === index }" 
          @click="selectCategory(index)"
        >
          {{ category.title }}
        </view>
      </view>
    </view>

    <!-- 物品列表 -->
    <view class="item-list">
      <view class="item" v-for="item in currentCategoryItems" :key="item.id">
        <text>{{ item.name }}</text>
        <view class="add-icon" v-if="item.showAddIcon" @click="addItem(item)">＋</view>
        <view v-if="item.completed">已添加</view>
      </view>
    </view>

    <!-- 保存按钮 -->
   <button class="save-button" @click="saveAndNavigate">保存</button>
  </view>
</template>

<script>
export default {
  data() {
    return {
      token: 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoyMDQ3NjQ5MDI0LCJpYXQiOjE3MzIyODkwMjQsImp0aSI6ImJkYmYzMWRlMTAwNTQ4ZTE5ZmI4NWQ5MDhjMGUzODZhIiwidXNlcl9pZCI6M30.JgXdiNcV3wVC73KWKORyOERdyeElEIm4ER5uWuNU3B0',
      currentCategory: 0,
    categories: [
        {
          title: '个人证件',
          items: [
            { id: 1, name: '身份证', completed: false, showAddIcon: true },
            { id: 2, name: '学生证', completed: false, showAddIcon: true },
            { id: 3, name: '户口本', completed: false, showAddIcon: true },
            { id: 4, name: '护照', completed: false, showAddIcon: true },
            { id: 5, name: '签证', completed: false, showAddIcon: true },
            { id: 6, name: '港澳通行证', completed: false, showAddIcon: true },
            { id: 7, name: '大陆居民往来通行证', completed: false, showAddIcon: true },
            { id: 8, name: '驾照', completed: false, showAddIcon: true }
          ]
        },
        {
          title: '数码产品',
          items: [
            { id: 9, name: '手机', completed: false, showAddIcon: true },
            { id: 10, name: '充电器', completed: false, showAddIcon: true },
            { id: 11, name: '耳机', completed: false, showAddIcon: true },
            { id: 12, name: '相机', completed: false, showAddIcon: true },
            { id: 13, name: '笔记本电脑', completed: false, showAddIcon: true },
            { id: 14, name: '平板电脑', completed: false, showAddIcon: true },
            { id: 15, name: '智能手表', completed: false, showAddIcon: true },
            { id: 16, name: '存储卡', completed: false, showAddIcon: true }
          ]
        },
        {
          title: '药品',
          items: [
            { id: 17, name: '感冒药', completed: false, showAddIcon: true },
            { id: 18, name: '创可贴', completed: false, showAddIcon: true },
            { id: 19, name: '止痛药', completed: false, showAddIcon: true },
            { id: 20, name: '消炎药', completed: false, showAddIcon: true },
            { id: 21, name: '晕车药', completed: false, showAddIcon: true },
            { id: 22, name: '防晒霜', completed: false, showAddIcon: true },
            { id: 23, name: '防蚊液', completed: false, showAddIcon: true },
            { id: 24, name: '维生素', completed: false, showAddIcon: true }
          ]
        },
        {
          title: '生活用品',
          items: [
            { id: 25, name: '牙刷', completed: false, showAddIcon: true },
            { id: 26, name: '牙膏', completed: false, showAddIcon: true },
            { id: 27, name: '毛巾', completed: false, showAddIcon: true },
            { id: 28, name: '洗发水', completed: false, showAddIcon: true },
            { id: 29, name: '沐浴露', completed: false, showAddIcon: true },
            { id: 30, name: '洗衣液', completed: false, showAddIcon: true },
            { id: 31, name: '卫生纸', completed: false, showAddIcon: true },
            { id: 32, name: '雨伞', completed: false, showAddIcon: true }
          ]
        }
      ]
    };
  },
computed: {
  currentCategoryItems() {
    const itemsMap = new Map();
    const uniqueItems = this.categories[this.currentCategory].items.filter(item => {
      if (!itemsMap.has(item.name)) {
        itemsMap.set(item.name, item);
        return true;
      }
      return false;
    });
    return uniqueItems.values();
  }
},
  mounted() {
    // 从路由参数中获取 trip_id
    const tripId = this.$route.query.trip_id;
    this.tripId = tripId; // 将 trip_id 存储在组件的数据中
    // 打印 trip_id
    console.log('当前页面的 trip_id:', this.tripId);
  },
  methods: {
    goBack() {
      uni.navigateBack();
    },
    selectCategory(index) {
      this.currentCategory = index;
    },
       addItem(item) {
          this.$set(item, 'completed', true);
          this.$set(item, 'showAddIcon', false);
          this.sendPostRequest(item, this.token); // 调用发送 POST 请求的方法
        },
     sendPostRequest(item) {
		  
       // 获取当前分类的 title
       const currentCategoryTitle = this.categories[this.currentCategory].title;
       const requestData = {
         id: item.id,
         name: item.name,
         note: currentCategoryTitle, // 使用当前分类的 title 作为 note 的值
         status: "no", // 默认为 no
         created_at: new Date().toISOString(), // 当前时间
         trip_information: this.tripId,
       };
     console.log('请求体数据:', requestData);
       fetch('https://734dw56037em.vicp.fun/api/memos/memos/',  { // 确保 URL 正确
         method: 'POST',
         headers: {
           'Content-Type': 'application/json', // 确保这是服务器期望的格式
           'Authorization': `Bearer ${this.token}` // 使用 this.token 引用组件的 token
         },
         body: JSON.stringify(requestData), // 将 JavaScript 对象转换为 JSON 字符串
       })
       .then(response => {
         if (response.ok) {
           return response.json();
         }
         throw new Error('Network response was not ok.');
       })
       .then(data => {
         console.log('Success:', data);
       })
       .catch((error) => {
         console.error('Error:', error);
       });
     },
	 navigateToPage(pagePath) {
	                const tripId = this.tripId;
	                if (tripId) {
	                  uni.navigateTo({
	                    url: `${pagePath}?trip_id=${tripId}`,
	                    success: (res) => {
	                      res.eventChannel.emit('acceptTripData', { tripData: this.tripData });
	                    }
	                  });
	                } else {
	                  console.error('未找到 trip_id 参数，无法跳转');
	                  uni.showToast({
	                    title: '未找到行程 ID，无法跳转',
	                    icon: 'none',
	                    duration: 3000
	                  });
	                }
	              },
	saveAndNavigate() {
	    this.navigateToPage('/pages/index2/index2');
	  }
  }
};
</script>

<style>
/* 页面整体样式 */
.header {
  background-color: #b0d8ff;
  padding: 20rpx;
  border-radius: 10rpx;
  text-align: center;
}

.title {
  font-size: 36rpx; /* 增大字体 */
  font-weight: bold;
  color: #333;
  line-height: 1.4; /* 增加行高以增加行间距 */
}

.subtitle {
  font-size: 24rpx; /* 较小字体用于副标题 */
  color: #666;
  margin-top: 8rpx; /* 增加与标题的间距 */
}

.container {
  background-color: #f4f7fa;
  padding: 10px;
  min-height: 100vh;
}

/* 顶部导航栏 */
.navbar {
  display: flex;
  align-items: center;
  padding: 10px 0;
  background-color: #fff;
  border-bottom: 1px solid #ddd;
}

.back-button {
  font-size: 18px;
  margin-right: 10px;
  color: #333;
}

.title {
  font-size: 18px;
  font-weight: bold;
  color: #333;
}

/* 搜索框 */
.search-bar {
  margin: 10px 0;
  padding: 10px;
  background-color: #fff;
  border-radius: 5px;
}

.search-input {
  width: 100%;
  font-size: 16px;
  border: none;
  outline: none;
}

/* 分类标题和选项卡 */
.category-section {
  margin-top: 10px;
}

.section-title {
  font-size: 16px;
  font-weight: bold;
  color: #333;
}

.category-tabs {
   display: flex;
   margin-top: 10px;
   overflow-x: auto; /* 当标签过多时允许横向滚动 */
   white-space: nowrap; /* 防止换行 */
}

.tab {
  padding: 8px 12px;
  background-color: #f5f5f5;
  color: #007acc;
  border-radius: 15px;
  margin-right: 10px;
  white-space: nowrap; /* 防止文字在按钮内换行 */
}

.tab.active {
  background-color: #007acc;
  color: #fff;
}

/* 物品列表 */
.item-list {
  margin-top: 10px;
  background-color: #fff;
}

.item {
  display: flex;
  justify-content: space-between;
  padding: 10px;
  border-bottom: 1px solid #ddd;
  align-items: center;
}

.add-icon {
  font-size: 18px;
  color: #007acc;
}

/* 保存按钮 */
/* 保存按钮样式 */
.save-button {
  width: 100%;
  padding: 12px;
  background-color: #4a90e2;
  color: white;
  font-size: 16px;
  font-weight: bold;
  text-align: center;
  border-radius: 5px;
  position: fixed; /* 将按钮固定在页面底部 */
  bottom: 0; /* 紧贴底部 */
  left: 0; /* 左边界位于页面的最左边 */
  right: 0; /* 右边界位于页面的最右边，确保宽度为100% */
  z-index: 100; /* 确保按钮在最上层 */
}
</style>