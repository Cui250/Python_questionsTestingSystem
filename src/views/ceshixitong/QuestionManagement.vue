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
                <el-breadcrumb-item>题库管理</el-breadcrumb-item>
              </el-breadcrumb>
            </div>
            <div class="box_right">
              <el-dropdown style="width: 70px; cursor: pointer;">
                <span>{{user.userName}}</span> <i class="el-icon-arrow-down" style="margin-left: 5px"></i>
                <el-dropdown-menu slot="dropdown">
                  <el-dropdown-item><router-link to="/PersonalInf" style="text-decoration: none; color: black;">个人信息</router-link></el-dropdown-item>
                  <el-dropdown-item style="text-decoration: none; color: black;" ><div @click="logout">退出</div></el-dropdown-item>
                </el-dropdown-menu>
              </el-dropdown>
            </div>
          </div>
        </el-header>
        <!--       主体部分-->
        <el-main class="backgroundph">
          <!--        一些按钮-->



          <!--          这里的地址需要换-->
          <el-upload action="http://127.0.0.1:5000/question_management/import_questions" :show-file-list="false" :on-success="importExcel" style="display: inline-block">
            <el-button type="primary"   style=" margin-left: 0px;" >导入<i class="el-icon-bottom"></i> </el-button>
          </el-upload>

          <el-button type="primary" @click = 'exportExcel'  style=" margin-left: 10px;"  >导出<i class="el-icon-top"></i> </el-button>
          <br><br>
          <el-button type="success" @click = 'handleAdd' >选择题添加</el-button>
          <!--        表格-->
          <div style="max-height: 400px; overflow: auto;">
            <el-table :data="questions" border style="width: 100%;margin-top: 10px;">
              <el-table-column prop="id" label="ID" width="50">
                <template slot-scope="scope">
                  <div class="ellipsis-text">{{ scope.row.id }}</div>
                </template>
              </el-table-column>
              <el-table-column prop="question" label="题目" width="160">
                <template slot-scope="scope">
                  <div class="ellipsis-text">{{ scope.row.question }}</div>
                </template>
              </el-table-column>
              <el-table-column prop="option1" label="选项1" width="95">
                <template slot-scope="scope">
                  <div class="ellipsis-text">{{ scope.row.option1 }}</div>
                </template>
              </el-table-column>
              <el-table-column prop="option2" label="选项2" width="95">
                <template slot-scope="scope">
                  <div class="ellipsis-text">{{ scope.row.option2 }}</div>
                </template>
              </el-table-column>
              <el-table-column prop="option3" label="选项3" width="95">
                <template slot-scope="scope">
                  <div class="ellipsis-text">{{ scope.row.option3 }}</div>
                </template>
              </el-table-column>
              <el-table-column prop="option4" label="选项4" width="95">
                <template slot-scope="scope">
                  <div class="ellipsis-text">{{ scope.row.option4 }}</div>
                </template>
              </el-table-column>
              <el-table-column prop="answer" label="答案" width="100">
                <template slot-scope="scope">
                  <div class="ellipsis-text">{{ scope.row.answer }}</div>
                </template>
              </el-table-column>
              <el-table-column prop="analysis" label="解析" width="100">
                <template slot-scope="scope">
                  <div class="ellipsis-text">{{ scope.row.analysis }}</div>
                </template>
              </el-table-column>
              <el-table-column prop="course" label="课程" width="160">
                <template slot-scope="scope">
                  <div class="ellipsis-text">{{ scope.row.course }}</div>
                </template>
              </el-table-column>
              <el-table-column prop="knowledge_point" label="知识点" width="100">
                <template slot-scope="scope">
                  <div class="ellipsis-text">{{ scope.row.knowledge_point }}</div>
                </template>
              </el-table-column>
              <el-table-column prop="level" label="难度" width="60">
                <template slot-scope="scope">
                  <div class="ellipsis-text">{{ scope.row.level }}</div>
                </template>
              </el-table-column>

              <el-table-column label="操作" width="160">
                <template slot-scope="scope">
                  <el-button type="primary" size="mini" @click="handleChange(scope.row)">编辑</el-button>
                  <!--              气泡确认框-->
                  <el-popconfirm
                      class="ml-5"
                      confirm-button-text='确定'
                      cancel-button-text='我在想想'
                      icon="el-icon-info"
                      icon-color="red"
                      title="您确定删除吗？"
                      @confirm="del(scope.row.id)"
                  >
                    <el-button size="mini" type="danger" slot="reference" >删除</el-button>
                  </el-popconfirm>
                </template>
              </el-table-column>
            </el-table>
          </div>

          <el-button type="success" @click = 'handleAdd_judgment' style="margin-top: 120px;">判断题添加</el-button>

          <br><br>

          <!--        表格-->
          <div style="max-height: 400px; overflow: auto;">
            <el-table :data="questions_new"  border style="width: 100%">
              <el-table-column prop="id" label="ID" width="60">
                <template slot-scope="scope">
                  <div class="ellipsis-text">{{ scope.row.id }}</div>
                </template>
              </el-table-column>
              <el-table-column prop="question" label="题目" width="200">
                <template slot-scope="scope">
                  <div class="ellipsis-text">{{ scope.row.question }}</div>
                </template>
              </el-table-column>
              <el-table-column prop="answer" label="答案" width="60">
                <template slot-scope="scope">
                  <div class="ellipsis-text">{{ scope.row.answer}}</div>
                </template>
              </el-table-column>
              <el-table-column prop="analysis" label="解析" width="120">
                <template slot-scope="scope">
                  <div class="ellipsis-text">{{ scope.row.analysis }}</div>
                </template>
              </el-table-column>
              <el-table-column prop="course" label="课程" width="200">
                <template slot-scope="scope">
                  <div class="ellipsis-text">{{ scope.row.course }}</div>
                </template>
              </el-table-column>
              <el-table-column prop="knowledge_point" label="知识点" width="120">
                <template slot-scope="scope">
                  <div class="ellipsis-text">{{ scope.row.knowledge_point }}</div>
                </template>
              </el-table-column>
              <el-table-column prop="level" label="难度" width="60">
                <template slot-scope="scope">
                  <div class="ellipsis-text">{{ scope.row.level }}</div>
                </template>
              </el-table-column>

              <el-table-column label="操作" width="180">
                <template slot-scope="scope">
                  <el-button type="primary" size="mini" @click="handleChange_judgment(scope.row) ">编辑</el-button>

                  <!--              气泡确认框-->
                  <el-popconfirm
                      class="ml-5"
                      confirm-button-text='确定'
                      cancel-button-text='我在想想'
                      icon="el-icon-info"
                      icon-color="red"
                      title="您确定删除吗？"
                      @confirm="del(scope.row.id)"
                  >
                    <el-button size="mini" type="danger" slot="reference" >删除</el-button>
                  </el-popconfirm>

                </template>
              </el-table-column>


            </el-table>
          </div>


          <!--      弹窗_选择题-->
          <el-dialog title="选择题管理" :visible.sync="dialogFormVisible" width="30%">
            <el-form label-width="80px" size="small">
              <el-form-item label="题目" >
                <el-input v-model="form.question" autocomplete="off"></el-input>
              </el-form-item>
              <el-form-item label="选项1" >
                <el-input v-model="form.option1" autocomplete="off"></el-input>
              </el-form-item>
              <el-form-item label="选项2" >
                <el-input v-model="form.option2" autocomplete="off"></el-input>
              </el-form-item>
              <el-form-item label="选项3" >
                <el-input v-model="form.option3" autocomplete="off"></el-input>
              </el-form-item>
              <el-form-item label="选项4" >
                <el-input v-model="form.option4" autocomplete="off"></el-input>
              </el-form-item>
              <el-form-item label="答案" >
                <el-input v-model="form.answer" autocomplete="off"></el-input>
              </el-form-item>
              <el-form-item label="解析" >
                <el-input v-model="form.analysis" autocomplete="off"></el-input>
              </el-form-item>
              <el-form-item label="课程" >
                <el-input v-model="form.course" autocomplete="off"></el-input>
              </el-form-item>
              <el-form-item label="知识点" >
                <el-input v-model="form.knowledge_point" autocomplete="off"></el-input>
              </el-form-item>
              <el-form-item label="难度" >
                <el-input v-model="form.level" autocomplete="off"></el-input>
              </el-form-item>
            </el-form>
            <div slot="footer" class="dialog-footer">
              <el-button @click="resetDialogAndLoad">取 消</el-button>
              <el-button type="primary" @click="handleEdit" >确 定</el-button>
            </div>
          </el-dialog>
          <!--          为了解决修改试题时修改ID造成BUG而新建的一个弹窗-->
          <el-dialog title="选择题管理" :visible.sync="dialogFormVisible_new" width="30%">
            <el-form label-width="80px" size="small">
              <el-form-item label="ID" >
                <el-input v-model="form.id" autocomplete="off" disabled></el-input>
              </el-form-item>
              <el-form-item label="题目" >
                <el-input v-model="form.question" autocomplete="off"></el-input>
              </el-form-item>
              <el-form-item label="选项1" >
                <el-input v-model="form.option1" autocomplete="off"></el-input>
              </el-form-item>
              <el-form-item label="选项2" >
                <el-input v-model="form.option2" autocomplete="off"></el-input>
              </el-form-item>
              <el-form-item label="选项3" >
                <el-input v-model="form.option3" autocomplete="off"></el-input>
              </el-form-item>
              <el-form-item label="选项4" >
                <el-input v-model="form.option4" autocomplete="off"></el-input>
              </el-form-item>
              <el-form-item label="答案" >
                <el-input v-model="form.answer" autocomplete="off"></el-input>
              </el-form-item>
              <el-form-item label="解析" >
                <el-input v-model="form.analysis" autocomplete="off"></el-input>
              </el-form-item>
              <el-form-item label="课程" >
                <el-input v-model="form.course" autocomplete="off"></el-input>
              </el-form-item>
              <el-form-item label="知识点" >
                <el-input v-model="form.knowledge_point" autocomplete="off"></el-input>
              </el-form-item>
              <el-form-item label="难度" >
                <el-input v-model="form.level" autocomplete="off"></el-input>
              </el-form-item>
            </el-form>
            <div slot="footer" class="dialog-footer">
              <el-button @click="resetDialogAndLoad">取 消</el-button>
              <el-button type="primary" @click="handleEdit" >确 定</el-button>
            </div>
          </el-dialog>
          <!--      弹窗_判断题-->
          <el-dialog title="判断题管理" :visible.sync="dialogFormVisible_judgment" width="30%">
            <el-form label-width="80px" size="small">
              <el-form-item label="题目" >
                <el-input v-model="form.question" autocomplete="off"></el-input>
              </el-form-item>
              <el-form-item label="答案" >
                <el-input v-model="form.answer" autocomplete="off"></el-input>
              </el-form-item>
              <el-form-item label="解析" >
                <el-input v-model="form.analysis" autocomplete="off"></el-input>
              </el-form-item>
              <el-form-item label="课程" >
                <el-input v-model="form.course" autocomplete="off"></el-input>
              </el-form-item>
              <el-form-item label="知识点" >
                <el-input v-model="form.knowledge_point" autocomplete="off"></el-input>
              </el-form-item>
              <el-form-item label="难度" >
                <el-input v-model="form.level" autocomplete="off"></el-input>
              </el-form-item>
            </el-form>
            <div slot="footer" class="dialog-footer">
              <el-button @click="resetDialogAndLoad">取 消</el-button>
              <el-button type="primary" @click="handleEdit_judgment" >确 定</el-button>
            </div>
          </el-dialog>
          <!--          为了解决修改试题时修改ID造成BUG而新建的一个弹窗-->
          <el-dialog title="判断题管理" :visible.sync="dialogFormVisible_judgment_new" width="30%">
            <el-form label-width="80px" size="small">
              <el-form-item label="ID" >
                <el-input v-model="form.id" autocomplete="off" disabled></el-input>
              </el-form-item>
              <el-form-item label="题目" >
                <el-input v-model="form.question" autocomplete="off"></el-input>
              </el-form-item>
              <el-form-item label="答案" >
                <el-input v-model="form.answer" autocomplete="off"></el-input>
              </el-form-item>
              <el-form-item label="解析" >
                <el-input v-model="form.analysis" autocomplete="off"></el-input>
              </el-form-item>
              <el-form-item label="课程" >
                <el-input v-model="form.course" autocomplete="off"></el-input>
              </el-form-item>
              <el-form-item label="知识点" >
                <el-input v-model="form.knowledge_point" autocomplete="off"></el-input>
              </el-form-item>
              <el-form-item label="难度" >
                <el-input v-model="form.level" autocomplete="off"></el-input>
              </el-form-item>
            </el-form>
            <div slot="footer" class="dialog-footer">
              <el-button @click="resetDialogAndLoad">取 消</el-button>
              <el-button type="primary" @click="handleEdit_judgment" >确 定</el-button>
            </div>
          </el-dialog>





        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script>
