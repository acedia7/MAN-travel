<template>
  <view class="container">
    <!-- 顶部导航栏 -->
    <view class="navbar">
      <view class="back-button" @click="goBack">＜</view>
      <text class="title">添加账单</text>
    </view>

    <!-- 分类图标区域 -->
    <view class="category-section">
      <view class="category-item" v-for="(item, index) in categories" :key="index" @click="selectCategory(index)">
        <view :class="['icon-wrapper', selectedCategory === index ? 'selected' : '']">
          <image :src="item.icon" class="icon" />
        </view>
        <text class="category-text">{{ item.name }}</text>
      </view>
    </view>

    <!-- 输入区域：日期选择、备注输入 -->
    <view class="input-section">
      <!-- 日期选择输入框 -->
      <view class="date-remark-container">
        <input class="date-input" placeholder="输入日期 YYYY-MM-DD" v-model="date" @input="handleDateInput" />
        <input class="remark-input" placeholder="在这里输入备注..." v-model="remark" />
      </view>
      
      <!-- 显示金额 -->
      <view class="amount">
        ¥ {{ amount }}
      </view>
    </view>

    <!-- 自定义数字键盘 -->
    <view class="keyboard">
      <view class="key" v-for="(key, index) in keys" :key="index" @click="handleKeyPress(key)">
        {{ key }}
      </view>
    </view>

    <!-- 完成按钮 -->
    <button class="submit-button" @click="submit">完成</button>
  </view>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      categories: [
        { name: "交通", icon: "/static/transport.png" },
        { name: "住宿", icon: "/static/hotel.png" },
        { name: "美食", icon: "/static/food.png" },
        { name: "景点", icon: "/static/scenic.png" },
        { name: "购物", icon: "/static/shopping.png" },
        { name: "活动", icon: "/static/activity.png" },
        { name: "其他", icon: "/static/others.png" }
      ],
      selectedCategory: null,
      remark: '',       // 存储备注
      amount: '0.00',    // 存储金额
      keys: ["1", "2", "3", "✖️", "4", "5", "6", "+", "7", "8", "9", "-", ".", "0", "完成"],
      date: "",          // 存储用户输入的日期
      showDateInputFlag: false, // 控制日期输入框的显示
      trip_information: 13,
	  tripId: null
    };
  },
  mounted() {
    // 从路由参数中获取 trip_id
    const tripId = this.$route.query.trip_id;
    this.tripId = tripId; // 将 trip_id 存储在组件的数据中
  
    // 打印 trip_id
    console.log('当前页面的 trip_id:', this.tripId);
  },
  methods: {
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
	
	jumpToIndex1() {
	   this.navigateToPage('/pages/index1/index1');
	  },
    // 选择分类
    selectCategory(index) {
      this.selectedCategory = index;
    },
    // 处理键盘按键事件
    handleKeyPress(key) {
      if (key === "✖️") {
        this.amount = "0.00";
      } else if (key === "完成") {
        this.submit();
      } else {
        // 数字输入逻辑
        if (this.amount === "0.00") {
          this.amount = key;
        } else {
          this.amount += key;
        }
      }
    },
    // 显示日期输入框
    showDateInput() {
      this.showDateInputFlag = true; // 控制日期输入框的显示
    },
    // 处理日期输入
    handleDateInput(event) {
      let value = event.target.value;
      // 确保日期格式正确
      if (value.length === 4 && !value.includes('-')) {
        value += '-';
      } else if (value.length === 7 && !value.includes('-')) {
        value = value.slice(0, 4) + '-' + value.slice(4, 7);
      } else if (value.length === 10 && !value.includes('-')) {
        value = value.slice(0, 7) + '-' + value.slice(7);
      }
      this.date = value;
    },
    // 返回上一页
    goBack() {
      uni.navigateBack();
    },
    // 完成提交
    async submit() {
      // 检查必填项
      if (!(this.selectedCategory+1) || !this.date || !this.amount) {
        uni.showToast({
          title: '请填写所有必填项',
          icon: 'none'
        });
        return;
      }

      try {
        // 构造请求体
	const token = uni.getStorageSync('access_token');
    const requestData = {
     category: this.categories[this.selectedCategory].name,
     remark: this.remark,
     date: this.date,
     amount: parseFloat(this.amount), // 转换为数字
     trip_information: this.tripId // 使用当前页面的 trip_id
   };
        console.log('Request Data:', requestData);
        // 设置 headers，包括身份认证信息
        const config = {
          header: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`, // 将 token 放入 Authorization 头中
          },
        };

        // 发送 POST 请求到后端
        const response = await axios.post('https://734dw56037em.vicp.fun/api/bills/expenses/', requestData, config);

        // 处理响应
        uni.showToast({
          title: response.data.message, // 假设后端返回的数据中有一个 message 字段
          icon: 'success'
        });
         this.jumpToIndex1();
      } catch (error) {
        // 错误处理
        uni.showToast({
          title: '请求失败，请稍后再试',
          icon: 'none'
        });
        console.error('请求错误:', error); // 在控制台打印错误信息
      }
    }
  }
};
</script>
<style scoped>
/* 页面整体样式 */
.container {
  padding: 20px;
  background-color: #f4f7fa;
  min-height: 100vh;
}

/* 顶部导航栏样式 */
.navbar {
  display: flex;
  align-items: center;
  margin-bottom: 20px;
  position: relative;
}

.back-button {
  font-size: 20px;
  margin-right: 10px;
  color: #333;
  cursor: pointer;
  position: absolute;
  left: 0;
}

.title {
  flex: 1;
  text-align: center;
  font-size: 20px;
  font-weight: bold;
  color: #333;
}

/* 分类图标区域样式 */
.category-section {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-around;
  margin-bottom: 20px;
}

.category-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 15px;
  cursor: pointer;
}

.icon-wrapper {
  width: 60px;
  height: 60px;
  background-color: #f0f0f0;
  border-radius: 15px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.icon-wrapper.selected {
  border: 2px solid #4a90e2;
  background-color: #e1f5fe;
}

.icon {
  width: 30px;
  height: 30px;
}

.category-text {
  font-size: 12px;
  color: #666;
  margin-top: 5px;
}

/* 输入区域样式 */
.input-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 20px;
}

/* 日期和备注容器 */
.date-remark-container {
  display: flex;
  width: 100%;
  margin-bottom: 10px;
}
.date-input {
  padding: 10px;
  font-size: 14px;
  color: #333;
  background-color: #f9f9f9;
  border-radius: 5px;
  margin-bottom: 10px;
}
.date-button {
  flex: 1;
  padding: 10px;
  background-color: #f0f0f0;
  border-radius: 5px;
  font-size: 14px;
  color: #333;
  text-align: left;
}

.remark-input {
  flex: 2;
  padding: 10px;
  font-size: 14px;
  color: #333;
  background-color: #f9f9f9;
  border-radius: 5px;
  margin-left: 10px;
}

/* 金额显示样式 */
.amount {
  font-size: 24px;
  font-weight: bold;
  color: #4a90e2;
  margin-bottom: 20px;
}

/* 自定义数字键盘样式 */
.keyboard {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 10px;
  padding: 10px;
}

.key {
  text-align: center;
  padding: 15px 0;
  font-size: 18px;
  background-color: #e1f0ff;
  border-radius: 5px;
  cursor: pointer;
}

.key:active {
  background-color: #b3d8f0;
}

/* 完成按钮样式 */
.submit-button {
  width: calc(100% - 80px); /* 减去左右的间距总和，确保按钮宽度合适 */
  padding: 12px;
  background-color: #4a90e2;
  color: white;
  font-size: 16px;
  border-radius: 5px;
  text-align: center;
  position: fixed; /* 将按钮固定在页面底部 */
  bottom: 50px; /* 距离页面底部 50px */
  left: 50%; /* 按钮左边界位于页面的 50% 位置 */
  transform: translateX(-50%); /* 将按钮向左移动自身宽度的一半，实现居中效果 */
  box-shadow: 0 -2px 10px rgba(0, 0, 0, 0.1); /* 添加阴影提升可见性 */
  z-index: 100; /* 确保按钮在最上层，不会被其他元素遮盖 */
}
</style>
