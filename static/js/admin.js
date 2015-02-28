var utils = {}
utils.generateDialog = function (type, text) {
    var n = noty({
        text        : text,
        type        : type,
        dismissQueue: true,
        layout      : 'center',
        closeWith   : ['click'],
        theme       : 'relax',
        maxVisible  : 10,
        animation   : {
            open  : 'animated bounceInDown',
            close : 'animated bounceOutDown',
            easing: 'swing',
            speed : 500
        }
    });
    return n;
}