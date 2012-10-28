$(function() {
    $(document).scroll(function() {
        if ($(window).scrollTop() + $(window).height() == $(document).height()) {
            load_content();
        }
    });

    function load_content() {
        var page = $("#media-content").attr("data-page");
        page = parseInt(page) - 1
        $.get("/media/page/" + page, function(data) {
            $("#media-content").append(data);
        });
        $("#media-content").attr("data-page", page);
    }

    $("#load-button").click(load_content);
});
