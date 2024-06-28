<template>
  <div class="background">
    <div style="margin: 200px auto; background-color:rgba(255, 255, 255, 0.5); width: 350px; height:300px; padding: 20px; border-radius: 10px">
      <div style="margin: 20px 0; text-align: center; font-size: 24px">
        <b>登录</b>
      </div>
      <!-- 邮箱输入框-->
      <el-input size="medium" style="margin: 10px 0" prefix-icon="el-icon-user" v-model="user.email" placeholder="请输入邮箱"></el-input>
      <!-- 密码输入框，按下回车登录-->
      <el-input size="medium" @keydown.enter.native="login" style="margin: 10px 0" prefix-icon="el-icon-lock" show-password v-model="user.password" placeholder="请输入密码"></el-input>

      <!-- 提交和注册按钮 -->
      <div style="margin: 10px 0; text-align: right">
        <el-button type="primary" size="small" @click="login">登录</el-button>
        <el-button type="warning" size="small" @click="regist">注册</el-button>
      </div>
    </div>
  </div>
</template>

<script >
import axios from "axios";
import { mapActions } from "vuex";

export default {
  name:"LogiN",
  data(){
    return{
      user:{
        id: '',
        userName: '',
        email: '',
        password: '',
        role: ''
      }
    }
  },
  methods:{
    ...mapActions(['setUser']), // 映射所需的 actions
    //登录
    login() {
      // 验证用户是否输入邮箱
      if (!this.user.email ) {
        this.$message.error('请输入您的邮箱');
        return;
      }
      // 验证用户是否输入密码
      if (!this.user.password) {
        this.$message.error('请输入您的密码');
        return;
      }
      //接口需要更换
      axios.post('http://127.0.0.1:5000/auth/login', this.user, {
        headers: {
          'Content-Type': 'application/json'
        }
      })
          .then(response => {
            if (response.data.code === 200) {
              this.user.id = response.data.userId;
              this.user.userName = response.data.userName;
              this.user.role = response.data.role;
              // 使用映射的 action 更新 Vuex store
              this.setUser(this.user);
              let roleMessage = '同学'
              if(this.user.role === 'teacher'){
                roleMessage = "老师"
              }
              if(this.user.role === 'admin'){
                roleMessage = "管理员"
              }
              this.$message.success("欢迎回来," + this.user.userName + roleMessage + "!");
              // 登录成功，跳转到主页
                this.$router.push('/MainPage');
            } else {
              // 登录失败，显示错误消息
              this.$message.error("用户名或密码错误！");
            }
          })
          .catch(error => {
            // 处理请求错误
            let errorMessage = error.response
                ? error.response.data.message
                : error.message;
            this.$message.error("登录失败: " + errorMessage);
            console.error("发生错误:", error);
          });
    },
    // 跳转到注册页面
    regist(){
      this.$router.push('Regist')
    }
  }
}

</script>

<style >
.background{
  height: 100vh;
  overflow: hidden;
  background: url('../../assets/loginpho.jpg');
  background-size: cover; /* 调整背景图片填充方式 */
  background-position: center; /* 调整背景图片位置 */
}

</style>

