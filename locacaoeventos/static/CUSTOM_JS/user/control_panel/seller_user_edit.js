$('#id_cellphone_seller').mask('(00) 00000-0000');
$('#id_cellphone_seller').keyup(function(){
  if($(this).val().length < 14) {
    $("#cellphone_seller_error").html("O número de celular é curto demais")
    $("#cellphone_seller_error").css("display", "block")
     document.getElementById("submit").disabled = true;
     validarSenhaSeller()
  } else {
    $("#cellphone_seller_error").css("display", "none")
     document.getElementById("submit").disabled = false;
     validarSenhaSeller()
  }
});

$('#id_cpf').mask('000.000.000-00');
$('#id_cnpj').mask('00.000.000/0000-00');

function validarSenhaSeller(){
 password = document.getElementById("id_password_seller").value
 confirm = document.getElementById("confirm_seller").value
 if(password!="" && confirm!=""){
	 if(password.length >= 6) {
	     $('#tooshort_seller').fadeOut(500);
	     document.getElementById("submit").disabled = false;

	   if (password == confirm){
	     $('#nomatchpswd_seller').fadeOut(500);
	     document.getElementById("submit").disabled = false; 
	   }
	   else{
	     $('#nomatchpswd_seller').fadeIn(500);
	     document.getElementById("submit").disabled = true;
	   }
	 } else {
	     $('#nomatchpswd_seller').fadeOut(500);
	     $('#tooshort_seller').fadeIn(500);
	     document.getElementById("submit").disabled = true;

	 } 	
	} else {
	     $('#tooshort_seller').fadeOut(500);
	     $('#nomatchpswd_seller').fadeOut(500);
	     document.getElementById("submit").disabled = false; 

	}

}