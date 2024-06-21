
<template>
  <div style="background-color:#FCFCFC;font-family:'宋体';height:100%;">
    <div>
      <my-bread level1='个人中心' level2='修改密码' :level3="levelName"></my-bread>
    </div>
    <div style="margin-top:25px;margin-left:80px;">
      <el-row :gutter="10">
        <el-col :span="2">
          <div style="background-color:#FFEBCD;width:60px;height:60px;display:inline-block;border-radius:50%;overflow:hidden;">
            <img src="../../assets/logo.png" style="width:60px;height:60px;">
          </div>
          <div style="margin-top:5px;margin-left:6px;">{{user.userName}}</div>
          <div style="margin-top:50px;margin-left:1px;"><el-button type="text" style="font-size:15px;color:#4D4D4D;"  @click="infomationClick()">个人信息<span style="color:#B0E0E6;" v-show="infomationShow" class="el-icon-s-promotion"></span></el-button></div>
          <div style="margin-top:5px;margin-left:1px;"><el-button type="text" style="font-size:15px;color:#4D4D4D;" @click="passwordClick()">修改密码<span style="color:#B0E0E6;" v-show="passwordShow" class="el-icon-s-promotion"></span></el-button></div>
          <div style="margin-top:5px;margin-left:1px;"><el-button type="text" style="font-size:15px;color:#4D4D4D;" @click="back()">返回<span style="color:#B0E0E6;" v-show="infomationShow" class="el-icon-s-promotion"></span></el-button></div>

        </el-col>

        <el-col :span="21">
          <!-- 个人信息 -->
          <el-row v-show="infomationShow">
            <el-card style="margin-top:30px;">
              <el-row>
                <el-col :span="6">
                  <el-row :gutter="12" style="margin-top:20px;">
                    <el-col :span="8"><div style="text-align:right;"><span>ID：</span></div></el-col>
                    <el-col :span="16">{{user.id}}</el-col>
                  </el-row>
                  <el-row :gutter="12" style="margin-top:30px;">
                    <el-col :span="8"><div style="text-align:right;"><span>名字：</span></div></el-col>
                    <el-col :span="16">{{user.userName}}</el-col>
                  </el-row>
                  <el-row :gutter="12" style="margin-top:30px;">
                    <el-col :span="8"><div style="text-align:right;"><span>电子邮箱：</span></div></el-col>
                    <el-col :span="16">{{user.email}}</el-col>
                  </el-row>
                  <el-row :gutter="12" style="margin-top:30px;">
                    <el-col :span="8"><div style="text-align:right;"><span>密码：</span></div></el-col>
                    <el-col :span="16">{{user.password}}</el-col>
                  </el-row>

                </el-col>
                <el-col :span="18">
                  <el-row>
                    <el-col>
                      <el-timeline>

                        <div>
                          <span style="float: left" shadow="hover"><b>个人说明</b></span>
                          <br />
                          <br />
                          <span>螃蟹在剥我的壳</span>
                          <el-divider></el-divider>
                          <span>笔记本在写我</span>
                          <el-divider></el-divider>
                          <span>漫天的我落在枫叶的雪花上</span>
                        </div>


                      </el-timeline>
                    </el-col>
                  </el-row>
                </el-col>
              </el-row>
            </el-card>
          </el-row>
          <!-- 修改密码 -->
          <el-row v-show="passwordShow">
            <el-card style="margin-top:30px;">
              <el-form :model="personalForm">
                <el-row :gutter="12" style="margin-top:20px;">

                </el-row>

                <el-row :gutter="12" style="margin-top:1px;">
                  <el-col :span="6">
                    <div style="text-align:right;"><span>邮箱：</span></div>
                  </el-col>
                  <el-col :span="5">
                    <el-form-item prop="email">
                      <el-input type="email" v-model="personalForm.email" placeholder="请输入邮箱" ></el-input>
                    </el-form-item>
                  </el-col>
                </el-row>

                <el-row :gutter="12" style="margin-top:1px;">
                  <el-col :span="6">
                    <div style="text-align:right;"><span>密码：</span></div>
                  </el-col>
                  <el-col :span="5">
                    <el-form-item prop="password">
                      <el-input type="password" show-password v-model="personalForm.password" placeholder="请输入新的密码" ></el-input>
                    </el-form-item>
                  </el-col>
                </el-row>
                <el-row :gutter="12" style="margin-top:1px;">
                  <el-col :span="6">
                    <div style="text-align:right;"><span>确认密码：</span></div>
                  </el-col>
                  <el-col :span="5">
                    <el-form-item prop="password2">
                      <el-input type="password" show-password v-model="personalForm.password2" placeholder="请再次输入新的密码" ></el-input>
                    </el-form-item>
                  </el-col>
                </el-row>

                <el-row :gutter="12" style="margin-top:10px;">
                  <el-col :span="17" style="text-align:center;">
                    <el-button type="primary" plain round size="medium" @click="submit()">修改</el-button>
                  </el-col>
                </el-row>
              </el-form>
            </el-card>
          </el-row>
        </el-col>
      </el-row>
    </div>

    <div>

    </div>
  </div>
</template>
<script>
import axios from "axios";

export default {
  data(){
    return {
      levelName:'',
      isCollapse:false,
      infomationShow:true,
      passwordShow:false,
      isDisabled:false,
      time:60,
      personalForm:{
        email:'',
        password:"",
        password2:"",
      }
    }
  },

  computed:{
    user() {
      return this.$store.getters.getUser;
    }
  },
  methods:{


    infomationClick(){    //个人信息事件
      this.infomationShow = true
      this.passwordShow = false
    },

    passwordClick(){     //密码事件
      this.infomationShow = false
      this.passwordShow = true
    },

    submit(){  //提交
      if(this.personalForm.password === ""){
        this.$message.warning("密码不能为空")
      }else if(this.personalForm.password2 === ""){
        this.$message.warning("密码不能为空")
      }else{
        if(this.personalForm.password === this.personalForm.password2){
          const params = {
            email:this.personalForm.email,
            password:this.personalForm.password,
            password2:this.personalForm.password2,
          }
          console.log(params)
          axios.post('http://127.0.0.1:5000/user_management/changepassword_new', params)
              .then(response => {
                if (response.data.status === 'success') {
                  // 密码修改成功
                  this.$message.success(response.data.message);
                  // 可以在这里添加其他逻辑，例如清空表单或重定向
                } else {
                  // 密码修改失败
                  this.$message.error(response.data.message);
                }
              })
              .catch(error => {
                console.error("请求失败:", error);
                this.$message.error("密码修改失败，请稍后重试");
              });
        }else{
          this.$message.warning("两次输入的密码不一致,请重新输入")
        }

      }
    },
    back(){
      this.$router.go(-1);
    }

  }
}
</script>

<style>
.name{ text-align: right; }
.value{ text-align: left; }
</style>
