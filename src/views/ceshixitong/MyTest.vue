<template>
  <div>
    <el-container style="height: 100%; ">
      <!--    侧边栏部分-->
      <InterFace></InterFace>
      <!--      头部部分-->
      <el-container>
        <el-header style="text-align: right; font-size: 12px; border-bottom: 2px solid #ccc; line-height: 60px;background-color: white">

        </el-header>
        <!--       主体部分-->
        <el-main>

          <!--        一些按钮-->

          <div  style=" overflow-y: auto; height: 45vw; border: 1px solid #ddd; box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); background-color: #f9f9f9;">

            <div class="chart-container">
            <!-- 图表 -->
            <div ref="stackedLineChart1" style="width: 80vw; height: 21vw;"></div>

            <!-- 用户选择下拉列表 -->
            <div class="user-select-container">
              <el-select v-model="selectedUserId" placeholder="请选择用户" @change="handleUserChange" size="small">
                <el-option
                    v-for="user in userOptions"
                    :key="user.value"
                    :label="user.label"
                    :value="user.value">
                </el-option>
              </el-select>
            </div>
          </div>

            <br>
            <hr>
            <br>

          <div class="chart-container">
            <!-- 图表 -->
            <div ref="stackedLineChart" style="width: 70vw; height: 21vw;"></div>

            <!-- 用户选择下拉列表 -->
            <div class="user-select-container">

              <el-select v-model="selectedCourse" placeholder="请选择课程" @change="handleCourseChange">
                <el-option
                    v-for="course in courseOptions"
                    :key="course.value"
                    :label="course.label"
                    :value="course.value">
                </el-option>
              </el-select>

            </div>
          </div>



          <!--                  表格，点击查看后隐藏-->
            <el-table :data="records" border v-if="!checked">
              <el-table-column prop="id" label="ID" width="120">
              </el-table-column>
              <el-table-column prop="userId" label="用户id" width="120">
              </el-table-column>
              <el-table-column prop="paperId" label="试卷id" width="120">
              </el-table-column>
              <el-table-column prop="course" label="所属课程" width="120">
              </el-table-column>
              <el-table-column prop="score" label="分数" width="200">
              </el-table-column>
              <el-table-column label="操作" width="180">
                <template slot-scope="scope">
                  <el-button type="primary" size="mini" @click="check(scope.row) ">查看</el-button>


                </template>
              </el-table-column>


            </el-table>
            <el-button v-if="checked" type="success" size="mini" @click="back">返回</el-button>
            <div v-if="checked">
              <div  style="margin-left: 5%">
                <p>测试时间：{{ record.testingTime }}</p>
                <p>测试用户id:{{record.userId}}</p>
                <p>测试试卷id:{{record.paperId}}</p>
                <p>测试得分:{{record.score}}</p>
                <p>测试详情:</p>
                <br>
                <div>
                  <!-- 保持原有页面样式 -->
                  <div v-for="(question, index) in testingPaper.questions" :key="index" >
                    <p>{{question.id}}.{{ question.question }}</p>
                    <ul>
                      <li v-for="(option, i) in question.options" :key="i" >
                        <!-- 使用 span 元素显示选项内容 -->
                        <span>{{ String.fromCharCode(65 + i) }}.{{ option }}</span>
                      </li>
                    </ul>
                    <div v-for="(situation, index) in record.answerSituation" :key="index"  >


                      <div v-if="question.id === situation.questionId">
                        <p style="color: green">正确答案：{{situation.correctAnswer}}</p>
                        <p :style="{ color: situation.correct === 'true' ? 'green' : 'red' }">你选择了：{{situation.chosen}}</p>
                        <p :style="{ color: situation.correct === 'true' ? 'green' : 'red' }">是否做对:{{ situation.correct === 'true' ? '是' : '否' }}</p>
                        <p>本题得分:{{situation.score}}</p>
                        <p>解析：{{question.analysis}}</p>
                        <p>知识点：{{question.knowledge_point}}</p>
                        <p>难度系数：{{question.level}}</p>
                      </div>
                    </div>
                    <!-- 空间留白 -->
                    <div style="margin-bottom: 20px;"></div>
                  </div>
                </div>

                <hr>
                <br>
              </div>

            </div>

          </div>


        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script>
// import request from "@/utils/request";
import axios from "axios";
import InterFace from "@/views/ceshixitong/InterFace.vue";
import * as echarts from 'echarts';


