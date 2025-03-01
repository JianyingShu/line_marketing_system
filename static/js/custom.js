$(document).ready(function() {
    $("#sidebarToggleBtn").on('click', function() {
        $("body").toggleClass("sidebar-toggled");
        $(".sidebar").toggleClass("toggled");

        // ✅ 當 sidebar 被縮小時，換 LOGO
        if ($(".sidebar").hasClass("toggled")) {
            $("#sidebarLogo").attr("src", "/static/img/small-logo.png");
        } else {
            $("#sidebarLogo").attr("src", "/static/img/it-logo.png");
        }
    });
});

