<template>
	<view class="travel-plan-overview-page">
		<!-- 返回按钮容器 -->
		<view class="back-button-container">
			<image src="/static/icons/back-icon.png" class="back-button" @click="goBack" />
		</view>

		<!-- 行程名 -->
		<view class="header">
			<text class="trip-name">{{ tripTitle }}</text>
		</view>
		<!-- 旅行时间 -->
		<view class="travel-time">{{ travelDateRange }} {{ tripDuration }}</view>
		<!-- 行程标题及横线 -->
		<view class="trip-section">
			<view class="button-group">
				<!-- 行程按钮 -->
				<button class="btn-title" @click="handleShowOverview">行程</button>
				<!-- 旅行账单按钮 -->
				<button class="btn-title" @click="handleShouyeClick">旅行账单</button>
				<!-- 行李清单按钮 -->
				<button class="btn-title" @click="handleXingliClick">行李清单</button>
			</view>
			<view class="horizontal-line"></view>
		</view>

    <!-- 白色矩形区域 -->
    <view class="white-rectangle">
      <!-- 账单标题 -->
      <view class="overview-title">旅行账单</view>

      <!-- 设置预算按钮 -->
      <view class="settings-button" @click="showBudgetInputOverlay">
        <text class="settings-text">设置预算</text>
      </view>

      <!-- 账单明细区域 -->
      <view class="bill">
        <view class="bill-item food left">
          <text class="label">🍽️ 美食 ¥288</text>
        </view>
        <view class="bill-item stay right">
          <text class="label">🏠 住宿 ¥988</text>
        </view>
        <view class="bill-item transport left">
          <text class="label">🚌 交通 ¥1888</text>
        </view>
      </view>
	  
	  <!-- 底部 Logo 和介绍 -->
	  <view class="footer">
	    <view class="footer-logo"></view>
	    <text class="footer-text">旅行账单 轻松记录</text>
	  </view>
	  
      <!-- 记一笔按钮 -->
      <button class="record-button" @click="goToAddBill">记一笔</button>
    </view>

    <!-- 设置预算的数字键盘输入框 -->
    <view class="budget-input-overlay" v-if="showBudgetInput">
      <view class="budget-input-container">
        <text class="budget-input-title">设置预算</text>
        <text class="budget-display">¥ {{ budget }}</text>
        <view class="number-keyboard">
          <view v-for="key in keys" :key="key" class="key" @click="handleKeyClick(key)">
            {{ key }}
          </view>
        </view>
        <button class="confirm-button" @click="confirmBudget">完成</button>
      </view>
    </view>
  </view>
</template>

<script>
import { useRoute, useRouter } from 'vue-router';

