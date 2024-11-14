<template>
  <!-- 原页面容器，只保留总览等按钮以上的部分 -->
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
    <!-- 白色矩形区域，用于放置按钮等 -->
    <view class="white-rectangle">
      <!-- 行程天数按钮及相关操作按钮，放在同一行可右滑 -->
      <scroll-view scroll-x class="day-buttons-container">
        <view class="day-buttons">
          <button
            v-for="(day, index) in days"
            :key="index"
            :class="['day-button', { active: currentDay === day }]"
            @click="setCurrentDay(day)"
          >{{ day }}</button>
        </view>
      </scroll-view>
    </view>
  </view>
  <!-- 新增的页面容器，用于展示具体行程内容，当不是总览时显示 -->
  <view v-if="currentDay!== '总览'" class="travel-plan-detail-page">
    <!-- 行程天数按钮及相关操作按钮 -->
    <!-- 根据当前选择的天展示具体行程内容 -->
    <scroll-view class="daily-trips-scroll" :scroll-y="true">
      <view v-if="currentDay === 'DAY1'" class="day1-trip-section">
        <!-- DAY1行程标题 -->
        <view class="day-header">
          <view class="day-label">{{ 'DAY1' }}</view>
          <view class="add-note" @click="addNote('DAY1')">添加备注</view>
        </view>
        <!-- DAY1行程地点信息，增加了每个行程之间的间隔（通过 margin-bottom） -->
        <view
          v-for="(place, pIndex) in dailyTrips[0].places.split(' - ')"
          :key="pIndex"
          class="place-item"
        >
          <!-- 获取地点图片，优先使用高德地图图片，没有则用定位图标 -->
          <image
            class="place-image"
            :src="getPlaceImage(place)"
            :alt="place"
            mode="aspectFill"
          />
          <view class="place-info">
            <!-- 显示地点类型 -->
            <view class="place-type">{{ getPlaceType(place) }}</view>
            <!-- 显示地点名称 -->
            <view class="place-name">{{ place }}</view>
            <!-- 显示距离和驾车时间 -->
            <view class="place-distance">{{ getDistance(place) }} | {{ getDriveTime(place) }}</view>
            <!-- 展开详情按钮 -->
            <view class="expand-button" @click="expandPlace(place)">展开详情</view>
          </view>
        </view>
        <!-- 添加地点行 -->
        <view class="add-place-row">
          <image class="add-place-image" src="/static/add_icon.png" />
          <view class="add-place-text">添加地点</view>
        </view>
      </view>
      <view v-if="currentDay === 'DAY2'" class="day2-trip-section">
        <view class="day-header">
          <view class="day-label">{{ 'DAY2' }}</view>
          <view class="add-note" @click="addNote('DAY2')">添加备注</view>
        </view>
        <view
          v-for="(place, pIndex) in dailyTrips[1].places.split(' - ')"
          :key="pIndex"
          class="place-item"
        >
          <image
            class="place-image"
            :src="getPlaceImage(place)"
            :alt="place"
            mode="aspectFill"
          />
          <view class="place-info">
            <view class="place-type">{{ getPlaceType(place) }}</view>
            <view class="place-name">{{ place }}</view>
            <view class="place-distance">{{ getDistance(place) }} | {{ getDriveTime(place) }}</view>
            <view class="expand-button" @click="expandPlace(place)">展开详情</view>
          </view>
        </view>
        <view class="add-place-row">
          <image class="add-place-image" src="/static/add_icon.png" />
          <view class="add-place-text">添加地点</view>
        </view>
      </view>
      <view v-if="currentDay === 'DAY3'" class="day3-trip-section">
        <view class="day-header">
          <view class="day-label">{{ 'DAY3' }}</view>
          <view class="add-note" @click="addNote('DAY3')">添加备注</view>
        </view>
        <view
          v-for="(place, pIndex) in dailyTrips[2].places.split(' - ')"
          :key="pIndex"
          class="place-item"
        >
          <image
            class="place-image"
            :src="getPlaceImage(place)"
            :alt="place"
            mode="aspectFill"
          />
          <view class="place-info">
            <view class="place-type">{{ getPlaceType(place) }}</view>
            <view class="place-name">{{ place }}</view>
            <view class="place-distance">{{ getDistance(place) }} | {{ getDriveTime(place) }}</view>
            <view class="expand-button" @click="expandPlace(place)">展开详情</view>
          </view>
        </view>
        <view class="add-place-row">
          <image class="add-place-image" src="/static/add_icon.png" />
          <view class="add-place-text">添加地点</view>
        </view>
      </view>
    </scroll-view>
  </view>
