$(function() {
    var speed = 800;//滚动速度
    var h=document.body.clientHeight;
    //回到顶部
    $("#toTop").click(function () {
        $('html,body').animate({
            scrollTop: '0px'
        },
        speed);
    });
    //回到底部
    var windowHeight = parseInt($("body").css("height"));//整个页面的高度
    $("#toBottom").click(function () {
        //alert(h);
        $('html,body').animate({
            scrollTop: h+'px'
        },
        speed);
    });
});