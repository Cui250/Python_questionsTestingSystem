function bindEmailCaptchaClick() {
    var $captchaBtn = $("#captcha-btn"); // 捕获按钮的引用
    $captchaBtn.off("click").on("click", function (event) {
        event.preventDefault();

        var email = $("input[name='email']").val();
        $.ajax({
            url: "/auth/captcha/email",
            method: "GET",
            data: { email: email },
            success: function (result) {
                var code = result['code'];
                if (code == 200) {
                    alert(message = "验证码已发送！")
                    var countdown = 60;
                    $captchaBtn.text(countdown + "s后重试"); // 使用捕获的引用
                    var timer = setInterval(function () {
                        countdown--;
                        $captchaBtn.text(countdown + "s后重试"); // 使用捕获的引用
                        if (countdown <= 0) {
                            clearInterval(timer);
                            $captchaBtn.text("获取验证码"); // 使用捕获的引用
                            // 这里不需要重新绑定点击事件，因为已经绑定过了
                        }
                    }, 1000);
                } else {
                    alert(result['message']);
                }
            },
            error: function (error) {
                console.log(error);
            }
        });
    });
}

$(function () {
    bindEmailCaptchaClick();
});