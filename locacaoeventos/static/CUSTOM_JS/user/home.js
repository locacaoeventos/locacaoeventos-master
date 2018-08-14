$(document).ready(function(){
	$('#date_id').datepicker({ dateFormat: 'dd/mm/yy' }).val()
	$('#date_id').mask("00/00/0000",{placeholder:"Data"});
})
$(document).on("click", "#home_arrow", function(){
	if($("#home_arrow_symbol").html()=="˅") {
		$("#home_arrow_symbol").html("&#708;")
	} else {
		$("#home_arrow_symbol").html("&#709;")
	}
	$("#home_advanced").slideToggle("slow")

})
