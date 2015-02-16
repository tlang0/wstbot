$(function () {
    var ITEMS_PER_PAGE = 15,
        ITEMS_TOTAL = ITEMS_PER_PAGE + 10;
        LOADED_ALL = false,
        justReachedBottom = false,
        mediaContent = $("#media-content");

    /***** Hiding Videos *****/

    // hide all videos (iframes)
    function hideVideos(context) {
        if (arguments.length === 0) {
            context = mediaContent;
        }

        $("iframe", context).before("<img src=\"/img/video_placeholder.png\" alt=\"Video Placeholder\" " +
            "title=\"Click to see the video\" class=\"video-placeholder\" />");
        $("iframe + .delete-button", context).hide();
        $("iframe", context).hide();
        $(".video-placeholder", context).click(showVideoClick);
    }
    // hide videos on startup
    hideVideos();

    function showVideoClick() {
        $(this).hide();
        $(this).siblings("iframe").show();
        $(this).siblings(".delete-button").show();
    }

    /***** Deleting *****/

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

    /***** Loading Content / Scrolling *****/

    function stop() {
        $("#load-button").hide();
        LOADED_ALL = true;
        mediaContent.append("<p>You have reached the bottom! ;)</p>");
    }

    // hide previous items
    function hideOld() {
        $(this).prevAll("hr, li").remove();
        $(window).scrollTop(0);
    }

    function bindHideOld() {
        $("hr").unbind("click").click(hideOld);
    }
    bindHideOld();

    // load additional items
    function loadContent() {
        var nr = mediaContent.attr("data-nr");
        if (LOADED_ALL) {
            return;
        }
        nr = parseInt(nr, 10) + ITEMS_PER_PAGE;
        // reached the end?
        $.get("/media/load/" + nr + window.location.search, function (data) {
            var dataDOM = $.parseHTML(data);

            // hide videos in new content
            hideVideos(dataDOM);

            mediaContent.append(dataDOM);
            mediaContent.attr("data-nr", nr);
            if (data === "") {
                stop();
            }
            justReachedBottom = false;
            bindDelete();
            bindHideOld();
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