import axios from "axios";
import InterFace from "@/views/ceshixitong/InterFace.vue";


export default {
  data() {
    return {
      questions:[],
      questions_new:[],
      dialogFormVisible:false, //弹窗显示
      dialogFormVisible_new:false,
      dialogFormVisible_judgment:false, //弹窗显示
      dialogFormVisible_judgment_new:false,
      form:{
        id:'',
        question:'',
        option1:'',
        option2:'',
        option3:'',
        option4:'',
        answer:'',
        analysis:'',
        course:'',
        knowledge_point:'',
        level:'',

      },
    }
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
    if(!this.user){
      this.$message.error("请先登录！！！")
      this.$router.push('/login');
    }
    else if((this.user.role !== "admin") && (this.user.role !== "teacher")){
      this.$message.error("非法跳转！权限不足！");
      this.$router.push('/MainPage');
    }
    else{
      // 请求分页查询数据
      this.load();
    }
  },

  methods: {
    logout() {
      // 确保使用 this.$store 来分发 Vuex action
      this.$store.dispatch('logout');
      this.$router.push('/login');
    },
    //请求数据
    load() {
      axios.get("http://127.0.0.1:5000/question_management/returnquestions")
          .then(res => {
            this.questions = res.data.data1.data;
            this.questions_new = res.data.data2.data;
            this.$message.success('加载数据成功，真不容易');
          })
          .catch(error => {
            console.error('请求失败:', error);
            this.$message.error('无法加载数据，请检查网络连接或服务器状态');
          });
    },
    resetDialogAndLoad() {
      // 隐藏对话框
      this.dialogFormVisible = false;
      this.dialogFormVisible_new=false;
      this.dialogFormVisible_judgment=false;
      this.dialogFormVisible_judgment_new=false;
      // 调用 load 方法刷新页面数据
      this.load();
      // this.load_judgment()
    },


    // 添加方法
    handleChange(row){
      this.form=row
      this.dialogFormVisible_new = true
    },
    handleAdd(){
      this.dialogFormVisible = true
      this.form={}
    },
    handleChange_judgment(row){
      this.form=row
      this.dialogFormVisible_judgment_new = true
    },
    handleAdd_judgment() {
      this.dialogFormVisible_judgment = true
      this.form = {}
    },
    // 编辑方法    新增和修改发往同一个接口
    async handleEdit() {
      try {
        const response = await axios.post("http://127.0.0.1:5000/question_management/editquestion", this.form); // 假设这是你的后端登录接口
        if (response.data.status === 'success') { // 根据后端返回的实际字段名进行修改
          this.$message.success(response.data.message || "操作成功")
          this.dialogFormVisible = false
          this.dialogFormVisible_new = false
          this.load()
        } else {
          this.$message.error(response.data.message || "操作失败"); // 显示后端返回的错误信息或默认信息
        }
      } catch (error) {
        console.error(error); // 打印错误到控制台
        this.$message.error("操作失败，请检查网络连接或稍后重试");
      }

    },
    async handleEdit_judgment() {
      try {
        const response = await axios.post("http://127.0.0.1:5000/question_management/editquestion_new", this.form); // 假设这是你的后端登录接口
        if (response.data.status === 'success') { // 根据后端返回的实际字段名进行修改
          this.$message.success(response.data.message || "操作成功")
          this.dialogFormVisible_judgment = false
          this.dialogFormVisible_judgment_new = false
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
    async del(id) {
      try {
        // 发送 DELETE 请求，包含 id 作为查询参数
        const response = await axios.delete(`http://127.0.0.1:5000/question_management/deletequestion`, {
          data: {id: id}  // 发送 JSON 数据
        });

        if (response.data.status === 'success') {
          // 成功删除后的逻辑
          this.$message.success(response.data.message || "删除成功");
          this.load(); // 重新加载数据
        } else {
          this.$message.error(response.data.message || "删除失败");
        }
      } catch (error) {
        console.error("删除时发生错误：", error);
        this.$message.error("删除时发生错误，请检查网络连接或稍后重试");
      }
    },
    exportExcel() {
      axios.get('http://127.0.0.1:5000/question_management/export_questions', { responseType: 'blob' })
          .then(response => {
            // 创建 Blob URL
            const blob = new Blob([response.data], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' });
            const url = URL.createObjectURL(blob);
            // 创建隐藏的下载链接并触发下载
            const link = document.createElement('a');
            link.href = url;
            link.download = 'questions.xlsx';
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);

            // 释放 Blob URL
            URL.revokeObjectURL(url);
          })
          .catch(error => {
            console.error('导出失败', error);
          });
    },
    importExcel(response) {
      if (response && response.status === 'success') {
        this.$message.success(response.message || "操作成功");
        this.load();
      } else {
        this.$message.error(response.message || "操作失败");
      }
    },
  },

}
</script>

<style>
.ml-5 {
  margin-left: 5px; /* 调整导出按钮和导入按钮之间的间距 */
}
.box {
  display: flex;


}

.box .box_left {
  flex: 1;
  display: flex;
  justify-content: start;
  align-items: center;
}

.box .box_right {
  flex: 1;
}

.ellipsis-text {
  max-width: 180px; /* 超过这个宽度的内容将被省略号替代 */
  white-space: nowrap; /* 文本不换行 */
  overflow: hidden; /* 超出部分隐藏 */
  text-overflow: ellipsis; /* 显示省略号 */
}

.backgroundph{
  height: 100vh;
  overflow: hidden;
  background: url('../../assets/beijing.jpg');
  background-size: cover; /* 调整背景图片填充方式 */
  background-position: center; /* 调整背景图片位置 */
}

</style>