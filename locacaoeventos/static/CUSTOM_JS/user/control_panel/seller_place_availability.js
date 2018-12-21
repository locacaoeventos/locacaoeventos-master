// ===========================================================
// Price
// ===========================================================
$(document).ready(function(){
    placeprice_get()
    unavailabilities_get()
})

// GET ===================================
function placeprice_get(){
    var place_pk = $("#id_place_pk").val()
    $.ajax({
        url: "/usuario/ajax/placeprice/get/",
        dataType: 'json',
        data: {
            "place_pk":place_pk,
        },
        success: function (data) {
            placeprice_show(data)
        }
    })    
}
function placeprice_show(data){
    str_div = ""
    for(i=0;i<data.placeprice_list.length;i++){
        var placeprice = data.placeprice_list[i]
        str_div += '<div class="col-md-6">'
        str_div += '<div class="placeprice_card">'
            str_div += '<div class="crossmark_delete" placeprice_pk="' + placeprice.pk + '" place_pk="' + placeprice.place_pk + '">&#10006;</div>'
            str_div += '<div class="separador-10"> </div>'
            str_div += '<div class="placeprice_card_name">' + placeprice.name + '</div><br>'
            str_div += '<span class="placeprice_card_attr">Valor: ' + placeprice.value + '</span><br>'
            str_div += '<span class="placeprice_card_attr">Descrição: ' + placeprice.description + '</span><br>'
            str_div += '<span class="placeprice_card_attr">Mínimo: ' + placeprice.capacity_min + ' pessoas</span><br>'
            str_div += '<span class="placeprice_card_attr">Máximo: ' + placeprice.capacity_max + ' pessoas</span><br>'
            str_div += '<div class="separador-10"> </div>'
        str_div += '</div>'                
        str_div += '</div>'                
    }


    $("#placeprice_container").html(str_div)
}


// CREATE ===================================
$(document).on("click", "#placeprice_add", function(){
    var is_valid = placeprice_validade_form()
    if(is_valid==false){
        $("#placeprice_add_error").css("display", "block")
    } else {
        $("#placeprice_add_error").css("display", "none")
        placeprice_add()
    }

})

function placeprice_validade_form(){
    var is_valid = true
    $(".placeprice_field").each(function(){
        if($(this).val()==""){
            is_valid = false
        }
    })
    return is_valid
}

function placeprice_add(){
    var place_pk = $("#id_place_pk").val()
    var name = $("#id_name").val()
    var description = $("#id_description").val()
    var value = $("#id_value").val()
    var capacity_min = $("#id_capacity_min").val()
    var capacity_max = $("#id_capacity_max").val()

    $.ajax({
        url: "/usuario/ajax/placeprice/create/",
        dataType: 'json',
        data: {
            "place_pk":place_pk,
            "name":name,
            "description":description,
            "value":value,
            "capacity_min":capacity_min,
            "capacity_max":capacity_max,
        },
        success: function (data) {
            placeprice_show(data)

            $("#id_name").val("")
            $("#id_description").val("")
            $("#id_value").val("")
            $("#id_capacity_min").val("")
            $("#id_capacity_max").val("")

        }
    })    

}


// DELETE ===================================
$(document).on("click", ".crossmark_delete", function(){
    var placeprice_pk = $(this).attr("placeprice_pk")
    var place_pk = $(this).attr("place_pk")
    $.ajax({
        url: "/usuario/ajax/placeprice/delete/",
        dataType: 'json',
        data: {
            "placeprice_pk":placeprice_pk,
            "place_pk":place_pk,
        },
        success: function (data) {
            placeprice_show(data)
        }
    })    

})






















// ===========================================================
// Unavailability
// ===========================================================
$('#date_id').mask("00 / 00 / 0000",{placeholder:"Data"});

// Erase Optional
$("#unavailability_optional_erase").click(function(){
    $("#id_late_begin").val("")
    $("#id_late_end").val("")

})

// Forms new Unavailability
  function load_calendar(place_pk, months, elem, period){
    console.log(place_pk)
    $.ajax({
      url: "/usuario/ajax/calendario/",
      dataType: 'json',
      data: {
        "pk": place_pk,
        "meses":months,
        "period":period,
      },
      success: function (data) {
        $("#month_ajax").html(data["month"])
        $("#month_ajax").attr("month", data["month_int"])
        $("#year_ajax").html(data["year"])
        str_days = ""
        for(i=0;i<data["list_month"].length;i++){
          str_days += data["list_month"][i]
        }
        $("#days_ajax").html(str_days)

        // Animation
        if(elem!="none"){
          if(elem.attr("count") == -1) {
            $(".calendar_wrapper").show("slide", { direction: "left" }, 500);
          } else {
            $(".calendar_wrapper").show("slide", { direction: "right" }, 500);
          }

        }

      }
    })


  }

$("#send_new_unavailability").click(function(e){
    $("#error_unavailability").css("display", "None")

    var day = $("#date_id").val()

    var has_period = false
    var id_min_period = false
    var id_max_period = false
    if($("#id_min_period").is(':checked')){
        has_period = true
        id_min_period = true
    }
    if($("#id_max_period").is(':checked')){
        has_period = true
        id_max_period = true
    }


    if(day != "" && has_period == true){ // All fields are filled
        e.preventDefault()
        place_pk = $("#id_place_pk").val()

        $.ajax({
            url: "/usuario/ajax/unavailability/create/",
            dataType: 'json',
            data: {
                "place_pk":$("#id_place_pk").val(),
                "day":day,
                "id_min_period":id_min_period,
                "id_max_period":id_max_period,
                "unavailability_repeat":$("#unavailability_repeat").val(),

            },
            success: function (data) {

                if(data.error==false) { // AJAX succeeded
                    $(".begin").each(function(){
                        $(this).val("")
                    })
                    $(".end").each(function(){
                        $(this).val("")
                    })
                    $("#date_id").val("")


                    load_calendar(place_pk, 0, "none", [1,1])
                    unavailabilities_get()

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


// Delete Unavailabilities
$(document).on("click", ".unavailability_crossmark_delete", function(){
    $.ajax({
        url: "/usuario/ajax/unavailability/delete/",
        dataType: 'json',
        data: {
            "placeunavailability_pk":$(this).attr("placeunavailability_pk"),
        },
        success: function (data) {
            unavailabilities_get()
            load_calendar($("#id_place_pk").val(), 0, "none", [1,1])

        }
    })
})



// Show unavailabilities
function unavailabilities_get(){
    $.ajax({
        url: "/usuario/ajax/unavailability/get/",
        dataType: 'json',
        data: {
            "place_pk":$("#id_place_pk").val(),
        },
        success: function (data) {
            div_str = ""
            unavailabilities = data.placeunavailabilities
            for(i=0;i<unavailabilities.length;i++){
                unavailability = unavailabilities[i]
                div_str += '<div class="col-md-6">'
                    div_str += '<div class="unavailability_card">'
                        div_str += '<div class="unavailability_crossmark_delete" placeunavailability_pk="' + unavailability.placeunavailability_pk + '">&#10006;</div>'
                        div_str += 'Dia: ' + unavailability.day + '<br>'
                        div_str += 'Horário: ' + unavailability.period + '<br>'
                        if(unavailability.repeat != null){
                            div_str += '<b>' + unavailability.repeat + '</b><br>'
                        }
                    div_str += '</div>'
                div_str += '</div>'                
            }
            $("#unavailability_container").html(div_str)
        }
    })
}


