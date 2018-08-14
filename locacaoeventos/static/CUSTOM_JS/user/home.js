$('#date_id').datepicker({ dateFormat: 'dd/mm/yy' }).val()
$('#date_id').mask("00/00/0000",{placeholder:"Data"});

$("#home_arrow").click(function(){
	$("#home_advanced").slideToggle("slow")
})