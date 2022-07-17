// Copyright 2015 Janusz Skonieczny
jQuery(document).ready(function($){
    var nav = $(".main .nav2");
    if (nav.is(':visible')) {
        var content = $(".main .content");
        var h = Math.max($(".main #hero-sidebar").height(), nav.height());
        if (h > content.height()) {
            content.css("min-height", h);
        }
    }

    $(".slider").flexslider({
        controlsContainer: ".slider",
        animation: "fade",
        slideshow: true,
        directionNav: true,
        controlNav: true,
        pauseOnHover: true,
        slideshowSpeed: 7000,
        animationDuration: 600
    });

    $('#search input').keyup(function(e){
        if (e.keyCode == 13) {
            window.location = "http://www.google.pl/search?&q=site:www.motylki.edu.pl+" + $('#search input').val();
            e.preventDefault();
        }
    });
});


