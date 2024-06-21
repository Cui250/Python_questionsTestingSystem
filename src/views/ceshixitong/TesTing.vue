<template>

  <el-container>
    <!--  头部-->
    <el-header class="header">考试界面</el-header>
    <!--  主要内容-->
    <el-main class="main" >
      <div class="test">
        <!--    选择试卷id界面，只有未获取试卷而且没有在查看考试记录的情况下才会显示-->
        <div v-if="!paperFetched && !testingRecordFetched">
          <strong style="color: red">重要提醒：请确认您的个人信息无误后再点击开始考试！！！</strong>
          <p>您的用户名:{{ user.userName }}</p>
          <p>您的用户id:{{ user.id }}</p>
          <p>您的邮箱：{{user.email}}</p>
          <span>请选择试卷id号</span>
          <el-select v-model="testingPaper.paperId" placeholder="请选择试卷id" size="medium" style="margin: 10px 0; width: 20vw;">

            <!-- 使用 el-option 来定义选项 -->
            <!-- 循环courses数组中的每个课程名称 -->
            <el-option v-for="course in testingPaperIds" :key="course" :label="course" :value="course">
            </el-option>
          </el-select>
          <!-- 父组件模板 -->
          <el-button type="primary" size="medium" @click="requestForTest">开始考试</el-button>
          <div style="text-align: center; margin-top: 1vw">
            <el-button type="primary" size="medium" @click="back()">返回</el-button>

          </div>

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
          <el-button type="primary" @click="startTesting">开始考试</el-button>
            </span>
        </el-dialog>

        <!--    答题页面，只有在获取到试卷且未提交且没有在查看考试记录的情况之下，才会显示-->
        <div v-if="paperFetched && !submitted && !testingRecordFetched">
          <p>用户名:{{user.userName}}</p>
          <p>用户id:{{user.id}}</p>
          <div v-for="(question, index) in testingPaper.questions" :key="index"  >
            <p>{{question.id}}.{{ question.question }}</p>
            <ul>
              <li v-for="(option, i) in question.options" :key="i">
                <input type="radio" :id="'option_' + index + '_' + i" :name="'answer_' + index" :value="option" v-model="answers[index]">
                <label :for="'option_' + index + '_' + i">{{ String.fromCharCode(65 + i) }}. {{ option }}</label>
                <!--            {{ String.fromCharCode(97 + i) }}：这部分是使用 JavaScript 的 String.fromCharCode 方法动态生成字母标识-->
                <!--            ，从 ‘a’ 开始逐个往后排列。例如，当 i 为 0 时，生成 ‘a’；当 i 为 1 时，生成 ‘b’，以此类推。-->
              </li>
            </ul>

            <!-- 空间留白 -->
            <div style="margin-bottom: 20px;"></div>
            
          </div>
          <el-button @click="submitAnswers" type="primary" round >交卷</el-button>
        </div>


        <!--    结束画面-->
        <!-- 第二个页面 -->

        <div v-if="submitted && !testingRecordFetched">
          <p>考试正常结束</p>
          <p>你的总得分为：{{results.score}}</p>
          <div style="text-align: center; margin-top: 1vw">
            <el-button type="primary" size="medium" @click="back()">返回</el-button>

          </div>
        </div>

      </div>
    </el-main>
  </el-container>
</template>

