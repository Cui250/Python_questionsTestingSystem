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
                <el-breadcrumb-item  style="font-weight: bold; color: black;">系统管理</el-breadcrumb-item>
                <el-breadcrumb-item>题库分析</el-breadcrumb-item>
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
        <el-main>
          <div>
            <el-row :gutter="10">
              <el-col :span="12">
                <el-card>
                  <div style="width: 100%;height: 400px" id="pie"></div>
                </el-card>
              </el-col>
              <el-col :span="12">
                <el-card>
                  <div style="width: 100%;height: 400px" id="bar"></div>
                </el-card>
              </el-col>
            </el-row>
          </div>

        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script>
import InterFace from "@/views/ceshixitong/InterFace.vue";
import * as echarts from 'echarts';
import axios from "axios";


const option ={
  title: {
    text: '试题类型比例图',
    left: 'center'
  },
  tooltip: {
    trigger: 'item'
  },
  legend: {
    left:'left',
    orient: 'vertical'
  },
  series: [
    {
      name: '题目数量',
      type: 'pie',
      radius: ['40%', '70%'],
      avoidLabelOverlap: false,
      padAngle: 5,
      itemStyle: {
        borderRadius: 10
      },
      label: {
        show: false,
        position: 'center'
      },
      emphasis: {
        label: {
          show: true,
          fontSize: 40,
          fontWeight: 'bold'
        }
      },
      labelLine: {
        show: false
      },
      data: []
    }
  ]
};



const option1 = {
  title:{
    text:'试题类型柱状图',
    left:'center'
  },
  legend: {
    left:'left',
  },
  tooltip:{
    trigger:'axis'
  },
  xAxis: {
    type: 'category',
    axisLabel: {
      formatter: function (value) {
        return value.replace(/(.{4})/g, '$1\n'); // 每3个字符折行
      }
    },
    data: []
  },
  yAxis: {
    type: 'value'
  },
  series: [
    { name:'试题数量',
      data: [],
      type: 'bar',
      smooth: true
    },

    { name:'平均试题难度',
      data: [],
      type: 'bar',
      smooth: true
    }
  ]
};

export default {
  name: 'ChartDisplay',
  components: {InterFace},

  data() {
    return {}
  },
  mounted() {  //等到页面的元素全部加载完成之后再初始化
    let pieDom = document.getElementById('pie');
    let pieChart = echarts.init(pieDom);
    pieChart.setOption(option)

    let barDom = document.getElementById('bar');
    let barChart = echarts.init(barDom);
    barChart.setOption(option1)
    axios.get('http://127.0.0.1:5000/question_management/analysis_bank').then(res =>{
      option.series[0].data=res.data.course_stats
      pieChart.setOption(option)


      option1.xAxis.data=res.data.level_stats.map(item => item.course)
      option1.series[0].data=res.data.course_stats.map(item => item.value)
      option1.series[1].data=res.data.level_stats.map(item => item.average_level),
          barChart.setOption(option1)
    })
  },
  computed:{
    user() {
      return this.$store.getters.getUser;
    }
  },


  methods:{
  }
};
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


</style>