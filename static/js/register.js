function  bindEmailCaptchaClick(){$("#captcha-btn").click(function (event){
    //$this:代表当前按钮的jquery对象
    var $this=$(this)
    //阻止默认的事件
    event.preventDefault();

    var email=$("input[name='email']").val();
    $.ajax({
      url:"/auth/captcha/email?email="+email,
      method:"GET",
      success:function (result){
        console.log(result);
        var code=result['code'];
        if (code==200){
          var countdown=60;
          $this.off("click") ;
          //取消按钮的点击事件
          var timer=setInterval(function (){
            $this.text(countdown);
            countdown-=1;
            if(countdown<=0){
              //清掉定时器
              clearInterval(timer);
              //将按钮的值修改回去
              $this.text('获取验证码');
              //恢复点击事件
              bindEmailCaptchaClick();
            }
          },1000);
          alert("邮箱验证码发送成功");
        }
      },
      fail:function (error){
        console.log(error);
      }
    })
  });

};




//整个网页都加载完毕后执行
$(function (){
  bindEmailCaptchaClick()
});