</template>

<script>
import { useRouter } from 'vue-router';
import { onMounted, watch } from 'vue';

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
      ]
    };
  },
  methods: {
    setCurrentDay(day) {
          const router = useRouter();
          if (day === '总览') {
            this.currentDay = day;
            router.push({ name: 'travelPlanOverview' }); // 跳转到TravelPlanOverview页面（这里可能是刷新当前页面之类的逻辑，具体看路由配置）
          } else {
            this.currentDay = day;
            router.push({ name: 'travelPlanDetail', params: { day } }); // 跳转到TravelPlanDetail页面，并传递天数参数
          }
        },
    addNote(day) {
      // 这里可以添加添加备注的逻辑，比如弹出输入框等
      console.log(`添加${day}备注`);
    },
    getPlaceImage(place) {
      // 这里需要根据实际情况获取对应地点的图片链接，假设都使用一个默认图片
      return "/static/logo.png";
    },
    getPlaceType(place) {
      // 简单判断地点类型示例，实际需要更完善的判断逻辑
      if (place.includes("公园") || place.includes("景点") || place.includes("山") || place.includes("杭") || place.includes("江") || place.includes("巷")) {
        return "景点 🏔";
      } else if (place.includes("炸鸡") || place.includes("捞化") || place.includes("美食街")) {
        return "吃喝 🍴";
      } else if (place.includes("站") || place.includes("机场")) {
        return "交通 🚗";
      } else {
        return "其他 💬";
      }
    },
    getDistance(place) {
      // 这里需要根据实际情况计算或获取距离信息，假设固定值
      return "7.8km";
    },
    getDriveTime(place) {
      // 这里需要根据实际情况计算或获取驾车时间信息，假设固定值
      return "27min";
    },
    expandPlace(place) {
      // 这里可以添加展开地点详情的逻辑，比如弹出模态框显示更多信息
      console.log(`展开${place}详情`);
    }
  }
};
</script>

<style lang="scss">
// 原页面（行程概览页）的整体样式
.travel-plan-overview-page {
  background-color: lightblue;
  padding: 20px 20px 5px 20px; // 依次表示上、右、下、左内边距的值

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

  // 白色矩形区域（放置按钮等元素）的样式
 .white-rectangle {
    background-color: white;
    border-radius: 20px;
    padding: 20px;
    margin-bottom: 20px;

    // 可滚动的按钮容器样式，用于让按钮能在同一行并可右滑
   .day-buttons-container {
      display: flex;
      align-items: center;
      white-space: nowrap;
      overflow-x: scroll;
      -webkit-overflow-scrolling: touch;

      // 行程天数按钮组样式
     .day-buttons {
        display: flex;
        flex-wrap: nowrap;
        margin-right: 10px;

        // 单个行程天数按钮样式
       .day-button {
          padding: 1px 8px;
          border: 1px solid #808080;
          border-radius: 20px;
          background-color: white;
          color: #808080;
          cursor: pointer;
          font-weight: normal;
          transition: all 0.3s ease;

          // 激活状态下的按钮样式
          &.active {
            border: 2px solid black;
            color: black;
            font-weight: bold;
          }

          // 鼠标悬停时的按钮样式
          &:hover {
            background-color: lightgray;
            color: black;
          }
        }
      }
    }
  }
}

