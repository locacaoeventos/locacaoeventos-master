$('#id_cpf_buyer').mask('000.000.000-00');
$('#id_cellphone').mask('(00)00000-0000');
$('#id_cellphone').keyup(function(){
  if($(this).val().length < 14) {
    $("#cellphone_error").html("O número de celular é curto demais")
    $("#cellphone_error").css("display", "block")
     document.getElementById("submit").disabled = true;
     validarSenhaSeller()
  } else {
    $("#cellphone_error").css("display", "none")
     document.getElementById("submit").disabled = false;
     validarSenhaSeller()
  }
});


function validarSenhaSeller(){
 password = document.getElementById("id_password").value
 confirm = document.getElementById("confirm").value
 if(password!="" && confirm!=""){
	 if(password.length >= 6) {
	     $('#tooshort').fadeOut(500);
	     document.getElementById("submit").disabled = false;

	   if (password == confirm){
	     $('#nomatchpswd').fadeOut(500);
	     document.getElementById("submit").disabled = false; 
	   }
	   else{
	     $('#nomatchpswd').fadeIn(500);
	     document.getElementById("submit").disabled = true;
	   }
	 } else {
	     $('#nomatchpswd').fadeOut(500);
	     $('#tooshort').fadeIn(500);
	     document.getElementById("submit").disabled = true;

	 } 	
	} else {
	     $('#tooshort').fadeOut(500);
	     $('#nomatchpswd').fadeOut(500);
	     document.getElementById("submit").disabled = false; 

	}

}