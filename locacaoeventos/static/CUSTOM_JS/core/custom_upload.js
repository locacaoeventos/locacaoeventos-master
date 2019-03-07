$(function () {
  $(".js-upload-photos").click(function () {
    $("#fileupload").click();
  });

  $("#fileupload").fileupload({
    dataType: 'json',
    sequentialUploads: true,  /* 1. SEND THE FILES ONE BY ONE */
    start: function (e) {  /* 2. WHEN THE UPLOADING PROCESS STARTS, SHOW THE MODAL */
      $("#modal-progress").modal("show");
    },
    stop: function (e) {  /* 3. WHEN THE UPLOADING PROCESS FINALIZE, HIDE THE MODAL */
      $("#modal-progress").modal("hide");
    },
    progressall: function (e, data) {  /* 4. UPDATE THE PROGRESS BAR */
      var progress = parseInt(data.loaded / data.total * 100, 10);
      var strProgress = progress + "%";
      $(".progress-bar").css({"width": strProgress});
      $(".progress-bar").text(strProgress);
    },
    done: function (e, data) {
      if (data.result.is_valid) {
        div_str = '<div class="upload_image">'
        div_str +=    '<span class="x_option x_option_upload" pk="' + data.result.pk + '">&times;</span>'
        div_str +=    '<img class="img_gallery" pk="' + data.result.pk + '" src="' + data.result.url + '">'
        div_str += '</div>'
        $("#gallery").prepend(div_str)
        $("#upload_frame").remove()
        var current_val = $("#id_photos").val().split(",")
        if(current_val != ""){
          current_val.push(data.result.pk)
        } else {
          current_val = data.result.pk
        }
        $("#id_photos").val(current_val)
        $("#fileupload").val('');
      }
    }

  });

});


$(document).on("click", ".x_option_upload", function(){
  var current_val = $("#id_photos").val().split(",")
  var pk = $(this).attr("pk")
  var index = current_val.indexOf(pk);
  current_val.splice(index, 1); // Removing pk from input field
  $("#id_photos").val(current_val)
  $(this).parent().fadeOut(500).remove()

})