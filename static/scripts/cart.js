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
	$(".pay-btn").each(function(){
		if (Number($(this).attr('quantity')) <= 0) {
		  $(this).attr("disabled", "true");
		}
	  });

	  socket = new WebSocket("ws://" + window.location.host + "/chat/");
	socket.onmessage = function(e) {
		alert(e.data);
	}
	socket.onopen = function() {
		socket.send("hello world");
	}
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