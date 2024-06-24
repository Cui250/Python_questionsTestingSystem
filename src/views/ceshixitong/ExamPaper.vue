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
                <el-breadcrumb-item :to="{ path: '/MainPage' }">首页</el-breadcrumb-item>
                <el-breadcrumb-item style="font-weight: bold; color: black;">系统管理</el-breadcrumb-item>
                <el-breadcrumb-item>试卷管理</el-breadcrumb-item>
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
        <el-main class="backgroundph">

          <!--        一些按钮-->
          <el-button type="success" @click = 'handleAdd' v-if="!checked">手动组卷</el-button>
          <el-button type="success" @click = 'randomAdd' v-if="!checked">随机组卷</el-button>
          <el-button type="primary" @click="exportToPDF1" v-if="checked">导出为 PDF</el-button>
          <el-button type="primary" @click="exportToPDF2" v-if="checked">导出为 PDF(带答案和解析)</el-button>
          <el-button type="success" @click="back" v-if="checked">返回</el-button>

          <!--          <el-button type="primary" @click="exportToWord" v-if="checked">导出为 Word</el-button>-->

          <br><br>

          <!--        表格-->
          <div v-if="!checked">
            <el-table :data="testingPapers" border>
              <el-table-column prop="paperId" label="ID" width="120">
              </el-table-column>
              <el-table-column prop="course" label="所属课程" width="200">
              </el-table-column>
              <el-table-column prop="questionId" label="题目id" width="120">
              </el-table-column>
              <el-table-column label="操作" width="230">
                <template slot-scope="scope">
                  <el-button type="success" size="mini" @click="checkPaperDetail(scope.row) ">查看详情</el-button>

                  <el-button type="primary" size="mini" @click="handleChange(scope.row) ">编辑</el-button>

                  <!--              气泡确认框-->
                  <el-popconfirm
                      class="ml-5"
                      confirm-button-text='确定'
                      cancel-button-text='我在想想'
                      icon="el-icon-info"
                      icon-color="red"
                      title="您确定删除吗？"
                      @confirm="del(scope.row.paperId)"
                  >
                    <el-button size="mini" type="danger" slot="reference" >删除</el-button>
                  </el-popconfirm>

                </template>
              </el-table-column>


            </el-table>
          </div>




