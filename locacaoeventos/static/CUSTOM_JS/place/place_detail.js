// ==========================================
// Gallery
// ==========================================
$("#detail_header_showphotos").click(function(){
  if($(this).hasClass("place_favorite")){
    $(this).removeClass("place_favorite")
    $(this).html('<img src="/static/img/icon/favorite.png" style="width:20px;vertical-align:bottom; display:inline-block"/> &nbsp;Amei')
  } else {
    $(this).addClass("place_favorite")
    $(this).html('<img src="/static/img/icon/favorite-selected.png" style="width:20px;vertical-align:bottom; display:inline-block"/> &nbsp;Amei')

  }
})






// ==========================================
// Buying Flux
// ==========================================
var window_width  = $(window).width();
if(window_width>=992){
  var top_offset = $('#buying_flux').offset().top - 50;
  var featured_offset = $('#featured').offset().top - 800;



  $(window).scroll(function (event) {
    var y = $(this).scrollTop();
    if (y >= top_offset){
      if(y>featured_offset){

        $('#buying_flux').removeClass('fixed');
        $('#buying_flux').addClass('absolute');
        $('#buying_flux').css('top', featured_offset-580);
        console.log(featured_offset)

      }
      else {
        $('#buying_flux').css('top', "50");
        $('#buying_flux').addClass('fixed');
        $('#buying_flux').removeClass('absolute');

      }
    }
    else{
      $('#buying_flux').css('top', "0");
      $('#buying_flux').removeClass('fixed');
      $('#buying_flux').removeClass('absolute');
    }
  });    
}
$(document).on("keyup mouseup", "#capacity_form", function(){
  check_field_availability()    
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














// ==========================================
// Reviews
// ==========================================
$("#review_read_more").click(function(){
	$("#reviews_wrapper").slideToggle(300)
})