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
    <view class="white-rectangle packing-list">
      <!-- 标签列表 -->
      <view class="tags">
        <view class="tag-row">
          <view class="tag">耳机</view>
        </view>
        <view class="tag-row">
          <view class="tag">充电宝</view>
          <view class="tag">洗漱用品</view>
        </view>
        <view class="tag-row">
          <view class="tag">身份证</view>
        </view>
      </view>

      <!-- 插图 -->
      <image src="/static/logo.png" class="illustration" mode="widthFix" />

      <!-- 提示文字 -->
      <text class="reminder-text">出行前记得对照清单\n检查一下物品是否都带啦</text>

      <!-- 开始添加按钮，添加点击事件 -->
      <button class="add-button" @click="goToAddPage">开始添加</button>
    </view>
  </view>
</template>

<script>
export default {
  data() {
    return {
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
	  
	      this.initMap(this.placeCoordinates);
	  },
	  goBack() {
	        // 返回到首页 index.vue
	        uni.navigateTo({
	          url: '/pages/index/index'
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
	goToAddPage() {
   		this.navigateToPage('/pages/tianjia/tianjia');
   	},
  }
};
</script>

<style scoped>
/* 页面整体样式 */
.travel-plan-overview-page {
  background-color: #e1f0ff;
  padding: 20px;
  min-height: 100vh;
}

/* 返回按钮容器样式 */
.back-button-container {
  margin-bottom: 10px; /* 设置与下方内容的间距 */
}

/* 返回按钮图标样式 */
.back-button {
  width: 30px;
  height: 30px;
  cursor: pointer;
}

/* 行程名样式 */
.header {
  margin-top: 10px; /* 设置与返回按钮的间距 */
  margin-bottom: 10px; /* 设置与下方内容的间距 */
}

.trip-name {
  font-size: 24px;
  font-weight: bold;
  color: #333;
}

/* 旅行时间样式 */
.travel-time {
  font-size: 16px;
  color: dimgray;
  text-align: left;
  margin-bottom: 10px;
}

/* 行程标题及横线 */
.trip-section {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  text-align: left;
}

.button-group {
  display: flex;
  gap: 20px;
}

.btn-title {
  font-size: 20px;
  font-weight: bold;
  color: black;
  background: none;
  border: none;
  outline: none;
  cursor: pointer;
}

.btn-title.active {
  color: #0066cc;
}

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
  min-height: 60vh; /* 设置最小高度为视口的100% */
  margin-top: 0; /* 移除上边距 */
  margin-left: auto; /* 水平居中 */
  margin-right: auto; /* 水平居中 */
  width: calc(100% - 40px); /* 设置宽度为屏幕宽度减去左右内边距 */
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); /* 可选，添加阴影以增强视觉效果 */
}

/* 行李清单内容样式 */
.packing-list {
  text-align: center;
}

/* 标签样式 */
.tags {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
  margin-bottom: 20px;
}

.tag-row {
  display: flex;
  gap: 10px;
  justify-content: center;
}

/* 标签样式 */
.tag {
  background-color: #e0f7fa;
  color: #333;
  padding: 5px 10px;
  border-radius: 15px;
  font-size: 20px;
  display: inline-flex;
  align-items: center;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  animation: fadeIn 0.5s ease-in-out;
}

/* 插图样式 */
/* 插图样式 */
/* 插图样式 */
.illustration {
  width: 150px;
  height: auto;
  display: block; /* 使图片块级显示，以便居中 */
  margin-left: auto; /* 水平居中 */
  margin-right: auto; /* 水平居中 */
  margin-top: 20px; /* 与上方元素的间距 */
  margin-bottom: 20px; /* 与下方元素的间距 */
}

/* 提示文字样式 */
.reminder-text {
  font-size: 16px;
  color: #555;
  text-align: center; /* 水平居中文本 */
  margin-top: 5px; /* 与上方元素的间距 */
  line-height: 1.6;
  white-space: pre-line;
  margin-bottom: 25px; /* 与下方元素的间距 */
}

/* 添加按钮样式 */
/* 添加按钮样式 */
.add-button {
  position: fixed; /* 固定定位 */
  bottom: 20px; /* 距离底部20px */
  left: 50%; /* 距离左侧50% */
  transform: translateX(-50%); /* 向左移动自身宽度的一半，实现水平居中 */
  width: 90%; /* 按钮宽度为白色区域宽度的90% */
  background-color: #4a90e2;
  color: white;
  padding: 10px 20px;
  border-radius: 20px;
  font-size: 16px;
  z-index: 100; /* 确保按钮在其他内容之上 */
}

/* 标签动画 */
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: scale(0.8);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}
</style>
