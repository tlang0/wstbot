$(function() {
    var ITEMS_PER_PAGE = 15;
    var just_reached_bottom = false;

    $(document).scroll(function() {
        if (just_reached_bottom === true) {
            return;
        }
        if ($(window).scrollTop() + $(window).height() >= $(document).height() * 0.90) {
            just_reached_bottom = true;
            load_content();
        }
    });

    function load_content() {
        var nr = $("#media-content").attr("data-nr");
        nr = parseInt(nr) + ITEMS_PER_PAGE
        // reached the end?
        $.get("/media/load/" + nr, function(data) {
            $("#media-content").append(data);
            $("#media-content").attr("data-nr", nr);
            if (data == "") {
                stop();
            }
            just_reached_bottom = false;
        });
    }

    function stop() {
        $("#load-button").hide();
    }

    $("#load-button").click(load_content);
});