<!--          试卷详情展示-->
          <div v-if="checked" style=" overflow-y: auto; height: 650px; border: 1px solid #ddd; box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); background-color: #f9f9f9;">
            <div  style="margin-left: 5%">
              <p>试卷id:{{ testingPaperDetail.paperId }}</p>
              <p>所属课程：{{testingPaperDetail.course}}</p>
              <p>试卷详情:</p>
              <br>
              <div>
                <!-- 保持原有页面样式 -->
                <div v-for="(question, index) in testingPaperDetail.questions" :key="index" >
                  <p>{{question.id}}.{{ question.question }}</p>
                  <ul>
                    <li v-for="(option, i) in question.options" :key="i">
                      <!-- 使用 span 元素显示选项内容 -->
                      <span>{{ String.fromCharCode(65 + i) }}.{{ option }}</span>
                    </li>
                  </ul>

                    <div >
                      <p style="color: green">正确答案：{{question.answer}}</p>
                      <p>解析：{{question.analysis}}</p>
                      <p>知识点：{{question.knowledgePoint}}</p>
                      <p>难度系数：{{question.level}}</p>
                      <p>本题分数：{{testingPaperDetail.scorePerQuestion[question.type.toString()]}}</p>
                    </div>

                  <!-- 空间留白 -->
                  <div style="margin-bottom: 20px;"></div>
                </div>
              </div>

              <hr>
              <br>
            </div>

          </div>






          <!--      手动组卷以及试题编辑弹窗-->
          <el-dialog title="试卷管理" :visible.sync="dialogFormVisible" width="50%">
            <el-form label-width="80px" size="small">
              <el-form-item label="所属课程" label-width="12%">
                <el-select v-model="form.course" placeholder="请选择新试卷的所属课程">
                  <!-- 使用 el-option 来定义选项 -->
                  <!-- 循环courses数组中的每个课程名称 -->
                  <el-option v-for="course in courses" :key="course" :label="course" :value="course">
                  </el-option>
                </el-select>
                <br>
                <el-button type="success" @click = 'check' >查看试题</el-button>
              </el-form-item>
              <el-form-item label="选择题总分" label-width="12%">
                <el-input v-model="form.choiceQuestionScore" autocomplete="off" type="number" min="0" placeholder="请输入选择题总分"></el-input>
              </el-form-item>
              <el-form-item label="每题分数" label-width="12%">
                <el-input :value="form.choiceQuestionScore / form.choiceQuestionNum"  disabled autocomplete="off" placeholder="请输入选择题数量"></el-input>
              </el-form-item>
              <el-form-item label="选择题id" label-width="12%">
                <el-input v-model="inputQuestionIds" autocomplete="off" placeholder="以英文逗号分隔，不要有空格"></el-input>
              </el-form-item>
              <el-form-item label="选择题数量" label-width="12%">
                <el-input v-model="form.choiceQuestionNum" autocomplete="off" disabled></el-input>
              </el-form-item>
              <el-form-item label="判断题总分" label-width="12%">
                <el-input v-model="form.judgmentQuestionScore" autocomplete="off" type="number" min="0" placeholder="请输入判断题总分"></el-input>
              </el-form-item>
              <el-form-item label="每题分数" label-width="12%">
                <el-input :value="form.judgmentQuestionScore / form.judgmentQuestionNum"  disabled autocomplete="off" placeholder="请输入选择题数量"></el-input>
              </el-form-item>
              <el-form-item label="判断题id" label-width="12%">
                <el-input v-model="inputQuestionIds2" autocomplete="off" placeholder="以英文逗号分隔，不要有空格"></el-input>
              </el-form-item>
              <el-form-item label="判断题数量" label-width="12%">
                <el-input v-model="form.judgmentQuestionNum" autocomplete="off" disabled></el-input>
              </el-form-item>
              <div v-if="(parseFloat(form.judgmentQuestionScore) + parseFloat(form.choiceQuestionScore)) !== 100.00" style="color: red">
                两类题目总分必须为100！
              </div>
            </el-form>
            <div slot="footer" class="dialog-footer">
              <el-button @click="resetDialogAndLoad">取 消</el-button>
              <el-button type="primary" @click="handleEdit" >确 定</el-button>
            </div>
          </el-dialog>

          <!--      随机组卷弹窗-->
          <el-dialog title="试卷管理" :visible.sync="dialogFormForRandomVisible" width="50%">
            <el-form label-width="80px" size="medium">
              <el-form-item label="所属课程" >
                <el-select v-model="form2.course" placeholder="请选择新试卷的所属课程">
                  <!-- 使用 el-option 来定义选项 -->
                  <!-- 循环courses数组中的每个课程名称 -->
                  <el-option v-for="course in courses" :key="course" :label="course" :value="course">
                  </el-option>
                </el-select>
                <br>
                <el-button type="success" @click = 'check' >查看试题</el-button>
              </el-form-item>
              <el-form-item label="选择题总分" label-width="15%">
                <el-input v-model="form2.choiceQuestionScore" autocomplete="off" placeholder="请输入选择题总分" type="number" min="0"></el-input>
              </el-form-item>
              <el-form-item label="选择题数量" label-width="15%">
                <el-input v-model="form2.choiceQuestionNum" autocomplete="off" placeholder="请输入选择题数量" type="number" min="0"></el-input>
              </el-form-item>
              <el-form-item label="每题选择题分数：" label-width="23%">
                <el-input autocomplete="off" :value="form2.choiceQuestionScore / form2.choiceQuestionNum" disabled></el-input>
              </el-form-item>
              <el-form-item label="难度系数" label-width="15%">
                <el-input v-model="form2.choiceQuestionLevel" autocomplete="off" placeholder="请输入选择题难度系数" type="number" min="0"></el-input>
              </el-form-item>
              <el-form-item label="判断题总分" label-width="15%">
                <el-input v-model="form2.judgmentQuestionScore" autocomplete="off" placeholder="请输入判断题总分" type="number" min="0"></el-input>
              </el-form-item>
              <el-form-item label="判断题数量" label-width="15%">
                <el-input v-model="form2.judgmentQuestionNum" autocomplete="off" placeholder="请输入判断题数量" type="number" min="0"></el-input>
              </el-form-item>
              <el-form-item label="每题选择题分数：" label-width="23%">
                <el-input autocomplete="off" :value="form2.judgmentQuestionScore / form2.judgmentQuestionNum" disabled></el-input>
              </el-form-item>
              <el-form-item label="难度系数" label-width="15%">
                <el-input v-model="form2.judgmentQuestionLevel" autocomplete="off" placeholder="请输入判断题难度系数" type="number" min="0"></el-input>
              </el-form-item>
            </el-form>
            <!--            如果两类题目总分不等于100-->
            <div v-if="(parseFloat(form2.judgmentQuestionScore) + parseFloat(form2.choiceQuestionScore)) !== 100.00" style="color: red">
              两类题目总分必须为100！
            </div>
            <div slot="footer" class="dialog-footer">
              <el-button @click="resetDialogAndLoad">取 消</el-button>
              <el-button type="primary" @click="randomSetting" >确 定</el-button>
            </div>
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
// 导入jsPDF（需要先安装）
import * as jsPDF from 'jspdf';
// 导入支持中文字符的字体（已经转换为js文件，直接设置进就行，不用注册）
import '../../../typeface/HarmonyOS_Sans_SC_Regular-normal'






