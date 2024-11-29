<template>
  <view class="container">
    <!-- 顶部导航栏 -->
    <view class="navbar">
      <text class="trip-name">{{ tripTitle }}</text>
      <text class="sub-title">10.1-10.3 | 3天2晚</text>
      <view class="tabs">
        <text class="tab-item">行程</text>
        <text class="tab-item active">旅行账单</text>
        <text class="tab-item" @click="goToPackingList">行李清单</text>
      </view>
    </view>

    <!-- 页面内容 -->
    <view class="bill-section">
      <view class="total-amount">
        <text class="total-label">总花费</text>
        <text class="amount">¥ {{ totalAmount }}</text>
      </view>
      <view class="budget">
        <text class="budget-label">预算</text>
        <text class="amount">¥ {{ budget }}</text>
      </view>
      <view class="set-budget-background"></view>
      <view class="set-budget-text" @click="showBudgetOverlay">
        <text class="set-budget">设置预算</text>
      </view>
    </view>

    <view class="detail-section">
      <view v-for="(record, index) in filteredBillRecords" :key="record.id" class="detail-item">
        <!-- 日期 -->
        <view class="date-wrapper">
          <text class="date">{{ record.date }}</text>
        </view>
        <!-- 项目详情 -->
        <view class="item">
          <!-- 动态绑定图标的 src 属性 -->
          <image :src="record.icon" class="icon"></image>
          <!-- 动态显示项目标题 -->
          <text class="item-title">{{ record.category }}</text>
          <!-- 动态显示金额 -->
          <text class="amount">¥ {{ record.amount }}</text>
        </view>
      </view>
    </view>

    <!-- 自定义数字键盘弹出层 -->
    <view class="budget-input-overlay" v-if="showBudgetInput">
      <view class="budget-input-container">
        <text class="budget-input-title">设置预算</text>
        <input class="budget-display" type="text" v-model="budget" />
        <view class="number-keyboard">
          <view class="key" v-for="key in keys" :key="key" @click="handleKeyClick(key)">
            {{ key }}
          </view>
        </view>
        <button class="confirm-button" @click="confirmBudget">确认</button>
      </view>
    </view>
  </view>
