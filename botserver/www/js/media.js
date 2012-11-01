$(function() {
    var ITEMS_PER_PAGE = 15;
    var just_reached_bottom = false;
    var delete_button = $(".delete-button");

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

    delete_button.click(function() {
        var button = $(this)
        var id = button.attr("id");
        var del = confirm("Delete item #" + id + "?");
        if (del) {
            $.post("/media/delete/" + id, function(data) {
                if (data === id) {
                    var parent_li = button.parent("li");
                    parent_li.next("hr").remove();
                    parent_li.remove();
                }
            });
        }
    });

});
