

items_pk = $("#items_pk").html()
load_places(items_pk)
function load_places(items_pk){
  $.ajax({
    url: "/buffet/ajax/get-place/",
    dataType: 'json',
    data: {
      "items_pk": items_pk,
    },
    success: function (data) {
      $("#list_item").html("")
      list_places = data.list_places
      str_total = ''
      str_total += '<div class="row">'
      for(i=0;i<list_places.length;i++){
        place = list_places[i]

        str_item = ''
        str_item += '<div class="col-md-4 col-sm-6">'
          str_item += '<div class="place_item" pk="' + place.pk + '">'
            str_item += '<div class="image">'
              str_item += '<a href="/buffet/detalhar/?pk=' + place.pk + '">'
                str_item += '<div class="overlay" id="overlay_' + place.pk + '">'
                  str_item += '<div class="inner">'
                    str_item += '<div class="content">'
                      str_item += '<p>' + place.description + '</p>'
                    str_item += '</div>'
                  str_item += '<div class="separador-20"> </div>'
                  str_item += '<div class="center_element">'
                    str_item += '<span style="color:#b4b5b4"><img src="/static/img/icon/person.png" alt="" style="width:10px;">&nbsp;&nbsp;' + place.capacity + ' pessoas</span>'
                  str_item += '</div>'

                  str_item += '</div>'
                str_item += '</div>'
                str_item += '<div class="place_featured">'
                  str_item += '<img src="/static/img/123festas/logo_white_squared.png">'
                str_item += '</div>'
                str_item += '<div class="img-center center-cropped place_image" style="background-image: url(/media/' + place.photo + ');"></div>'
              str_item += '</a>'
            str_item += '</div>'
            str_item += '<div class="wrapper place_description_wrapper">'
              str_item += '<div class="place_description_cell">'
                str_item += '<a class="place_name" href="/buffet/detalhar/?pk=' + place.pk + '">'
                  str_item += place.name
                str_item += '</a>'
                str_item += '<div class="separador-2"> </div>'
                str_item += '<figure class="place_address">' + place.address + '</figure>'
                str_item += '<h4 class="place_price">R$</h4>'
                str_item += '<h3 class="place_price">' + place.placeprice_min + '</h3>'
              str_item += '</div>'
              str_item += '<div class="place_description_cell" style="height:50px;">'
                str_item += '<div class="separador-5"> </div>'
                if(place.review_list.review_rates == "None") {
                  str_item += '<figure style="font-size:12px; color:#888888">Aguardando Primeira Avaliaçao!</figure>'
                } else {
                  str_item += '<div style="display:block">'
                    str_item += '<span style="color:#70b7c8; dislay:inline" class="stars" data-rating="' + place.review_list.review_rates.rate_average + '" data-num-stars="5"></span>&nbsp;'
                    str_item += '<span style="font-size:12px; color:#888888">' + place.review_list.review_rates.n_review + ' Avaliações</span>'
                  str_item += '</div>'                
                }

              str_item += '</div>'
            str_item += '</div>'
          str_item += '</div>'
        str_item += '</div>'

        str_total += str_item
      }
      str_total += '</div>'

      $("#list_item").append(str_total)
      $('.stars').stars();


    }
  })  
}







// ==================== 
// Order By
// ====================    
$("#order_by").on("change", function(){
  var current_pks = $("#places_pk").html()
  $.ajax({
    url: "/buffet/ajax/order-by/",
    dataType: 'json',
    data: {
      "current_pks":String(current_pks),
      "option":$("#order_by").val(),
    },
    success: function (data) {
      load_places(JSON.stringify(data.items_pk))
    }
  })
})












