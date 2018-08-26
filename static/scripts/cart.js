// function pay(id){
	
// 	var _data = 
// 		{"cart":id};
// 	console.log(_data);
// 	$.ajax({
// 		url: "/orders/",
// 		method: "POST",
// 		data: JSON.stringify(_data),
// 		datatype: "json",
// 		contentType: "application/json",
// 	}).done(function(response){
// 		console.log(response);
// 		// alert('Added To Cart SuccessFully');
// 		if(response.status){
// 			$("#myModal").modal();
// 			var html = "<p> Your Product is ordered Successfully</p>"+
// 						"<a href='/orders/' class='btn btn-info' role='button'> Click here to Track your order</a>";
// 			$("#modal-body").html(html);
// 			window.location.reload();
// 		} else{
// 			var html = "<p>" + response.error +"</p>";
// 			$("#modal-body").html(html);
// 		}
		

// 	});
// }
function pay(){
	
	var _data ={};
	$.ajax({
		url: "/orders/",
		method: "POST",
		data: JSON.stringify(_data),
		datatype: "json",
		contentType: "application/json",
	}).done(function(response){
		console.log(response);
		// alert('Added To Cart SuccessFully');
		if(response.status){
			$("#myModal").modal();
			var html = "<p> Your Product is ordered Successfully</p>"+
						"<a href='/orders/' class='btn btn-info' role='button'> Click here to Track your order</a>";
			$("#modal-body").html(html);
			window.location.reload();
		} else{
			var html = "<p>" + response.error +"</p>";
			$("#modal-body").html(html);
		}
		

	});
}
$(document).ready(function(){
	var cntr = 0;
    var interval = null;
	$(".pay-btn").each(function(){
		if (Number($(this).attr('quantity')) <= 0) {
		  $(this).attr("disabled", "true");
		}
	  });

	socket = new WebSocket("ws://" + window.location.host + "/cart/");
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
                clearTimeout(interval);
            }
		
	},15000);
	// Call onopen directly if socket is already open
	if (socket.readyState == WebSocket.OPEN) socket.onopen();
});
function delete_Cart(id){
	
	$.ajax({
		url: "/cart/"+id+"/",
		method: "DELETE",
		datatype: "json",
		contentType: "application/json",
	}).done(function(response){
		console.log(response);
		// alert('Added To Cart SuccessFully');
		if(response.status){
			$("#myModal").modal();
			var html = "<p> Your Product is Removed Successfully</p>";
			$("#modal-body").html(html);
			window.location.reload();
		} else{
			var html = "<p>" + response.error +"</p>";
			$("#modal-body").html(html);
		}
		

	});
}