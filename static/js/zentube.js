$(document).ready(function() {
  $('#youtube-link').keyup(function() {
    var yt_link = $('#youtube-link').val();
    var zt_link = 'http://' + window.location.host + '/' + yt_link.substr([yt_link.lastIndexOf('v=') + 2]);
    $('#zentube-link').html(zt_link);
    $('#zentube-link').attr('href', zt_link);
    $('#link-container').addClass('has-link');
  });
});

