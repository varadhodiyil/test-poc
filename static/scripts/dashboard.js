function addToCart(id,varient_id=null){
	console.log(id);
	varient_val = $("#"+varient_id).val();
	if(varient_val == "" || varient_val == null){
		alert("Please select a varient")
		return;
	}
	var _data = [{
		"product": id,
		"varient":this.inventory_id
	  }];
	  console.log(Array.from(_data));
	  console.log(_data);	
	 
	$.ajax({
		url: "/cart/",
		method: "POST",
		data: JSON.stringify(_data),
		datatype: "json",
		contentType: "application/json",
	}).done(function(response){
		console.log(response);
		// alert('Added To Cart SuccessFully');
		$("#myModal").modal();
		var html = "<p> Added to Cart SuccessFuly</p>"+
					"<a href='/cart/' class='btn btn-info' role='button'> Click here to view Cart</a>";
		$("#modal-body").html(html);

	});
}

var inventory_id = null;
function select_product(sel){
	console.log(sel.value);
	this.inventory_id = sel.value;
}
function checkQty(qty){
if(qty<0){
	return false;
}	
return true;
}
$(document).ready(function(){
	$("option").each(function(){
		if (Number($(this).attr('quantity')) <= 0) {
		  $(this).attr("disabled", "true");
		}
		});
	
});