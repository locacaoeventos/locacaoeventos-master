/* ===========================================
General
=========================================== */
// $("input").each(function(){
//   $(this).attr("oninvalid", "this.setCustomValidity('Por favor, preencher este campo corretamente')")
// })







/* ===========================================
Buyer
=========================================== */
$('#id_cpf_buyer').mask('000.000.000-00');
$('#id_cellphone').mask('(00)00000-0000');
$('#id_cellphone').keyup(function(){
  if($(this).val().length < 14) {
    $("#cellphone_error").html("O número de celular é curto demais")
    $("#cellphone_error").css("display", "block")
     document.getElementById("send").disabled = true;
  } else {
    $("#cellphone_error").css("display", "none")
     document.getElementById("send").disabled = false;
  }
});
function validarSenha(){
 password = document.getElementById("id_password").value
 confirm = document.getElementById("confirm").value
 if(password.length >= 6) {
     document.getElementById('tooshort').style.display = 'none';
     document.getElementById("send").disabled = false;

   if (password == confirm){
     document.getElementById('nomatchpswd').style.display = 'none';
     document.getElementById("send").disabled = false; 
   }
   else{
     document.getElementById('nomatchpswd').style.display = 'inline-block';
     document.getElementById("send").disabled = true;
   }
 } else {
     document.getElementById('tooshort').style.display = 'inline-block';
     document.getElementById("send").disabled = true;
 }
}
$("#buyer_button").click(function(){
  $("#buyer_wrapper").fadeIn(300)
  $("#seller_wrapper").css("display", "none")
  $(this).css("background-color", "#98d000")
  $("#seller_button").css("background-color", "#e4e4e4")
  $(".create_user_container").css("overflow-y", "scroll")
})











/* ===========================================
Seller
=========================================== */
$('#id_cpf').mask('000.000.000-00');
$('#id_cnpj').mask('00.000.000/0000-00');
$('#id_cellphone_seller').mask('(00)00000-0000');
$('#id_cellphone_seller').keyup(function(){
  if($(this).val().length < 14) {
    $("#cellphone_seller_error").html("O número de celular é curto demais")
    $("#cellphone_seller_error").css("display", "block")
     document.getElementById("send").disabled = true;
  } else {
    $("#cellphone_seller_error").css("display", "none")
     document.getElementById("send").disabled = false;
  }
});
function validarSenhaSeller(){
 password = document.getElementById("id_password_seller").value
 confirm = document.getElementById("confirm_seller").value
 if(password.length >= 6) {
     document.getElementById('tooshort_seller').style.display = 'none';
     document.getElementById("send_seller").disabled = false;

   if (password == confirm){
     document.getElementById('nomatchpswd_seller').style.display = 'none';
     document.getElementById("send_seller").disabled = false; 
   }
   else{
     document.getElementById('nomatchpswd_seller').style.display = 'inline-block';
     document.getElementById("send_seller").disabled = true;
   }
 } else {
     document.getElementById('tooshort_seller').style.display = 'inline-block';
     document.getElementById("send_seller").disabled = true;

 }
}

// $("#id_cpf").keyup(function(){
//   var cpf_valid = testCPF()
//   if(cpf_valid==true){
//     // alert("A")
//   } else {
//     // alert("B")
//   }

// })
$("#seller_button").click(function(){
  $("#buyer_wrapper").css("display", "none")
  $("#seller_wrapper").fadeIn(300)
  $(this).css("background-color", "#98d000")
  $("#buyer_button").css("background-color", "#e4e4e4")
  $(".create_user_container").css("overflow-y", "scroll")
})







// function testCPF() {
//   var strCPF = $("#id_cpf").val().replace(".","").replace("-","").replace(".","").replace(".","")
//   var Soma;
//   var Resto;
//   Soma = 0;
//   if (strCPF == "00000000000") return false;
     
//   for (i=1; i<=9; i++) Soma = Soma + parseInt(strCPF.substring(i-1, i)) * (11 - i);
//   Resto = (Soma * 10) % 11;
   
//     if ((Resto == 10) || (Resto == 11))  Resto = 0;
//     if (Resto != parseInt(strCPF.substring(9, 10)) ){

//       document.getElementById('cpf_error').style.display = 'inline-block';
//       document.getElementById("send_seller").disabled = true;
//     };
   
//   Soma = 0;
//     for (i = 1; i <= 10; i++) Soma = Soma + parseInt(strCPF.substring(i-1, i)) * (12 - i);
//     Resto = (Soma * 10) % 11;
   
//     if ((Resto == 10) || (Resto == 11))  Resto = 0;
//     if (Resto != parseInt(strCPF.substring(10, 11) ) ){
//       document.getElementById('cpf_error').style.display = 'inline-block';
//       document.getElementById("send_seller").disabled = true;
//     };
//     document.getElementById('cpf_error').style.display = 'none';
//     document.getElementById("send_seller").disabled = false;
// }