</template>
<script>
export default {
  data() {
    return {
	  tripTitle: '', // 行程标题
      showBudgetInput: false,
      budget: '',
      keys: ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', 'C', '←'],
      billRecords: [],
      tripId: null, // 存储trip_id的值
    };
  },
 computed: {
    // 根据 trip_id 过滤账单记录
    filteredBillRecords() {
		console.log('路由参数 trip_id 更新为:', this.tripId);
      // 确保 this.tripId 已经被定义，并且 billRecords 数组中有 trip_information 属性
      return this.billRecords.filter(record => record.trip_information === parseInt(this.tripId));
    },
    // 计算 filteredBillRecords 的总金额
    totalAmount() {
      // 确保 filteredBillRecords 不是空数组
      return this.filteredBillRecords.reduce((total, record) => {
        return total + parseFloat(record.amount);
      }, 0).toFixed(2);
    }
  },
  mounted() {
    // 从查询参数中获取 trip_id
    this.tripId = this.$route.query.trip_id;
    console.log('路由参数 trip_id 更新为:', this.tripId);
    this.fetchBillRecords();
  },
  methods: {
	fetchTripActivities(tripId) {
	    if (!tripId) {
	        uni.showToast({
	            title: '缺少行程 ID',
	            icon: 'none',
	        });
	        return;
	    }
	
	    // 构建请求 URL，添加查询参数，参数名为 trip_information_id
	    const url = `https://734dw56037em.vicp.fun/api/trip/get_trip_activities/?trip_information_id=${tripId}`;
	    console.log('请求 URL:', url);
	
	    // 发起 GET 请求
	    uni.request({
	        url: url,
	        method: 'GET',
	        headers: {
	          'Content-Type': 'application/json',
	          // 根据需要可以添加更多的请求头
	        },
	        success: (res) => {
	            console.log('响应状态码:', res.statusCode);
	            console.log('响应数据:', res.data);
	            console.log('响应头:', res.header);
	
	            if (res.statusCode === 200) {
	                const tripData = res.data;
	                if (!tripData) {
	                    console.error('未获取到有效的行程数据');
	                    return;
	                }
	                console.log('行程数据:', tripData);
	                this.initTripData(tripData);
	            } else {
	                uni.showToast({
	                    title: res.data.error || '请求失败',
	                    icon: 'none',
	                });
	            }
	        },
	        fail: (err) => {
	            console.error('请求失败:', err);
	            uni.showToast({
	                title: '网络请求失败，请稍后重试',
	                icon: 'none',
	            });
	        },
	    });
	},
    goToPackingList() {
      uni.navigateTo({
        url: '/pages/xingli/xingli'  // 跳转路径
      });
    },
    showBudgetOverlay() {
      this.showBudgetInput = true;
    },
    handleKeyClick(key) {
      if (key === 'C') {
        this.budget = ''; // 清空输入
      } else if (key === '←') {
        this.budget = this.budget.slice(0, -1); // 删除最后一个字符
      } else {
        this.budget += key; // 添加数字
      }
    },
    confirmBudget() {
      this.showBudgetInput = false;
      // 这里可以添加将预算值保存到数据存储或发送到服务器的代码
      uni.showToast({
        title: `预算已设置为 ¥${this.budget}`,
        icon: 'success',
        duration: 2000
      });
    },
    closeKeyboard() {
      this.showBudgetInput = false;
    },
 fetchBillRecords() {
       const token = uni.getStorageSync('access_token');
       const apiUrl = `https://734dw56037em.vicp.fun/api/bills/expenses/`;  // 确保这是您的后端API地址
       uni.request({
         url: apiUrl,
         method: 'GET',
         header: {
           'Content-Type': 'application/json',
           'Authorization': `Bearer ${token}`,
         },
		 
         success: (res) => {
           if (res.statusCode === 200) {
             this.billRecords = res.data;
             console.log('更新后的 billRecords:', this.billRecords);
           } else {
             uni.showToast({
               title: '获取账单记录失败: ' + res.statusCode,
               icon: 'none'
             });
             console.error('获取账单记录失败，状态码：', res.statusCode);
           }
         },
         fail: (err) => {
           console.error('请求失败:', err);
           uni.showToast({
             title: '请求失败，请检查网络连接或联系服务提供商',
             icon: 'none'
           });
         }
       });
     },
	 
   },
   initTripData(tripData) {
       if (!tripData) {
           console.error('没有行程数据');
           return;
       }
   
       const isLocalData = typeof tripData.trip_id !== 'undefined';
       if (isLocalData) {
           this.tripTitle = tripData.title || '未知行程';
           this.travelDateRange = tripData.dateRange || '';
           this.tripDuration = tripData.duration || '';
           this.places = tripData.places || [];
           this.weatherForecast = tripData.weather || [];
           this.placeCoordinates = tripData.placeCoordinates || {};
           this.dailyTrips = tripData.dailyTrips || [];
           
           const dayCount = this.dailyTrips.length;
           this.days = ['总览', ...Array.from({ length: dayCount }, (_, i) => `DAY${i + 1}`)];
       } else {
           const tripInfo = tripData.trip && tripData.trip.length > 0 ? tripData.trip[0] : {};
           const activities = tripData.activities || [];
   
           if (!tripInfo.trip_name) {
               console.error('tripData 中没有有效的行程信息');
               return;
           }
   
           this.tripTitle = tripInfo.trip_name || '未知行程';
           this.travelDateRange = `${tripInfo.start_date} 至 ${tripInfo.end_date}`;
           const startDate = new Date(tripInfo.start_date);
           const endDate = new Date(tripInfo.end_date);
           const timeDiff = endDate - startDate;
           const daysDiff = timeDiff / (1000 * 3600 * 24) + 1;
           this.tripDuration = `${daysDiff}天`;
   
           this.places = activities.map(activity => activity.trip_destination);
           this.placeCoordinates = {};
           this.dailyTrips = [];
           const activitiesByDay = {};
           activities.forEach(activity => {
               const dayKey = `DAY${activity.days}`;
               if (!activitiesByDay[dayKey]) {
                   activitiesByDay[dayKey] = [];
               }
               activitiesByDay[dayKey].push(activity.trip_destination);
           });
   
           for (let day in activitiesByDay) {
               this.dailyTrips.push({
                   day: day,
                   city: tripInfo.trip_name,
                   places: activitiesByDay[day].join(' - ')
               });
           }
   
           this.days = ['总览', ...Array.from({ length: daysDiff }, (_, i) => `DAY${i + 1}`)];
       }
   
       this.initMap(this.placeCoordinates);
   },
   
  beforeDestroy() {
    if (this.timer) {
      clearInterval(this.timer);
    }
  }
};
</script>
<style>

