// $(document).ready(function () {

document.addEventListener('DOMContentLoaded', function () {
    var elems = document.querySelectorAll('.sidenav');
    var options = {};
    var instances = M.Sidenav.init(elems, options);
});
// });


$(".switch").find("input[type=checkbox]").on("change",function() {
    var status = $(this).prop('checked');

     $.ajax({
        url : url,
        type : "post",
        data : { status : status}
    })
});