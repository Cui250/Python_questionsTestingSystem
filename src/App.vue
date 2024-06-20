<template>
  <div >
   <router-view></router-view>
  </div>
</template>

<script >
export default {
  components:{},
  data(){
    return {
      message:"hello vue"
    }
  },
  methods:{

  }
}  //导出成为一个模块
</script>

<style>
#app{
  height:100%
}

</style>
