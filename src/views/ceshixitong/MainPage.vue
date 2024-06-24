<template>
  <div>
    <el-container style="height: 100%; ">
      <!--    侧边栏部分--><el-aside width="200px" style="background-color: rgb(238, 241, 246); height:100vh;box-shadow: 2px 0 6px rgb(0,21,41,0.35)">
      <el-menu :default-openeds="['1', '3']" style="height: 100%" background-color="rgb(48,65,86)"
               text-color="#fff" active-text-color="#ffd04b"
               router
      >
        <!--        头部logo-->
        <div style="height:60px;line-height:60px;text-align: center">
          <img src="../../assets/logo.png" style="width: 20px;position: relative;top: 5px;margin-right: 5px" alt="">
          <b style="color: white">考试系统</b>
        </div>
        <el-menu-item index="/Test" v-if="user.role === 'admin' || user.role === 'teacher' ||
      user.role === 'student'"><i class="el-icon-s-management"></i>开始考试</el-menu-item>

        <el-submenu index="1" v-if="user.role === 'admin' || user.role === 'teacher'">
          <template slot="title"><i class="el-icon-s-tools"></i>系统管理</template>
          <el-menu-item index="/Question" v-if="user.role === 'admin' || user.role === 'teacher'">题库管理</el-menu-item>
          <el-menu-item index="/QuestionAnalysis" v-if="user.role === 'admin' || user.role === 'teacher'">题库分析</el-menu-item>
          <el-menu-item index="/UserManagement" v-if="user.role === 'admin' ">用户管理</el-menu-item>
          <el-menu-item index="/ExamPaper" v-if="user.role === 'admin' || user.role === 'teacher'">试卷管理</el-menu-item>
          <!--        <el-submenu index="1-4">-->
          <!--          <template slot="title">选项3</template>-->
          <!--          <el-menu-item index="1-4-1">选项4-1</el-menu-item>-->
          <!--        </el-submenu>-->
        </el-submenu>
        <el-submenu index="2">
          <template slot="title"><i class="el-icon-user-solid"></i>我的信息</template>
          <el-menu-item index="/MyTest" v-if="user.role === 'admin' || user.role === 'teacher' || user.role === 'student' ">我的考试</el-menu-item>
        </el-submenu>
      </el-menu>
    </el-aside>
      <!--      头部部分-->
      <el-container>
        <el-header style="text-align: right; font-size: 12px; border-bottom: 2px solid #ccc; line-height: 60px;background-color: white">
          <div class="box">
            <div class="box_left">
              <el-breadcrumb separator="">
                <el-breadcrumb-item  style="font-weight: bold; color: black;">首页</el-breadcrumb-item>
                <el-breadcrumb-item></el-breadcrumb-item>
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
        <el-main class="backgroundph" style="display: flex; justify-content: center; align-items: center; height: 100%; position: relative;">
          <div style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%);">
            <span style="font-family: 'YourArtisticFont', cursive; font-size: 80px;">欢迎使用考试系统！</span>
          </div>
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script>


export default {
  data() {
    return {
    }
  },

  computed: {
    user(){
      return this.$store.state.user;
    }
  },
  created() {
    if(!this.user){
      this.$message.error("请先登录！！！")
      this.$router.push('/login');
    }
  },


  methods: {
    logout() {
      // 确保使用 this.$store 来分发 Vuex action
      this.$store.dispatch('logout');
      this.$router.push('/login');
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
