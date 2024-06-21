<template>
<!--  用于主体页面-->
  <el-aside width="200px" style="background-color: rgb(238, 241, 246); height:200vh;box-shadow: 2px 0 6px rgb(0,21,41,0.35)">
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

</template>
<script setup>

</script>
<script>
export default {
  computed: {
    user(){
      return this.$store.state.user;
    }
  },
}

</script>

<style scoped>

</style>