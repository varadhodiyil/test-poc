function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

var csrftoken = getCookie('csrftoken');
function csrfSafeMethod(method) {
  // these HTTP methods do not require CSRF protection
  return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
var cntr = 0;

$(document).ready(function(){
    var interval = null;
	$.ajaxSetup({
		beforeSend: function(xhr, settings) {
			if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
				xhr.setRequestHeader("X-CSRFToken", csrftoken);
			}
		}
      });
      socket = new WebSocket("ws://" + window.location.host + "/promotions/");
      socket.onmessage = function(e) {
          console.log(e.data);
          var _data = JSON.parse(e.data);
          var x = document.getElementById("snackbar");
          x.innerHTML = _data.message;
          x.className = "show";
          setTimeout(function(){ x.className = x.className.replace("show", ""); }, 3000);
      }
      socket.onopen = function() {
          socket.send("hello world");
      }
      interval = setInterval(function(){
          socket.send("hello world");
            cntr++;
            if(cntr >=2){
                clearInterval(interval);
            }
      },15000);
      // Call onopen directly if socket is already open
      if (socket.readyState == WebSocket.OPEN) socket.onopen();
});
