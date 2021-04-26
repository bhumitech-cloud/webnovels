
$(document).ready(function () {
    $(".nav li a").click(function () {
        $(this).tab('show');
    });
    $('#ctable').DataTable();
});
