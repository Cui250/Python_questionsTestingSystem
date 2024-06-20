<template>
  <div>
    <el-container style="height: 100%; ">
      <!--    侧边栏部分-->
      <InterFace></InterFace>
      <!--      头部部分-->
      <el-container>
        <el-header style="text-align: right; font-size: 12px; border-bottom: 2px solid #ccc; line-height: 60px;background-color: white">
          <div class="box">
            <div class="box_left">
              <el-breadcrumb separator="/">
                <el-breadcrumb-item  style="font-weight: bold; color: black;">我的信息</el-breadcrumb-item>
                <el-breadcrumb-item>我的考试</el-breadcrumb-item>
              </el-breadcrumb>
            </div>
            <div class="box_right">
              <el-dropdown style="width: 70px; cursor: pointer;">
                <span>{{user.userName}}</span> <i class="el-icon-arrow-down" style="margin-left: 5px"></i>
                <el-dropdown-menu slot="dropdown">
                  <el-dropdown-item><router-link to="/PersonalInf" style="text-decoration: none; color: black;">个人信息</router-link></el-dropdown-item>
                  <el-dropdown-item><router-link to="/login" style="text-decoration: none; color: black;">退出</router-link></el-dropdown-item>
                </el-dropdown-menu>
              </el-dropdown>
            </div>
          </div>
        </el-header>
        <!--       主体部分-->
        <el-main>
          <!--        一些按钮-->
          <el-button type="success" @click = 'dialogFormVisible=true' >开始考试</el-button>

          <br><br>

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



          <div v-if="checked " style=" overflow-y: auto; height: 650px; border: 1px solid #ddd; box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); background-color: #f9f9f9;">
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
                    <li v-for="(option, i) in question.options" :key="i"  :style="{ color: determineOptionColor(j, i) }">
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

          <div ref="scoreChart" style="width: 600px;height:400px;"></div>
          <div>
            {{scoreDate}}
          </div>



          <!-- 开始考试弹窗-->
          <el-dialog title="考试须知" :visible.sync="dialogFormVisible" width="30%" :before-close="handleClose">
            <span>1. 电脑：台式或笔记本电脑一台，操作系统须为Windows11、Windows10、Windows7，或 Mac
                  OS10.15.6 及以上系统。
                  2. 浏览器：须为最新版谷歌Chrome浏览器（推荐使用），或最新版 360 极速浏览器。
                  3. 考试客户端：须从设备检测及模拟试考网址或者正式考试网址下载并安装最新版考试安全客
                   户端。4. 双摄像头：①电脑自带前置摄像头或外接摄像头；②用于监考的手机摄像头（手机须安装
                最新版微信），建议准备手机支架。5. 麦克风和扬声器：电脑自带或外接。6. 网络：网络带宽 50Mbps及以上，下载速度 5MB/S及以上。
                 . 请确保上述设备可正常工作，用电设备电量充足（建议全程使用外接电源），网络稳定</span>
            <span slot="footer" class="dialog-footer">
          <el-button @click="dialogFormVisible = false">取 消</el-button>
          <el-button type="primary" @click="begintest">开始考试</el-button>
            </span>
          </el-dialog>


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
      dialogFormVisible:false, //弹窗显示
      testingPaper: {
        paperId: '',
        course: '',
        questions: {},
      },
      record: {},
      records: [],
      // 存储 ECharts 实例
      scoreChart: null,
      // 模拟的分数数据，每个对象包含日期和分数
      scoreDate: [
        // { date: '2021-06-10 22:04:05', score: 88 },
        // { date: '2021-06-15 22:04:05', score: 92 },
        // { date: '2021-06-20 22:04:05', score: 85 },
        // 可以添加更多数据点
      ],

    }
  },
  mounted() {
    this.initScoreChart();
  },
  components:{
    InterFace
  },
  computed:{
    user() {
      return this.$store.getters.getUser;
    }
  },
  created() {
    // 请求分页查询数据
    this.fetchTestingRecord()
  },

  methods: {
    //请求数据
    async fetchTestingRecord() {
      try {
        // 发起获取测试记录的请求
        const response = await axios.get('http://127.0.0.1:5000/testing/', {
          headers: {
            'Content-Type': 'application/json'
          }
        });

        // 检查响应代码
        if (response.data.code === 200) {
          // 请求成功
          this.$message.success('加载数据成功，真不容易');
          this.testingRecordFetched = true;
          this.records = response.data.records; // 保存测试记录到this.records

        } else {
          // 请求失败
          this.$message.error(response.data.message || '请求提交失败');
        }
      } catch (error) {
        // 捕获并处理错误
        let errorMessage = error.response ? error.response.data.message : error.message;
        this.$message.error("请求提交失败: " + errorMessage);
        console.error("请求提交发生错误:", error);
      }
    },
    determineOptionColor() {
      return "initial";
      // // 假设每个问题选项都有一个唯一的 ID，并且这个 ID 与 results 数组中的某个对象的 ID 相匹配
      // const result = this.results.find(result => result === optionId);
      //
      // // 如果找到了对应的结果，并且答案是正确的
      // if (result && result.correct === 'true') {
      //   return 'green'; // 正确答案的样式
      // } else {
      //   return 'red'; // 错误答案的样式
      // }
    },
    begintest() {
      this.dialogFormVisible = false,
          this.$router.push('/Test')
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
    // 初始化图表的方法
    initScoreChart() {
      // 检查 scoreDate 是否已经初始化
      if (!this.scoreDate || this.scoreDate.length === 0) {
        this.fetchScoreData();
      } else {
        // 如果已经有数据，直接创建图表
        this.createScoreChart();
      }
    },

    // 请求分数数据的方法
    fetchScoreData() {
      axios.post('http://127.0.0.1:5000/testing/', {
        fetchScoreDate: true
      }, {
        headers: {
          'Content-Type': 'application/json'
        }
      })
          .then(response => {
            if (response.data.code === 200) {
              // 假设返回的数据格式为 [{date: '日期字符串', score: 分数}, ...]
              this.scoreDate = response.data.scoreDate;
              this.createScoreChart(); // 数据获取成功后创建图表
            } else {
              this.$message.error(response.data.message || '获取分数数据失败');
            }
          })
          .catch(error => {
            console.error('请求失败:', error);
            this.$message.error('无法加载数据，请检查网络连接或服务器状态');
          });
    },

    // 根据获取的数据创建图表的方法
    createScoreChart() {
      // 确保 this.$refs.scoreChart 是有效的 DOM 元素
      if (!this.$refs.scoreChart) return;

      // 使用 echarts 初始化图表
      this.scoreChart = echarts.init(this.$refs.scoreChart);

      // 提取日期和分数
      // 提取日期和分数
      const dates = this.scoreDate.map(item => new Date(item.date).toLocaleDateString());
      const scores = this.scoreDate.map(item => item.score);

      // 准备图表的配置项
      const option = {
        title: { text: '用户考试分数随时间变化' },
        xAxis: {
          type: 'category',
          data: dates
        },
        yAxis: {
          type: 'value',
          axisLabel: {
            formatter: '{value} 分'
          }
        },
        series: [{
          data: scores,
          type: 'line',
          smooth: true, // 曲线平滑
        }]
      };
      // 使用配置项设置图表
      this.scoreChart.setOption(option);
    },

    // 组件销毁前销毁 ECharts 实例的方法
    beforeDestroy() {
      if (this.scoreChart) {
        this.scoreChart.dispose();
      }
    },
    back(){
      this.checked = false;
    },
  },


}
</script>

<style>

</style>