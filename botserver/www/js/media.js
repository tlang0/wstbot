$(function () {
    var ITEMS_PER_PAGE = 15,
        LOADED_ALL = false,
        justReachedBottom = false,
        mediaContent = $("#media-content");

    function deleteItemClick() {
        var button = $(this),
            id = button.attr("id");

        if (confirm("Delete item #" + id + "?")) {
            $.post("/media/delete/" + id, function (data) {
                if (data === id) {
                    var parentLi = button.parent("li");
                    parentLi.next("hr").remove();
                    parentLi.remove();
                }
            });
        }
    }

    function bindDelete() {
        $(".delete-button").unbind("click").click(deleteItemClick);
    }
    bindDelete();

    function stop() {
        $("#load-button").hide();
        LOADED_ALL = true;
        mediaContent.append("<p>You have reached the bottom! :)</p>");
    }

    function loadContent() {
        var nr = mediaContent.attr("data-nr");
        if (LOADED_ALL) {
            return;
        }
        nr = parseInt(nr, 10) + ITEMS_PER_PAGE;
        // reached the end?
        $.get("/media/load/" + nr, function (data) {
            mediaContent.append(data);
            mediaContent.attr("data-nr", nr);
            if (data === "") {
                stop();
            }
            justReachedBottom = false;
            bindDelete();
        });
    }

    $(document).scroll(function () {
        if (justReachedBottom || LOADED_ALL) {
            return;
        }
        if ($(window).scrollTop() + $(window).height() >= $(document).height() * 0.90) {
            justReachedBottom = true;
            loadContent();
        }
    });

    $("#load-button").click(loadContent);
});
