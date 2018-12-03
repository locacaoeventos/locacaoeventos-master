// ===========================================================
// Price
// ===========================================================
$(document).ready(function(){
    placeprice_get()
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
            console.log("aaaaaaaaaaaaaaaaaa")
            console.log("aaaaaaaaaaaaaaaaaa")
            console.log("aaaaaaaaaaaaaaaaaa")
            placeprice_show(data)
        }
    })    

})






















// ===========================================================
// Unavailability
// ===========================================================
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




