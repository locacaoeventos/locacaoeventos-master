
// ===========================================================
// Menu
// ===========================================================
$('.calendar_input').mask("00 / 00 / 0000",{placeholder:"Data"});
$(".bread").click(function(){
    var id = $(this).attr("id")
    var option = $(this).attr("option")
    $(".bread").removeClass("breadcrumbs_selected")
    $("#"+id).addClass("breadcrumbs_selected")
    $(".options_menu").css("display", "none")
    $("#"+option).css("display", "block")
})






// ===========================================================
// Price
// ===========================================================
$(document).ready(function(){
    placeprice_get()
    unavailabilities_get()
    sazonality_get()
})

// Description ===================================================
    
    // ======================================================== //
    // ================== Adding Description ================== //
    // ======================================================== //
function titleCase(str) {
   var splitStr = str.toLowerCase().split(' ');
   for (var i = 0; i < splitStr.length; i++) {
       // You do not need to check if i is larger than splitStr length, as your for does that for you
       // Assign it back to the array
       splitStr[i] = splitStr[i].charAt(0).toUpperCase() + splitStr[i].substring(1);     
   }
   // Directly return the joined string
   return splitStr.join(' '); 
}



function add_description_to_container(){
    // var type = $(this).attr("type")  ==========> I am seting as "description" bc there are no other options such as children_rides
    $("#placeholder_description").remove()
    var type = "description"

    var input_id = "#id_" + type + "_input"
    var form_id = "#id_" + type
    var container_id = "#id_" + type + "_container"

    var input_val = titleCase($(input_id).val())
    var current_val = $(form_id).val().replace("[", "").replace("]", "")
    if(input_val!=""){
        if(current_val==""){
            $(form_id).val("[" + current_val + input_val + "]")
        } else {
            $(form_id).val("[" + current_val + "," + input_val + "]")
        }
        $(input_id).val("")     
        div_str = '<div class="add_option" input_val="' + input_val + '" type="' + type + '">'
        div_str     += input_val + '<span class="x_option x_option_add" input_val="' + input_val + '">&times;</span>'
        div_str += '</div>'
        $(container_id).append(div_str).hide().fadeIn(500)
    }  
}
$(".add_button").click(function(){
    add_description_to_container()
})

$("#id_description_input").keyup(function(e){
    if(e.which == 13) { // enter key
        e.stopPropagation()
        add_description_to_container()
    }
})




    // ======================================================== //
    // ================ Subtracting Description =============== //
    // ======================================================== //
$(document).on("click", ".x_option_add", function(){
    var input_val = $(this).attr("input_val")
    var type = $(this).parent().attr("type")
    var form_id = "#id_" + type
    $(this).parent().fadeOut(400, function() { $(this).remove();})

    var form_val = $(form_id).val().replace("[", "").replace("]", "")
    var current_array = form_val.split(",")
    var index_object = current_array.indexOf(input_val)
    current_array.splice(index_object, 1);
    current_array = "[" + String(current_array) + "]"

    if(current_array=="[]"){
        current_array = ""
    }
    $(form_id).val(current_array)

})


// Place Price Price
    $('#id_value').keyup(function(){
        $('#id_value').maskMoney();
    });    
    $('#id_value_min').keyup(function(){
        $('#id_value_min').maskMoney();
    });    


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
        try { // There were some prices which were not with lists
            var descriptions = JSON.parse(placeprice.description)
        }
        catch(err) {
            var descriptions = [placeprice.description]
        }
        str_div += '<div class="placeprice_card">'
            str_div += '<div class="crossmark_delete" placeprice_pk="' + placeprice.pk + '" place_pk="' + placeprice.place_pk + '">&#10006;</div>'
            str_div += '<div class="separador-20"> </div>'
            str_div += '<div class="placeprice_card_name">' + placeprice.name + '</div><br>'
            str_div += '<div class="placeprice_card_description_long">' + placeprice.description_long + '</div><br>'
            for(j=0;j<descriptions.length;j++){
                str_div += '<span class="placeprice_card_attr">- ' + descriptions[j] + '</span><br>'

            }
            str_div += '<div class="separador-10"> </div>'

            str_div += '<span class="placeprice_card_attr"><b>Mínimo</b>: ' + placeprice.capacity_min + ' pessoas</span><br>'
            str_div += '<span class="placeprice_card_attr"><b>Máximo</b>: ' + placeprice.capacity_max + ' pessoas</span><br>'
            str_div += '<span class="placeprice_card_attr"><b>Valor</b>: R$ ' + placeprice.value + '</span><br>'
            str_div += '<span class="placeprice_card_attr"><b>Valor Mínimo</b>: R$ ' + placeprice.value_min + '</span><br>'
            str_div += '<div class="separador-10"> </div>'
        str_div += '</div>'                
    }

    $("#placeprice_container").html(str_div);

    // if(data.placeprice_list.length==0){
    //     $("#has_place_price_list").css("display", "block")
    // } else {
    //     $("#has_place_price_list").css("display", "none")
    // }

}


