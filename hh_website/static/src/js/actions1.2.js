$(document).ready(function() {
    var getUrlParameter = function getUrlParameter(sParam) {
        var sPageURL = decodeURIComponent(window.location.search.substring(1)),
            sURLVariables = sPageURL.split('&'),
            sParameterName,
            i;

        for (i = 0; i < sURLVariables.length; i++) {
            sParameterName = sURLVariables[i].split('=');

            if (sParameterName[0] === sParam) {
                return sParameterName[1] === undefined ? false : sParameterName[1];
            }
        }
        return false;
    };

    function setCookie(name, value, expires, path, domain, secure) {
        var today = new Date();
        today.setTime(today.getTime());
        if (expires) {
            expires = expires * 1000 * 60 * 60 * 24;
        }
        var expires_date = new Date(today.getTime() + (expires));
        document.cookie = name + '=' + escape(value) +
            ((expires) ? ';expires=' + expires_date.toGMTString() : '') + //expires.toGMTString()
            ((path) ? ';path=' + path : '') +
            ((domain) ? ';domain=' + domain : '') +
            ((secure) ? ';secure' : '');
    };

    function getCookie(name) {
        var start = document.cookie.indexOf(name + "=");
        var len = start + name.length + 1;
        if ((!start) && (name != document.cookie.substring(0, name.length))) {
            return null;
        }
        if (start == -1) return null;
        var end = document.cookie.indexOf(';', len);
        if (end == -1) end = document.cookie.length;
        return unescape(document.cookie.substring(len, end));
    };

    $(".clickable-row").click(function() {
        window.location = $(this).data("href");
    });
    $(".sort_intern").click(function() {
//        window.location = $(this).data("href");
        var sort = getCookie('sort_by_room');
        if (sort!=null  && sort == 'true'){
            setCookie('sort_by_room','false',30,null,null,null);
        }
        else{
            setCookie('sort_by_room','true',30,null,null,null);
        }
        window.location.reload(true);
    });

    $(".sort_by_time_promotion").click(function() {
//        window.location = $(this).data("href");
        var sort = getCookie('sort_by_time_promotion');
        if (sort!=null  && sort == 'true'){
            setCookie('sort_by_time_promotion','false',30,null,null,null);
        }
        else{
            setCookie('sort_by_time_promotion','true',30,null,null,null);
        }
        window.location.reload(true);
    });

});