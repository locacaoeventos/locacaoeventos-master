  // Load Messages
  function load_messages_visualize(place_pk, buyerprofile_pk){
    $.ajax({
      url: "/usuario/chat/get-visualizar/",
      dataType: 'json',
      data: {
        "place_pk":place_pk,
        "buyerprofile_pk":buyerprofile_pk,
      },
      success: function (data) {
        if(data.messages.length>0) {
          var div_str = ''
          for(i=0;i<data.messages.length;i++) {
            var message = data.messages[i]
            if(message.photo.indexOf("/media")>0) {
              message.photo.replaceWith("/media") = ""
            }
            if(message.photo.indexOf("//media/")>0) {
              message.photo.replaceWith("/media") = ""
            }

            div_str += '<div class="chat_message">'
            div_str +=   '<div class="chat_photo' 
                    if(message.from_this_user==true){div_str += ' chat_photo_from'}
                    div_str += '">'
            div_str +=     '<div class="center-cropped img-center" style="background-image: url(' + message.photo + '); width:40px; height:40px; border-radius:50%"></div>'
            div_str +=   '</div>'
            div_str +=    '<div class="chat_info'

                    if(message.from_this_user==true){div_str += ' chat_info_from'}
                    div_str += '">'

            div_str +=     '<div class="chat_author">'
            div_str +=       message.from
            div_str +=     '</div>'
            div_str +=     '<div class="chat_text_container">'
            for(j=0;j<message.message_text.length;j++){
              div_str +=     '<div class="chat_text">' + message.message_text[j] + "</div><br>"
            }
            div_str +=     '</div>'
            div_str +=   '</div>'
            div_str += '</div>'
          }
          $("#chat_conversation_container").html(div_str)              
        } else {
          $("#chat_conversation_container").html("Envie uma mensagem!<br><br>")              
        }

      }
    })
  }
  function send_message_visualize(place_pk, buyerprofile_pk) {
    var message_text = $("#message_input").val()
    if(message_text != ""){
      $.ajax({
        url: "/usuario/chat/contact/",
        dataType: 'json',
        data: {
          "place_pk":place_pk,
          "message_text":message_text,
          "buyerprofile_pk":buyerprofile_pk,
        },
        success: function (data) {
          $("#message_input").val("")

          load_messages_visualize(place_pk, buyerprofile_pk)
          setTimeout(function(){
            var objDiv = document.getElementById("chat_conversation_container")
            objDiv.scrollTop = objDiv.scrollHeight
          }, 1000)
        }
      })
    }  
  }
  function load_messages_detail(place_pk, buyerprofile_pk){
    $.ajax({
      url: "/usuario/chat/get-visualizar/",
      dataType: 'json',
      data: {
        "place_pk":place_pk,
      },
      success: function (data) {
        if(data.messages.length>0) {
          var div_str = ''
          for(i=0;i<data.messages.length;i++) {
            var message = data.messages[i]

            message.photo = message.photo.replace("/media//", "/")

            div_str += '<div class="chat_message'
                    if(message.from_this_user==true){div_str += ' chat_message_from'}
                    div_str += '">'


            div_str +=   '<div class="chat_photo'
                    if(message.from_this_user==true){div_str += ' chat_photo_from'}
                    div_str += '">'

            div_str +=     '<div class="center-cropped img-center" style="background-image: url(' + message.photo + '); width:30px; height:30px; border-radius:50%"></div>'
            div_str +=   '</div>'
            div_str +=   '<div class="chat_text_container">'
            div_str +=     '<div class="chat_author">'
            div_str +=       message.from
            div_str +=     '</div>'
            div_str +=     '<div class="chat_text">'
            for(j=0;j<message.message_text.length;j++){
              div_str += message.message_text[j] + "<br>"
            }
            div_str +=     '</div>'
            div_str +=   '</div>'
            div_str += '</div>'
          }
          $("#chat_conversation_container").html(div_str)              
        } else {
          $("#chat_conversation_container").html("Envie uma mensagem!<br><br>")              
        }

      }
    })


  }

