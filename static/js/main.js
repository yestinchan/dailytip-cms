;
(function($){
    var title_point = $('.navbar').waypoint({
      handler: function(direction) {
        if(direction == 'up'){
            $(this.element).css({"position":"relative"});
        }else if(direction == 'down'){
            $(this.element).css({"position":"fixed","top":"0","width":"100%"});
        }
      }
    });

    $(window).scroll(function(e){
        var _top = $(document).scrollTop();
        if(_top < 200){
            $(".title-wrapper").css({"padding-top":(100+_top/3)+"px"});
            $(".title-wrapper .title").css({"font-size":(4-_top/200)+"rem"});
        }else{
            $(".title-wrapper").css({"padding-top":"100px"});
            $(".title-wrapper .title").css({"font-size":"4rem"});
        }
    });

    blockWebsiteMaybe();

    function loadBrowserVersion(){
        var userAgent = navigator.userAgent.toLowerCase();
        // Figure out what browser is being used 
        jQuery.browser = {
            version: (userAgent.match(/.+(?:rv|it|ra|ie)[\/: ]([\d.]+)/) || [])[1],
            webkit: /webkit/.test(userAgent),
            opera: /opera/.test(userAgent),
            //msie: /msie/.test(userAgent) && !/opera/.test(userAgent),
            msie:(!!window.ActiveXObject || "ActiveXObject" in window) ,
            mozilla: /mozilla/.test(userAgent) && !/(compatible|webkit)/.test(userAgent)
        }; 
    }
    function blockWebsiteMaybe(){
        loadBrowserVersion();
        if($.browser.msie && ($.browser.version == "8.0" || $.browser.version == "7.0" || $.browser.version == "6.0" || $.browser.version == "5.5")){
            blockWebsite();
        }
    }
    function blockWebsite(){
        $('body').append('<div class="block"> <div class="block-content"> <p>Your browser is too old. Update before view this website.</p> <p class="small">Support browser:{"IE":"9+","mozilla":"8+","opera":"11+","safari":"unkown", "chrome":"15+"}.</p> </div> <div class="block-foot"> <p><a href="http://iyestin.com">iyestin.com</a> All right reserved.</p> </div> </div> ');
    }

    $(".archive")
    .on('mouseenter',function(e){
        $(this).find('.archive-head')
        .css({'display':'block'})
        .addClass('animated pulse');
    })
    .on('mouseleave',function(e){
        $(this).find('.archive-head')
        .css({'display':'none'})
        .removeClass('animated pulse');
    }).on('click', function(e){
        var link = $(this).find('a').attr('href');
        //redriect:
        location.href = link;
    });
})(jQuery);
