$('#date_id').mask("00 / 00 / 0000",{placeholder:"Data"});





$(document).on("click", "#home_arrow", function(){
	if($("#home_arrow_symbol").html()=="˅") {
		$("#home_arrow_symbol").html("&#708;")
	} else {
		$("#home_arrow_symbol").html("&#709;")
	}
	$("#home_advanced").slideToggle()

})


$(".howworks_option").click(function(){
	var is_underlined = $(this).css("border-width")
	if(is_underlined=="0px") {
		var border_color = $(this).css("border-color")
		$(".howworks_option").css("border-width", "0px")
		$(".row_option").css("display", "none")
		$(this).css("border-bottom", "2px solid " + border_color)
		if($(this).hasClass("buyer")) {
			$("#buyer_row").fadeIn(500)
		} else {
			$("#seller_row").fadeIn(500)
		}
	}
})