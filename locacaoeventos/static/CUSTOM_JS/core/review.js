$(".see_more_reviews").click(function(){
	var pk = $(this).attr("pk")
	$(".more_rating_" + pk).toggle("slow")
})