export default {
  data() {

    return {
      checked: false,
      questions:[],
      testingPaper: {
        paperId: '',
        course: '',
        questions: {},
      },
      record: {},
      records: [],
      userUserName: {},
      // 存储 ECharts 实例
      stackedLineChart: null,
      stackedLineChart1: null, // ECharts 实例（如果需要在组件的其它地方访问）
      // 模拟的分数数据，每个对象包含日期和分数
      scoreDate: [
        // { date: '2021-06-10 22:04:05', score: 88 },
        // { date: '2021-06-15 22:04:05', score: 92 },
        // { date: '2021-06-20 22:04:05', score: 85 },
        // 可以添加更多数据点
      ],
      // 如果您的堆叠折线图的数据也需要作为初始状态，可以添加如下：
      stackedLineData: {
        courses: [], // 存储课程和对应的用户及分数数据
        allDates: [] // 存储所有考试日期
      },
      selectedCourse: '', // 当前选中的课程,
      selectedUserId: '',
      stackedLineData1: {
        userId: '',
        xAxisData: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
        seriesData: [
          { name: 'Email', data: [120, 132, 101, 134, 200, 150, 180] },
          { name: 'Union Ads', data: [220, 182, 191, 234, 290, 330, 310] },
          // 可以根据需要添加更多系列的默认数据
        ],
      },

    }
  },

  components:{
    InterFace
  },
  computed: {
    // 使用 Vuex store 获取用户信息
    user() {
      return this.$store.getters.getUser;
    },
    // 根据records生成课程选项，使用集合去除重复课程
    courseOptions() {
      const coursesSet = new Set();
      this.records.forEach(record => coursesSet.add(record.course));
      return Array.from(coursesSet).map(course => ({
        value: course,
        label: course,
      }));
    },
    // 根据records生成用户选项，使用集合去除重复用户
    userOptions() {
      const userIdsSet = new Set(this.records.map(record => record.userId));
      return Array.from(userIdsSet).map(userId => {
        return {
          // 这里转换为string是为了和selectedUserId完全匹配，确保列表的默认被选值正常显示
          value: userId.toString(),
          label: this.userUserName[userId] || userId, // 使用userName作为label，如果没有userName则使用userId
        };
      });
    },
  },

  mounted() {
    // 请求数据，不要在这里初始化图表
    this.fetchTestingRecord();
  },

  methods: { // 根据选中的课程更新图表
    updateChartByCourse() {
      this.stackedLineChart.dispose();
      // 重新准备图表配置项并更新图表
      this.initStackedLineChart();
    },

    // 根据选中的用户更新图表
    updateChartByUser() {
      this.stackedLineChart1.dispose();
      // 重新准备图表配置项并更新图表
      this.initStackedLineChart1();
    },

    // 处理课程变化
    handleCourseChange(newValue) {
      this.selectedCourse = newValue;
      this.updateChartByCourse();
    },

    // 处理用户变化
    handleUserChange(newValue) {
      this.selectedUser = newValue;
      this.updateChartByUser();
    },
//请求数据
    async fetchTestingRecord() {
      try {
        const response = await axios.get('http://127.0.0.1:5000/testing/');
        if (response.data.code === 200) {
          this.records = response.data.records;
          this.stackedLineData.courses = response.data.dataForPerCourse.courses;
          this.stackedLineData.allDates = response.data.dataForPerCourse.allDates;
          this.selectedCourse = this.stackedLineData.courses[0].course;
          this.stackedLineData1 = response.data.dataForPerUser;
          this.userUserName = response.data.userUserName;
          // this.selectedUserId = this.records.length > 0 ? this.records[0].userId : ''; // 假设取第一个记录的用户ID
          // 确保数据加载完成后再初始化图表

        }
        this.selectedUserId = Object.keys(this.stackedLineData1)[0]; // 选择第一个用户ID
        // 确保数据加载完成后再初始化图表
        this.initStackedLineChart();
        this.initStackedLineChart1();
      } catch (error) {
        let errorMessage = error.response ? error.response.data.message : error.message;
        this.$message.error("数据请求失败: " + errorMessage);
        console.error("请求数据发生错误:", error);
      }
    },
    async fetchTestingPaper() {
      // 验证是否成功传入试卷id
      if (!this.testingPaper.paperId) {
        // 如果没有传入试卷id，返回一个rejected Promise
        return Promise.reject(new Error('缺少试卷ID'));
      }

      try {
        // 使用await等待axios的响应
        const response = await axios.post('http://127.0.0.1:5000/testing/', {
          paperId: this.testingPaper.paperId
        }, {
          headers: {
            'Content-Type': 'application/json'
          }
        });
        // 判断响应代码并处理
        if (response.data.code === 200) {
          // 返回response，这样调用者可以访问到它
          this.testingPaper.paperId = response.data.paperId;
          this.testingPaper.questions = response.data.questions;
          this.testingPaper.course = response.data.course;
        } else {
          // 如果响应不是200，使用throw抛出错误
          throw new Error(response.data.message || '试卷获取失败');
        }
      } catch (error) {
        // 捕获并抛出错误
        this.$message.error("试卷获取失败: " + error.message);
        console.error("试卷获取发生错误:", error);
        // 返回一个rejected Promise
        return Promise.reject(error);
      }
    },
    check(record) {
      this.checked = true;
      this.record = record;
      this.testingPaper.paperId = record.paperId;
      this.fetchTestingPaper()


    },


    back() {
      this.checked = false;
    },    // 初始化堆叠折线图的方法
    initStackedLineChart() {
        // 确保 DOM 元素存在且数据已准备好
        if (!this.$refs.stackedLineChart || !this.stackedLineData.courses.length || !this.stackedLineData.allDates.length) {
          console.error('ECharts data is not ready');
          return;
        }
      const myChart = echarts.init(this.$refs.stackedLineChart);
      const option = this.prepareStackedLineOption(this.stackedLineData, this.selectedCourse);
      myChart.setOption(option);
      this.stackedLineChart = myChart;
    },

    // 准备堆叠折线图的配置项
    prepareStackedLineOption(data, selectedCourse) {
      const courseInfo = data.courses.find(course => course.course === selectedCourse);
      if (!courseInfo) return;
      console.log(courseInfo.users.map(user => this.userUserName[user.userId.toString()]))



      return {
        title: {
          text: `${selectedCourse}课程分数变化趋势`
        },
        tooltip: {
          trigger: 'axis'
        },
        legend: {
          data: courseInfo.users.map(user => this.userUserName[user.userId.toString()]),
        },
        grid: {
          left: '3%',
          right: '4%',
          bottom: '3%',
          containLabel: true
        },
        toolbox: {
          feature: {
            saveAsImage: {}
          }
        },
        xAxis: {
          type: 'category',
          boundaryGap: false,
          data: data.allDates
        },
        yAxis: {
          type: 'value'
        },
        series: courseInfo.users.map(user => ({
          name: this.userUserName[user.userId.toString()],
          type: 'line',
          stack: 'score',
          data: user.scores,
        }))
      };
    },

// 初始化特定用户的得分趋势图的方法
// 初始化特定用户的得分趋势图的方法
    initStackedLineChart1() {
      const userId = this.selectedUserId; // 从数据属性中获取当前选中的用户ID
      if (!userId) {
        console.error('No user selected');
        return;
      }

      // 确保 DOM 元素存在
      if (!this.$refs.stackedLineChart1) {
        console.error('The stackedLineChart1 DOM element does not exist.');
        return;
      }

      // 根据用户ID获取数据
      const userCourses = this.stackedLineData1[userId];

      // 初始化 ECharts 实例
      const myChart1 = echarts.init(this.$refs.stackedLineChart1);

      // 准备堆叠折线图的配置项
      const option1 = this.prepareStackedLineOption1(userCourses);

      // 使用配置项设置图表
      myChart1.setOption(option1);

      // 存储 ECharts 实例
      this.stackedLineChart1 = myChart1;
    },

    // 准备特定用户的堆叠折线图配置项
    prepareStackedLineOption1(userCourses) {
      // 假设 userCourses 是一个对象，包含了特定用户的所有课程数据
      const coursesData = Object.entries(userCourses.courses); // 获取所有的课程条目

      return {
        title: {
          text: `${this.userUserName[userCourses.userId.toString()]}的课程得分趋势`
        },
        tooltip: {
          trigger: 'axis'
        },
        legend: {
          data: coursesData.map(([courseName]) => courseName)
        },
        grid: {
          left: '3%',
          right: '4%',
          bottom: '3%',
          containLabel: true
        },
        toolbox: {
          feature: {
            saveAsImage: {}
          }
        },
        xAxis: {
          type: 'category',
          data: coursesData[0][1].dates // 假设所有课程的日期相同，取第一个课程的日期
        },
        yAxis: {
          type: 'value'
        },
        series: coursesData.map(([courseName, courseData]) => ({
          name: courseName,
          type: 'line',
          stack: 'Total',
          data: courseData.scores,
        }))
      };
    },
  },
  beforeDestroy() {
    if (this.stackedLineChart) {
      this.stackedLineChart.dispose();
    }
    if (this.stackedLineChart1) {
      this.stackedLineChart1.dispose();
    }
  },


}
</script>

<style scoped>
.chart-container {
  display: flex;
  align-items: center;
  justify-content: space-between; /* 根据需要调整这个属性 */
}

.user-select-container {
  flex-shrink: 0; /* 确保下拉列表不因图表大小变化而变化 */
  width: 8vw; /* 根据需要设置宽度，或者使用百分比 */
}

/* 可以根据需要添加更多样式 */
</style>