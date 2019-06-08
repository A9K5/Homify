document.addEventListener('DOMContentLoaded', function () {
  var elems = document.querySelectorAll('.datepicker');
  var options = {}
  var instances = M.Datepicker.init(elems, options);
});

document.addEventListener('DOMContentLoaded', function () {
  var elems = document.querySelectorAll('.sidenav');
  var options = {}
  var instances = M.Sidenav.init(elems, options);
});