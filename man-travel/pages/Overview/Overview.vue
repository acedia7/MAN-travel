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
			<!-- 行程天数按钮 -->
			<view class="day-buttons">
				<!-- 行程天数按钮 -->
				<button v-for="(day, index) in days" :key="index"
					:class="['day-button', { active: currentDay === day }]"
					@click="handleDayClick(day)">{{ day }}</button>
			</view>
			<!-- 行程概览标题 -->
			<view class="overview-title">行程概览</view>
			<!-- 地图区域，使用 div 作为地图容器，添加 map-container 类名 -->
			<div id="map-container" class="map-container"></div>
			<!-- 每天行程信息 -->
			<view class="daily-trips">
				<view v-for="(dayTrip, index) in dailyTrips" :key="index" class="daily-trip"
					@click="handleDayClick(dayTrip.day)">
					<view class="day-label">{{ dayTrip.day }}</view>
					<view class="city-label">{{ dayTrip.city }}</view>
					<view class="places-label">{{ dayTrip.places }}</view>
				</view>
				<!-- 待规划行程 -->
				<view class="to-plan-trip">待规划</view>
			</view>

		</view>
		<!-- 天气预报标题 -->
		<view class="weather-title">天气预报</view>
		<!-- 天气预报区域 -->
		<view class="weather-info" v-if="weatherForecast && weatherForecast.length > 0">
			<view v-for="(weather, index) in weatherForecast" :key="index" class="weather-item">
				<view>{{ weather.city }}</view>
				<view>{{ weather.date }} {{ weather.weekday }} {{ weather.icon }} {{ weather.condition }}
					{{ weather.temperature }}
				</view>
			</view>
		</view>
		<!-- 如果没有天气信息，显示为空 -->
		<view v-else>
			<view>暂无天气信息</view>
		</view>
	</view>
</template>

<script>
    import AMapLoader from '@amap/amap-jsapi-loader';
    import { useRoute, useRouter } from 'vue-router';
    import { ref, onMounted } from 'vue';

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
            // 从服务器获取行程数据
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

            // 初始化地图
            initMap(placeCoordinates) {
                const that = this;
                AMapLoader.load({
                    key: 'd702b20c1d0b7a34eaffae39500d2210',
                    version: '2.0',
                    plugins: ['AMap.ToolBar']
                }).then((AMap) => {
                    that.map = new AMap.Map('map-container', {
                        center: [119.306238, 26.075302],
                        zoom: 12
                    });
                    that.map.addControl(new AMap.ToolBar());

                    const dayMarkers = [];
                    const dayColors = {
                        DAY1: '#FF5733',
                        DAY2: '#33FF57',
                        DAY3: '#5733FF'
                    };

                    this.dailyTrips.forEach((dayTrip) => {
                        const places = dayTrip.places.split(' - ');
                        let prevMarker = null;
                        places.forEach((place) => {
                            const coordinates = placeCoordinates[place];
                            if (coordinates) {
                                const marker = new AMap.Marker({
                                    position: coordinates,
                                    map: that.map,
                                    title: place
                                });
                                if (prevMarker) {
                                    const polyline = new AMap.Polyline({
                                        path: [prevMarker.getPosition(), marker.getPosition()],
                                        map: that.map,
                                        strokeColor: dayColors[dayTrip.day],
                                        strokeWeight: 6
                                    });
                                }
                                prevMarker = marker;
                            }
                        });
                    });

                    const firstDayTrip = that.dailyTrips[0];
                    if (firstDayTrip) {
                        const firstPlace = firstDayTrip.places.split(' - ')[0];
                        const coordinates = placeCoordinates[firstPlace];
                        if (coordinates) {
                            that.map.setCenter(coordinates);
                            that.map.setZoom(12);
                        }
                    }
                });
            },

            // 概览页的 navigateToPage 方法
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

            // 点击“旅行账单”按钮的跳转逻辑
            handleShouyeClick() {
                this.navigateToPage('/pages/shouye/shouye');
            },
           
            // 点击“行李清单”按钮的跳转逻辑
            handleXingliClick() {
                this.navigateToPage('/pages/xingli/xingli');
            },

            // 点击行程天数按钮后的跳转逻辑
            handleDayClick(day) {
                if (!this.tripId) {
                    console.error('未找到 trip_id 参数');
                    return;
                }

                if (day !== '总览') {
                    const selectedTrip = this.dailyTrips.find((trip) => trip.day === day);
                    if (selectedTrip) {
                        let places = selectedTrip.places;
                        const placesEncoded = encodeURIComponent(places);
                        uni.navigateTo({
                            url: `/pages/DayDetail/DayDetail?day=${day}&id=${this.tripId}&places=${placesEncoded}`
                        });
                    }
                } else {
                    this.setCurrentDay(day);
                }
            },

            // 设置当前展示的天数
            setCurrentDay(day) {
                this.currentDay = day;
                const trip = this.tripsById[this.tripId];

                if (trip) {
                    if (day !== '总览') {
                        const selectedTrip = this.dailyTrips.find((trip) => trip.day === day);
                        if (selectedTrip) {
                            const firstPlace = selectedTrip.places.split(' - ')[0];
                            const coordinates = trip.placeCoordinates[firstPlace];
                            if (coordinates) {
                                this.map.setCenter(coordinates);
                                this.map.setZoom(14);
                            }
                        }
                    } else {
                        const firstDayTrip = this.dailyTrips[0];
                        const firstPlace = firstDayTrip.places.split(' - ')[0];
                        const coordinates = trip.placeCoordinates[firstPlace];
                        if (coordinates) {
                            this.map.setCenter(coordinates);
                            this.map.setZoom(12);
                        }
                    }
                }
            }
        }
    };
