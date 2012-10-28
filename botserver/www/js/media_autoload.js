$(function() {
    var just_reached_bottom = false;

    $(document).scroll(function() {
        if (just_reached_bottom === true) {
            return;
        }
        if ($(window).scrollTop() + $(window).height() == $(document).height()) {
            just_reached_bottom = true;
            load_content();
        }
    });

    function load_content() {
        var page = $("#media-content").attr("data-page");
        page = parseInt(page) - 1
        // reached the end?
        if (page <= 0) {
            return;
        }
        $.get("/media/page/" + page, function(data) {
            $("#media-content").append(data);
            $("#media-content").attr("data-page", page);
            just_reached_bottom = false;
        });
    }

    $("#load-button").click(load_content);
});