function placesazonality_show(data){
    div_str = ""
    $("#sazonality_container").empty();

    for(i=0;i<data.placesazonality_list.length;i++){
        var placesazonality = data.placesazonality_list[i]
        div_str += '<div class="placesazonality_card">'
        div_str += '<div class="col-md-6">'
        div_str += '<div class="unavailability_card">'
            div_str += '<div class="sazonality_crossmark_delete" sazonality_pk="' + placesazonality.pk + '">&#10006;</div>'
            div_str += 'Dia: ' + placesazonality.day + '<br>'
            div_str += 'Modificador: ' + placesazonality.modifier +'%'+ '<br>'
            div_str += 'Período: ' + placesazonality.period +'<br>'
        div_str += '</div>'
        div_str += '</div>'        
        div_str += '</div>'        
          
    }
    $("#sazonality_container").html(div_str)      


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

$(document).on("click", "#placesazonality_add", function(){
    var is_valid = placesazonality_validade_form()
    if(is_valid==false){
        $("#placesazonality_add_error").css("display", "block")
    } else {
        $("#placesazonality_add_error").css("display", "none")
        placesazonality_add()
    }
})


function placeprice_validade_form(){
    var is_valid = true
    $(".placeprice_field").each(function(){
        if($(this).val()==""){
            if($(this).attr("id" != "id_value_min")) {
                is_valid = false

            }
        }
    })
    return is_valid
}


function placesazonality_validade_form(){
    var is_valid = true
    console.log(sazonalities)
    $(".placesazonality_input").each(function(){
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
    var description_long = $("#id_description_long").val()
    var value = $("#id_value").val()
    var value_min = $("#id_value_min").val()
    var capacity_min = $("#id_capacity_min").val()
    var capacity_max = $("#id_capacity_max").val()

    $.ajax({
        url: "/usuario/ajax/placeprice/create/",
        dataType: 'json',
        data: {
            "place_pk":place_pk,
            "name":name,
            "description":description,
            "description_long":description_long,
            "value":value,
            "value_min":value_min,
            "capacity_min":capacity_min,
            "capacity_max":capacity_max,
        },
        success: function (data) {
            placeprice_show(data)

            $("#id_name").val("")
            $("#id_description").val("")
            $("#id_description_long").val("")
            $("#id_value").val("")
            $("#id_value_min").val("")
            $("#id_capacity_min").val("")
            $("#id_capacity_max").val("")
            $("#id_description_container").html(" ")
        }
    })    

}


function placesazonality_add(){
    var place_pk = $("#id_place_pk").val()
    var modifier = $("#modifier_percent").val()
    var date = $("#date_id").val()
    var id_min_period = false
    var id_max_period = false
    console.log($("#id_min_period_mod"))
    if($("#id_min_period_mod").is(':checked')){
        id_min_period = true
    }
    
    if($("#id_max_period_mod").is(':checked')){
        id_max_period = true
    }

    $.ajax({
        url: "/usuario/ajax/sazonality/create/",
        dataType: 'json',
        data: {
            "place":place_pk,
            "modifier":modifier,
            "day":date,
            "id_min_period":id_min_period,
            "id_max_period":id_max_period,
        },
        success: function (data) {
            $("#placesazonality_add_error_date").css("display", "none")
            placesazonality_show(data)
            $("#modifier_percent").val("")
            $("#date_id").val("")
        },
        error: function(){
            $("#placesazonality_add_error_date").css("display", "block")

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
$('#date_id').mask("00 / 00 / 0000",{placeholder:"DD / MM / AAAA"});

// Erase Optional
$("#unavailability_optional_erase").click(function(){
    $("#id_late_begin").val("")
    $("#id_late_end").val("")

})

// Forms new Unavailability
  function load_calendar(place_pk, months, elem, period){
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


    if(day != ""){ // All fields are filled
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
                $("#id_min_period").attr("checked", false)
                $("#id_max_period").attr("checked", false)
                
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

$(document).on("click", ".sazonality_crossmark_delete", function(){
    $.ajax({
        url: "/usuario/ajax/sazonality/delete/",
        dataType: 'json',
        data: {
            "sazonality_pk":$(this).attr("sazonality_pk"),
            "place_pk":$("#id_place_pk").val(),
        },
        success: function (data) {
            placesazonality_show(data)
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

function sazonality_get(){
    $.ajax({
        url: "/usuario/ajax/sazonality/get/",
        dataType: 'json',
        data: {
            "place_pk":$("#id_place_pk").val(),
        },
        success: function (data) {
            div_str = ""
            sazonalities = data.placesazonality_list
            for(i=0;i<sazonalities.length;i++){
                sazonality = sazonalities[i]
                div_str += '<div class="col-md-6">'
                    div_str += '<div class="unavailability_card">'
                        div_str += '<div class="sazonality_crossmark_delete" sazonality_pk="' + sazonality.pk + '">&#10006;</div>'
                        div_str += 'Dia: ' + sazonality.day + '<br>'
                        div_str += 'Modificador: ' + sazonality.modifier +'%'+ '<br>'
                        div_str += 'Período: ' + sazonality.period +'<br>'
                    div_str += '</div>'
                div_str += '</div>'                
            }
            $("#sazonality_container").html(div_str)
        }
    })
}