</script>



<style lang="scss">
	.travel-plan-overview-page {
		background-color: #e1f0ff;
		padding: 20px;
		min-height: 100vh; // 100% 视口高度
		box-sizing: border-box;


		/* 返回按钮容器样式 */
		.back-button-container {
			margin-bottom: 10px;
			/* 设置与下方内容的间距 */
		}

		/* 返回按钮图标样式 */
		.back-button {
			width: 30px;
			height: 30px;
			cursor: pointer;
		}

		/* 行程名样式 */
		.header {
			margin-top: 10px;
			/* 设置与返回按钮的间距 */
			margin-bottom: 10px;
			/* 设置与下方内容的间距 */
		}

		// 行程名样式
		.trip-name {
			font-size: 24px;
			font-weight: bold;
			text-align: left;
			margin-bottom: 10px;
		}

		// 旅行时间样式
		.travel-time {
			font-size: 16px;
			color: dimgray;
			text-align: left;
			margin-bottom: 10px;
		}

		.trip-section {
			display: flex;
			flex-direction: column;
			/* 使其内部子项垂直排列 */
			align-items: flex-start;
			/* 确保内容从左侧对齐 */
			text-align: left;
			/* 保证文本左对齐 */
			border: none;
			/* 移除任何边框 */
			padding: 0;
			/* 确保没有多余的内边距 */


			.button-group {
				display: flex;
				/* 使用 flex 布局让按钮并排 */
				align-items: center;
				/* 垂直居中对齐按钮文本 */
				justify-content: flex-start;
				/* 水平方向左对齐 */
				gap: 40rpx;
				/* 使用 rpx 确保按钮之间有合适的间距（适合小程序环境） */
				margin-left: 15rpx;
				/* 确保按钮组容器没有左侧内边距或外边距 */
				padding-left: 0;
				/* 确保没有额外的左侧填充 */
			}

			.btn-title {
				font-size: 20px;
				/* 字体大小 */
				font-weight: bold;
				/* 字体加粗 */
				color: black;
				/* 黑色字体 */
				background: none;
				/* 移除按钮的背景 */
				border: none;
				/* 移除按钮的边框 */
				outline: none;
				/* 去掉焦点时的边框 */
				padding: 0;
				/* 无额外内边距 */
				cursor: pointer;
				/* 鼠标悬浮显示手型 */
				text-decoration: none;
				/* 去掉默认的文本装饰，比如下划线 */
				transition: color 0.3s ease;
				/* 颜色渐变过渡效果 */
			}

			.btn-title:hover {
				color: gray;
				/* 悬停时字体颜色变灰 */
			}

			.btn-title:focus {
				outline: none;
				/* 点击时不显示边框 */
			}

			.horizontal-line {
				width: 100%;
				height: 1px;
				background-color: gray;
				margin-top: 10px;
				/* 保证横线和按钮之间有足够的间隔 */
			}
		}

		// 白色矩形区域样式
		.white-rectangle {
			background-color: white;
			border-radius: 20px;
			padding: 20px;
			margin-bottom: 20px;

			/* 行程天数按钮样式 */
			.day-buttons {
			  display: flex;
			  overflow-x: auto; /* 使容器可以左右滑动 */
			  white-space: nowrap; /* 防止子元素换行 */
			  margin-bottom: 5px;
			}
			
			.day-button {
			  flex: 0 0 auto; /* 防止按钮缩放，保持固定宽度 */
			  width: 70px; /* 设置固定的宽度，可以根据需要调整 */
			  height: 45px;
			  margin-right: 8px; /* 添加按钮间的间距 */
			  border: 1px solid #808080; /* 未点击时边框深灰色 */
			  border-radius: 20px;
			  background-color: white;
			  color: #808080; /* 未点击时字体深灰色 */
			  cursor: pointer;
			  font-weight: normal; /* 未点击时字体正常粗细 */
			  transition: all 0.3s ease; /* 添加过渡效果，使样式变化更平滑 */
			}
			
			.day-button.active {
			  border: 2px solid black; /* 点击后边框加粗且为黑色 */
			  color: black; /* 点击后字体变为黑色 */
			  font-weight: bold; /* 点击后字体加粗 */
			}

			// 行程概览标题样式
			.overview-title {
				font-size: 18px;
				font-weight: bold;
				margin-top: 25px;
				margin-bottom: 10px;
			}

			// 地图容器样式
			.map-container {
				width: 100%;
				height: 200px; // 根据需求调整地图容器高度
				border-radius: 20px;
				margin-bottom: 20px;
			}

			// 每天行程信息样式
			.daily-trips {
				display: flex;
				flex-wrap: wrap;
				justify-content: space-between;

				.daily-trip {
					width: 100%; // 修改为占满父容器宽度
					height: 80px; // 设置固定高度为80px
					background-color: white;
					box-shadow: 0 0 5px lightgray;
					padding: 10px;
					margin-bottom: 20px;
					border-radius: 10px;

					.day-label {
						font-size: 16px;
						font-weight: bold;
						margin-bottom: 5px;
					}

					.city-label {
						font-size: 14px;
						color: lightgray;
						margin-bottom: 5px;
					}

					.places-label {
						font-size: 14px;
					}
				}

				.to-plan-trip {
					width: 100%;
					background-color: white;
					box-shadow: 0 0 5px lightgray;
					padding: 10px;
					margin-bottom: 20px;
					border-radius: 10px;
					font-size: 16px;
					font-weight: bold;
					text-align: center;
				}
			}
		}

		// 天气预报标题样式
		.weather-title {
			font-size: 18px;
			font-weight: bold;
			margin-bottom: 10px;
		}

		// 天气预报区域样式
		.weather-info {
			background-color: white;
			box-shadow: 0 0 5px lightgray;
			padding: 10px;
			border-radius: 10px;

			.weather-item {
				margin-bottom: 10px;
			}
		}
	}
</style>