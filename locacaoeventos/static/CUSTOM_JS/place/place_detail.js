// ==========================================
// Detail Header
// ==========================================
// Detail Image
$(".detail_header_img").hover(function(){
	$(".detail_header_img_round").fadeIn(300)
})
$(".detail_header_img").mouseleave(function(){
	$(".detail_header_img_round").fadeOut(300)
})
$(".detail_header_img_round").click(function() {
	var photo_links = []
	var photo_counter = 0
	var photo_index = 0
	var photo_move_type = $(this).attr("type")
	// Find indexes
	$(".detail_photo").each(function(){
		photo_links.push($(this).attr("style"))
		if($(this).hasClass("detail_photo_active")){
			if (photo_move_type=="right") {
				photo_index = photo_counter + 1
			} else {
				photo_index = photo_counter - 1
			}
			$(this).removeClass("detail_photo_active")
		}
		photo_counter += 1
	})	
	// Fix index
	if(photo_index==-1) {
		photo_index = photo_counter-1
	} else if(photo_index==photo_counter) {
		photo_index = 0
	}
	// Fix image
	var photo_counter_other = 0
	$(".detail_photo").each(function(){
		if(photo_counter_other==photo_index) {
			$(this).addClass("detail_photo_active")
		}
		photo_counter_other += 1
	})	

	$(".detail_header_img").attr("style", photo_links[photo_index])
})














// ==========================================
// Detail Description
// ==========================================


$(document).ready(function(){
	var div_height = $(".detail_description_text").height()
	if(div_height>70) {
		var fadeout_str = ""
        fadeout_str += '<div class="fadeout" id="detail_description_text_fadeout"></div>'
        fadeout_str += '<div id="detail_description_text_expand">Leia mais sobre este Espaço</div>'
        $(".detail_description_text").after(fadeout_str)
        $(".detail_description_text").css("height", "110")
	}
})
$(document).on("click", ".detail_photo", function(){
	$(".detail_photo").each(function(){
		$(this).css("opacity", "0.2")
	})
	$(this).css("opacity", "1")
	$(".detail_header_img").attr("style", $(this).attr("style"))

})
$(document).on("click", "#detail_description_text_expand", function(){
	$(".detail_description_text").css("height", "auto")
	$("#detail_description_text_fadeout").remove()
	$(this).remove()
})
