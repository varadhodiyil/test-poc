function pay(id){
	
	var data = [
		{"cart":id}
	];
	console.log(data);
	$.post("/orders/",data,function(response){
		console.log(response);
	});
}