<template>
  <div class="background">
    <div style="margin: 200px auto ;  background-color:rgba(255, 255, 255, 0.5); width: 350px;height:400px;padding: 20px;border-radius: 10px" >
      <div style="margin: 20px 0 ;text-align: center;font-size: 24px">
        <b>注 册</b>
      </div>
      <el-input size="medium" style="margin: 10px 0 " prefix-icon="el-icon-user" v-model="user.email" placeholder="请输入您的邮箱"></el-input>
      <el-input size="medium" style="margin: 10px 0 " prefix-icon="el-icon-lock"  show-password v-model="user.password" placeholder="请输入您的密码"></el-input>
      <!-- 在el-input密码输入框下方添加验证码输入框 -->
      <el-input size="medium" style="margin: 10px 0 " prefix-icon="el-icon-key" v-model="user.captcha" placeholder="请输入您的邮箱收到的验证码"></el-input>
      <!-- 新增用户名输入框 -->
      <el-input size="medium" style="margin: 10px 0 " prefix-icon="el-icon-user" v-model="user.userName" placeholder="请输入您的用户名（不超过100字符）"></el-input>

      <div style="margin: 10px 0; display: flex; justify-content: space-between;">
        <!-- 发送验证码按钮，添加倒计时显示 -->
        <el-button
            type="info"
            size="small"
            autocomplete="off"
            :disabled="sendingCaptcha || captchaTimerCount > 0"
            @click="sendCaptcha"
            :class="{'cooldown': captchaTimerCount > 0}"
            style="background-color: cyan; border: none; border-radius: 10px;"
        >
          <!-- 根据按钮状态显示不同文本 -->
          {{ sendingCaptcha ? '发送中...' : (captchaTimerCount > 0 ? `${captchaTimerCount}秒后重试` : '获取验证码') }}
        </el-button>
        <div>
          <el-button type="primary" size="small" autocomplete="off" @click="register">注册</el-button>
          <el-button type="warning" size="small" autocomplete="off" @click="back">返回登陆</el-button>
        </div>
      </div>
    </div>
  </div>



</template>

<script>
import axios from 'axios'; // 引入axios

export default {
  name: "LogiN",
  data() {
    return {
      user: {
        email: '',
        password: '',
        captcha: '',
        userName: ''
      },
      sendingCaptcha: false,
      captchaTimerCount: 0, // 初始化倒计时为0

    };
  },
  methods: {
    sendCaptcha() {
      if (!this.user.email) {
        this.$message.error('请先输入邮箱');
        return;
      }
      if (this.sendingCaptcha || this.captchaTimerCount > 0) {
        this.$message.info('请等待验证码发送');
        return;
      }
      this.sendingCaptcha = true;
      axios.post("http://localhost:5000/auth/captcha/email", { email: this.user.email }, {
        headers: {
          'Content-Type': 'application/json'
        }
      })
          .then(response => {
            this.sendingCaptcha = false;
            if (response.data.code === 200) {
              this.$message.success('验证码发送成功');
              // 发送成功后，开始倒计时
              this.captchaTimerCount = 30; // 设置倒计时为30秒
              const countdown = setInterval(() => {
                if (this.captchaTimerCount > 0) {
                  this.captchaTimerCount--; // 倒计时减少
                } else {
                  clearInterval(countdown); // 倒计时结束，清除定时器
                  this.sendingCaptcha = false; // 重置发送状态
                }
              }, 1000);
            } else {
              this.$message.error('验证码发送失败');
            }
          })
          .catch(error => {
            this.sendingCaptcha = false;
            let errorMessage = error.response ? error.response.data.message : error.message;
            this.$message.error("发送验证码失败: " + errorMessage);
            console.error("发送验证码发生错误:", error);
          });

    },
    register() {
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
      // 验证用户是否输入邮箱验证码
      if (!this.user.captcha ) {
        this.$message.error('请输入您的邮箱验证码');
        return;
      }
      // 验证用户是否输入用户名
      if (!this.user.userName) {
        this.$message.error('请输入您的用户名');
        return;
      }
      axios.post("http://localhost:5000/auth/register", this.user, {
        headers: {
          'Content-Type': 'application/json'
        }
      })
          .then(response => {
            // 判断并且输出展示注册结果
            if (response.data.code === 200) {
              this.$message.success('注册成功');
              // 注册成功，跳转到登录页面
              this.$router.push('/login');
            } else {
              this.$message.error(response.data.message || '注册失败');
            }
          })
          // 错误信息输出展示
          .catch(error => {
            let errorMessage = error.response ? error.response.data.message : error.message;
            this.$message.error("注册失败: " + errorMessage);
            console.error("注册发生错误:", error);
          });
    },
    back() {
      this.$router.push('/login');
    }
  }
};
</script>

<style >
.background{
  height: 100vh;
  overflow: hidden;
  background: url('../../assets/loginpho.jpg');
  background-size: cover; /* 调整背景图片填充方式 */
  background-position: center; /* 调整背景图片位置 */
}

/* 添加按钮冷却样式 */
.cooldown {
  background-color: #cccccc !important; /* 冷却时按钮颜色变灰 */
}


</style>

