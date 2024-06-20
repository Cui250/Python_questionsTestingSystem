import Vue from 'vue'
import VueRouter from 'vue-router'
import LogiN from "@/views/ceshixitong/LogiN.vue";
import QuestionManagement from "@/views/ceshixitong/QuestionManagement.vue";
import TesTing from "@/views/ceshixitong/TesTing.vue";
import UserManagement from "@/views/ceshixitong/UserManagement.vue";
import RegisteR from "@/views/ceshixitong/RegisteR.vue";
import MyTest from "@/views/ceshixitong/MyTest.vue";
import ExamPaper from "@/views/ceshixitong/ExamPaper.vue";
import PaperSetting from "@/views/ceshixitong/PaperSetting.vue";
import QuestionAnalysis from "@/views/ceshixitong/QuestionAnalysis.vue";
import PersonalInf from "@/views/ceshixitong/PersonalInf.vue";

Vue.use(VueRouter)

const routes = [
  { //定义路由信息
    path: '/login',   //如果访问的地址是
    name: 'login',
    component: LogiN   //则访问某个组件
  },
  {//跳转到登录页面
    path: '/',
    redirect:'/login'  //重定向
  },
  {//跳转到注册页面
    path: '/Regist',   //如果访问的地址是
    name: 'regist',
    component: RegisteR   //则访问某个组件
  },
  {  //跳转到考题管理
    path: '/Question',
    name: 'question',
    component: QuestionManagement
  },
  {  //跳转到考试
    path: '/Test',
    name: 'test',
    component: TesTing
  },
  {  //跳转到用户管理
    path: '/UserManagement',
    name: 'usermanagement',
    component: UserManagement
  },
  {  //跳转到我的考试
    path: '/MyTest',
    name: 'mytest',
    component: MyTest
  },
  {  //跳转到组卷页面
    path: '/ExamPaper',
    name: 'exampaper',
    component: ExamPaper
  },
  {  //组卷中的页面
    path: '/PaperSetting',
    name: 'papersetting',
    component: PaperSetting
  },
  {  //题库分析的页面
    path: '/QuestionAnalysis',
    name: 'questionanalysis',
    component: QuestionAnalysis
  },
  {  //个人信息展示
    path: '/PersonalInf',
    name: 'personalinf',
    component:PersonalInf
  },

]

const router = new VueRouter({
  routes
})

export default router
