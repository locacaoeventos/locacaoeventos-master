$(".review_plussign").click(function(){
	var place_pk = $(this).attr("place-pk")
	if($(this).html()=="+"){
		$(this).html("&minus;")
	} else {
		$(this).html("+")
	}

	$("#review_wrapper_" + place_pk).slideToggle()
})