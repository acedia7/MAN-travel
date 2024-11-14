<template>
  <view class="travel-plan-overview-page">
    <!-- 行程名 -->
    <view class="trip-name">福州三日游 | 在三坊七巷感受榕城秋日古韵</view>
    <!-- 旅行时间 -->
    <view class="travel-time">10.1 - 10.3  3天2晚</view>
    <!-- 行程标题及横线 -->
    <view class="trip-section">
      <view class="trip-title">行程</view>
      <view class="horizontal-line"></view>
    </view>
    <!-- 白色矩形区域 -->
    <view class="white-rectangle">
      <!-- 行程天数按钮 -->
      <view class="day-buttons">
        <button v-for="(day, index) in days" :key="index" :class="['day-button', { active: currentDay === day }]"
          @click="setCurrentDay(day)">{{ day }}</button>
      </view>
      <!-- 行程概览标题 -->
      <view class="overview-title">行程概览</view>
      <!-- 地图区域，使用 div 作为地图容器，添加 map-container 类名 -->
      <div id="map-container" class="map-container"></div>
      <!-- 每天行程信息 -->
      <view class="daily-trips">
        <view v-for="(dayTrip, index) in dailyTrips" :key="index" class="daily-trip">
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
    <view class="weather-info">
      <view v-for="(weather, index) in weatherForecast" :key="index" class="weather-item">
        <view>{{ weather.city }}</view>
        <view>{{ weather.date }}  {{ weather.weekday }}  {{ weather.icon }}  {{ weather.condition }}
          {{ weather.temperature }}</view>
      </view>
    </view>
  </view>
</template>

<script>
import AMapLoader from '@amap/amap-jsapi-loader';
import { useRouter } from 'vue-router';

export default {
  data() {
    return {
      // 假设行程天数示例，实际需根据用户行程动态生成
      days: ['总览', 'DAY1', 'DAY2', 'DAY3'],
      currentDay: '总览',
      // 每天行程信息示例，实际需根据用户行程动态生成
      dailyTrips: [
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
      ],
      // 天气预报信息示例，实际需根据旅行期间天气数据动态生成
      weatherForecast: [
        {
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
      map: null,
      // 新增地点坐标数据示例，格式为地点名称对应坐标数组（经度，纬度），实际需准确获取对应坐标
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
      }
    };
  },
  mounted() {
    // 在组件挂载后初始化地图
    this.initMap();
  },
  methods: {
    initMap() {
      const that = this;
      AMapLoader.load({
        key: 'd702b20c1d0b7a34eaffae39500d2210', // 替换为你的高德地图 API 密钥
        version: '2.0',
        plugins: ['AMap.ToolBar']
      }).then((AMap) => {
        that.map = new AMap.Map('map-container', {
          center: [119.306238, 26.075302],
          zoom: 12
        });
        that.map.addControl(new AMap.ToolBar());

        // 用于存储每天行程区域的标记
        const dayMarkers = [];
        // 定义每天行程对应的颜色（示例颜色，可根据喜好修改）
        const dayColors = {
          DAY1: '#FF5733',
          DAY2: '#33FF57',
          DAY3: '#5733FF'
        };

        // 遍历每天行程信息，添加标记和连线
        this.dailyTrips.forEach((dayTrip, index) => {
          const places = dayTrip.places.split(' - ');
          let prevMarker = null;
          places.forEach((place, innerIndex) => {
            const coordinates = this.placeCoordinates[place];
            if (coordinates) {
              const marker = new AMap.Marker({
                position: coordinates,
                map: that.map,
                title: place
              });
              if (prevMarker) {
                // 根据当天行程设置连线颜色
                const polyline = new AMap.Polyline({
                  path: [prevMarker.getPosition(), marker.getPosition()],
                  map: that.map,
                  strokeColor: dayColors[dayTrip.day],
                  strokeWeight: 3
                });
              }
              prevMarker = marker;
            }
          });

          // 获取当天行程区域的中心坐标（简单取第一个地点坐标，可优化为计算平均坐标等更合理方式）
          const firstPlace = places[0];
          const centerCoordinates = this.placeCoordinates[firstPlace];
          if (centerCoordinates) {
            // 创建代表当天行程的标记（如DAY1、DAY2、DAY3）
            const dayMarker = new AMap.Marker({
              position: centerCoordinates,
              map: that.map,
              title: dayTrip.day,
              icon: new AMap.Icon({
                size: new AMap.Size(25, 25),
                // 这里需要替换为真实的图标地址或者使用Base64编码的图标数据等合适方式来显示图标，示例只是占位
                imageSize: new AMap.Size(25, 25)
              }),
              offset: new AMap.Pixel(-12, -12), // 调整图标偏移，使其居中显示，可根据实际图标大小调整
              // 设置标记颜色（和当天行程连线颜色一致）
              label: {
                content: dayTrip.day,
                offset: new AMap.Pixel(0, 0),
                style: {
                  color: dayColors[dayTrip.day],
                  fontSize: '16px',
                  fontWeight: 'bold'
                }
              }
            });
            dayMarkers.push(dayMarker);
          }
        });

        // 连线每天行程的代表标记（DAY1、DAY2、DAY3之间连线）
        for (let i = 0; i < dayMarkers.length - 1; i++) {
          const polyline = new AMap.Polyline({
            path: [dayMarkers[i].getPosition(), dayMarkers[i + 1].getPosition()],
            map: that.map,
            strokeColor: dayColors[this.dailyTrips[i].day],
            strokeWeight: 3
          });
        }
      }).catch((error) => {
        console.error('高德地图加载失败：', error);
      });
    },
    setCurrentDay(day) {
      const router = useRouter();
      if (day === '总览') {
        this.currentDay = day;
        router.push({ name: 'travelPlanOverview' }); // 跳转到TravelPlanOverview页面（这里可能是刷新当前页面之类的逻辑，具体看路由配置）
      } else {
        this.currentDay = day;
        router.push({ name: 'travelPlanDetail', params: { day } }); // 跳转到TravelPlanDetail页面，并传递天数参数
      }
    }
  }
};
</script>

<style lang="scss">
.travel-plan-overview-page {
  background-color: lightblue;
  padding: 20px;

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

  // 行程标题及横线所在区域样式
.trip-section {
    text-align: left;
    margin-bottom: 10px;

    // 行程标题样式
.trip-title {
      font-size: 20px;
      font-weight: bold;
      margin-bottom: 5px;
    }

    // 横线样式
.horizontal-line {
      width: 100%;
      height: 1px;
      background-color: gray;
    }
  }

  // 白色矩形区域样式
.white-rectangle {
    background-color: white;
    border-radius: 20px;
    padding: 20px;
    margin-bottom: 20px;

    // 行程天数按钮样式
.day-buttons {
      display: flex;
      justify-content: space-around;
      margin-bottom: 10px;

  .day-button {
        padding: 1px 8px;
        border: 1px solid #808080; // 未点击时边框深灰色
        border-radius: 20px;
        background-color: white;
        color: #808080; // 未点击时字体深灰色
        cursor: pointer;
        font-weight: normal; // 未点击时字体正常粗细
        transition: all 0.3s ease; // 添加过渡效果，使样式变化更平滑

        &.active {
          border: 2px solid black; // 点击后边框加粗且为黑色
          color: black; // 点击后字体变为黑色
          font-weight: bold; // 点击后字体加粗
        }
      }
    }

    // 行程概览标题样式
.overview-title {
      font-size: 18px;
      font-weight: bold;
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