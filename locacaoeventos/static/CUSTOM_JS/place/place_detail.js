








// ==========================================
// Price Sticky
// ==========================================
  var window_width  = $(window).width();

  if(window_width>=992){
    var top_offset = $('#buying_flux').offset().top - 86;
	var featured_offset = $('#featured').offset().top -250;


    $(window).scroll(function (event) {
      var y = $(this).scrollTop();

      if (y >= top_offset){
        if(y>featured_offset){

          $('#buying_flux').removeClass('fixed');
          $('#buying_flux').addClass('absolute');
          $('#buying_flux').css('top', featured_offset-500);

        }
        else {
          $('#buying_flux').css('top', "");
          $('#buying_flux').addClass('fixed');
          $('#buying_flux').removeClass('absolute');

        }
      }
      else{
          $('#buying_flux').css('top', "");
        $('#buying_flux').removeClass('fixed');
        $('#buying_flux').removeClass('absolute');
      }
    });    
  }





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