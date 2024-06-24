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
                <el-breadcrumb-item  style="font-weight: bold; color: black;">系统管理</el-breadcrumb-item>
                <el-breadcrumb-item>用户管理</el-breadcrumb-item>
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
          <el-button type="success" @click = 'handleAdd_user' >添加</el-button>
          <br><br>

          <!--        表格-->
          <el-table :data="users" border>
            <el-table-column prop="id" label="ID" width="120">
            </el-table-column>
            <el-table-column prop="username" label="用户名" width="120">
            </el-table-column>
            <el-table-column prop="email" label="邮箱" width="200">
            </el-table-column>
            <el-table-column prop="register_time" label="注册时间" width="250">
            </el-table-column>
            <el-table-column prop="role" label="身份" width="80">
            </el-table-column>



            <el-table-column label="操作" width="250">
              <template slot-scope="scope">
                <el-button type="primary" size="mini" @click="handleChange_userpassword(scope.row) ">重置密码</el-button>
                <el-button type="primary" size="mini" @click="handleChange_user(scope.row) ">编辑</el-button>

                <!--              气泡确认框-->
                <el-popconfirm
                    class="ml-5"
                    confirm-button-text='确定'
                    cancel-button-text='我在想想'
                    icon="el-icon-info"
                    icon-color="red"
                    title="您确定删除吗？"
                    @confirm="del_user(scope.row.id)"
                >
                  <el-button size="mini" type="danger" slot="reference" >删除</el-button>
                </el-popconfirm>

              </template>
            </el-table-column>


          </el-table>


          <!--      弹窗-重置密码-->
          <el-dialog title="重置密码" :visible.sync="dialogFormVisible_userpassword" width="30%">
            <el-form label-width="80px" size="small">
              <el-form-item label="邮箱" >
                <el-input v-model="form.email" autocomplete="off" disabled></el-input>
              </el-form-item>
              <el-form-item label="新密码" >
                <el-input v-model="form.password" autocomplete="off"></el-input>
              </el-form-item>
            </el-form>
            <div slot="footer" class="dialog-footer">
              <el-button @click="resetDialogAndLoad_userpassword">取 消</el-button>
              <el-button type="primary" @click="handleChange_password" >确 定</el-button>
            </div>
          </el-dialog>

          <!--      弹窗-增添用户-->
          <el-dialog title="用户管理" :visible.sync="dialogFormVisible_adduser" width="30%">
            <el-form label-width="80px" size="small">
              <el-form-item label="用户名" >
                <el-input v-model="form.username" autocomplete="off"></el-input>
              </el-form-item>
              <el-form-item label="邮箱" >
                <el-input v-model="form.email" autocomplete="off"></el-input>
              </el-form-item>
              <el-form-item label="密码" >
                <el-input v-model="form.password" autocomplete="off"></el-input>
              </el-form-item>
              <el-form-item label="身份" >
                <el-input v-model="form.role" autocomplete="off"></el-input>
              </el-form-item>
            </el-form>
            <div slot="footer" class="dialog-footer">
              <el-button @click="resetDialogAndLoad_adduser">取 消</el-button>
              <el-button type="primary" @click="handle_adduser" >确 定</el-button>
            </div>
          </el-dialog>

          <!--      弹窗-编辑用户-->
          <el-dialog title="用户管理" :visible.sync="dialogFormVisible_changeuser" width="30%">
            <el-form label-width="80px" size="small">
              <el-form-item label="ID">
                <!-- 禁用输入框，用户不能修改 ID -->
                <el-input v-model="form.id" autocomplete="off" disabled></el-input>
              </el-form-item>
              <el-form-item label="用户名" >
                <el-input v-model="form.username" autocomplete="off"></el-input>
              </el-form-item>
              <el-form-item label="邮箱" >
                <el-input v-model="form.email" autocomplete="off"></el-input>
              </el-form-item>
              <el-form-item label="身份" >
                <el-input v-model="form.role" autocomplete="off"></el-input>
              </el-form-item>
            </el-form>
            <div slot="footer" class="dialog-footer">
              <el-button @click="resetDialogAndLoad_changeuser">取 消</el-button>
              <el-button type="primary" @click="handle_changeuser" >确 定</el-button>
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
      users:[],
      dialogFormVisible_adduser:false, //弹窗显示
      dialogFormVisible_userpassword:false,
      dialogFormVisible_changeuser:false,

      form: {
        id: '',
        username: '',
        email: '',
        password: '',
        role: '',

      }
    }
  },
  //引入的组件管理
  components: {
    InterFace
  },
  computed: {
    user() {
      return this.$store.getters.getUser;
    }
  },
  created() {
    // 请求分页查询数据
    this.load_user()
  },

  methods: {
    //请求数据
    load_user() {
      axios.get("http://127.0.0.1:5000/user_management/returnusers")
          .then(res => {
            this.users = res.data.data;
            this.$message.success('加载数据成功，真不容易');
          })
          .catch(error => {
            console.error('请求失败:', error);
            this.$message.error('无法加载数据，请检查网络连接或服务器状态');
          });
    },

    //点击取消按钮后刷一下页面的方法
    resetDialogAndLoad_adduser() {
      // 隐藏对话框
      this.dialogFormVisible_adduser = false;
      // 调用 load 方法刷新页面数据
      this.load_user();
    },
    resetDialogAndLoad_userpassword() {
      // 隐藏对话框
      this.dialogFormVisible_userpassword = false;
      // 调用 load 方法刷新页面数据
      this.load_user();
    },
    resetDialogAndLoad_changeuser() {
      // 隐藏对话框
      this.dialogFormVisible_changeuser = false;
      // 调用 load 方法刷新页面数据
      this.load_user();
    },


    // 方法
    handleChange_userpassword(row) {
      this.form.email = row.email
      this.dialogFormVisible_userpassword = true
    },

    handleChange_user(row) {
      this.form = row
      this.dialogFormVisible_changeuser = true
    },
    handleAdd_user() {
      this.dialogFormVisible_adduser = true
      this.form = {}
    },

    //重置密码方法
    async handleChange_password() {
      try {
        const response = await axios.post("http://127.0.0.1:5000/user_management/changepassword", {
          data: {email: this.form.email, password: this.form.password}  // 发送 JSON 数据
        }); // 假设这是你的后端登录接口
        if (response.data.status === 'success') { // 根据后端返回的实际字段名进行修改
          this.$message.success(response.data.message || "操作成功")
          this.dialogFormVisible_userpassword = false
          this.load_user()
        } else {
          this.$message.error(response.data.message || "操作失败"); // 显示后端返回的错误信息或默认信息
        }
      } catch (error) {
        console.error(error); // 打印错误到控制台
        this.$message.error("操作失败，请检查网络连接或稍后重试");
      }

    },
    // 添加用户方法
    async handle_adduser() {
      try {
        const response = await axios.post("http://127.0.0.1:5000/user_management/adduser", this.form); // 假设这是你的后端登录接口
        if (response.data.status === 'success') { // 根据后端返回的实际字段名进行修改
          this.$message.success(response.data.message || "操作成功")
          this.dialogFormVisible_adduser = false
          this.load_user()
        } else {
          this.$message.error(response.data.message || "操作失败"); // 显示后端返回的错误信息或默认信息
        }
      } catch (error) {
        console.error(error); // 打印错误到控制台
        this.$message.error("操作失败，请检查网络连接或稍后重试");
      }

    },
    // 编辑用户方法
    async handle_changeuser() {
      try {
        const response = await axios.post("http://127.0.0.1:5000/user_management/changeuser", this.form); // 假设这是你的后端登录接口
        if (response.data.status === 'success') { // 根据后端返回的实际字段名进行修改
          this.$message.success(response.data.message || "操作成功")
          this.dialogFormVisible_changeuser = false
          this.load_user()
        } else {
          this.$message.error(response.data.message || "操作失败"); // 显示后端返回的错误信息或默认信息
        }
      } catch (error) {
        console.error(error); // 打印错误到控制台
        this.$message.error("操作失败，请检查网络连接或稍后重试");
      }

    },
    // 删除方法
    async del_user(id) {
      try {
        // 发送 DELETE 请求，包含 id 作为查询参数
        const response = await axios.delete(`http://127.0.0.1:5000/user_management/deleteuser`, {
          data: {id: id}  // 发送 JSON 数据
        });

        if (response.data.status === 'success') {
          // 成功删除后的逻辑
          this.$message.success(response.data.message || "删除成功");
          this.load_user(); // 重新加载数据
        } else {
          this.$message.error(response.data.message || "删除失败");
        }
      } catch (error) {
        console.error("删除时发生错误：", error);
        this.$message.error("删除时发生错误，请检查网络连接或稍后重试");
      }
    },
  },
}
</script>

<style>
.el-header {
  background-color: #B3C0D1;
  color: #333;
  line-height: 60px;
}

.el-aside {
  color: #333;
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

.backgroundph{
  height: 100vh;
  overflow: hidden;
  background: url('../../assets/beijing.jpg');
  background-size: cover; /* 调整背景图片填充方式 */
  background-position: center; /* 调整背景图片位置 */
}


</style>