<script>
import axios from "axios";
export default {
  data() {

    return {
      testingPaper: {
        paperId: '',
        course: '',
        questions: {},
      },
      testingPaperIds: [],
      answers: {},
      results: {},
      testingPaperIdInRecords: [],
      testingPaperInRecords: [],
      paperFetched:false,
      submitted: false,
      testingRecordFetched: false,
      dialogFormVisible: false,
    };
  },

  // 从vuex获取用户信息
  computed: {
    user() {
      return this.$store.state.user;
    }
  },
  created() {
    // 请求分页查询数据
    this.load();
    // 假设 getUser 是一个已经定义好的 action
    this.$store.dispatch('getUser')
        .then(() => {
          // 用户信息获取成功后的逻辑
        })
        .catch(error => {
          console.error("created钩子获取用户信息失败:", error);
        })



  },

  methods: {
    //请求数据，加载所有的试卷,并且拿回题库里面所有的试卷id信息
    load() {
      axios.post('http://127.0.0.1:5000/testing/',{isFetchTestingPaperIds: "true"})
          .then(res => {
            this.testingPaperIds = res.data.testingPaperIds;
            this.$message.success('加载数据成功，真不容易');
          })
          .catch(error => {
            console.error('请求失败:', error);
            this.$message.error('无法加载数据，请检查网络连接或服务器状态');
          });
    },
// 确保使用async关键字声明这个方法
    async fetchTestingPaper() {
      // 验证用户是否输入试卷id
      if (!this.testingPaper.paperId) {
        // 如果没有输入试卷id，返回一个rejected Promise
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
          this.paperFetched = true;
          // 更新Vue实例的数据
          this.testingPaper.questions = response.data.questions;
          this.testingPaper.course = response.data.course;
          // 遍历 this.testingPaper.questions 的键
          for (const questionKey in this.testingPaper.questions) {
            // 在 this.answers 中为对应的键设置 "未作答"
            this.answers[questionKey] = "未作答";

          }
          // 返回response，这样调用者可以访问到它
          return response;
        } else {
          // 如果响应不是200，使用throw抛出错误
          throw new Error(response.data.message || '开始考试失败');
        }
      } catch (error) {
        // 捕获并抛出错误
        this.$message.error("开始考试失败: " + error.message);
        console.error("开始考试发生错误:", error);
        // 返回一个rejected Promise
        return Promise.reject(error);
      }
    },
    async startTesting() {
      try {
        await this.fetchTestingPaper(); // 假设 fetchTestingPaper 返回一个 Promise
        this.dialogFormVisible = false;
        this.$message.success('开始考试');
      } catch (error) {
        // 处理错误，例如显示一个错误消息
        this.$message.error('获取试卷时出错: ' + error.message);
      }
    },
    submitAnswers() {
      let unansweredKeys = [];
      for (let key in this.answers) {
        if (this.answers[key] === "未作答") {
          unansweredKeys.push(key);
        }
      }

      if (unansweredKeys.length > 0) {
        // 使用join方法将数组转换为用逗号分隔的字符串
        let unansweredKeysString = unansweredKeys.join(", ");
        // 使用confirm函数询问用户是否继续提交
        if (confirm("第" + unansweredKeysString + "题未作答，您确定要提交吗？")) {
          // 用户点击了“确定”，继续提交答案
          alert("没做完你也敢交？6！")
          this.submitAnswersToServer(); // 假设这是提交答案到服务器的函数
        } else {
          // 用户点击了“取消”，停止提交并允许用户继续作答
          // 这里可以什么都不做，因为用户已经取消了提交
        }
      } else {
        // 如果没有未作答的题目，直接提交答案
        this.submitAnswersToServer(); // 假设这是提交答案到服务器的函数
      }
    },

    submitAnswersToServer() {
      // 发送Ajax请求提交答案
      // 示例：使用axios发送POST请求
      axios.post('http://127.0.0.1:5000/testing/', {
        paperId: this.testingPaper.paperId,
        answers: this.answers,
        user: this.user
      }, {
        headers: {
          'Content-Type': 'application/json'
        }
      })
          .then(response => {
            if (response.data.code === 200) {
              this.$message.success('交卷成功');
              this.submitted = true;
              this.results = response.data.results;
            } else {
              this.$message.error(response.data.message || '交卷失败');
            }
          })
          // 错误信息输出展示
          .catch(error => {
            let errorMessage = error.response ? error.response.data.message : error.message;
            this.$message.error("交卷失败: " + errorMessage);
            console.error("交卷发生错误:", error);
          });
    },
    requestForTest(){
      this.dialogFormVisible = true;
    },
    back(){
      this.$router.go(-1);
    }
  }
};
</script>

<style>
.header {
  text-align: center;
}

.main {
  font-size: 20px;
}

.test {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  padding: 20px;
  margin-right: 200px;
  margin-left: 200px;
  border: 1px solid #ccc;
  border-radius: 5px;
  background-color: #f9f9f9;
}

ul {
  list-style: none;
}

ul li:hover {
  background-color: #f0f0f0;
}


</style>