.budget-input-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.6);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 999; /* 确保弹窗在最上层 */
}


.budget-input-container {
  background-color: #fff;
  padding: 30px;
  border-radius: 10px;
  width: 300px;
  text-align: center;
}

.budget-input-title {
  font-size: 18px;
  font-weight: bold;
  color: #333;
  margin-bottom: 10px;
}

.budget-display {
  font-size: 28px;
  font-weight: bold;
  color: #007acc;
  margin-bottom: 20px;
}

.number-keyboard {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 10px;
  margin-bottom: 20px;
}

.key {
  background-color: #e1f0ff;
  padding: 15px 0;
  border-radius: 10px;
  font-size: 20px;
  font-weight: bold;
  color: #333;
  text-align: center;
}

.confirm-button {
  background-color: #007acc;
  color: #fff;
  padding: 10px 0;
  border-radius: 10px;
  font-size: 16px;
  width: 100%;
}

.overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: transparent;
}
/* 页面整体样式 */
.container {
  background-color: #f4f7fa;
  padding: 20px;
}

/* 顶部导航栏样式 */
.navbar {
  background-color: #e1f0ff;
  padding: 20px;
  border-radius: 10px;
  text-align: center;
}

.title {
  font-size: 18px;
  font-weight: bold;
  color: #333;
}

.sub-title {
  font-size: 14px;
  color: #888;
  margin-top: 5px;
}

.tabs {
  display: flex;
  justify-content: space-around;
  margin-top: 15px;
}

.tab-item {
  font-size: 16px;
  color: #888;
}

.tab-item.active {
  color: #0066cc;
  font-weight: bold;
}

/* 账单总花费样式 */
.bill-section {
  background-color: #d6f4ff; /* 较深的浅蓝色背景 */
  padding: 20px;
  border-radius: 10px;
  margin-top: 20px;
  text-align: center;
  position: relative; /* 用于定位子元素 */
}

/* 总花费和金额显示 */
.total-amount {
  display: flex;
  flex-direction: column; /* 垂直布局 */
  align-items: center; /* 水平居中对齐 */
  margin-bottom: 10px;
  position: relative; /* 相对定位，避免被背景遮挡 */
  z-index: 2; /* 确保在背景之上显示 */
}
.total-label {
  font-size: 12px; /* 增大字体大小 */
  font-weight: bold;
  color: #333;
}

.amount {
  font-size: 36px; /* 增大字体大小，使金额更显眼 */
  font-weight: bold;
  color: #000;
  margin-top: 5px;
}

/* 浅蓝色背景，覆盖到整个下半部分，并扩大到更多区域 */
.set-budget-background {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 40%; /* 扩大高度，覆盖更多上半部分 */
  background-color: #e1f5fe; /* 浅蓝色背景 */
  border-bottom-left-radius: 10px;
  border-bottom-right-radius: 10px;
  z-index: 1; /* 放在主内容的下层 */
}

/* 设置预算文本样式 */
.set-budget-text {
  position: relative;
  z-index: 2; /* 确保文字在背景之上 */
  margin-top: 50px; /* 下移设置预算文本 */
}

.set-budget {
  font-size: 16px;
  color: #007acc; /* 蓝色字体 */
  text-align: center;
}

/* 明细信息样式 */
.detail-section {
  background-color: #fff;
  padding: 20px;
  border-radius: 10px;
  margin-top: 20px;
}

/* 日期和金额部分样式，添加背景 */
.date-wrapper {
  background-color: #f0f0f0; /* 灰色背景 */
  padding: 8px 12px;
  border-radius: 10px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.date {
  font-size: 16px;
  color: #333;
  display: flex;
  justify-content: space-between;
  width: 100%;
}

.date text {
  margin-right: 20px; /* 增加日期和金额的距离 */
}

.item {
  display: flex;
  align-items: center;
  padding: 10px 0;
  border-bottom: 1px solid #f1f1f1;
}

.icon {
  width: 24px;
  height: 24px;
  background-color: #e1f5fe; /* 浅蓝色背景 */
  padding: 5px;
  border-radius: 50%;
  margin-right: 10px;
}

.item-title {
  font-size: 16px;
  color: #333;
  flex: 1;
}

.amount {
  font-size: 16px;
  color: #333;
}
</style>
