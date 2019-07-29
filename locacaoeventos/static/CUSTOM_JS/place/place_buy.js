// =====================================
// Select Price
// =====================================
$(document).on("click", ".placeprice_card", function () {
    $(".placeprice_card").each(function () {
        $(this).removeClass("placeprice_selected")
    })
    $(this).addClass("placeprice_selected")
    if($("#place_checkout").hasClass("place_checkout_disable")){
        $("#place_checkout").removeClass("place_checkout_disable")
        $('#place_checkout').animate({backgroundColor: '#98d000'}, 'slow');     
    }


    $(this).attr("pk")
    $("#placeprice_pk").val($(this).attr("pk"))
    console.log($(this).attr("name-price"))
    console.log($(this).attr("value-price"))
    $("#placeprice_chosen_name").html($(this).attr("name-price"))
    $("#placeprice_chosen_value").html($(this).attr("value-price"))

    $("#placeprice_value").val($(this).attr("placeprice").replace(".", "").replace(",", ""))
})

$(document).on("click", "#place_checkout", function () {
    if (!$(this).hasClass("place_checkout_disable")) { // PRICE SELECTED

        
        
        
        $('#buyingflux_checkout').fadeOut(400, function () {
            var div_str_payment_container = $("#payment_container").html()
            $("#payment_container").html("")
            var div_str_buyingflux_checkout = $("#buyingflux_checkout").html()
            $(this).html(div_str_payment_container).fadeIn(800)
            $("#payment_container").html(div_str_buyingflux_checkout)
        });


    }
})



// =====================================
// Paying
// =====================================
$('#zip_code').mask('00000-000');



$(document).ready(function(){
    $(document).on("keyup", ".pay_col_editable", function(){
        console.log($(this).attr("id"))
        if($(this).attr("id").includes("zip")){
            if($("#zip_code").val().length >= 9){
                var cep = $("#zip_code").val().replace("-", "")
                $.getJSON("https://viacep.com.br/ws/" + cep + "/json/").done(function( data ) {
                    if(data.erro) {
                        disable_button()

                    } else {
                        $("#number").removeClass("pay_noneditable_field")               
                        $("#number").attr("readonly", false)



                        $("#id_state").val(data.uf)
                        $("#id_city").val(data.localidade)
                        $("#id_neighbourhood").val(data.bairro)
                        $("#id_street").val(data.logradouro)
                        
                    }
                });
            } else {
                disable_button()
            }
        } else {            
            console.log($("#number").val())
            if($("#number").val() != ""){
                console.log("foi")
                $(".pay_button").removeClass("pay_button_disabled")
                $(".pay_button").addClass("pay_button_green")
            } else {
                console.log("fn oi")
                $(".pay_button").addClass("pay_button_disabled")
                $(".pay_button").removeClass("pay_button_green")

            }
        }


    })
    // Back To Price button
    $(document).on("click", "#backto_selectprice", function () {

        $('#buyingflux_checkout').fadeOut(400, function () {
            var div_str_buyingflux_checkout = $("#buyingflux_checkout").html()
            $("#buyingflux_checkout").html("")
            var div_str_payment_container = $("#payment_container").html()

            $(this).html(div_str_payment_container).fadeIn(800)
            $("#payment_container").html(div_str_buyingflux_checkout)
        });


    })

})




function disable_button(){
    $("#number").addClass("pay_noneditable_field")              
    $("#number").attr("readonly", true)
    $("#number").val("")
    $("#id_state").val("")
    $("#id_city").val("")
    $("#id_neighbourhood").val("")
    $("#id_street").val("")
    $(".pay_button").addClass("pay_button_disabled")
    // $('.pay_button').animate({backgroundColor: '#dddddd'}, 'slow');
}
