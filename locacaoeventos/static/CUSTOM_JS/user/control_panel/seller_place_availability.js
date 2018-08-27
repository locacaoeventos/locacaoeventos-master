// Forms new Unavailability
$("#send_new_unavailability").click(function(e){
	 $("#error_unavailability").css("display", "None")
	var unavailability_begin = []
	var unavailability_end = []
	$(".begin").each(function(){
		unavailability_begin.push($(this).val())
	})
	$(".end").each(function(){
		unavailability_end.push($(this).val())
	})

	if(unavailability_begin.indexOf("")<0 && unavailability_end.indexOf("")<0){ // All fields are filled
		e.preventDefault()
		place_pk = $("#place_pk").attr("pk")

	  	$.ajax({
	  		url: "/usuario/ajax/unavailability/create/",
	  		dataType: 'json',
	  		data: {
				"place_pk":place_pk,
				"unavailability_begin":String(unavailability_begin),
				"unavailability_end":String(unavailability_end),
	  		},
	  		success: function (data) {

	  			if(data.error=="false") { // AJAX succeeded
					$(".begin").each(function(){
						$(this).val("")
					})
					$(".end").each(function(){
						$(this).val("")
					})


				    $.ajax({
				      url: "/usuario/ajax/calendario/",
				      dataType: 'json',
				      data: {
				        "pk": data.place_pk,
				        "meses":0
				      },
				      success: function (data) {
				        $("#month_ajax").html(data["month"])
				        $("#year_ajax").html(data["year"])
				        str_days = ""
				        for(i=0;i<data["list_month"].length;i++){
				          str_days += data["list_month"][i]
				        }
				        $("#days_ajax").html(str_days)
				      }
				    })
	  			} else {
	  				$("#error_unavailability").html(data.error)
					$("#error_unavailability").css("display", "block")
	  			}
	  		}
	  	})
	}
})







// Same day
$("#unavailability_sameday").click(function(){
	var unavailability_begin = []
	$(".begin").each(function(){
		unavailability_begin.push($(this).val())
	})
	var i = 0
	$(".end").each(function(){
		$(this).val(unavailability_begin[i])
		i += 1
	})

})







// Select day
$(document).on("click", ".day_select", function() {
	var day = String($(this).html())
	if(day.length==1) {
		day = "0" + day
	}
	$("#id_day_begin").val(day)

	var month = String($("#month_ajax").attr("month"))
	if(month.length==1) {
		month = "0" + month
	}
	$("#id_month_begin").val(month)

	var year = $("#year_ajax").html()
	$("#id_year_begin").val(year)

})