export default {
  data() {
    return {
      inputQuestionIds: '',
      inputQuestionIds2: '',
      testingPapers: [],
      testingPaper: {
        paperId: '',
        course: '',
        questions: {},
      },
      testingPaperDetail: {
        paperId: '',
        course: '',
        questions:[],
        scorePerQuestion: {}

      },
      dialogFormVisible:false, //手动组卷以及试题编辑弹窗显示
      dialogFormForRandomVisible: false, //随机组卷弹窗显示
      checked: false, //试卷详情页显示
      exportAnswerPaper: false, //是否输出带答案的试卷
      courses: [],
      form:{
        // 新增id属性（更改试卷信息要用）
        paperId: '',
        choiceQuestionIds: '',
        judgmentQuestionIds: '',
        choiceQuestionNum: '',
        choiceQuestionScore: '',
        judgmentQuestionNum: '',
        judgmentQuestionScore: '',
        course:'',
      },
      form2:{
        course: '',
        choiceQuestionNum: '',
        choiceQuestionScore: '',
        choiceQuestionLevel: '',
        judgmentQuestionNum: '',
        judgmentQuestionScore: '',
        judgmentQuestionLevel: '',
        questionId: ''

      },
      isAdd: 'true'
    }
  },
  components:{
    InterFace
  },
  computed:{
    user() {
      return this.$store.getters.getUser;
    },
    questionNumberCount() {
      // 计算题号数量，如果字符串以逗号结尾，则去掉最后一个逗号
      const cleanInput = this.inputQuestionIds.replace(/,+$/, '');
      const questionCount = (cleanInput.match(/,/g) || []).length + 1;
      return questionCount;
    },
    questionNumberCount2() {
      // 计算题号数量，如果字符串以逗号结尾，则去掉最后一个逗号
      const cleanInput = this.inputQuestionIds2.replace(/,+$/, '');
      const questionCount = (cleanInput.match(/,/g) || []).length + 1;
      return questionCount;
    }


  },
  watch: {
    // 监听 inputQuestionIds 的变化，并更新 form.choiceQuestionNum
    inputQuestionIds() {
      // 直接使用计算属性的值更新 form.choiceQuestionNum
      this.form.choiceQuestionNum = this.questionNumberCount;
      this.form.choiceQuestionIds = this.inputQuestionIds
    },
    inputQuestionIds2() {
      // 直接使用计算属性的值更新 form.choiceQuestionNum
      this.form.judgmentQuestionNum = this.questionNumberCount2;
      this.form.judgmentQuestionIds = this.inputQuestionIds2
    }
  },
  created() {
    // 请求分页查询数据
    this.load()
  },

  methods: {
    //请求数据，加载所有的试卷,并且拿回题库里面所有的课程信息
    load() {
      axios.get("http://127.0.0.1:5000/paperSetting/")
          .then(res => {
            this.testingPapers = res.data.testingPapers;
            this.courses = res.data.courses;
            this.$message.success('加载数据成功，真不容易');
          })
          .catch(error => {
            console.error('请求失败:', error);
            this.$message.error('无法加载数据，请检查网络连接或服务器状态');
          });
    },
    // 提交随机组卷请求
    randomSetting(){
      if(!this.form2.course){
        this.$message.error("请选择试卷所属课程！");
        return;
      }
      else if(isNaN(parseFloat(this.form2.choiceQuestionNum)) && isNaN(parseFloat(this.form2.judgmentQuestionNum))){
        this.$message.error("所有题目的数量不能同时为零！");
        return;
      }
      else if(parseFloat(this.form2.choiceQuestionScore) + parseFloat(this.form2.judgmentQuestionScore) !== 100){
        this.$message.error("两类题目的总分必须等于100！");
        return;
      }
      axios.post('http://127.0.0.1:5000/paperSetting/',{course: this.form2.course, scorePerQuestion:
            {"0": parseFloat(this.form2.choiceQuestionScore) / parseFloat(this.form2.choiceQuestionNum),
              "1": parseFloat(this.form2.judgmentQuestionScore) / parseFloat(this.form2.judgmentQuestionNum)},
        questionNum: {"0": this.form2.choiceQuestionNum, "1": this.form2.judgmentQuestionNum},
        level: {"0": this.form2.choiceQuestionLevel, "1": this.form2.judgmentQuestionLevel}})
          .then(response => {
            if(response.data.code === 200){
              this.dialogFormForRandomVisible = false;
              this.load();
              this.$message.success('随机组卷成功！');
            }
            else {
              // 如果响应不是200，使用throw抛出错误
              throw new Error(response.data.message || '开始考试失败');
            }
          })
          .catch(error => {
            console.error('请求失败:', error);
            this.$message.error('无法加载数据，请检查网络连接或服务器状态');
          });

    },
    //点击取消按钮后刷一下页面的方法
    resetDialogAndLoad() {
      // 隐藏对话框
      this.dialogFormVisible = false;
      this.dialogFormForRandomVisible = false
      // 调用 load 方法刷新页面数据
      this.load();
    },

    // 编辑方法
    handleChange(row){
      this.form.course=row.course;
      this.form.paperId=row.paperId;
      this.dialogFormVisible = true;
      //   设置标志isAdd = 'flase',告知后端本次操作是修改
      this.isAdd = 'false';
    },
    // 添加方法
    handleAdd(){
      this.dialogFormVisible = true
      this.form={}
      //   不对标志位isAdd进行设置，告知后端此次操作为新增
    },
    randomAdd(){
      this.dialogFormForRandomVisible = true
      this.form2={}
      //   不对标志位isAdd进行设置，告知后端此次操作为新增
    },
    // 编辑方法    新增和修改发往同一个接口
    async handleEdit(){
      if(!this.form.course){
        this.$message.error("请选择试卷所属课程！");
        return;
      }
      else if(isNaN(parseFloat(this.form.choiceQuestionNum)) && isNaN(parseFloat(this.form.judgmentQuestionNum))){
        this.$message.error("所有题目的数量不能同时为零！");
        return;
      }
      else if(parseFloat(this.form.choiceQuestionScore) + parseFloat(this.form.judgmentQuestionScore) !== 100){
        this.$message.error("两类题目的总分必须等于100！");
        return;
      }
      try {
        const response = await axios.post("http://127.0.0.1:5000/paperSetting/", {form: this.form ,isAdd: this.isAdd,scorePerQuestion:
              {"0": parseFloat(this.form.choiceQuestionScore) / parseFloat(this.form.choiceQuestionNum),
                "1": parseFloat(this.form.judgmentQuestionScore) / parseFloat(this.form.judgmentQuestionNum)},}); // 假设这是你的后端组卷接口
        if (response.data.code === 200) { // 根据后端返回的实际字段名进行修改
          this.$message.success(response.data.message || "操作成功")
          this.dialogFormVisible=false
          this.load()
        } else {
          this.$message.error(response.data.message || "操作失败"); // 显示后端返回的错误信息或默认信息
        }
      } catch (error) {
        console.error(error); // 打印错误到控制台
        this.$message.error("操作失败，请检查网络连接或稍后重试");
      }

    },

    // 删除方法
    async del(paperId) {
      try {
        const response = await axios.delete('http://127.0.0.1:5000/paperSetting/', {
          data: { paperId: paperId }
        });

        if (response.status === 200) {
          // 成功删除后的逻辑
          this.load()
        } else {
          // 非200状态码的处理
          throw new Error('删除失败，状态码：' + response.status); // 抛出错误以便在catch中处理
        }
      } catch (error) {
        if (error.response) {
          // 请求已发出，但服务器响应的状态码不在2xx范围内
          console.error('删除时发生错误（状态码：', error.response.status, '）:', error.response.data);
          this.$message.error('删除时发生错误，状态码：' + error.response.status + '，错误信息：' + error.response.data.message);
        } else {
          // 处理其他错误情况
          this.$message.error('删除时发生错误，请检查网络连接或稍后重试');
        }
      }
    },

    check(){
      this.$router.push('/PaperSetting');
    },
    // 查看试卷详情
    checkPaperDetail(row){
      this.testingPaperDetail.paperId = row.paperId;
      this.testingPaperDetail.course = row.course;
      axios.post('http://127.0.0.1:5000/paperSetting/',{paperId:row.paperId, questionIds: row.questionId})
          .then(response => {
            if(response.data.code === 200){
              this.testingPaperDetail.questions = response.data.questions;
              this.testingPaperDetail.scorePerQuestion = response.data.scorePerQuestion;
              this.dialogFormForRandomVisible = false;
              this.load();
              this.checked =true;
              this.$message.success('试卷获取成功！');
            }
            else {
              // 如果响应不是200，使用throw抛出错误
              throw new Error(response.data.message || '开始考试失败');
            }
          })
          .catch(error => {
            console.error('请求失败:', error);
            this.$message.error('无法加载数据，请检查网络连接或服务器状态');
          });

    },
    exportToPDF() {
      const pdf = new jsPDF.jsPDF({
        orientation: 'p',
        unit: 'pt',
        format: 'a4'
      });
      pdf.setFont('HarmonyOS_Sans_SC_Regular');

      // 添加试卷标题
      const title = `${this.testingPaperDetail.course} 试卷`; // 假设 this.testingPaperDetail.course 包含课程名
      pdf.setFontSize(24); // 设置标题字体大小
      pdf.setTextColor(0, 0, 0); // 设置标题字体颜色

      // 计算标题宽度并居中
      const titleWidth = pdf.getStringUnitWidth(title) * 24; // 根据字体大小计算标题宽度
      const titleX = (pdf.internal.pageSize.width - titleWidth) / 2; // 居中标题

      // 增加距离顶部的距离
      const titleY = 40; // 你可以根据需要调整这个值

      // 在页面顶部中间位置添加标题
      pdf.text(title, titleX, titleY);

      // 试卷标题下方留一些空间
      let currentY = titleY + 50; // 从标题下方开始绘制内容，30是标题与内容之间的间距

      const questionSpacing = 15; // 每个问题之后的空间高度

      for (let i = 0; i < this.testingPaperDetail.questions.length; i++) {
        // 如果是每6题之后，或者当前位置加上问题高度超出页面底部，则添加新页面
        if ((i % 5 === 0 && i !== 0) || currentY + questionSpacing + 10 > pdf.internal.pageSize.height) {
          pdf.addPage();
          // 重置 currentY 为标题下方的位置
          currentY = titleY + 30;
        }

        // 添加题目信息
        pdf.setFontSize(12);
        pdf.text(i + 1 + '. ' + this.testingPaperDetail.questions[i].question + '(               )', 40, currentY);
        currentY += 15; // 问题标题和内容之间的间距
        this.testingPaperDetail.questions[i].options.forEach((option, j) => {
          pdf.text(`${String.fromCharCode(65 + j)}. ${option}`, 40, currentY);
          currentY += 12; // 选项之间的间距
        });



        // 如果要打印带答案的试卷
        if(this.exportAnswerPaper){
          // 添加解析
          let analysis = this.testingPaperDetail.questions[i]
          pdf.text('答案：' + analysis.answer, 40, currentY);
          currentY += 12; // 解析之间的间距
          pdf.text('解析：' + analysis.analysis, 40, currentY);
          currentY += 12; // 解析之间的间距
          pdf.text('难度系数：' + analysis.level, 40, currentY);
          currentY += 12; // 解析之间的间距
          pdf.text('知识点：' + analysis.knowledgePoint, 40, currentY);
          currentY += 12; // 解析之间的间距
          pdf.text('本题分数：' + this.testingPaperDetail.scorePerQuestion[analysis.type], 40, currentY);
          currentY += 20; // 加宽一些与下题距离
        }

        // 更新当前Y位置，为下一个问题预留足够的空间
        currentY += questionSpacing;
      }

      // 使用 jsPDF 生成 PDF
      pdf.output('dataurlnewwindow');
    },
    exportToPDF1(){
      this.exportAnswerPaper = false;
      this.exportToPDF()

    },
    exportToPDF2(){
      this.exportAnswerPaper = true;
      this.exportToPDF()

    },
    back(){
      this.checked = false;
    }



  },

}
</script>

<style>
.box{
  display: flex;


}
.box .box_left{
  flex: 1;
  display: flex;
  justify-content: start;
  align-items: center;
}
.box .box_right{
  flex: 1;
}

.backgroundph{
  height: 100vh;
  overflow: hidden;
  background: url('../../assets/beijing.jpg');
  background-size: cover; /* 调整背景图片填充方式 */
  background-position: center; /* 调整背景图片位置 */
}

</style>