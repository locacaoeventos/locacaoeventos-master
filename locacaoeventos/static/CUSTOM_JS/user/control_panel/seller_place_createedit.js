$(document).ready(function(){
	$("textarea").attr("rows", "7")

	// Children Rides
	var find = "\"";
	var re = new RegExp(find, 'g'); // Yup, we have to do this to replace all
	var current_input = $("#id_children_rides").val().replace(/\'/g, "\"").replace(re, "").replace("[", "{").replace("]", "}")
	current_input = current_input.replace("[", "").replace("]", "")
	if(current_input=="{}"){current_input=""}
	$("#id_children_rides").val(current_input)
	var children_rides_current = $("#id_children_rides").val().replace(/\'/g, "\"").replace(re, "").replace("{", "").replace("}", "")
	var children_rides_list = children_rides_current.split(",")
	var div_str = ""
	for(i=0;i<children_rides_list.length;i++) {
		div_str += '<div class="add_option" input_val="' + children_rides_list[i] + '" type="children_rides">'
		div_str +=     children_rides_list[i] + '<span class="x_option x_option_add" input_val="' + children_rides_list[i] + '">&times;</span>'
		div_str += '</div>'	
	}
	$("#id_children_rides_container").append(div_str)


	// Decoration
	var current_input = $("#id_decoration").val().replace(/\'/g, "\"").replace(re, "").replace("[", "{").replace("]", "}")
	current_input = current_input.replace("[", "").replace("]", "")
	if(current_input=="{}"){current_input=""}
	$("#id_decoration").val(current_input)
	var decoration_current = $("#id_decoration").val().replace(/\'/g, "\"").replace(re, "").replace("{", "").replace("}", "")
	var decoration_list = decoration_current.split(",")
	var div_str = ""
	for(i=0;i<decoration_list.length;i++) {
		div_str += '<div class="add_option" input_val="' + decoration_list[i] + '" type="decoration">'
		div_str +=     decoration_list[i] + '<span class="x_option x_option_add" input_val="' + decoration_list[i] + '">&times;</span>'
		div_str += '</div>'	
	}
	$("#id_decoration_container").append(div_str)



	// Photos
	var photos_list = $("#id_photos").val().replace(/\'/g, "\"")
  	$.ajax({
  		url: "/get_photo/",
  		dataType: 'json',
  		data: {
  			"photos_list": photos_list,
  		},
  		success: function (data) {
  			var div_str = ""
  			for(i=0;i<data.photos.length;i++) {
  				photo = data.photos[i]
		        div_str += '<div class="upload_image">'
		        div_str +=    '<span class="x_option x_option_upload" pk="' + photo.pk + '">&times;</span>'
		        div_str +=    '<img class="img_gallery" src="/media/' + photo.url + '">'
		        div_str += '</div>'
  			}
  			if(data.photos.length>0) {
        		$("#upload_frame").remove()
  			}

	        $("#gallery").prepend(div_str)
  		}
  	})







})







$(".add_button").click(function(){
	var type = $(this).attr("type")
	var input_id = "#id_" + type + "_input"
	var form_id = "#id_" + type
	var container_id = "#id_" + type + "_container"

	var input_val = $(input_id).val()
	var current_val = $(form_id).val().replace("{", "").replace("}", "")

	if(input_val!=""){
		if(current_val==""){
			$(form_id).val("{" + current_val + input_val + "}")
		} else {
			$(form_id).val("{" + current_val + "," + input_val + "}")
		}
		$(input_id).val("")		
		div_str = '<div class="add_option" input_val="' + input_val + '" type="' + type + '">'
		div_str     += input_val + '<span class="x_option x_option_add" input_val="' + input_val + '">&times;</span>'
		div_str += '</div>'
		$(container_id).append(div_str).hide().fadeIn(500)
	}

})


$(document).on("click", ".x_option_add", function(){
	var input_val = $(this).attr("input_val")
	var type = $(this).parent().attr("type")
	var form_id = "#id_" + type
	$(this).parent().fadeOut(400, function() { $(this).remove();})

	var form_val = $(form_id).attr("value").replace("{", "").replace("}", "")
	var current_array = form_val.split(",")
	var index_object = current_array.indexOf(input_val)
	current_array.splice(index_object, 1);
	current_array = "{" + String(current_array) + "}"

	if(current_array=="{}"){
		current_array = ""
	}
	$(form_id).attr("value", current_array)

})

$(document).on("click", "#menu_click", function(){
	$("#id_menu").trigger("click")
})