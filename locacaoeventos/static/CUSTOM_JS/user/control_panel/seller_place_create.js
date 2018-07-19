$(document).ready(function(){
	$("textarea").attr("rows", "7")
})

$(".add_button").click(function(){
	var type = $(this).attr("type")
	var input_id = "#id_" + type + "_input"
	var form_id = "#id_" + type
	var container_id = "#id_" + type + "_container"

	var input_val = $(input_id).val()
	var current_val = $(form_id).val()

	if(input_val!=""){
		if(current_val==""){
			$(form_id).val(current_val + input_val)
		} else {
			$(form_id).val(current_val + "," + input_val)
		}
		$(input_id).val("")		
		div_str = '<div class="add_option" input_val="' + input_val + '" type="' + type + '">'
		div_str     += input_val + '<span class="x_option x_option_add">&times;</span>'
		div_str += '</div>'
		$(container_id).append(div_str).hide().fadeIn(500)
	}

})


$(document).on("click", ".x_option_add", function(){
	var input_val = $(this).attr("input_val")
	var type = $(this).parent().attr("type")
	var form_id = "#id_" + type
	$(this).parent().fadeOut(400, function() { $(this).remove();})

	var form_val = $(form_id).attr("value")
	var current_array = form_val.split(",")
	var index_object = current_array.indexOf(5)
	current_array.splice(index_object, 1);

	$(form_id).attr("value", current_array)

})