// 行程详情页面的整体样式
.travel-plan-detail-page {
  background-color: lightblue; // 保持和原页面一样的背景色
  padding: 0px 20px 20px 20px; // 依次表示上、右、下、左内边距的值

  // 可滚动的按钮容器样式，用于让按钮能在同一行并可右滑
 .day-buttons-container {
    display: flex;
    align-items: center;
    white-space: nowrap;
    overflow-x: scroll;
    -webkit-overflow-scrolling: touch;

    // 行程天数按钮组样式
   .day-buttons {
      display: flex;
      flex-wrap: nowrap;
      margin-right: 10px;

      // 单个行程天数按钮样式
     .day-button {
        padding: 1px 8px;
        border: 1px solid #808080;
        border-radius: 20px;
        background-color: white;
        color: #808080;
        cursor: pointer;
        font-weight: normal;
        transition: all 0.3s ease;

        // 激活状态下的按钮样式
        &.active {
          border: 2px solid black;
          color: black;
          font-weight: bold;
        }

        // 鼠标悬停时的按钮样式
        &:hover {
          background-color: lightgray;
          color: black;
        }
      }
    }

    // 操作按钮组（待规划、添加等）样式
   .action-buttons {
      display: flex;
      flex-wrap: nowrap;

      // 待规划按钮样式
     .to-plan-button {
        padding: 1px 8px;
        border: 1px solid #808080;
        border-radius: 20px;
        background-color: white;
        color: #808080;
        cursor: pointer;
        font-weight: normal;
        margin-right: 5px;
		}

        // 鼠标悬停时的按钮样式
        &:hover {
          background-color: lightgray;
          color: black;
        }
      }

      // 添加按钮样式
     .add-button {
        padding: 1px 8px;
        border: 1px solid #808080;
        border-radius: 20px;
        background-color: white;
        color: #808080;
        cursor: pointer;
        font-weight: normal;

        // 鼠标悬停时的按钮样式
        &:hover {
          background-color: lightgray;
          color: black;
        }
      }
    }

    // 编辑按钮样式
   .edit-button {
      padding: 1px 8px;
      border: 1px solid #808080;
      border-radius: 20px;
      background-color: white;
      color: #808080;
      cursor: pointer;
      font-weight: normal;
      margin-left: auto;

      // 鼠标悬停时的按钮样式
      &:hover {
        background-color: lightgray;
        color: black;
      }
    }
  }

  // 具体行程内容可滚动区域的样式
.daily-trips-scroll {
    height: calc(100vh - 200px);
    overflow-y: auto;

    // 不同天行程板块样式
  .day1-trip-section,
  .day2-trip-section,
  .day3-trip-section {
      margin-bottom: 5px;

      // 行程标题头部样式
     .day-header {
		font-size: 25px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 15px;

        // 天数标签样式
      .day-label {
          font-size: 18px;
          font-weight: bold;
        }

        // 添加备注按钮样式
      .add-note {
          font-size: 14px;
          color: blue;
          cursor: pointer;

          &:hover {
            text-decoration: underline;
          }
        }
      }

      // 行程地点项样式
     .place-item {
        background-color: white;
        box-shadow: 0 0 5px lightgray;
        padding: 15px;
        margin-bottom: 20px;
        border-radius: 10px;
        display: flex;
        align-items: center;

        // 地点图片样式
      .place-image {
          width: 80px;
          height: 80px;
          margin-right: 15px;
          border-radius: 10px;
        }

        // 地点信息容器样式
      .place-info {
          flex: 1;

          // 地点类型样式
        .place-type {
            font-size: 14px;
            color: gray;
            margin-bottom: 5px;
          }

          // 地点名称样式
        .place-name {
            font-size: 16px;
            font-weight: bold;
            margin-bottom: 5px;
          }

          // 距离和驾车时间样式
        .place-distance {
            font-size: 14px;
            color: lightgray;
            margin-bottom: 10px;
          }

          // 展开详情按钮样式
        .expand-button {
            font-size: 14px;
            color: blue;
            cursor: pointer;

            &:hover {
              text-decoration: underline;
            }
          }
        }
      }

      // 添加地点行样式
     .add-place-row {
        display: flex;
        align-items: center;
        padding: 10px;
        border-radius: 10px;
        background-color: white;
        box-shadow: 0 0 5px lightgray;
        cursor: pointer;

        // 添加地点图标样式
      .add-place-image {
          width: 20px;
          height: 20px;
          margin-right: 10px;
        }

        // 添加地点文字样式
      .add-place-text {
          font-size: 16px;
          color: gray;
        }
      }
    } 
  }
</style>