export default {
  data() {
    return {
      showBudgetInput: false,
      budget: '', // 预算输入值
      keys: ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', 'C', '←'],
	 tripId: '', // 存储当前行程 ID
	 currentDay: '总览', // 当前选择的行程天数
	 weatherForecast: [], // 天气预报
	 tripTitle: '', // 行程标题
	 travelDateRange: '', // 旅行日期范围
	 tripDuration: '', // 旅行时长
	 places: [], // 旅行地点
	 map: null, // 地图实例
	 days: [], // 存储行程天数（如：总览，DAY1, DAY2）
	 dailyTrips: [], // 每日行程
	 placeCoordinates: {}, // 地点坐标
	 activities: [], // 活动列表，从服务器获取
	 tripData: {}, // 存储从服务器获取的行程数据
	 tripsById: {
	 	1: {
	 		trip_id:1,
	 		title: '【示例】福州三日游 | 在三坊七巷感受榕城秋日古韵',
	 		dateRange: '11.01至11.03',
	 		duration: '3天2晚',
	 		places: [
	 			'烟台山公园', '崔酱炸鸡', '上下杭', '三坊七巷', '后街捞化',
	 			'鼓山', '福道', '达明美食街', '森林公园', '温泉公园', '闽江夜游'
	 		],
	 		weather: [{
	 				city: '福州市',
	 				date: '10.1',
	 				weekday: '周二',
	 				icon: '☀',
	 				condition: '晴朗无云',
	 				temperature: '24°~28°'
	 			},
	 			{
	 				city: '福州市',
	 				date: '10.2',
	 				weekday: '周三',
	 				icon: '☁',
	 				condition: '多云',
	 				temperature: '22°~26°'
	 			},
	 			{
	 				city: '福州市',
	 				date: '10.3',
	 				weekday: '周四',
	 				icon: '🌧',
	 				condition: '小雨',
	 				temperature: '18°~22°'
	 			}
	 		],
	 		placeCoordinates: {
	 			'烟台山公园': [119.3112, 26.0558],
	 			'崔酱炸鸡': [119.3080, 26.0612],
	 			'上下杭': [119.3002, 26.0655],
	 			'三坊七巷': [119.3005, 26.0688],
	 			'后街捞化': [119.3020, 26.0710],
	 			'鼓山': [119.3258, 26.0830],
	 			'福道': [119.3030, 26.0800],
	 			'达明美食街': [119.3010, 26.0720],
	 			'森林公园': [119.3300, 26.0900],
	 			'温泉公园': [119.3100, 26.0850],
	 			'闽江夜游': [119.3050, 26.0700]
	 		},
	 		dailyTrips: [ // 每个行程对应的每日行程数据
	 			{
	 				day: 'DAY1',
	 				city: '福州市',
	 				places: '烟台山公园 - 崔酱炸鸡 - 上下杭 - 三坊七巷 - 后街捞化'
	 			},
	 			{
	 				day: 'DAY2',
	 				city: '福州市',
	 				places: '鼓山 - 福道 - 达明美食街'
	 			},
	 			{
	 				day: 'DAY3',
	 				city: '福州市',
	 				places: '森林公园 - 温泉公园 - 闽江夜游'
	 			}
	 		]
	 	},
	 	2: {
	 		trip_id:2,
	 		title: '【示例】泉州三日游 | 螃蟹游记',
	 		dateRange: '12.01至12.03',
	 		duration: '3天2晚',
	 		places: [
	 			'泉州古城', '清源山', '东西塔', '泉州东街口', '南门市场',
	 			'泉州大桥', '泉州博物馆', '泉州夜市', '洛阳桥', '九日山'
	 		],
	 		weather: [{
	 				city: '泉州市',
	 				date: '12.1',
	 				weekday: '周六',
	 				icon: '☀',
	 				condition: '晴朗无云',
	 				temperature: '22°~26°'
	 			},
	 			{
	 				city: '泉州市',
	 				date: '12.2',
	 				weekday: '周日',
	 				icon: '☁',
	 				condition: '多云',
	 				temperature: '20°~24°'
	 			},
	 			{
	 				city: '泉州市',
	 				date: '12.3',
	 				weekday: '周一',
	 				icon: '🌧',
	 				condition: '小雨',
	 				temperature: '18°~22°'
	 			}
	 		],
	 		placeCoordinates: {
	 			'泉州古城': [118.6007, 24.9018],
	 			'清源山': [118.7058, 24.9062],
	 			'东西塔': [118.6005, 24.9068],
	 			'泉州东街口': [118.5894, 24.9132],
	 			'南门市场': [118.6001, 24.9143],
	 			'泉州大桥': [118.6256, 24.9099],
	 			'泉州博物馆': [118.6093, 24.9076],
	 			'泉州夜市': [118.5876, 24.9135],
	 			'洛阳桥': [118.6310, 24.8968],
	 			'九日山': [118.6315, 24.8633]
	 		},
	 		dailyTrips: [{
	 				day: 'DAY1',
	 				city: '泉州市',
	 				places: '泉州古城 - 清源山 - 东西塔 - 泉州东街口 - 南门市场'
	 			},
	 			{
	 				day: 'DAY2',
	 				city: '泉州市',
	 				places: '泉州大桥 - 泉州博物馆 - 泉州夜市'
	 			},
	 			{
	 				day: 'DAY3',
	 				city: '泉州市',
	 				places: '洛阳桥 - 九日山'
	 			}
	 		]
	 	},
	 	3: {
	 		trip_id:3,
	 		title: '【示例】武汉三日游 | 遍吃逛吃武汉',
	 		dateRange: '10.01至10.03',
	 		duration: '3天2晚',
	 		places: [],
	 		weather: [],
	 		placeCoordinates: {},
	 		dailyTrips: [] // 如果没有行程数据，这里设置为空
	 	}
	 }
    };
  },
mounted() {
            // 先检查是否有本地 trip_id，如果没有再查找服务器返回的 trip_information_id
            const tripId = this.$route.query.trip_information_id || this.$route.query.trip_id || this.$route.query.id;

            if (tripId) {
                console.log('获取到的 tripId:', tripId);
                this.tripId = tripId; // 将 tripId 存储到组件的 data 中

                // 判断是本地数据还是从服务器获取数据
                if (this.tripsById[tripId]) {
                    // 使用本地的行程数据进行初始化
                    console.log('使用本地行程数据');
                    this.initTripData(this.tripsById[tripId]);
                } else {
                    // 使用服务器数据
                    console.log('请求服务器获取行程数据');
                    this.fetchTripActivities(tripId);
                }
            } else {
                console.error('未找到 trip_id 或 trip_information_id 参数');
                uni.showToast({
                    title: '未找到行程ID，请重新进入页面',
                    icon: 'none',
                    duration: 3000
                });
            }
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
	         success: (res) => {
	             console.log('响应数据:', res);
	             if (res.statusCode === 200) {
	                 const tripData = res.data && res.data ? res.data : undefined;
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
	 
	 // 初始化行程数据
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
	 
	   
	 },

	goBack() {
	        // 返回到首页 index.vue
	        uni.navigateTo({
	          url: '/pages/index/index'
	        });
	      },
	
	// 点击“旅行账单”按钮的跳转逻辑
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
  handleShouyeClick() {
      this.navigateToPage('/pages/shouye/shouye');
  },
             
  // 点击“行李清单”按钮的跳转逻辑
  handleXingliClick() {
      this.navigateToPage('/pages/xingli/xingli');
  },
  
    handleShowOverview() {
		this.navigateToPage('/pages/Overview/Overview');
	},
 goToAddBill() {
 this.navigateToPage('/pages/addBill/addBill');
 },
    showBudgetInputOverlay() {
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
      console.log('预算设置为:', this.budget);
    }
  }
};
</script>

<style scoped>
/* 页面整体样式 */
.travel-plan-overview-page {
  background-color: #e1f0ff;
  padding: 20px;
}

/* 返回按钮容器样式 */
.back-button-container {
  margin-bottom: 10px;
}

/* 返回按钮图标样式 */
.back-button {
  width: 30px;
  height: 30px;
  cursor: pointer;
}

/* 行程名样式 */
.trip-name {
  font-size: 24px;
  font-weight: bold;
  text-align: left;
  margin-bottom: 10px;
}

/* 旅行时间样式 */
.travel-time {
  font-size: 16px;
  color: dimgray;
  text-align: left;
  margin-bottom: 10px;
}

/* 行程标题及按钮样式 */
.trip-section {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  text-align: left;
}

.button-group {
  display: flex;
  align-items: center;
  justify-content: flex-start;
  gap: 40rpx;
  margin-left: 15rpx;
}

.btn-title {
  font-size: 20px;
  font-weight: bold;
  color: black;
  background: none;
  border: none;
  outline: none;
  padding: 0;
  cursor: pointer;
  text-decoration: none;
  transition: color 0.3s ease;
}

.btn-title.active {
  color: #4c8cf5;
  border-bottom: 3rpx solid #4c8cf5;
}

.btn-title:hover {
  color: gray;
}

/* 横线样式 */
.horizontal-line {
  width: 100%;
  height: 1px;
  background-color: gray;
  margin-top: 10px;
}

/* 白色矩形区域样式 */
.white-rectangle {
  background-color: white;
  border-radius: 20px;
  padding: 20px;
  margin-bottom: 20px;
}

/* 账单标题样式 */
.overview-title {
  font-size: 18px;
  font-weight: bold;
  margin-bottom: 10px;
}

/* 设置预算按钮样式 */
.settings-button {
  font-size: 24rpx;
  color: #4c8cf5;
  display: flex;
  align-items: center;
  margin-bottom: 20rpx;
}

.settings-text {
  margin-left: 5rpx;
}

/* 底部 Logo 和介绍 */
.footer {
  text-align: center;
  margin-bottom: 20rpx;
}

.footer-logo {
  width:  400rpx;
  height: 400rpx;
  background: url('/static/logo.png') no-repeat center;
  background-size: cover;
  margin: 0 auto 10rpx;
}

.footer-text {
  font-size: 26rpx;
  color: #888;
  margin-bottom: 20rpx;
}

/* 账单明细样式 */
.bill {
  display: flex;
  flex-direction: column;
  gap: 20rpx;
  margin-bottom: 20rpx;
}

/* 气泡框样式 */
.bill-item {
  padding: 15rpx 30rpx;
  border-radius: 20rpx;
  font-size: 40rpx;
  font-weight: bold;
  color: #333;
  width: 60%;
  position: relative;
  box-shadow: 0 4rpx 8rpx rgba(0, 0, 0, 0.1);
  margin-bottom: 40rpx;
}

/* 不同颜色的背景 */
.food {
  background-color: #ffe6e6;
}

.stay {
  background-color: #fff5cc;
}

.transport {
  background-color: #e6ffe6;
}

/* 左右错落布局 */
.left {
  align-self: flex-start;
}

.right {
  align-self: flex-end;
}

/* 记一笔按钮样式 */
.record-button {
  font-size: 28rpx;
  background-color: #4c8cf5;
  color: #fff;
  padding: 12rpx 30rpx;
  border-radius: 24rpx;
  text-align: center;
  width: 50%;
  margin: 0 auto;
  display: block;
}

/* 设置预算输入框样式 */
.budget-input-overlay {
  position: fixed;
  bottom: 0;
  left: 0;
  width: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 20rpx;
}

.budget-input-container {
  width: 90%;
  background-color: #fff;
  border-radius: 20rpx;
  padding: 30rpx;
  text-align: center;
}

.budget-input-title {
  font-size: 28rpx;
  font-weight: bold;
  color: #333;
  margin-bottom: 20rpx;
}

.budget-display {
  font-size: 36rpx;
  color: #4c8cf5;
  margin-bottom: 20rpx;
}

.number-keyboard {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
  gap: 10rpx;
  margin-bottom: 20rpx;
}

.key {
  width: 30%;
  padding: 15rpx 0;
  background-color: #f0f0f0;
  font-size: 28rpx;
  color: #333;
  border-radius: 10rpx;
  text-align: center;
}

.confirm-button {
  width: 100%;
  padding: 15rpx;
  font-size: 28rpx;
  background-color: #4c8cf5;
  color: #fff;
  border-radius: 15rpx;
}
</style>
