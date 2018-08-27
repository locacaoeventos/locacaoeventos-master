// Rewriting function rating
function rating(element){
    var ratingElement =
        '<span class="stars">'+
            '<i class="fa fa-star s1" data-score="1"></i>'+
            '<i class="fa fa-star s2" data-score="2"></i>'+
            '<i class="fa fa-star s3" data-score="3"></i>'+
            '<i class="fa fa-star s4" data-score="4"></i>'+
            '<i class="fa fa-star s5" data-score="5"></i>'+
        '</span>'
    ;
    if( !element ) { element = ''; }
    $.each( $(element + ' .rating'), function(i) {
        $(this).append(ratingElement);
        if( $(this).hasClass('active') ){
            $(this).append('<input readonly hidden="" name="score_' + $(this).attr('data-name') +'" id="score_' + $(this).attr('data-name') +'">');
        }
        var rating = $(this).attr('data-rating');
        for( var e = 0; e < rating; e++ ){
            var rate = e+1;
            $(this).children('.stars').children( '.s' + rate ).addClass('active');
        }
    });

    var ratingActive = $('.rating.active i');
    ratingActive.on('hover',function(){
        for( var i=0; i<$(this).attr('data-score'); i++ ){
            var a = i+1;
            $(this).parent().children('.s'+a).addClass('hover');
        }
    },
    function(){
        for( var i=0; i<$(this).attr('data-score'); i++ ){
            var a = i+1;
            $(this).parent().children('.s'+a).removeClass('hover');
        }
    });
    ratingActive.on('click', function(){
        // Adjusting Scores to input
        var score = $(this).attr('data-score')
        var input_id = "#" + $(this).parent().parent().attr('id').replace("figure_", "") + "_id"
        $(input_id).val(score)



        // Old JS
        $(this).parent().parent().children('input').val( $(this).attr('data-score') );
        $(this).parent().children('.fa').removeClass('active');
        for( var i=0; i<$(this).attr('data-score'); i++ ){
            var a = i+1;
            $(this).parent().children('.s'+a).addClass('active');
        }

        // Checking if all the inputs are filled
        $("#send_button").prop("disabled", false)
        $(".rate").each(function(){
            if($(this).val() == ""){
                $("#send_button").prop("disabled", true)
            }
        })

        check_average()

        return false;
    });

}

$("#comment_id").keyup(function(){
    check_average()
})

// Calculate average
function check_average() {
    var rate_sum = 0
    $(".rate").each(function(){
        rate_sum += parseInt($(this).attr("value"))
    })
    rate_average = rate_sum/5
    if(rate_average<2.5 && $("#comment_id").val() == "") {
        if($("#comment_obligatory").css("display")=="none") {
            $("#comment_obligatory").fadeIn(500)   
            $("#send_button").attr("disabled", "disabled")            
        }
    } else {
        $("#comment_obligatory").fadeOut(500)    
        $("#send_button").removeAttr("disabled") 
    }  
}