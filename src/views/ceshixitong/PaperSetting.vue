<template>
  <el-container>
    <!--  头部-->
    <el-header class="header">组卷界面</el-header>
    <!--  主要内容-->
    <el-main class="main" >
      <div class="test">
        <div v-if="!submitted">
          <div>
            <div style="margin: 50px auto;  width: 200px; height:300px; padding: 20px; border-radius: 10px">
              <div style="margin: 20px 0; text-align: center; font-size: 24px">
                <b>请选择课程</b>
              </div>
              <el-select v-model="selectedCourse" placeholder="请选择试题所属课程" size="medium" style="margin: 10px 0; width: 20vw;">

                <!-- 使用 el-option 来定义选项 -->
                <!-- 循环courses数组中的每个课程名称 -->
                <el-option v-for="course in courses" :key="course" :label="course" :value="course">
                </el-option>
              </el-select>
              <div style="margin: 10px 0; text-align: right">
                <el-button @click="begin" type="primary" round >确定</el-button>
              </div>
            </div>
          </div>
        </div>


        <!-- 第二个页面 -->
        <div v-else>
          <div v-for="(question, index) in filteredQuestions" :key="index">
            <div>
              <p>{{question.id}}.{{ question.question }}</p>
              <ul>
                <li v-for="(option, i) in question.options" :key="i" >
                  <!-- 使用 span 元素显示选项内容 -->
                  <span>{{ String.fromCharCode(65 + i) }}.{{ option }}</span>
                </li>
              </ul>
              <p>知识点：{{question.knowledgePoint}}</p>
              <p>答案：{{question.answer}}</p>
              <!-- 空间留白 -->
              <div style="margin-bottom: 20px;"></div>

            </div>
          </div>
          <el-button @click="submit" type="primary" round >开始组卷</el-button>
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
      questions: [],
      //模拟题目数据
      // questions: [
      //   { id: 1, course: "语文", question: "What is the capital of France?", options: ["Paris", "London", "Berlin", "Rome"] },
      //   { id: 2, course: "Python语言程序设计实践", question: "What is the largest planet in our solar system?", options: ["Jupiter", "Saturn", "Mars", "Earth"] },
      //   { id: 3, course: "数学", question: "Who wrote 'Romeo and Juliet'?", options: ["William Shakespeare", "Charles Dickens", "Jane Austen", "Mark Twain"] }
      // ],
      answers: [],
      submitted: false,
      courses:[],
      selectedCourse: '',
    };
  },
  //计算属性 通过这个在渲染数据的时候提前把问题进行归类
  computed: {
    // 从vuex获取用户信息
      user() {
        return this.$store.state.user;
      },

    filteredQuestions() {
      return this.questions.filter(q => q.course === this.selectedCourse);
    }
  },
  mounted() {

    // 加载页面时就开始获取课程列表
    this.load()
    // 发送Ajax请求从后端获取题目数据
    this.fetchQuestions();
  },
  methods: {
    load() {
      axios.get("http://127.0.0.1:5000/paperSetting")
          .then(res => {
            this.courses = res.data.courses;
            this.$message.success('加载数据成功，真不容易');
          })
          .catch(error => {
            console.error('请求失败:', error);
            this.$message.error('无法加载数据，请检查网络连接或服务器状态');
          });
    },
    fetchQuestions() {
      // 发送Ajax请求
      // 示例：使用axios发送GET请求
      axios.get('http://127.0.0.1:5000/paperSetting')
          .then(response => {
            this.questions = response.data.questions;
          })
          .catch(error => {
            console.error('Error fetching questions:', error);
          });
    },
    //开始组卷
    begin() {
      // 隐藏课程选择页面
      this.submitted = true;

    },
    submit(){
      this.$router.push('/ExamPaper');
    },
  }
};
</script>

<style>
.header{
  text-align: center;
}
.main{
  font-size: 20px;
}
.test{
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  padding: 20px;
  margin-right: 200px;
  margin-left:  200px;
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