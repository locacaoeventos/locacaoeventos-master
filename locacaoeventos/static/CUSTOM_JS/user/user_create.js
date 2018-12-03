/* ===========================================
General
=========================================== */
$("input").each(function(){
  $(this).attr("oninvalid", "this.setCustomValidity('Por favor, preencher este campo corretamente')")
})







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
  $("#seller_button").css("background-color", "#4fa7bc")
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
$("#seller_button").click(function(){
  $("#buyer_wrapper").css("display", "none")
  $("#seller_wrapper").fadeIn(300)
  $(this).css("background-color", "#98d000")
  $("#buyer_button").css("background-color", "#4fa7bc")
})










