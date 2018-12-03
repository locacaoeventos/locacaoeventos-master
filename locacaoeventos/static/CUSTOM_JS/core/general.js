function get_url_parameter(url_string, url_parameter){
	var url = new URL(url_string);
	var url_parameter = url.searchParams.get(url_parameter);
	return url_parameter
}


$(document).ready(function(){
    $.fn.stars = function() {
        return $(this).each(function() {

            var rating = parseFloat($(this).data("rating"));
            var numStars = parseFloat($(this).data("numStars"));
            var fullStar = new Array(Math.floor(rating + 1)).join('<i class="fa fa-star"></i>');

            var halfStar = ((rating%1) !== 0) ? '<i class="fa fa-star-half-empty"></i>': '';

            var noStar = new Array(Math.floor(numStars + 1 - rating)).join('<i class="fa fa-star-o"></i>');

            $(this).html(fullStar + halfStar + noStar);

        });
    }
    $('.stars').stars();
})
function loading_icon() {
  var div_loading = ''
  div_loading += '<div style="width:100%; text-align:center; padding-top:50px; opacity:0.4">'
  div_loading +=   '<img src="/static/img/icon/loading.gif" style="width:50px">'
  div_loading += '</div>'
  $("#list_item").html(div_loading)
}