$(".see_more_reviews").click(function(){
	var pk = $(this).attr("pk")
	$(".more_rating_" + pk).slideToggle()
	var sign = $(this).html()
	if(sign=="+"){
		$(this).html("-")
	} else {
		$(this).html("+")

	}
})